import factory
from faker import Faker
from apps.users.models import CustomUser

fake = Faker().seed_instance(9999)


class CustomUserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = CustomUser

    email = factory.LazyAttribute(lambda _: fake.email())
    first_name = factory.LazyAttribute(lambda _: fake.first_name())
    last_name = factory.LazyAttribute(lambda _: fake.last_name())
    phone = factory.LazyAttribute(lambda _: fake.phone_number())
    birthday = factory.LazyAttribute(
        lambda _: fake.date_of_birth(minimum_age=18))

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the default _create method to set a password for the user.
        """
        password = 'contrasenia'
        user = model_class(*args, **kwargs)
        user.set_password(password)
        user.save()
        return user
