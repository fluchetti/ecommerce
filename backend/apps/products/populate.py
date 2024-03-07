import factory
from faker import Factory as FakerFactory
from apps.products.models import Product
from apps.category.populate import CategoryFactory
from apps.users.populate import CustomUserFactory

faker = FakerFactory.create()


class ProductFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Product
    # Esto me crea category y owner nuevo por cada producto.
    # Ver forma de usar los ya existentes.
    category = factory.SubFactory(CategoryFactory)
    owner = factory.SubFactory(CustomUserFactory)
    title = factory.LazyAttribute(lambda _: faker.word())
    summary = factory.LazyAttribute(lambda _: faker.sentence())
    description = factory.LazyAttribute(lambda _: faker.paragraph())
    price = factory.LazyAttribute(lambda _: faker.random_number(digits=3))
    discount_percentage = factory.LazyAttribute(
        lambda _: faker.random_number(digits=2))
    status = Product.PUBLISHED

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the default _create method to save the object after creation.
        """
        product = model_class(*args, **kwargs)
        product.save()
        return product
