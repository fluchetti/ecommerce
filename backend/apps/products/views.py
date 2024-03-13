from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from .serializers import ProductSerializer, ProductCreateEditSerializer
from .models import Product
from .permissions import IsOwnerOrReadOnly, IsUserAdminStaffOrReadOnly
from django.db.models import Q
from rest_framework.pagination import PageNumberPagination
from rest_framework.parsers import MultiPartParser, FormParser


class ListProducts(GenericAPIView):
    """
    Vista para listar los productos.
    """
    serializer_class = ProductSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        """
        Retorna el queryset de productos publicados.

        parametros:
        - ?q=: texto a buscar en el titulo del producto.

        Retorna:
        - queryset de productos publicados.
        - queryset de productos publicados que contienen el texto en el titulo (si hay texto en la url)
        """
        queryset = Product.objects.filter(status='published')
        q = self.request.query_params.get('title')
        if (q is not None):
            return queryset.filter(title__icontains=q) if len(queryset.filter(title__icontains=q)) > 0 else queryset
        return queryset

    def get(self, request):
        """
        Retorna una lista de productos publicados paginados.
        """
        products = self.get_queryset()
        resultados = self.paginate_queryset(products)
        product_serializer = self.serializer_class(resultados, many=True)
        return self.get_paginated_response(product_serializer.data)


class DetailDeleteProduct(GenericAPIView):
    """
    Vista para ver detalle y borrar un producto.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsOwnerOrReadOnly,]

    def get_queryset(self):
        return Product.objects.filter(Q(status='published') | Q(status='paused'))

    def get(self, request, slug):
        """
        Retorna el detalle de un producto por su slug.

        parametros:
        - slug: El slug del producto.

        Retorna:
        - detalle del producto y status 200 si existe.
        - status 404 si no existe.
        """
        try:
            product = self.get_queryset().get(slug=slug)
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'Error': '404 not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug):
        """
        Borra un producto por su slug.

        parametros:
        - slug: El slug del producto.

        Retorna:
        - status 204 si el producto fue borrado.
        - status 404 si el producto no existe.
        - status 403 si el usuario no es el propietario del producto.
        """
        try:
            product = self.get_queryset().get(slug=slug)
            self.check_object_permissions(request, product)
            product.delete()
            return Response({'Succes': 'Product deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Product.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class EditProduct(GenericAPIView):
    """
    Vista para editar un producto.
    """
    serializer_class = ProductCreateEditSerializer
    permission_classes = [IsOwnerOrReadOnly]
    parser_classes = (MultiPartParser, FormParser)

    def get_queryset(self):
        return Product.objects.filter(Q(status='published') | Q(status='paused'))

    def get(self, request, slug):
        """
        Obtiene el producto por su slug.

        parametros:
        - slug: El slug del producto.

        Retorna:
        - El producto y status 200 si existe.
        - status 404 si no existe.
        """
        try:
            product = self.get_queryset().get(slug=slug)
            product_serializer = self.serializer_class(product)
            return Response(product_serializer.data, status=status.HTTP_200_OK)
        except Product.DoesNotExist:
            return Response({'Error': '404 not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug):
        """
        Modifica un producto por su slug.

        parametros:
        - slug: El slug del producto.
        - request.data: Los datos a modificar.

        Retorna:
        - El producto modificado y status 200 si el serializer es valido.
        - status 404 si no existe.
        - status 400 si el serializer no es valido.
        - status 403 si el usuario no es el propietario del producto.
        """
        try:
            product = self.get_queryset().get(slug=slug)
            self.check_object_permissions(request, product)
            product_serializer = self.serializer_class(
                instance=product, data=request.data)
            if product_serializer.is_valid():
                product_serializer.save()
                return Response(product_serializer.data, status=status.HTTP_200_OK)
            return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Product.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)


class CreateProduct(GenericAPIView):
    """
    Vista para crear un producto.
    """
    serializer_class = ProductCreateEditSerializer
    permission_classes = [IsUserAdminStaffOrReadOnly,]
    parser_classes = (MultiPartParser, FormParser)

    # Publicar producto. Requiere autenticacion.
    def post(self, request):
        """
        Publica un producto.

        parametros:
        - request.data: Los datos del producto.

        Retorna:
        - El producto publicado y status 200 si el serializer es valido.
        - status 400 si el serializer no es valido.
        - status 401 si el usuario no esta autenticado.
        """
        product_serializer = self.serializer_class(
            data=request.data, context={'request': self.request})
        if product_serializer.is_valid():
            print('serializer valido')
            product_serializer.save()
            return Response(product_serializer.data, status=status.HTTP_201_CREATED)
        print('serializer no valido')
        print(product_serializer.errors)
        return Response(product_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListProductsByCategory(GenericAPIView):
    """
    Lista los productos de una categoria.
    """
    serializer_class = ProductSerializer

    def get_queryset(self):
        """
        Retorna el queryset de productos publicados de una categoria.
        """
        products = Product.objects.filter(
            category=self.kwargs['category_id'], status='published')
        return products

    def get(self, request, category_id):
        """
        Retorna una lista de productos publicados de una categoria.

        parametros:
        - category_id: El id de la categoria.

        Retorna:
        - Lista de productos publicados de una categoria y status 200.
        - status 404 si no hay productos.
        """
        products = self.get_queryset()
        product_serializer = self.serializer_class(products, many=True)
        return Response(product_serializer.data, status=status.HTTP_200_OK)
