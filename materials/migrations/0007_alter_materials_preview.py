# Generated by Django 4.2.5 on 2023-10-08 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0006_rename_title_materials_name_materials_price_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materials',
            name='preview',
            field=models.ImageField(blank=True, null=True, upload_to='blog/', verbose_name='изображение'),
        ),
    ]
