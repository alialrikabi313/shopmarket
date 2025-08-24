from rest_framework import viewsets, permissions, filters, response, status, generics
from django.shortcuts import get_object_or_404
from .serializers import ProductSerializer, CategorySerializer, BrandSerializer, ReviewSerializer
from .permissions import IsOwnerOrAdmin
from apps.common.permissions import IsAdminOrReadOnly, IsReviewOwnerOrStaff
from .models import Product, Brand, Category, ProductImage, Review
from .serializers import (
    ProductSerializer, BrandSerializer, CategorySerializer, ProductImageSerializer
)

class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all().select_related("brand", "category")
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]

class BrandViewSet(viewsets.ModelViewSet):
    queryset = Brand.objects.all()
    serializer_class = BrandSerializer
    permission_classes = [IsAdminOrReadOnly]

class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]

class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    permission_classes = [IsAdminOrReadOnly]

class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.select_related("product", "user").all()
    serializer_class = ReviewSerializer

    def get_permissions(self):
        if self.action in ["update", "partial_update", "destroy"]:
            return [permissions.IsAuthenticated(), IsReviewOwnerOrStaff()]
        elif self.action in ["create"]:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]  # list/retrieve

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
        from rest_framework import generics, permissions
from rest_framework.exceptions import ValidationError, PermissionDenied
from .models import Product, Review
from .serializers import ReviewSerializer, ReviewCreateSerializer

class IsOwnerOrStaff(permissions.BasePermission):
    def has_object_permission(self, request, view, obj: Review):
        return request.user.is_staff or obj.user_id == request.user.id

class ProductReviewListCreateView(generics.ListCreateAPIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs["product_id"]).select_related("user", "product")

    def get_serializer_class(self):
        if self.request.method == "POST":
            return ReviewCreateSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        product_id = self.kwargs["product_id"]
        if Review.objects.filter(product_id=product_id, user=self.request.user).exists():
            raise ValidationError("You have already reviewed this product.")
        product = Product.objects.get(pk=product_id)
        serializer.save(user=self.request.user, product=product)

class ReviewDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Review.objects.select_related("user", "product")
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrStaff]

    def get_serializer_class(self):
        if self.request.method in ["PUT", "PATCH"]:
            return ReviewCreateSerializer
        return ReviewSerializer

    def perform_update(self, serializer):
        obj = self.get_object()
        if not (self.request.user.is_staff or obj.user_id == self.request.user.id):
            raise PermissionDenied("Not allowed.")
        serializer.save()

    def perform_destroy(self, instance):
        if not (self.request.user.is_staff or instance.user_id == self.request.user.id):
            raise PermissionDenied("Not allowed.")
        instance.delete()
