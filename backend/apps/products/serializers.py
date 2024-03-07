from rest_framework import serializers
from apps.products.models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = '__all__'
        read_only_fields = ['slug', 'owner',
                            'status', 'created_at', 'updated_at']

    def to_representation(self, instance):
        """
        Forma de representar el objeto en la respuesta.
        """
        return {
            'id': instance.id,
            'category': instance.category.name,
            'category_slug': instance.category.slug,
            'title': instance.title,
            'owner': instance.owner.first_name,
            'owner_slug': instance.owner.slug,
            'owner_id': instance.owner.id,
            'summary': instance.summary,
            'slug': instance.slug,
            'description': instance.description,
            'image': instance.image.url,
            'price': instance.price,
            'discount_percentage': instance.discount_percentage,
            'discount_value': instance.discount_value
        }


class ProductCreateEditSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['category', 'title', 'image', 'summary', 'description',
                  'price', 'discount_percentage',  'status', 'slug']
        read_only_fields = ['slug']

    def create(self, validated_data):
        """
        Sobreescribimos el metodo create para asignar el usuario que esta creando el producto.
        """
        validated_data['owner'] = self.context['request'].user
        print(validated_data)
        producto = Product.objects.create(**validated_data)
        return producto
