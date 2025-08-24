from django.conf import settings
from django.db import models
from apps.catalog.models import Product

User = settings.AUTH_USER_MODEL

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart")
    updated_at = models.DateTimeField(auto_now=True)
    def __str__(self): return f"Cart({self.user})"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    class Meta:
        unique_together = ("cart","product")
