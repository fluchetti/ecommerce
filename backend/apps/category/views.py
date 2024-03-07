from rest_framework.generics import GenericAPIView
from rest_framework.views import APIView
from apps.category.serializers import CategorySerializer
from apps.category.models import Category
from rest_framework import status
from rest_framework.response import Response
from apps.category.permissions import IsAdminStaffOrReadOnly
from rest_framework.pagination import PageNumberPagination


class ListCreateCategory(GenericAPIView):
    """
    Vista para listar y crear categorias.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAdminStaffOrReadOnly,]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        return Category.objects.all()

    def get(self, request):
        """
        Obtener lista paginada de categorias.

        Parametros de consulta opcionales:
        - ?page=<int>: El numero de pagina a retornar.

        Retorna:
        - Una lista paginada de categorias o un mensaje de error si no existe la pagina.
        """
        categories = self.get_queryset()
        paginated_categories = self.paginate_queryset(categories)
        category_serializer = self.serializer_class(
            paginated_categories, many=True)
        return self.get_paginated_response(category_serializer.data)

    def post(self, request):
        """
        Crear una nueva categoria.

        Parametros:
        - name: Nombre de la categoria (obligatorio).
        - description: Descripcion de la categoria (obligatorio).
        - image: Imagen de la categoria (opcional).

        Retorna:
        - La categoria creada y sus detalles con codigo 201 si la peticion es exitosa.
        - Un mensaje de error con codigo 400 si la peticion es erronea.
        - Un mensaje de error con codigo 401 si el usuario no tiene permisos.
        """

        category_serializer = self.serializer_class(data=request.data)
        if category_serializer.is_valid():
            category_serializer.save()
            return Response(category_serializer.data, status=status.HTTP_201_CREATED)
        return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListAllCategories(APIView):
    """
    Vista para listar todas las categorias.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAdminStaffOrReadOnly]
    pagination_class = None

    def get(self, request):
        """
        Retorna una lista de todas las categorias.
        """
        categories = Category.objects.all()
        category_serializer = self.serializer_class(categories, many=True)
        return Response(category_serializer.data, status=status.HTTP_200_OK)


class DetailDeleteCategory(GenericAPIView):
    """
    Vista para ver, actualizar y eliminar categorias.
    """
    serializer_class = CategorySerializer
    permission_classes = [IsAdminStaffOrReadOnly,]

    def get_queryset(self):
        return Category.objects.all()

    def get(self, request, slug):
        """
        Retorna los detalles de una categoria.

        Parametros:
        - slug: El slug de la categoria a buscar (obligatorio).

        Retorna:
        - Los detalles de la categoria (si existe) con codigo 200.
        - Un mensaje de error con codigo 404 si la categoria no existe.
        """
        try:
            category = self.get_queryset().get(slug=slug)
            serializer = self.serializer_class(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, id):
        """
        Elimina una categoria.

        Parametros:
        - id: El id de la categoria a eliminar (obligatorio).

        Retorna:
        - Un mensaje de exito con codigo 204 si la categoria fue eliminada.
        - Un mensaje de error con codigo 404 si la categoria no existe.
        - Un mensaje de error con codigo 401 si el usuario no tiene permisos.
        """
        try:
            category = self.get_queryset().get(id=id)
            category.delete()
            return Response({'Succes': 'Category deleted'}, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, id):
        """
        Edita una categoria.

        Parametros:
        - id: El id de la categoria a editar (obligatorio).
        - name: Nuevo nombre de la categoria (opcional).
        - description: Nueva descripcion de la categoria (opcional).
        - image: Nueva imagen de la categoria (opcional).

        Retorna:
        - Los detalles de la categoria editada con codigo 204 si la peticion es exitosa.
        - Un mensaje de error con codigo 404 si la categoria no existe.
        - Un mensaje de error con codigo 400 si la peticion es erronea.
        - Un mensaje de error con codigo 401 si el usuario no tiene permisos.
        """
        print(request.data)
        try:
            category = self.get_queryset().get(id=id)
            category_serializer = self.serializer_class(
                instance=category, data=request.data)
            if category_serializer.is_valid():
                category_serializer.save()
                return Response(category_serializer.data, status=status.HTTP_204_NO_CONTENT)
            else:
                return Response(category_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Category.DoesNotExist:
            return Response({'Error': 'Not found'}, status=status.HTTP_404_NOT_FOUND)
