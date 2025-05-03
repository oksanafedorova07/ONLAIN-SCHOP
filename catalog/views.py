from django.shortcuts import render, get_object_or_404
from .models import Product, Contact, Category



def product_list(request):
    products = Product.objects.all()
    context = {"products": products}
    return render(request, 'catalog/product_list.html', context)

def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    context = {"product": product}
    return render(request, 'catalog/product_detail.html', context)

def contacts(request):
    if request.method == "POST":
        name = request.POST.get("name")
        phone = request.POST.get("phone")
        message = request.POST.get("message")

        if name and phone and message:
            print(f"Новое сообщение от {name} ({phone}): {message}")
            return render(request, "catalog/contacts.html", {"success": True})
        else:
            return render(
                request, "catalog/contacts.html", {"error": "Заполните все поля"}
            )

    return render(request, "catalog/contacts.html")
