from io import BytesIO
from PIL import Image
from django.core.files.base import ContentFile
from django.db.models import CharField, FloatField, TextField, ImageField, ForeignKey, CASCADE
from django.utils.translation import gettext_lazy as _
from apps.models.base import UUIDBaseModel, CreatedBaseModel


class Product(UUIDBaseModel, CreatedBaseModel):
    name = CharField(max_length=255, verbose_name=_("Name"))
    price = FloatField(verbose_name=_("Price"))
    discount_price = FloatField(blank=True, null=True, verbose_name=_("Discount price"))
    discount_percent = FloatField(blank=True, null=True, verbose_name=_("Discount percent"))
    product_amount = FloatField(blank=True, null=True, verbose_name=_("Amount"))
    description = TextField(verbose_name=_('Description'))

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    @property
    def image_count(self):
        return self.images.count()

    @property
    def first_image(self):
        image = self.images.first()
        if image:
            return image.image.url
        return None


class ProductImage(UUIDBaseModel):
    product = ForeignKey('apps.Product', CASCADE, related_name='images')
    image = ImageField(upload_to='images/%Y/%m/%d')

    def save(self, *args, **kwargs):
        if self.image:
            img = Image.open(self.image)
            img = img.convert('RGB')

            img.thumbnail((800, 800), Image.ANTIALIAS)

            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=80)
            file_name = self.image.name.split('.')[0] + '.webp'
            self.image.save(file_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)


class ProductAttribute(UUIDBaseModel):
    product = ForeignKey(Product, CASCADE, related_name='attributes')
    key = CharField(max_length=50, verbose_name=_("Attribute Name"))
    value = CharField(max_length=100, verbose_name=_("Attribute Value"))

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")
        unique_together = ('product', 'key')