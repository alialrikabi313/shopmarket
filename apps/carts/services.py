# apps/carts/services.py
from django.db import transaction
from django.shortcuts import get_object_or_404
from .models import Cart, CartItem
from apps.catalog.models import Product


def get_or_create_cart(user):
    """أرجع عربة المستخدم أو أنشئ واحدة."""
    cart, _ = Cart.objects.get_or_create(user=user)
    return cart


@transaction.atomic
def add_to_cart(user, product: Product, quantity: int = 1):
    """
    أضِف منتجًا إلى عربة المستخدم. لو العنصر موجود يزيد الكمية؛ وإلا يُنشَأ.
    """
    if quantity <= 0:
        return get_or_create_cart(user)

    cart = get_or_create_cart(user)
    # قفل الصف أثناء التعديل لتفادي السباق
    item, _ = CartItem.objects.select_for_update().get_or_create(
        cart=cart, product=product, defaults={"quantity": 0}
    )
    item.quantity = item.quantity + quantity
    item.save()
    # حدّث وقت آخر تعديل إن كان لديك حقل updated_at على Cart
    if hasattr(cart, "save"):
        cart.save(update_fields=None)
    return cart


@transaction.atomic
def set_quantity_for_product(user, product: Product, quantity: int):
    """
    عيّن كمية محددة لمنتج في عربة المستخدم.
    لو الكمية <= 0 يتم حذف العنصر.
    """
    cart = get_or_create_cart(user)
    item = CartItem.objects.filter(cart=cart, product=product).first()

    if item is None:
        if quantity <= 0:
            return cart
        CartItem.objects.create(cart=cart, product=product, quantity=quantity)
    else:
        if quantity <= 0:
            item.delete()
        else:
            item.quantity = quantity
            item.save()

    if hasattr(cart, "save"):
        cart.save(update_fields=None)
    return cart
