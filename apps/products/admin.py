from django.contrib import admin

from apps.products.models import Product, ProductImage,ProductFeatures


class ProductFeatureInline(admin.TabularInline):
    model = ProductFeatures
    min_num = 1



class ProductImageInline(admin.TabularInline):  # To'g'ri inline klassini aniqlang
    model = ProductImage


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductFeatureInline,ProductImageInline]
    readonly_fields = ('price','old_price')

