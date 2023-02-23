from django.contrib import admin
from mptt.admin import MPTTModelAdmin
from .models import Category, ProductProp, ProductType, ProductImage, ProductDetail, ProductPropValue, Product

admin.site.register(Category, MPTTModelAdmin)


class ProductPropInline(admin.TabularInline):
    model = ProductProp


@admin.register(ProductType)
class ProductTypeAdmin(admin.ModelAdmin):
    inlines = [
        ProductPropInline
    ]


class ProductImageInline(admin.TabularInline):
    model = ProductImage


class ProductDetailInline(admin.TabularInline):
    model = ProductDetail


class ProductPropValueInline(admin.TabularInline):
    model = ProductPropValue


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [
        ProductPropValueInline,
        ProductDetailInline,
        ProductImageInline
    ]
# Register your models here.
