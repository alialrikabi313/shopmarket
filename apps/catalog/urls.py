from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProductViewSet, CategoryViewSet, BrandViewSet, ReviewViewSet

router = DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'categories', CategoryViewSet, basename='category')
router.register(r'brands', BrandViewSet, basename='brand')

# مسارات المراجعات متداخلة حسب المنتج:
product_reviews = [
    path('products/<int:product_id>/reviews/', ReviewViewSet.as_view({'get': 'list', 'post': 'create'}), name='product-review-list'),
    path('products/<int:product_id>/reviews/<int:pk>/', ReviewViewSet.as_view({'get': 'retrieve', 'put': 'update', 'patch': 'partial_update', 'delete': 'destroy'}), name='product-review-detail'),
]

urlpatterns = [
    path('', include(router.urls)),
] + product_reviews
