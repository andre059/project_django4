# Generated by Django 4.2.3 on 2023-08-25 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalog', '0006_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='product',
            name='email',
            field=models.EmailField(blank=True, max_length=254, null=True, unique=True, verbose_name='почта'),
        ),
    ]