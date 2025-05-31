from django.core.cache import cache
from django.shortcuts import get_object_or_404

from catalog.models import Product, Category
from config.settings import CACHE_ENABLED


def get_product_from_cache():
    """Получаем данные про товары из кэша, если кэш пуст, получаем данные из БД."""
    if not CACHE_ENABLED:
        return Product.objects.all()
    key = "product_list"
    products = cache.get(key)
    if products is not None:
        return products
    products = Product.objects.all()
    cache.set(key, products)
    return products


def get_products_by_category(category_slug, only_published=True):
    """Возвращает продукты категории с кешированием."""
    cache_key = f'category_products_{category_slug}_{only_published}'
    products = cache.get(cache_key)

    if products is None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category)
        if only_published:
            products = products.filter(is_published=True)
        products = products.select_related('owner', 'category')
        cache.set(cache_key, products, 60 * 60 * 2)  # Кеш на 2 часа
    return products
