# Generated by Django 4.2 on 2024-03-06 15:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("carts", "0002_alter_cart_options"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="cartitem",
            name="cart_id",
        ),
        migrations.RemoveField(
            model_name="cartitem",
            name="product_item_id",
        ),
        migrations.DeleteModel(
            name="Cart",
        ),
        migrations.DeleteModel(
            name="CartItem",
        ),
    ]
