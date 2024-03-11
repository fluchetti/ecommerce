from tests.test_setup import TestSetUp
from apps.users.models import CustomUser
from rest_framework import status
from apps.products.models import Product
from apps.category.models import Category


class ProductsTest(TestSetUp):

    def test_create_product(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category = Category.objects.create(name='test', description="test")
        response = self.client.post('/api/token/', {
            'email': user.email, 'password': 'test'}, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.post(
            '/api/products/create', {
                'title': 'test',
                'price': 1000,
                'description': 'test',
                'category': category.id,
                'owner': user.id
            }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Product.objects.count(), 1)
        self.assertEqual(Product.objects.get().title, 'test')

    def test_create_product_fail(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category = Category.objects.create(name='test', description="test")
        response = self.client.post(
            '/api/products/create', {
                'title': 'test',
                'price': 1000,
                'description': 'test',
                'category': category.id,
                'owner': user.id
            }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_list_products(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category = Category.objects.create(name='test', description="test")
        for i in range(10):
            Product.objects.create(
                title=f'test {i}',
                price=1000,
                description='test',
                category=category,
                owner=user
            )
        for i in range(5):
            Product.objects.create(
                title=f'test {i+10}',
                price=1000,
                description='test',
                category=category,
                owner=user,
                status='withdrawn'
            )
        response = self.client.get('/api/products/list')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Product.objects.filter(status='published')), 10)
        self.assertEqual(len(Product.objects.all()), 15)

    def test_list_products_by_category(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category1 = Category.objects.create(
            name='test 1', description="test 1")
        category2 = Category.objects.create(
            name='test 2', description="test 2")
        for i in range(5):
            Product.objects.create(
                title=f'test {i}',
                price=1000,
                description='test',
                category=category1,
                owner=user
            )
        for i in range(3):
            Product.objects.create(
                title=f'test {i+5}',
                price=1000,
                description='test',
                category=category2,
                owner=user
            )
        response = self.client.get(f'/api/products/list/{category1.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Product.objects.filter(category=category1)), 5)
        response = self.client.get(f'/api/products/list/{category2.id}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(Product.objects.filter(category=category2)), 3)

    def test_delete_product(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category = Category.objects.create(name='test', description="test")
        product = Product.objects.create(
            title='test',
            price=1000,
            description='test',
            category=category,
            owner=user
        )
        response = self.client.post('/api/token/', {
            'email': user.email, 'password': 'test'}, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        response = self.client.delete(f'/api/products/detail/{product.slug}')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Product.objects.filter(status="withdrawn").count(), 1)

    def test_delete_product_not_found(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category = Category.objects.create(name='test', description="test")
        product = Product.objects.create(
            title='test',
            price=1000,
            description='test',
            category=category,
            owner=user
        )
        response = self.client.delete(f'/api/products/detail/slug')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product_fail(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category = Category.objects.create(name='test', description="test")
        product = Product.objects.create(
            title='test',
            price=1000,
            description='test',
            category=category,
            owner=user
        )
        response = self.client.delete(f'/api/products/detail/{product.slug}')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Product.objects.filter(status="withdrawn").count(), 0)

    def test_edit_product(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category = Category.objects.create(name='test', description="test")
        response = self.client.post('/api/token/', {
            'email': user.email, 'password': 'test'}, format='json')
        token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + token)
        product = Product.objects.create(
            title='test',
            price=1000,
            description='test',
            category=category,
            owner=user
        )
        response = self.client.put(
            f'/api/products/edit/{product.slug}', {
                'title': 'test edit',
                'price': 2000,
                'description': 'test edit',
            }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Product.objects.get().title, 'test edit')
        self.assertEqual(Product.objects.get().price, 2000)
        self.assertEqual(Product.objects.get().description, 'test edit')

    def test_edit_product_fail(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category = Category.objects.create(name='test', description="test")
        product = Product.objects.create(
            title='test',
            price=1000,
            description='test',
            category=category,
            owner=user
        )
        response = self.client.put(
            f'/api/products/edit/{product.slug}', {
                'title': 'test edit',
                'price': 2000,
                'description': 'test edit',
            }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_product_not_found(self):
        response = self.client.put(
            f'/api/products/edit/slug', {
                'title': 'test edit',
                'price': 2000,
                'description': 'test edit',
            }, format='multipart')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_detail_product(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test"
        )
        category = Category.objects.create(name='test', description="test")
        product = Product.objects.create(
            title='test',
            price=1000,
            description='test',
            category=category,
            owner=user
        )
        response = self.client.get(f'/api/products/detail/{product.slug}')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['title'], 'test')
        self.assertEqual(response.data['price'], 1000)
        self.assertEqual(response.data['description'], 'test')

    def test_detail_product_not_found(self):
        response = self.client.get(f'/api/products/detail/slug')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
