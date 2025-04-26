from django.core.management.base import BaseCommand
from catalog.models import Product, Category


class Command(BaseCommand):
    help = "Load test products"

    def handle(self, *args, **options):
        Product.objects.all().delete()
        Category.objects.all().delete()

        cat1 = Category.objects.create(name="Test Category 1", description="...")
        Product.objects.create(name="Test Product 1", category=cat1, price=100)
        self.stdout.write(self.style.SUCCESS("Тестовые данные добавлены"))
