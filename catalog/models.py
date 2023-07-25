from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.CharField(max_length=150, verbose_name='описание')
    image = models.ImageField(upload_to='preview/', verbose_name='изображение ', **NULLABLE)
    category = models.CharField(max_length=150, verbose_name='категория')
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='цена за покупку', **NULLABLE)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_modified_date = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')

    availability = models.BooleanField(default=True, verbose_name='есть в наличии')

    def __str__(self):

        return f'{self.name} {self.description} {self.image} {self.category} ' \
               f'{self.purchase_price} {self.creation_date} {self.last_modified_date} {self.availability}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('category', 'name',)


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.CharField(max_length=150, verbose_name='описание')
