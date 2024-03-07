from django.db.models.signals import pre_delete
from django.dispatch import receiver
from apps.products.models import Product
from apps.category.models import Category


@receiver(pre_delete, sender=Category)
def set_products_to_withdrawn(sender, instance, **kwargs):
    products_to_withdrawn = Product.objects.filter(category=instance)
    products_to_withdrawn.update(status=Product.WITHDRAWN)
