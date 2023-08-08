# Generated by Django 4.2.3 on 2023-08-08 08:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0002_materials_is_published_materials_slug_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='materials',
            name='created_at',
            field=models.DateField(auto_now_add=True, null=True, verbose_name='дата создания'),
        ),
        migrations.AddField(
            model_name='materials',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='Превью'),
        ),
    ]
