from django.contrib import admin
from catalog.models import Product


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image', 'availability',)
    search_fields = ('name', 'category', 'image', 'availability',)
    list_filter = ('availability',)
