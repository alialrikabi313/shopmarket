from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.db.models import Avg, Count
from .models import Review, Product

def _recompute_product_stats(product_id: int):
    agg = Review.objects.filter(product_id=product_id).aggregate(
        avg=Avg("rating"), cnt=Count("id")
    )
    Product.objects.filter(id=product_id).update(
        average_rating=(agg["avg"] or 0),
        reviews_count=agg["cnt"] or 0,
    )

@receiver(post_save, sender=Review)
def on_review_saved(sender, instance: Review, **kwargs):
    _recompute_product_stats(instance.product_id)

@receiver(post_delete, sender=Review)
def on_review_deleted(sender, instance: Review, **kwargs):
    _recompute_product_stats(instance.product_id)
