from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsOwnerOrAdmin(BasePermission):
    """
    Allow update/delete only for owner or admin.
    """
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        if request.user and request.user.is_staff:
            return True
        return obj.user == request.user

class IsAuthenticatedSafeMethod(BasePermission):
    """
    Allow safe methods for authenticated users.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return False
    