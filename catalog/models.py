from django.db import models


NULLABLE = {'blank': True, 'null': True}


class Category(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.TextField(**NULLABLE, verbose_name='описание')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Product(models.Model):
    name = models.CharField(max_length=150, verbose_name='наименование')
    description = models.CharField(max_length=150, verbose_name='описание')
    image = models.ImageField(upload_to='preview/', verbose_name='изображение ', **NULLABLE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='категория')
    purchase_price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name='цена за килограмм', **NULLABLE)
    creation_date = models.DateTimeField(auto_now_add=True, verbose_name='дата создания')
    last_modified_date = models.DateTimeField(auto_now=True, verbose_name='дата последнего изменения')

    availability = models.BooleanField(default=True, verbose_name='есть в наличии')

    def __str__(self):

        return f'{self.name} {self.description} {self.image} {self.category} {self.purchase_price}' \
               f'{self.creation_date} {self.last_modified_date} {self.availability}'

    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ('category', 'name',)


class Subject(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    description = models.TextField(verbose_name='описание')

    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='продукт')

    def __str__(self):
        return f'{self.title} ({self.product})'

    class Meta:
        verbose_name = 'предмет'
        verbose_name_plural = 'предметы'

