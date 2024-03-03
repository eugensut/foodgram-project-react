from rest_framework import permissions


class RecipesPermissions(permissions.BasePermission):

    def has_permission(self, request, view):
        return bool(
            request.method in permissions.SAFE_METHODS or
            request.method in ('POST', 'PATCH')
            and request.user.is_authenticated
        )
    
    def has_object_permission(self, request, view, obj):
        return bool(
            request.method in permissions.SAFE_METHODS
            or request.user.is_staff
            or obj.author == request.user
        )


