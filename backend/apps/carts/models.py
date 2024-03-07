from django.db import models
from core.settings import AUTH_USER_MODEL
from apps.products.models import Product


class Cart(models.Model):

    owner = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    total_price = models.FloatField(default=0)
    is_delivered = models.BooleanField(default=False)

    def __str__(self):
        return f'Cart {self.id} owned by {self.owner}.'


class CartItem(models.Model):

    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    price = models.FloatField()

    def __str__(self):
        return f'{self.quantity} x {self.product.title} - {self.cart}'
