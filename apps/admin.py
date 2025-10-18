from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html

from apps.models import ProductImage, Product, User
from apps.models.products import ProductAttribute


class ProductImageInline(admin.StackedInline):
    model = ProductImage
    extra = 0
    min_num = 0
    max_num = 8


class ProductAttributeInline(admin.TabularInline):
    model = ProductAttribute
    extra = 1
    min_num = 0


@admin.register(ProductImage)
class ProductImageModelAdmin(admin.ModelAdmin):
    list_display = ["id", "product_name", "show_image"]

    @admin.display(description="Product Name")
    def product_name(self, obj):
        return obj.product.name

    @admin.display(description="Picture")
    def show_image(self, obj):
        return format_html('<img src="{}" width="90" height="80">', obj.image.url)


@admin.register(Product)
class ProductModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'image_count')
    inlines = [ProductImageInline, ProductAttributeInline]


@admin.register(User)
class UserModelAdmin(UserAdmin):
    pass
