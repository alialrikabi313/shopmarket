from rest_framework import permissions

class IsOwnerOrAdmin(permissions.BasePermission):
    """
    يسمح للمالك بالتعديل/الحذف، وكذلك للمشرفين (staff/superuser).
    القراءة متاحة للجميع (إن استخدمتها مع قواعد عامة).
    """
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        if request.user and request.user.is_superuser:
            return True
        return getattr(obj, "user_id", None) == getattr(request.user, "id", None)
