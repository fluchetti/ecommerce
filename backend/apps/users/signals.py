from django.db.models.signals import post_delete
from django.dispatch import receiver
from django.conf import settings
import os


@receiver(post_delete, sender=settings.AUTH_USER_MODEL)
def delete_avatar(sender, instance, **kwargs):
    # Eliminar la imagen de avatar del usuario cuando se elimina el usuario
    if instance.avatar and instance.avatar.name != 'users/default_user.png':
        # Construir la ruta completa al archivo de avatar
        avatar_path = os.path.join(
            f'{settings.MEDIA_ROOT}', instance.avatar.name)
        # Verificar si el archivo existe y eliminarlo
        if os.path.exists(avatar_path):
            os.remove(avatar_path)
