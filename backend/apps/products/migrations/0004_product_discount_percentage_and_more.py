# Generated by Django 4.2 on 2024-02-29 14:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("products", "0003_alter_product_discount_value"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="discount_percentage",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name="product",
            name="discount_value",
            field=models.FloatField(default=0),
        ),
    ]