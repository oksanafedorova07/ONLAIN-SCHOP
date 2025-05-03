from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import product_detail, contacts, product_list

app_name = "catalog"

urlpatterns = [
     path("product/", product_list, name="product_list"),
     path("contacts/", contacts, name="contacts"),
     path('product/<int:pk>/', product_detail, name="product_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)