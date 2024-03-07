from rest_framework.test import APITestCase
from faker import Faker
from rest_framework import status
from apps.users.models import CustomUser

fake = Faker()

class TestSignUp(APITestCase):

    def test_signup(self):
        signup_url = "api/users/signup"
        data = {
            "first_name":fake.name(),
            "last_name":fake.last_name(),
            "email":fake.email(),
            "birthday":fake.date(),
            "phone":fake.phone_number(),
            "password":"contrasenia"
        }

        response = self.client.post(signup_url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        self.assertTrue(CustomUser.objects.filter(email = data['email']).exists())

        self.assertIn('access', response.data)
