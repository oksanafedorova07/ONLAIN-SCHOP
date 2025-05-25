from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, View, CreateView, UpdateView, DeleteView
import os
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from .models import Product, Contact
from .forms import ProductForm


class ProductListView(ListView):
    model = Product



class ProductDetailView(DetailView):
    model = Product


class ProductCreateView(LoginRequiredMixin, CreateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_form.html"
    success_url = reverse_lazy('catalog:product_list')


class ProductUpdateView(LoginRequiredMixin, UpdateView):
    model = Product
    form_class = ProductForm
    template_name = "catalog/product_update.html"
    success_url = reverse_lazy('catalog:product_list')


class ProductDeleteView(LoginRequiredMixin, DeleteView):
    model = Product
    success_url = reverse_lazy('catalog:product_list')
    template_name = 'catalog/product_confirm_delete.html'
    login_url = '/accounts/login/'

    def delete(self, request, *args, **kwargs):
        # Удаление файла изображения
        self.object = self.get_object()
        if self.object.photo:
            file_path = os.path.join(settings.MEDIA_ROOT, str(self.object.photo))
            if os.path.exists(file_path):
                os.remove(file_path)
        return super().delete(request, *args, **kwargs)



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
