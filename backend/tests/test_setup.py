from rest_framework.test import APITestCase
from faker import Faker
from rest_framework import status
from apps.users.models import CustomUser

fake = Faker()


class TestSetUp(APITestCase):

    def setUp(self):
        self.login_url = '/api/token/'
        self.user = CustomUser.objects.create(
            first_name='Test',
            last_name='User',
            email=fake.email(),
            birthday=fake.date(),
            phone=fake.phone_number()
        )
        self.user.set_password('developer')  # Setear la contraseña usando set_password
        self.user.save()

        response = self.client.post(
            self.login_url, {
                'email': self.user.email,
                'password': 'developer'
            }, format='json'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']  # Acceder al token de autenticación
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.token}')

        return super().setUp()

    def test_login(self):
        pass
