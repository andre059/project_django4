from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Materials(models.Model):
    name = models.CharField(max_length=150, verbose_name='название')
    body = models.TextField(verbose_name='описение')

    price = models.IntegerField(**NULLABLE, verbose_name='цена')

    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    preview = models.ImageField(verbose_name='изображение', upload_to='blog/', **NULLABLE)
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)

    is_active = models.BooleanField(default=True, verbose_name='есть в наличии')

    def __str__(self):
        return f'{self.name} {self.preview}'

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
