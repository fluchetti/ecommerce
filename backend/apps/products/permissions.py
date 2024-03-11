from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        # Permitimos leer a cualquiera
        if request.method == 'GET':
            return True
        # Autenticado y dueño
        return request.user.is_authenticated and (obj.owner == request.user)


class IsUserAdminStaffOrReadOnly(BasePermission):

    def has_permission(self, request, view):
        # Permitimos leer a cualquiera
        if request.method == 'GET':
            return True
        # Autenticado y admin o staff
        return request.user.is_authenticated or (request.user.is_staff or request.user.is_superuser)
