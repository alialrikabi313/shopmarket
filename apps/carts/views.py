# apps/carts/views.py
from rest_framework import viewsets, permissions, decorators, response, status
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from .serializers import CartSerializer, CartItemSerializer
from apps.catalog.models import Product
from .services import add_to_cart, set_quantity_for_product
from ..common.permissions import IsCartItemOwner


class CartViewSet(viewsets.ViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def list(self, request):
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return response.Response(CartSerializer(cart).data)

    @decorators.action(detail=False, methods=["post"], url_path="add")
    def add(self, request):
        product_id = request.data.get("product_id")
        qty = int(request.data.get("quantity", 1))
        product = get_object_or_404(Product, pk=product_id)
        cart = add_to_cart(request.user, product, qty)
        return response.Response(CartSerializer(cart).data, status=status.HTTP_200_OK)


class CartItemViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsCartItemOwner]

    def get_queryset(self):
        # يجيب فقط عناصر سلة المستخدم
        return CartItem.objects.filter(cart__user=self.request.user).select_related("product", "cart")

    def partial_update(self, request, pk=None):
        """تحديث الكمية (PATCH /api/v1/cart-items/{id}/)"""
        qty = int(request.data.get("quantity", 1))
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        cart = set_quantity_for_product(request.user, item.product, qty)
        return response.Response(CartSerializer(cart).data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        """حذف عنصر من السلة (DELETE /api/v1/cart-items/{id}/)"""
        item = get_object_or_404(CartItem, pk=pk, cart__user=request.user)
        item.delete()
        cart, _ = Cart.objects.get_or_create(user=request.user)
        return response.Response(CartSerializer(cart).data, status=status.HTTP_200_OK)
