from rest_framework import serializers
from .models import Address, Order, OrderItem
from apps.carts.models import Cart, CartItem
from django.db import transaction
from django.core.exceptions import ValidationError

class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = ["id","full_name","line1","line2","city","country","phone"]

class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id","product","unit_price","quantity"]
        read_only_fields = ["unit_price"]

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    shipping_address_id = serializers.PrimaryKeyRelatedField(queryset=Address.objects.all(), source="shipping_address", write_only=True)
    class Meta:
        model = Order
        fields = ["id","status","subtotal","total","created_at","items","shipping_address_id"]
        read_only_fields = ["status","subtotal","total","created_at","items"]

    @transaction.atomic
    def create(self, validated_data):
        user = self.context["request"].user
        shipping_address = validated_data["shipping_address"]
        cart = Cart.objects.get(user=user)
        items_qs = CartItem.objects.filter(cart=cart).select_related("product")

        if not items_qs.exists():
            raise ValidationError("Cart is empty")

        order = Order.objects.create(user=user, shipping_address=shipping_address)
        subtotal = 0

        # تحقق مخزون
        for item in items_qs:
            if item.quantity > item.product.stock:
                raise ValidationError(f"Not enough stock for {item.product.title}")

        # أنشئ البنود وخصم المخزون
        for item in items_qs:
            price = item.product.price
            OrderItem.objects.create(
                order=order, product=item.product, unit_price=price, quantity=item.quantity
            )
            item.product.stock -= item.quantity
            item.product.save(update_fields=["stock"])
            subtotal += price * item.quantity

        order.subtotal = subtotal
        order.total = subtotal
        order.save(update_fields=["subtotal", "total"])

        items_qs.delete()  # تفريغ السلة
        return order