from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.core.exceptions import PermissionDenied

from .models import Product, Contact
from .forms import ProductForm





class PublishProduct(LoginRequiredMixin, PermissionRequiredMixin, View):
    permission_required = 'catalog.can_unpublish_product'
    raise_exception = True  # Показывать 403 вместо перенаправления на логин

    def post(self, request, pk):
        product = get_object_or_404(Product, pk=pk)
        product.is_published = not product.is_published  # Инвертируем статус
        product.save()
        return redirect('catalog:product_detail', pk=product.pk)



class ProductListView(ListView):
    model = Product



class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    success_url = reverse_lazy('catalog:product_list')

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_update.html"
    success_url = reverse_lazy('catalog:product_list')

    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if obj.owner != request.user:
            raise PermissionDenied("Вы не являетесь владельцем этого продукта.")
        return super().dispatch(request, *args, **kwargs)


class ProductDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')

    def test_func(self):
        product = self.get_object()
        return (
            product.owner == self.request.user or
            self.request.user.has_perm('catalog.can_delete_product')
        )

    def handle_no_permission(self):
        raise PermissionDenied("У вас нет прав для удаления этого продукта")

    def custom_permission_denied(request, exception=None):
        return HttpResponseForbidden(render(request, '403.html'))


class ContactView(View):
    model = Contact
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
