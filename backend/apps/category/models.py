from django.db import models
import os
from django.utils.text import slugify


def category_file_path(instance, filename):
    """
    Funcion para generar la ruta de la imagen de la categoria.

    Parametros:
    - instance: La instancia del modelo.
    - filename: El nombre del archivo.

    Retorna:
    - La ruta de la imagen de la categoria.
    """
    ext = filename.split('.')[-1]
    filename = f'{instance.name}.{ext}'
    return os.path.join('categorys', filename)


class Category(models.Model):
    """
    Modelo de Categoria

    Campos:
    - slug: El slug de la categoria.
    - name: El nombre de la categoria (obligatorio).
    - description: La descripcion de la categoria (obligatorio).
    - image: La imagen de la categoria.
    """
    slug = models.SlugField(max_length=200, blank=True,
                            null=False, unique=True)
    name = models.CharField(max_length=255, blank=False, null=False)
    description = models.TextField(blank=False, null=False)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    image = models.ImageField(
        upload_to=category_file_path, default='categorys/default_category.png')

    REQUIRED_FIELDS = ['name', 'description']

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        db_table = "categorias"
        ordering = ['-updated_at']

    def save(self, *args, **kwargs):
        """
        Sobreescribe el metodo save para generar el slug.
        """
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name}'
