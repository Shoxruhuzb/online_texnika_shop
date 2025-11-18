from django.db.models import CASCADE, ForeignKey, PositiveIntegerField, OneToOneField

from apps.models.base import CreatedBaseModel, UUIDBaseModel


class Cart(UUIDBaseModel, CreatedBaseModel):
    user = OneToOneField('apps.User', CASCADE, related_name='cart')

    @property
    def total_items(self):
        return self.items.count()

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class CartItem(UUIDBaseModel, CreatedBaseModel):
    cart = ForeignKey('apps.Cart', CASCADE, related_name='items')
    product = ForeignKey('apps.Product', CASCADE)
    quantity = PositiveIntegerField(default=1)

    class Meta:
        unique_together = ('cart', 'product')

    @property
    def total_price(self):
        return (self.product.discount_price or self.product.price) * self.quantity
