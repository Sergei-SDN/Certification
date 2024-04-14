from rest_framework import permissions


class IsActiveEmployee(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if user and user.is_authenticated and user.is_active:
            return True
        return False
