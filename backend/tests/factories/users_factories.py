from faker import Faker
from apps.users.models import CustomUser
from apps.products.models import Product
faker = Faker()


class UserFactory:

    def create_user(self, **kwargs):
        return CustomUser.objects.create_user(
            email=kwargs.get('email', faker.email()),
            first_name=kwargs.get('first_name', faker.first_name()),
            last_name=kwargs.get('last_name', faker.last_name()),
            phone=kwargs.get('phone', faker.phone_number()),
            birthday=kwargs.get('birthday', faker.date_of_birth()),
            password=kwargs.get('password', 'password')
        )

    def create_product(self, **kwargs):
        return Product.objects.create(
            title=kwargs.get('name', faker.name()),
            price=kwargs.get('price', faker.random_number()),
            description=kwargs.get('description', faker.text()),
            category=kwargs.get('category', faker.random_number()),
            owner=kwargs.get('owner', self.create_user())
        )
