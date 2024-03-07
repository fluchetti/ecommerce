from django.db import models
from core.settings import AUTH_USER_MODEL
import os
from apps.category.models import Category
from django.utils.text import slugify


def product_file_path(instance, filename):
    """
    funcion para generar la ruta de la imagen del producto.
    """
    ext = filename.split('.')[-1]
    filename = f'{instance.title}_{instance.id}.{ext}'
    return os.path.join('products', filename)


class Product(models.Model):
    """
    Modelo de Producto

    Atributos:
    - slug: El slug del producto.
    - category: La categoria del producto (FK a Category)
    - owner: El propietario del producto (FK a CustomUser)
    - title: El titulo del producto.
    - image: La imagen del producto.
    - summary: El resumen del producto.
    - description: La descripcion del producto.
    - price: El precio del producto.
    - discount_percentage: El porcentaje de descuento del producto.
    - discount_value: El valor del producto con descuento.
    - status: El estado del producto (published, paused, withdrawn)

    Metodos:
    - save: Sobreescribe el metodo save para generar el slug y calcular el valor del descuento.
    - delete: Sobreescribe el metodo delete para cambiar el estado del producto a withdrawn.
    - __str__: Retorna el titulo del producto.
    - calculate_discount_value: Calcula el valor del descuento del producto.
    """
    slug = models.SlugField(max_length=200, blank=True,
                            null=False, unique=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_DEFAULT, default=None, null=True)
    owner = models.ForeignKey(AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=255, null=False, blank=True)
    image = models.ImageField(
        upload_to=product_file_path, default='products/default_product.png')
    summary = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    price = models.FloatField(default=0)
    discount_percentage = models.PositiveIntegerField(default=0)
    discount_value = models.FloatField(default=0)
    created_at = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated_at = models.DateTimeField(auto_now_add=False, auto_now=True)
    # Status
    PUBLISHED = 'published'
    PAUSED = 'paused'
    WITHDRAWN = 'withdrawn'
    STATUS_CHOICES = [
        (PUBLISHED, 'Published'),
        (PAUSED, 'Paused'),
        (WITHDRAWN, 'Withdrawn'),
    ]
    status = models.CharField(
        max_length=15, choices=STATUS_CHOICES, default=PUBLISHED, blank=True, null=False)

    REQUIRED_FIELDS = ['category', 'owner', 'title',]

    class Meta:
        verbose_name = "Producto"
        verbose_name_plural = "Productos"
        db_table = "productos"
        ordering = ['-updated_at']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        # Calcula y asigna el valor del descuento
        self.discount_value = self.calculate_discount_value()
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.status = self.WITHDRAWN
        self.save(update_fields=['status'])

    def __str__(self):
        return f'{self.title}'

    def calculate_discount_value(self):
        if self.discount_percentage > 0:
            discount_amount = (self.discount_percentage / 100) * self.price
            discounted_price = self.price - discount_amount
            return discounted_price
        else:
            return self.price
