from apps.models import Product, ProductImage, User
from apps.models.products import ProductAttribute
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.html import format_html


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
class CustomUserAdmin(UserAdmin):
    list_display = ('id', 'phone', 'is_active', 'is_staff', 'is_superuser')
    list_filter = ('is_staff', 'is_superuser', 'is_active')
    search_fields = ('phone',)
    ordering = ('id',)

    fieldsets = (
        (None, {'fields': ('phone', 'password')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('phone', 'password1', 'password2', 'is_active', 'is_staff', 'is_superuser'),
        }),
    )
