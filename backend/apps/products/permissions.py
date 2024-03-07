from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Permitimos leer a cualquiera
        if request.method == 'GET':
            return True
        # Autenticado y dueño
        return request.user.is_authenticated and (obj.owner == request.user)
