from tests.test_setup import TestSetUp
from apps.users.models import CustomUser
from rest_framework import status
from apps.products.models import Product
from apps.category.models import Category
from apps.carts.models import Cart, CartItem


class TestCarts(TestSetUp):

    def test_create_cart(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test")
        product1 = Product.objects.create(
            owner=user,
            title='product1',
            price=100,
            category=Category.objects.create(
                name='category1', description='description1')
        )
        product2 = Product.objects.create(
            owner=user,
            title='product2',
            price=200,
            category=Category.objects.create(
                name='category2', description='description2')
        )
        cart_data = [
            {
                "id": 1,
                "quantity": 1,
                "discount_value": 100
            },
            {
                "id": 2,
                "quantity": 2,
                "discount_value": 200
            }
        ]
        response = self.client.post('/api/token/', {
            'email': user.email,
            'password': 'test'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(
            '/api/carts/', cart_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Cart.objects.count(), 1)
        self.assertEqual(CartItem.objects.count(), 2)
        self.assertEqual(Cart.objects.first().total_price, 500)

    def test_create_cart_unauthenticated(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test")
        product1 = Product.objects.create(
            owner=user,
            title='product1',
            price=100,
            category=Category.objects.create(
                name='category1', description='description1')
        )
        product2 = Product.objects.create(
            owner=user,
            title='product2',
            price=200,
            category=Category.objects.create(
                name='category2', description='description2')
        )
        cart_data = [
            {
                "id": 1,
                "quantity": 1,
                "discount_value": 100
            },
            {
                "id": 2,
                "quantity": 2,
                "discount_value": 200
            }
        ]
        response = self.client.post(
            '/api/carts/', cart_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(Cart.objects.count(), 0)

    def test_list_carts(self):
        user = CustomUser.objects.create_user(
            email="test@test.com",
            first_name="test",
            last_name="test",
            phone="test",
            birthday="1999-12-12",
            password="test")
        product1 = Product.objects.create(
            owner=user,
            title='product1',
            price=100,
            category=Category.objects.create(
                name='category1', description='description1')
        )
        product2 = Product.objects.create(
            owner=user,
            title='product2',
            price=200,
            category=Category.objects.create(
                name='category2', description='description2')
        )
        cart_data = [
            {
                "id": 1,
                "quantity": 1,
                "discount_value": 100
            },
            {
                "id": 2,
                "quantity": 2,
                "discount_value": 200
            }
        ]
        response = self.client.post('/api/token/', {
            'email': user.email,
            'password': 'test'
        }, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.client.credentials(
            HTTP_AUTHORIZATION='Bearer ' + response.data['access'])
        response = self.client.post(
            '/api/carts/', cart_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/api/carts/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
