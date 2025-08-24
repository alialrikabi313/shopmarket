# apps/common/permissions.py
from rest_framework.permissions import BasePermission, SAFE_METHODS

class IsAdminOrReadOnly(BasePermission):
    """قراءة مفتوحة للجميع، والكتابة/الحذف فقط للـ staff."""
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return bool(request.user and request.user.is_staff)

class IsOwner(BasePermission):
    """يسمح بالوصول إذا كان الكائن يخصّ المستخدم."""
    owner_attr = "user"  # غيّرها داخل الviews إذا اختلفت

    def has_object_permission(self, request, view, obj):
        user = getattr(obj, self.owner_attr, None)
        return bool(request.user and user == request.user)

class IsCartItemOwner(BasePermission):
    """الكارت آيتم يخصّ صاحب الـ cart."""
    def has_object_permission(self, request, view, obj):
        return bool(request.user and obj.cart.user_id == request.user.id)

class IsOrderOwnerOrStaff(BasePermission):
    """صاحب الطلب أو staff."""
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return bool(request.user and obj.user_id == request.user.id)

class IsReviewOwnerOrStaff(BasePermission):
    """صاحب المراجعة أو staff."""
    def has_object_permission(self, request, view, obj):
        if request.user and request.user.is_staff:
            return True
        return bool(request.user and obj.user_id == request.user.id)
