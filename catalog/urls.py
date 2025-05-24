from django.urls import path
from django.conf import settings
from django.conf.urls.static import static


from .views import ProductDetailView, ContactView, ProductListView, ProductCreateView, ProductUpdateView, ProductDeleteView

app_name = "catalog"

urlpatterns = [
     path("product/", ProductListView.as_view(), name="product_list"),
     path("product/form/", ProductCreateView.as_view(), name= "product_form"),
     path("product/update/<int:pk>/", ProductUpdateView.as_view(), name= "product_update"),
     path("contacts/", ContactView.as_view(), name="contacts"),
     path('product/<int:pk>/', ProductDetailView.as_view(), name="product_detail"),
     path('<int:pk>/delete/', ProductDeleteView.as_view(), name="product_confirm_delete"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)