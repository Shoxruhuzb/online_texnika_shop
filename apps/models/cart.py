from django.db import models
from django.conf import settings
from apps.models.products import Product
from apps.models.base import UUIDBaseModel, CreatedBaseModel

User = settings.AUTH_USER_MODEL


class Cart(UUIDBaseModel, CreatedBaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=255, null=True, blank=True)
    is_active = models.BooleanField(default=True)

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
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def total_price(self):
        price = self.product.discount_price or self.product.price
        return price * self.quantity
