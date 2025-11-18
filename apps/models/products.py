from io import BytesIO

from PIL import Image
from PIL.Image import Resampling
from django.core.files.base import ContentFile
from django.db.models import CASCADE, CharField, FloatField, ForeignKey, ImageField
from django.utils.translation import gettext_lazy as _
from django_ckeditor_5.fields import CKEditor5Field

from apps.models.base import CreatedBaseModel, UUIDBaseModel


class Product(UUIDBaseModel, CreatedBaseModel):
    name = CharField(_("Name"), max_length=255)
    price = FloatField(_("Price"))
    discount_price = FloatField(_("Discount price"), blank=True, null=True)
    product_amount = FloatField(_("Amount"), blank=True, null=True)
    # description = TextField(verbose_name=_('Description'))
    description = CKEditor5Field(verbose_name=_("Description"), config_name="default")

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

            img.thumbnail((800, 800), Resampling.LANCZOS)

            buffer = BytesIO()
            img.save(buffer, format='WEBP', quality=80)
            file_name = self.image.name.split('.')[0] + '.webp'
            self.image.save(file_name, ContentFile(buffer.getvalue()), save=False)

        super().save(*args, **kwargs)


class ProductAttribute(UUIDBaseModel):
    product = ForeignKey(Product, CASCADE, related_name='attributes')
    key = CharField(_("Attribute Name"), max_length=50)
    value = CharField(_("Attribute Value"), max_length=100)

    def __str__(self):
        return f"{self.key}: {self.value}"

    class Meta:
        verbose_name = _("Product Attribute")
        verbose_name_plural = _("Product Attributes")
        unique_together = ('product', 'key')
