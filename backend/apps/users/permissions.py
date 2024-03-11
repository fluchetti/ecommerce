from rest_framework.permissions import BasePermission


class IsUserAdminStaffOrReadOnly(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method == 'GET':
            return True

        return request.user == obj or request.user.is_superuser or request.user.is_staff


class IsAdminStaffOrPostOnly(BasePermission):

    def has_permission(self, request, view):

        if request.method != 'GET':
            return True

        return request.user.is_staff or request.user.is_superuser


class IsUser(BasePermission):

    def has_object_permission(self, request, view, obj):
        return request.user == obj
