from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import ProductDetailView, ContactView, ProductListView

app_name = "catalog"

urlpatterns = [
     path("product/", ProductListView.as_view(), name="product_list"),
     path("contacts/", ContactView.as_view(), name="contacts"),
     path('product/<int:pk>/', ProductDetailView.as_view(), name="product_detail"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)