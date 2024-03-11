from rest_framework import serializers
from apps.users.models import CustomUser
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = CustomUser
        fields = ['id', 'email', 'first_name', 'last_name', 'phone', 'avatar',
                  'bio', 'birthday', 'role', 'created_at', 'updated_at', 'slug', 'password']
        read_only_fields = ('created_at', 'updated_at',
                            'slug', 'role', 'id', 'email')
        extra_kwargs = {
            # Permitir que el avatar sea opcional al actualizar
            'avatar': {'required': False},
        }

    def create(self, validated_data):
        """
        Funcion para crear un usuario.

        Parametros:
        - validated_data: Un diccionario con los datos validados.

        Retorna:
        - El usuario creado con la contraseña hasheada.
        """
        password = validated_data.pop('password')
        instance = super().create(validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def update(self, instance, validated_data):
        """
        Funcion para actualizar un usuario.

        Parametros:
        - instance: El usuario a actualizar.
        - validated_data: Un diccionario con los datos validados.

        Retorna:
        - El usuario actualizado.
        """
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.set_password(password)
            instance.save()
        return instance

    def to_representation(self, instance):
        """
        Formatea la respuesta del usuario.
        """
        return {
            'id': instance.id,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'phone': instance.phone,
            'slug': instance.slug,
            'bio': instance.bio,
            'birthday': instance.birthday,
            'created_at': instance.created_at.strftime("%Y-%m-%d"),
            'avatar': instance.avatar.url
        }


class CreateCustomUserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'phone',
                  'birthday', 'avatar', 'password', 'confirm_password']

    def validate(self, data):
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError("Las contraseñas no coinciden")
        return data

    def create(self, validated_data):
        # Eliminar confirm_password del diccionario
        validated_data.pop('confirm_password')
        instance = super().create(validated_data)
        password = validated_data.pop('password')
        instance.set_password(password)
        instance.save()
        return instance

    def to_representation(self, instance):
        """
        Formatea la respuesta del usuario.
        """
        return {
            'id': instance.id,
            'email': instance.email,
            'first_name': instance.first_name,
            'last_name': instance.last_name,
            'phone': instance.phone,
            'slug': instance.slug,
            'bio': instance.bio,
            'birthday': instance.birthday,
            'created_at': instance.created_at.strftime("%Y-%m-%d"),
            'avatar': instance.avatar.url
        }


class ChangePasswordSerializer(serializers.Serializer):
    model = CustomUser

    password = serializers.CharField(required=True)
    password2 = serializers.CharField(required=True)

    def validate(self, data):
        """
        Valida que las contraseñas coincidan.

        Parametros:
        - data: Un diccionario con las contraseñas.

        Retorna:
        - Un diccionario con las contraseñas si son validas.
        - Un mensaje de error si las contraseñas no coinciden.
        """
        if data['password'] != data['password2']:
            raise serializers.ValidationError(
                {'new_password': 'Las contraseñas no coinciden.'})
        return data


class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Serializer de los tokens de los usuarios.
    Añade el slug del usuario al token.
    """
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        # Encripto el slug del usuario en el token.
        token['slug'] = user.slug
        return token
