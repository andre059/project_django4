# Generated by Django 4.2.3 on 2023-08-04 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='materials',
            name='is_published',
            field=models.BooleanField(default=True, verbose_name='опубликовано'),
        ),
        migrations.AddField(
            model_name='materials',
            name='slug',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='slug'),
        ),
        migrations.AddField(
            model_name='materials',
            name='views_count',
            field=models.IntegerField(default=0, verbose_name='просмотры'),
        ),
    ]
