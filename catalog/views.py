from django.shortcuts import render
from .models import Product, Category  # Импорт всех необходимых моделей


def home(request):
    latest_products = Product.objects.order_by("-created_at")[:5]
    categories = Category.objects.all()
    context = {"products": latest_products, "categories": categories}
    return render(request, "catalog/home.html", context)


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
