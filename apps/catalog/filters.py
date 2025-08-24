import django_filters as df
from .models import Product

class ProductFilter(df.FilterSet):
    q = df.CharFilter(field_name="title", lookup_expr="icontains")
    min_price = df.NumberFilter(field_name="price", lookup_expr="gte")
    max_price = df.NumberFilter(field_name="price", lookup_expr="lte")
    brand = df.CharFilter(field_name="brand__slug", lookup_expr="iexact")
    category = df.CharFilter(field_name="category__slug", lookup_expr="iexact")

    class Meta:
        model = Product
        fields = ["q", "min_price", "max_price", "brand", "category", "is_active"]
