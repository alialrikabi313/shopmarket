# apps/orders/views.py
from rest_framework import viewsets, permissions, response, status
from rest_framework.decorators import action
from .models import Address, Order
from .serializers import AddressSerializer, OrderSerializer
from apps.common.permissions import IsOwner
from .serializers import AddressSerializer

class AddressViewSet(viewsets.ModelViewSet):
    serializer_class = AddressSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def get_queryset(self):
        return Address.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework import viewsets, permissions, decorators, response, status
from apps.common.permissions import IsOrderOwnerOrStaff
from .models import Order
from .serializers import OrderSerializer

class OrderViewSet(viewsets.ModelViewSet):
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticated, IsOrderOwnerOrStaff]

    def get_queryset(self):
        qs = Order.objects.all().prefetch_related("items")
        if self.request.user.is_staff:
            return qs
        return qs.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @decorators.action(detail=True, methods=["post"], permission_classes=[permissions.IsAdminUser])
    def set_status(self, request, pk=None):
        order = self.get_object()
        new_status = request.data.get("status")
        # تحقق من القيم المسموحة...
        order.status = new_status
        order.save(update_fields=["status"])
        return response.Response({"id": order.id, "status": order.status})
