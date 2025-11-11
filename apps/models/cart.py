from apps.models.base import CreatedBaseModel, UUIDBaseModel
from apps.models.products import Product
from django.conf import settings
from django.db.models import CASCADE, BooleanField, CharField, ForeignKey, PositiveIntegerField

User = settings.AUTH_USER_MODEL


class Cart(UUIDBaseModel, CreatedBaseModel):
    user = ForeignKey(User, CASCADE, null=True, blank=True)  # null=True, blank=True olib tashlash
    session_key = CharField(max_length=255, null=True, blank=True)
    is_active = BooleanField(default=True)

    def __str__(self):
        if self.user:
            return f"Cart ({self.user.phone})"
        return f"Cart (session: {self.session_key})"

    @property
    def total_items(self):
        return self.items.count()

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(UUIDBaseModel, CreatedBaseModel):
    cart = ForeignKey(Cart, CASCADE, related_name='items')
    product = ForeignKey(Product, on_delete=CASCADE)
    quantity = PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def total_price(self):
        price = self.product.discount_price or self.product.price
        return price * self.quantity
