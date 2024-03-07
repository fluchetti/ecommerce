# Generated by Django 4.2 on 2024-03-07 13:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("carts", "0004_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="cart",
            name="is_delivered",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="cart",
            name="total_price",
            field=models.FloatField(default=0),
        ),
        migrations.AddField(
            model_name="cartitem",
            name="price",
            field=models.FloatField(default=0),
            preserve_default=False,
        ),
    ]
