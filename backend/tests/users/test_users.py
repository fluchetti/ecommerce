from tests.test_setup import TestSetUp
from tests.factories.users_factories import UserFactory
from apps.users.models import CustomUser
from rest_framework import status
from apps.products.models import Product
from apps.category.models import Category


class UserTest(TestSetUp):

    def test_get_user(self):
        user = UserFactory().create_user()

        response = self.client.get(f'/api/users/{user.slug}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['email'], user.email)
        self.assertEqual(response.data['first_name'], user.first_name)
        self.assertEqual(response.data['last_name'], user.last_name)
        self.assertEqual(response.data['phone'], user.phone)
        self.assertEqual(response.data['birthday'], (user.birthday))

    def test_get_users(self):
        response = self.client.get('/api/users/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_user(self):
        response = self.client.post('/api/users/signup', {
            "email": "test@test.com",
            "first_name": "test",
            "last_name": "test",
            "phone": "test",
            "birthday": "1999-12-12",
            "password": "test",
            "confirm_password": "test"}, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        user = CustomUser.objects.get(email="test@test.com")
        self.assertEqual(user.first_name, "test")
        self.assertEqual(user.last_name, "test")
        self.assertEqual(user.phone, "test")

    def test_update_user_(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )

        response = self.client.post("/api/token/", {
            'email': "test@test.com",
            'password': 'test'
        }, format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(f'/api/users/{user.slug}', {
            'first_name': 'nuevo nombre',
            'last_name': 'nuevo apellido',
            'phone': 'nuevo telefono',
            'bio': 'nueva bio'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Esto falla.
        # self.assertEqual(user.first_name, 'nuevo nombre')
        # Esto esta bien. No entiendo por qué falla el anterior.
        updated_user = CustomUser.objects.get(slug=user.slug)
        self.assertEqual(updated_user.first_name, 'nuevo nombre')
        self.assertEqual(updated_user.last_name, 'nuevo apellido')
        self.assertEqual(updated_user.phone, 'nuevo telefono')
        self.assertEqual(updated_user.bio, 'nueva bio')

    def test_update_user_with_admin_token(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.put(f'/api/users/{user.slug}', {
            'first_name': 'nuevo nombre',
            'last_name': 'nuevo apellido',
            'phone': 'nuevo telefono',
            'bio': 'nueva bio'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Esto falla.
        # self.assertEqual(user.first_name, 'nuevo nombre')
        # Esto esta bien. No entiendo por qué falla el anterior.
        updated_user = CustomUser.objects.get(slug=user.slug)
        self.assertEqual(updated_user.first_name, 'nuevo nombre')
        self.assertEqual(updated_user.last_name, 'nuevo apellido')
        self.assertEqual(updated_user.phone, 'nuevo telefono')
        self.assertEqual(updated_user.bio, 'nueva bio')

    def test_update_user_without_token(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        response = self.client.put(f'/api/users/{user.slug}', {
            'first_name': 'nuevo nombre',
            'last_name': 'nuevo apellido',
            'phone': 'nuevo telefono',
            'bio': 'nueva bio'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_update_user_with_wrong_token(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        user2 = CustomUser.objects.create_user(
            email="test2@test.com",
            first_name="test2",
            last_name="test2",
            phone="test2",
            birthday="1999-12-12",
            password="test2"
        )
        response = self.client.post("/api/token/", {
            "email": "test2@test.com",
            "password": "test2"
        }, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.put(f'/api/users/{user.slug}',
                                   {'first_name': 'nuevo nombre',
                                    'last_name': 'nuevo apellido',
                                    'phone': 'nuevo telefono',
                                    'bio': 'nueva bio'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )

        response = self.client.post("/api/token/", {
            'email': "test@test.com",
            'password': 'test'
        }, format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(f'/api/users/{user.slug}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(CustomUser.objects.filter(slug=user.slug).first())

    def test_delete_user_with_admin_token(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')
        response = self.client.delete(f'/api/users/{user.slug}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIsNone(CustomUser.objects.filter(slug=user.slug).first())

    def test_delete_user_without_token(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        response = self.client.delete(f'/api/users/{user.slug}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIsNotNone(CustomUser.objects.filter(slug=user.slug).first())

    def test_delete_user_with_wrong_token(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        user2 = CustomUser.objects.create_user(
            email="test2@test.com",
            first_name="test2",
            last_name="test2",
            phone="test2",
            birthday="1999-12-12",
            password="test2"
        )
        response = self.client.post("/api/token/", {
            "email": "test2@test.com",
            "password": "test2"
        }, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.delete(f'/api/users/{user.slug}')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIsNotNone(CustomUser.objects.filter(slug=user.slug).first())
        self.assertIsNotNone(
            CustomUser.objects.filter(slug=user2.slug).first())

    def test_change_password(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        response = self.client.post("/api/token/", {
            'email': "test@test.com",
            'password': 'test'
        }, format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post("/api/users/change_password", {
            "password": "nuevacontraseña",
            "password2": "nuevacontraseña"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user = CustomUser.objects.get(email="test@test.com")
        self.assertTrue(user.check_password("nuevacontraseña"))

    def test_change_password_without_token(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        response = self.client.post("/api/users/change_password", {
            "password": "nuevacontraseña",
            "password2": "nuevacontraseña"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertTrue(user.check_password("test"))

    def test_change_password_fail(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        response = self.client.post("/api/token/", {
            'email': "test@test.com",
            'password': 'test'
        }, format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.post("/api/users/change_password", {
            "password": "nuevacontrasenia",
            "password2": "viejacontrasenia"
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertTrue(user.check_password("test"))

    def test_get_user_posts(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category = Category.objects.create(
            name='category', description='description')
        for i in range(5):
            Product.objects.create(
                title=f'product{i}',
                description=f'description{i}',
                owner=user,
                category=category)
        response = self.client.post("/api/token/", {
            'email': user.email,
            'password': 'test'
        }, format='json'
        )
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {token}')
        response = self.client.get(f'/api/users/posts')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 5)
        self.assertEqual(response.data[0]['owner'], user.first_name)
