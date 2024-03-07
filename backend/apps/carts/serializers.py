from rest_framework import serializers
from .models import Cart, CartItem


class CartItemSerializer(serializers.ModelSerializer):

    product = serializers.ReadOnlyField(source='product.title')

    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.email')
    cart_items = serializers.SerializerMethodField(read_only=True)
    created = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Cart
        fields = '__all__'

    def get_cart_items(self, obj):
        items = obj.cartitem_set.all()
        serializer = CartItemSerializer(items, many=True)
        print(serializer.data)
        return serializer.data

    def get_created(self, obj):
        return obj.created.strftime('%Y-%m-%d')
