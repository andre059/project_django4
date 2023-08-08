from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Materials(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    body = models.TextField(verbose_name='содержимое')

    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)
    created_at = models.DateField(verbose_name='Дата создания', auto_now_add=True)
    preview = models.ImageField(verbose_name='Превью', upload_to='blog/', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
