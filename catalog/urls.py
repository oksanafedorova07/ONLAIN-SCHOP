from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.views.decorators.cache import cache_page

from .views import ProductDetailView, ContactView, ProductListView, ProductCreateView, ProductUpdateView, \
     ProductDeleteView, PublishProduct, CategoryProductsView, CategoryListView

app_name = "catalog"

urlpatterns = [
     path("product/", ProductListView.as_view(), name="product_list"),
     path("product/form/", ProductCreateView.as_view(), name= "product_form"),
     path("product/update/<int:pk>/", ProductUpdateView.as_view(), name= "product_update"),
     path("contacts/", ContactView.as_view(), name="contacts"),
     path('product/<int:pk>/', cache_page(60)(ProductDetailView.as_view()), name="product_detail"),
     path('<int:pk>/delete/', ProductDeleteView.as_view(), name="product_confirm_delete"),
     path('product/<int:product_id>/unpublish/', PublishProduct.as_view(), name='publish_product'),
     path('product/<int:pk>/toggle-publish/', PublishProduct.as_view(), name='toggle_publish'),
     path('category/', CategoryListView.as_view(), name='category_list'),
     path('category/<slug:category_slug>/', CategoryProductsView.as_view(), name='category_products'),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)