from django.db import models

NULLABLE = {'blank': True, 'null': True}


class Materials(models.Model):
    title = models.CharField(max_length=150, verbose_name='название')
    body = models.TextField(verbose_name='содержимое')

    views_count = models.IntegerField(default=0, verbose_name='просмотры')
    is_published = models.BooleanField(default=True, verbose_name='опубликовано')
    created_at = models.DateField(auto_now_add=True, verbose_name='дата создания')
    preview = models.ImageField(verbose_name='Превью', upload_to='blog/', **NULLABLE)
    slug = models.CharField(max_length=150, verbose_name='slug', **NULLABLE)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'материал'
        verbose_name_plural = 'материалы'
