from django.shortcuts import render
from django.http import HttpResponse


def home(request):
    latest_products = Product.objects.order_by("-created_at")[:5]
    print("Последние продукты:", latest_products)
    return render(request, "catalog/home.html", {"products": latest_products})


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
