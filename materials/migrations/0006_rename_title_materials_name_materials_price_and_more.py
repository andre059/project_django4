# Generated by Django 4.2.5 on 2023-10-06 15:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0005_materials_is_active'),
    ]

    operations = [
        migrations.RenameField(
            model_name='materials',
            old_name='title',
            new_name='name',
        ),
        migrations.AddField(
            model_name='materials',
            name='price',
            field=models.IntegerField(blank=True, null=True, verbose_name='цена'),
        ),
        migrations.AlterField(
            model_name='materials',
            name='body',
            field=models.TextField(verbose_name='описение'),
        ),
        migrations.AlterField(
            model_name='materials',
            name='is_active',
            field=models.BooleanField(default=True, verbose_name='есть в наличии'),
        ),
    ]
