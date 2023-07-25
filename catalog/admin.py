from django.contrib import admin
from catalog.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image', 'purchase_price', 'availability',)
    search_fields = ('name', 'category', 'image', 'purchase_price', 'availability',)
    list_filter = ('availability',)
