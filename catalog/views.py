from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.core.exceptions import PermissionDenied
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.core.cache import cache
from django.db.models import Q

from .models import Product, Contact, Category
from .forms import ProductForm
from .services import get_product_from_cache, get_products_by_category


@method_decorator(cache_page(60 * 15), name='dispatch')
class ProductDetailView(DetailView):
    model = Product
    context_object_name = 'product'


class CategoryListView(ListView):
    """Список всех категорий"""
    model = Category
    template_name = 'catalog/category_list.html'
    context_object_name = 'categories'

    def get_queryset(self):

     return Category.objects.all()


def get_category_products(category_slug):
    """Возвращает продукты указанной категории с кешированием"""
    cache_key = f'category_products_{category_slug}'
    products = cache.get(cache_key)

    if products is None:
        # Если нет в кеше - получаем из БД
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(
            category=category,
            is_published=True
        ).select_related('owner', 'category')
        cache.set(cache_key, products, 60 * 60 * 2)  # Кешируем на 2 часа
    return products


class CategoryProductsView(ListView):
    template_name = 'catalog/category_products.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        category_slug = self.kwargs.get('category_slug')
        only_published = not self.request.user.is_staff  # Для админов показываем все
        return get_products_by_category(category_slug, only_published)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        category_slug = self.kwargs.get('category_slug')
        context['category'] = get_object_or_404(Category, slug=category_slug)
        return context


class ProductListView(ListView):
    model = Product
    template_name = 'catalog/product_list.html'
    context_object_name = 'products'
    paginate_by = 10

    def get_queryset(self):
        return get_product_from_cache()


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = 'catalog/product_form.html'
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого продукта.")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    template_name = 'catalog/product_confirm_delete.html'
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        return (
                product.owner == self.request.user or
                self.request.user.has_perm('catalog.can_delete_product')
        )

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав для удаления этого продукта")


class PublishProduct(LoginRequiredMixin, PermissionRequiredMixin, View):
    """Изменение статуса публикации товара"""
    permission_required = 'catalog.can_publish_product'
    raise_exception = True

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = not product.is_published
        product.save()

        # Инвалидация кеша при изменении статуса публикации
        cache.delete(f'category_products_{product.category.slug}')
        return redirect('catalog:product_detail', pk=product.pk)


class ContactView(View):
    """Страница контактов"""
    template_name = 'catalog/contacts.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        context = {}
        if name and phone and message:
            print(f"Новое сообщение от {name} ({phone}): {message}")
            context['success'] = True
        else:
            context['error'] = 'Заполните все поля'

        return render(request, self.template_name, context)