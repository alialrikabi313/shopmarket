from rest_framework import serializers
from .models import Cart, CartItem
from apps.catalog.serializers import ProductSerializer
from apps.catalog.models import Product

class CartItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)  # عرض تفاصيل المنتج
    product_id = serializers.PrimaryKeyRelatedField(
        queryset=Product.objects.all(), source="product", write_only=True
    )

    class Meta:
        model = CartItem
        fields = ["id", "product", "product_id", "quantity"]

class CartSerializer(serializers.ModelSerializer):
    items = CartItemSerializer(many=True, read_only=True)
    total = serializers.SerializerMethodField()

    class Meta:
        model = Cart
        fields = ["id", "items", "total", "updated_at"]

    def get_total(self, obj):
        return float(sum(i.product.price * i.quantity for i in obj.items.select_related("product")))
