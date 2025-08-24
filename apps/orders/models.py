from django.conf import settings
from django.db import models
from apps.catalog.models import Product

User = settings.AUTH_USER_MODEL

class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    full_name = models.CharField(max_length=120)
    line1 = models.CharField(max_length=200)
    line2 = models.CharField(max_length=200, blank=True)
    city = models.CharField(max_length=100)
    country = models.CharField(max_length=2, default="IQ")
    phone = models.CharField(max_length=30, blank=True)
    def __str__(self): return f"{self.full_name} - {self.city}"

class Order(models.Model):
    PENDING, PAID, SHIPPED, CANCELLED = "PENDING","PAID","SHIPPED","CANCELLED"
    STATUS_CHOICES = [(PENDING,PENDING),(PAID,PAID),(SHIPPED,SHIPPED),(CANCELLED,CANCELLED)]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    shipping_address = models.ForeignKey(Address, on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=PENDING)
    subtotal = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    def __str__(self): return f"Order#{self.id} - {self.user}"

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)
