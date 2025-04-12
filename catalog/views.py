from django.shortcuts import render
from django.http import HttpResponse


def contacts(request):
    return render(request, 'catalog/contacts.html')

def home(request):
    return render(request, 'catalog/home.html')


def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        message = request.POST.get('message')

        if name and phone and message:
            print(f"Новое сообщение от {name} ({phone}): {message}")
            return render(request, 'catalog/contacts.html', {'success': True})
        else:
            return render(request, 'catalog/contacts.html', {'error': 'Заполните все поля'})

    return render(request, 'catalog/contacts.html')