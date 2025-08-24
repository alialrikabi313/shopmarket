from rest_framework import serializers
from .models import Product, ProductImage, Category, Brand, Review

class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = ["id", "name", "slug"]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug"]

class ProductImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)

    class Meta:
        model = ProductImage
        fields = ["id", "image", "alt_text", "is_primary"]

class ReviewSerializer(serializers.ModelSerializer):
    user_id = serializers.IntegerField(source="user.id", read_only=True)
    username = serializers.CharField(source="user.username", read_only=True)

    class Meta:
        model = Review
        fields = [
            "id", "product", "user_id", "username",
            "rating", "title", "comment",
            "created_at", "updated_at",
        ]
        read_only_fields = ["product", "user_id", "username", "created_at", "updated_at"]

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("rating must be between 1 and 5.")
        return value

class ProductSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()
    category = CategorySerializer()
    images = ProductImageSerializer(many=True, read_only=True)
    primary_image_url = serializers.SerializerMethodField()
    average_rating = serializers.DecimalField(max_digits=3, decimal_places=2, read_only=True)
    reviews_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "sku", "title", "slug", "description",
            "brand", "category", "price", "stock", "is_active",
            "primary_image_url", "images",
            "average_rating", "reviews_count",
        ]

    def get_primary_image_url(self, obj):
        request = self.context.get("request")
        primary = next((img for img in obj.images.all() if img.is_primary), None)
        if not primary:
            primary = obj.images.first()
        if not primary:
            return None
        url = primary.image.url
        return request.build_absolute_uri(url) if request else url

from rest_framework import serializers
from .models import Review, Product

class ReviewSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = ["id", "product", "user", "rating", "title", "body", "created_at", "updated_at"]
        read_only_fields = ["id", "user", "created_at", "updated_at", "product"]

class ReviewCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Review
        fields = ["rating", "title", "body"]

    def validate_rating(self, value):
        if not (1 <= value <= 5):
            raise serializers.ValidationError("Rating must be between 1 and 5.")
        return value
