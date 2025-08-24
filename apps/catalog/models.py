from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.db.models import Avg, Count
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver

User = settings.AUTH_USER_MODEL

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Brand(models.Model):
    name = models.CharField(max_length=120, unique=True)
    slug = models.SlugField(max_length=140, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name


class Product(models.Model):
    sku = models.CharField(max_length=64, unique=True)
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # حقول مجمّعة للمراجعات
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0)  # 0.00 .. 5.00
    reviews_count = models.PositiveIntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=["slug"], name="catalog_pro_slug_idx"),
            models.Index(fields=["brand", "category"], name="catalog_pro_brand_cat_idx"),
        ]
        ordering = ["-id"]

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    image = models.ImageField(upload_to="products/%Y/%m")
    alt_text = models.CharField(max_length=255, blank=True)
    is_primary = models.BooleanField(default=False)

    class Meta:
        ordering = ["-id"]

    def __str__(self):
        return f"Image for {self.product_id}"


# ============ الجديد: نموذج المراجعات ============
class Review(models.Model):
    RATING_CHOICES = [(i, str(i)) for i in range(1, 6)]  # 1..5

    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    title = models.CharField(max_length=200, blank=True)
    comment = models.TextField(blank=True, max_length=4000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "user")
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["product"], name="catalog_review_product_idx"),
            models.Index(fields=["user"], name="catalog_review_user_idx"),
            models.Index(fields=["rating"], name="catalog_review_rating_idx"),
        ]

    def __str__(self):
        return f"Review p{self.product_id} u{self.user_id} r{self.rating}"


# تحديث التجميعيّات على المنتج عند إنشاء/تعديل/حذف مراجعة
def _recompute_product_rating_counts(product_id: int):
    agg = Review.objects.filter(product_id=product_id).aggregate(
        avg=Avg("rating"), cnt=Count("id")
    )
    avg = agg["avg"] or 0
    cnt = agg["cnt"] or 0
    # تحديث المنتج مباشرةً
    Product.objects.filter(id=product_id).update(
        average_rating=round(avg, 2) if avg else 0,
        reviews_count=cnt,
    )

@receiver(post_save, sender=Review)
def on_review_saved(sender, instance: Review, **kwargs):
    _recompute_product_rating_counts(instance.product_id)

@receiver(post_delete, sender=Review)
def on_review_deleted(sender, instance: Review, **kwargs):
    _recompute_product_rating_counts(instance.product_id)
from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator

class Review(models.Model):
    product = models.ForeignKey(Product, related_name="reviews", on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="reviews", on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    title = models.CharField(max_length=200, blank=True)
    body = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("product", "user")
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.product.title} - {self.user} ({self.rating})"
