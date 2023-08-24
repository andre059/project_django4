from django.contrib import admin
from catalog.models import Product, Category, Subject


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'category', 'image', 'purchase_price', 'availability', 'creation_date',
                    'last_modified_date',)
    list_display_links = ('name',)
    search_fields = ('name', 'category', 'purchase_price', 'availability',)
    list_filter = ('availability',)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'product')
    list_filter = ('product',)
