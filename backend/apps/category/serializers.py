from rest_framework import serializers
from apps.category.models import Category


class CategorySerializer(serializers.ModelSerializer):
    """
    Serializador para el modelo Category.
    """
    class Meta:
        model = Category
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'slug']
        extra_kwargs = {
            # Permitir que la imagen sea opcional al actualizar
            'image': {'required': False},
        }

    def to_representation(self, instance):
        """
        Formatea la respuesta de la categoria.
        """
        return {
            'id': instance.id,
            'name': instance.name,
            'description': instance.description,
            'image': instance.image.url,
            'slug': instance.slug,
        }
