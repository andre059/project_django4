from django.core.management import BaseCommand

from catalog.models import Product, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        product_list = [
            {'name': 'Дыня', 'category': 'Плодоовощные товары'},
            {'name': 'Молоток', 'category': 'Ручной инструмент'},
            {'name': 'Хлеб', 'category': 'Зерно-мучные товары'},
        ]

        product_objects = []
        for product_item in product_list:
            product_objects.append(Product(**product_item))

        Product.objects.bulk_create(product_objects)

        Category.objects.all().delete()
