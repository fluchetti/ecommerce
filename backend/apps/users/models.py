from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractUser
from django.utils.text import slugify
import os


def avatar_file_path(instance, filename):
    """
    Metodo para crear la ruta de la imagen de perfil del usuario.
    """
    ext = filename.split('.')[-1]
    filename = f'{instance.first_name}_{instance.last_name}.{ext}'
    return os.path.join('users', filename)


class CustomUserManager(BaseUserManager):
    """
    Manager personalizado para el modelo CustomUser.

    Metodos:
    - create_user: Crear un usuario (is_staff=False, is_superuser=False, is_active=True)
    - create_superuser: Crear un superusuario (is_staff=True, is_superuser=True, is_active=True)
    """

    def create_user(self, email, first_name, last_name, phone, birthday, password=None, **extra_fields):
        if not email:
            raise ValueError('El email es obligatorio')
        if not first_name:
            raise ValueError('Debes ingresar un nombre para el usuario')
        if not last_name:
            raise ValueError('Debes ingresar un apellido para el usuario')
        if password is None:
            raise ValueError('Debes ingresar una contraseña para el usuario')
        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
            phone=phone,
            birthday=birthday,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, first_name, last_name, phone, birthday, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser debe tener is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser debe tener is_superuser=True.')
        if extra_fields.get('is_active') is not True:
            raise ValueError('Superuser debe tener is_active=True.')
        return self.create_user(email=email, first_name=first_name, last_name=last_name,
                                phone=phone, birthday=birthday, password=password, **extra_fields)


class CustomUser(AbstractUser):
    """
    Modelo de usuario personalizado.

    Campos:
    - slug: El slug del usuario (unique).
    - email: El email del usuario (unique).
    - first_name: El nombre del usuario.
    - last_name: El apellido del usuario.
    - phone: El telefono del usuario (unique).
    - avatar: La imagen de perfil del usuario.
    - created_at: La fecha de creacion del usuario.
    - updated_at: La fecha de actualizacion del usuario.
    - bio: La biografia del usuario.
    - birthday: La fecha de nacimiento del usuario.
    - role: El rol del usuario (choices: customer, staff, admin).
    """
    slug = models.SlugField(max_length=200, unique=True,
                            null=False, blank=True)
    username = None
    email = models.EmailField(
        max_length=50, blank=False, null=False, unique=True)
    first_name = models.CharField(max_length=50, blank=False, null=False)
    last_name = models.CharField(max_length=50, blank=False, null=False)
    phone = models.CharField(
        max_length=50, blank=False, null=False, unique=True)
    avatar = models.ImageField(
        upload_to=avatar_file_path, default='users/default_user.png', blank=True)
    created_at = models.DateTimeField(auto_now=False, auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, auto_now_add=False)
    bio = models.TextField(max_length=255, blank=True, null=True)
    birthday = models.DateField(
        auto_now=False, auto_now_add=False, null=False, blank=False)
    # Roles
    CUSTOMER = 'customer'
    STAFF = 'staff'
    ADMIN = 'admin'
    ROLE_CHOICES = [
        (CUSTOMER, 'Customer'),
        (STAFF, 'Staff'),
        (ADMIN, 'Admin'),
    ]
    role = models.CharField(
        max_length=10, choices=ROLE_CHOICES, default=CUSTOMER, blank=True, null=False)
    # FIELDS
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'phone', 'birthday']
    objects = CustomUserManager()

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        db_table = "custom_users"
        ordering = ["-created_at"]
        constraints = [
            models.UniqueConstraint(fields=['email'], name='unique_email'),
            models.UniqueConstraint(fields=['phone'], name='unique_phone'),
        ]

    def save(self, *args, **kwargs):
        """
        Metodo para guardar el usuario. Si no tiene un slug, se crea uno a partir del email.
        """
        if not self.slug:
            self.slug = slugify(self.email)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    def delete_avatar(self):
        """
        Metodo para eliminar el avatar del usuario y asignarle el avatar por defecto.
        """
        if self.avatar.name != 'users/default_user.png':
            self.avatar.delete(save=False)
            self.avatar = 'users/default_user.png'
            self.save()
            return True
        return False
