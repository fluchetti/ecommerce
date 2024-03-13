from rest_framework.test import APITestCase
from apps.users.models import CustomUser
from rest_framework import status


class TestSetUp(APITestCase):

    def setUp(self):
        self.login_url = '/api/token/'
        self.admin_user = CustomUser.objects.create_superuser(
            email="admin@admin.com",
            first_name="admin",
            last_name="admin",
            phone="admin",
            birthday="1999-12-12",
            password="admin"
        )
        response = self.client.post(self.login_url, {
            'email': self.admin_user.email,
            'password': 'admin'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.token = response.data['access']
        self.user = CustomUser.objects.create_user(
            email="user@user.com",
            first_name="user",
            last_name="user",
            phone="user",
            birthday="1999-12-12",
            password="user")

        return super().setUp()

    def test_pass(self):
        pass
