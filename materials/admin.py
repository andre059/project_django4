from django.contrib import admin

from materials.models import Materials


@admin.register(Materials)
class MaterialsAdmin(admin.ModelAdmin):
    list_display = ('name', 'body', 'price', 'views_count', 'is_published', 'created_at', 'preview', 'slug', 'is_active')
    list_filter = ('name', 'views_count', 'created_at', 'is_active')
