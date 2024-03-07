from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import CartSerializer, CartItemSerializer
from .models import Cart, CartItem
from apps.products.models import Product
from rest_framework.permissions import IsAuthenticated


class ListCreateCartView(GenericAPIView):
    serializer_class = CartSerializer
    permission_classes = [IsAuthenticated,]

    def get_queryset(self):
        user = self.request.user
        return Cart.objects.filter(owner=user)

    def get(self, request):
        carts = self.get_queryset()
        carts_serializer = self.serializer_class(carts, many=True)
        return Response(carts_serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # request.data trae una lista con diccionarios representando cada producto.
        # lo relevante de cada diccionario sera el id, discount_value y quantity.
        # lo usamos para crear cart items.
        total_price = sum(
            float(item['discount_value']) * int(item['quantity']) for item in request.data)

        cart = Cart.objects.create(
            owner=request.user,
            total_price=total_price
        )

        for item in request.data:
            product = Product.objects.get(id=item['id'])
            cart_item = CartItem.objects.create(
                product=product,
                quantity=item['quantity'],
                price=item['discount_value'],
                cart=cart
            )
        cart_serializer = self.serializer_class(cart)
        return Response(cart_serializer.data, status=status.HTTP_201_CREATED)


class DetailCartView(GenericAPIView):
    serializer_class = CartSerializer

    def get_queryset(self):
        return Cart.objects.all()

    def get(self, request, pk):
        try:
            cart = self.get_queryset().get(id=pk)
            cart_serializer = self.serializer_class(cart, many=True)
            return Response(cart_serializer.data, status=status.HTTP_200_OK)
        except Cart.DoesNotExist:
            return Response({'Error': '4O4 Not Found'}, status=status.HTTP_404_NOT_FOUND)
