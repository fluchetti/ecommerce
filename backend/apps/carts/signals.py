from django.db.models.signals import post_save
from django.dispatch import receiver


# @receiver(post_save, sender=Cart)
# def create_cart_items_and_order(sender, instance, created, **kwargs):
#     if created:
#         print(instance.cartitem_set.all())
#         # Aquí creas los CartItems asociados al Cart
#         for item in instance.cartitem_set.all():

#             CartItem.objects.create(
#                 cart_id=instance,
#                 product_item_id=item.product_item_id,
#                 quantity=item.quantity
#             )

#         # Calculas el total del pedido sumando los precios de todos los productos
#         order_total = sum(item.product_item_id.price *
#                           item.quantity for item in instance.cartitem_set.all())

#         # Creas la Order asociada al Cart
#         Order.objects.create(
#             user_id=instance.user_id,
#             cart=instance,
#             order_total=order_total
#         )
