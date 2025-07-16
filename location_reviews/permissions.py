from rest_framework.permissions import BasePermission, SAFE_METHODS

    
class IsAuthenticatedOrAdminForUnsafe(BasePermission):
    """
    Дозволяє SAFE_METHODS для автентифікованих, інші — лише для адмінів.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return request.user and request.user.is_authenticated
        return request.user and request.user.is_staff 
    
class IsAuthenticatedOrAdminOwnerForUnsafe(BasePermission):
    """
    Дозволяє доступ до безпечних методів автентифікованим користувачам,
    а до небезпечних — лише власнику або адміністратору.
    """
    def has_object_permission(self, request, view, obj):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.method in SAFE_METHODS:
            return True
        if request.user.is_staff:
            return True
        return hasattr(obj, 'user') and obj.user == request.user 
    