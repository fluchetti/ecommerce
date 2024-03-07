import factory
from faker import Factory as FakerFactory
from apps.category.models import Category

faker = FakerFactory.create()


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = factory.LazyAttribute(lambda _: faker.word())
    description = factory.LazyAttribute(lambda _: faker.text())

    @classmethod
    def _create(cls, model_class, *args, **kwargs):
        """
        Override the default _create method to save the object after creation.
        """
        category = model_class(*args, **kwargs)
        category.save()
        return category
