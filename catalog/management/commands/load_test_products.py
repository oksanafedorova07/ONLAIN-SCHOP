from django.core.management.base import BaseCommand
from catalog.models import Category, Product
from faker import Faker
import random

fake = Faker("ru_RU")


class Command(BaseCommand):
    help = "Загрузка тестовых товаров и категорий"

    def handle(self, *args, **options):
        # Очистка старых данных
        Product.objects.all().delete()
        Category.objects.all().delete()

        # Создание категорий
        categories = [
            Category.objects.create(
                name=fake.word().capitalize(), description=fake.text()
            )
            for _ in range(5)
        ]

        # Создание товаров (по 10 в каждой категории)
        for category in categories:
            for _ in range(10):
                Product.objects.create(
                    name=fake.sentence(nb_words=3),
                    description=fake.text(),
                    image="products/default.jpg",  # Требуется предварительно создать
                    category=category,
                    price=random.randint(100, 10000),
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"Успешно создано: {Category.objects.count()} категорий и {Product.objects.count()} товаров"
            )
        )
