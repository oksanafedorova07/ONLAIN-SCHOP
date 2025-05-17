from django.shortcuts import render
from django.views.generic import ListView, DetailView, View

from .models import Product, Contact



class ProductListView(ListView):
    model = Product



class ProductDetailView(DetailView):
    model = Product


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
