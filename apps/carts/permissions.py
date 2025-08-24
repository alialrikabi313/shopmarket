from rest_framework.permissions import BasePermission

class IsCartOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return getattr(obj, "user", getattr(obj, "cart", None).user) == request.user
