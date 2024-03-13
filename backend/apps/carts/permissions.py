from rest_framework.permissions import BasePermission


class IsOwnerAdminStaff(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user or request.user.is_staff or request.user.is_admin
