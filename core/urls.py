# core/urls.py
from logging import root

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import HttpResponse
from django.views.generic import RedirectView

from apps.catalog.views import ProductReviewListCreateView, ReviewDetailView

from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

def health(request):
    return HttpResponse("ok")

urlpatterns = [
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("admin/", admin.site.urls),
    path("health/", health),
    path("", RedirectView.as_view(url="/api/docs/", permanent=False)),  # الهوم -> الدوكس
    path("admin/", admin.site.urls),
    path("health/", lambda r: HttpResponse("ok")),
    path("api/docs/", include("drf_spectacular.urls")),  # swagger/redoc
    path("api/v1/", include("apps.catalog.urls")),
    path("api/v1/", include("apps.carts.urls")),
    path("api/v1/", include("apps.orders.urls")),    path("api/v1/products/<int:product_id>/reviews/", ProductReviewListCreateView.as_view(), name="product-reviews"),
    path("api/v1/reviews/<int:pk>/", ReviewDetailView.as_view(), name="review-detail"),
    path("admin/", admin.site.urls),
    path("health/", health),

    # ✅ مخطط OpenAPI:
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),

    # ✅ Swagger UI مقيّد بالمخطط السابق
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),

    # (اختياري) ReDoc:
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
