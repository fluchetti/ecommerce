from rest_framework.generics import GenericAPIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import CustomUserSerializer, ChangePasswordSerializer, CreateCustomUserSerializer
from .models import CustomUser
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.permissions import IsUserAdminStaffOrReadOnly, IsUser
from rest_framework_simplejwt.views import TokenObtainPairView
from apps.users.serializers import MyTokenObtainPairSerializer
from apps.products.serializers import ProductSerializer
from apps.products.models import Product
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser


class ListUsers(GenericAPIView):
    """
    Vista para listar todos los usuarios.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [AllowAny,]

    def get_queryset(self):
        return CustomUser.objects.all()

    def get(self, request):
        """
        Obtener lista de usuarios.
        """
        queryset = self.get_queryset()
        serializer = self.serializer_class(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class DetailDeleteUpdateUser(GenericAPIView):
    """
    Vista para obtener, eliminar y actualizar un usuario.
    """
    serializer_class = CustomUserSerializer
    permission_classes = [IsUserAdminStaffOrReadOnly,]
    parser_classes = [MultiPartParser, FormParser]

    def get_queryset(self):
        return CustomUser.objects.all()

    def get(self, request, slug):
        """
        Obtener un usuario por su slug.

        Parametros:
        - slug: El slug del usuario (obligatorio).

        Retorna:
        - Los detalles del usuario (si existe) con codigo 200.
        - Un mensaje de error con codigo 404 si el usuario no existe.
        """
        try:
            user = self.get_queryset().get(slug=slug)
            user_serializer = self.serializer_class(user)
            return Response(user_serializer.data, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'Error': '404 not found'}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, slug):
        """
        Eliminar un usuario por su slug.

        Parametros:
        - slug: El slug del usuario (obligatorio).

        Retorna:
        - Un mensaje de exito con codigo 200 si el usuario fue eliminado.
        - Un mensaje de error con codigo 404 si el usuario no existe.
        - Un mensaje de error con codigo 401 si el usuario no tiene permisos.
        """
        try:
            user = self.get_queryset().get(slug=slug)
            self.check_object_permissions(self.request, user)
            user.delete()
            return Response({'message': 'Cuenta eliminada.'}, status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({'Error': '404 not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, slug):
        """
        Editar un usuario por su slug.

        Parametros:
        - slug: El slug del usuario (obligatorio).

        Retorna:
        - Los detalles del usuario editado con codigo 200.
        - Un mensaje de error con codigo 404 si el usuario no existe.
        - Un mensaje de error con codigo 401 si el usuario no tiene permisos.
        """
        try:
            print('en put user')
            user = self.get_queryset().get(slug=slug)
            self.check_object_permissions(self.request, user)
            user_serializer = self.serializer_class(
                user, data=request.data, partial=True)
            if user_serializer.is_valid():
                print('serializer valido')
                user_serializer.save()
                return Response(user_serializer.data, status=status.HTTP_200_OK)
            print('serializer no valido')
            print(user_serializer.errors)
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({'Error': '404 not found'}, status=status.HTTP_404_NOT_FOUND)


class MyTokenObtainPairView(TokenObtainPairView):
    """
    Vista para obtener los tokens de un usuario. (Login endpoint )
    """
    serializer_class = MyTokenObtainPairSerializer


class UserSignupView(GenericAPIView):
    """
    Vista para registrar un usuario.
    """
    serializer_class = CreateCustomUserSerializer

    def post(self, request):
        """
        Crear un usuario.

        Parametros:
        - email: El email del usuario (obligatorio y unique).
        - first_name: El nombre del usuario (obligatorio).
        - last_name: El apellido del usuario (obligatorio).
        - phone: El telefono del usuario (obligatorio y unique).
        - birthday: La fecha de nacimiento del usuario (obligatorio).
        - password: La contraseña del usuario (obligatorio).
        - password2: La confirmacion de la contraseña del usuario (obligatorio).

        Retorna:
        - Los detalles del usuario creado con codigo 201.
        - Un mensaje de error con codigo 400 si el usuario no es valido.
        - Un mensaje de error con codigo 400 si el email o telefono ya esta en uso.
        - Un mensaje de error con codigo 400 si hay otros errores.
        """
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            user_serializer.save()
            return Response(user_serializer.validated_data, status=status.HTTP_201_CREATED)
        else:
            print(user_serializer.errors)
            if 'email' in user_serializer.errors:
                error_message = {
                    'message': 'Ya existe un usuario con este email.', 'status': 400}
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            elif 'phone' in user_serializer.errors:
                error_message = {
                    'message': 'Ya existe un usuario con este telefono.', 'status': 400}
                return Response(error_message, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ListUserProducts(GenericAPIView):
    """
    Vista para listar los productos de un usuario.
    """
    serializer_class = ProductSerializer
    permission_classes = [IsUserAdminStaffOrReadOnly,]

    def get_queryset(self):
        """
        Obtener los productos de el usuario autenticado.
        """
        products = Product.objects.filter(
            owner=self.request.user.id, status__in=['published', 'paused'])
        return products

    def get(self, request):
        """
        Listar los productos de el usuario autenticado.
        """
        products = self.get_queryset()
        products_serializer = self.serializer_class(products, many=True)
        return Response(products_serializer.data, status=status.HTTP_200_OK)


class ChangeUserPassword(GenericAPIView):
    """
    Vista para cambiar la contraseña de un usuario.
    """
    serializer_class = ChangePasswordSerializer
    permission_classes = [IsUser, IsAuthenticated]

    def post(self, request):
        """
        Cambiar la contraseña de un usuario.

        Parametros:
        - password: La nueva contraseña del usuario (obligatorio).
        - password2: La nueva contraseña del usuario (obligatorio).

        Retorna:
        - Un mensaje de exito con codigo 200 si la contraseña fue cambiada.
        - Un mensaje de error con codigo 400 si las contraseñas no coinciden.
        """
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            new_password = user_serializer.validated_data['password2']
            request.user.set_password(new_password)
            request.user.save()
            return Response({'message': 'Contraseña cambiada.'}, status=status.HTTP_200_OK)
        else:
            return Response(user_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteUserProfileImage(GenericAPIView):
    """
    Vista para eliminar la imagen de perfil de un usuario.
    """
    permission_classes = [IsUserAdminStaffOrReadOnly,]

    def delete(self, request):
        """
        Borrar la imagen de perfil de un usuario.

        Retorna:
        - Un mensaje de exito con codigo 200 si la imagen fue eliminada.
        """
        user = request.user
        self.check_object_permissions(request, user)
        user.delete_avatar()
        return Response({'message': 'Imagen de perfil eliminada.'}, status=status.HTTP_200_OK)
