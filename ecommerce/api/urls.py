from django.urls import path
from .views import list_products, create_product

urlpatterns = [
    path('products/', list_products, name="ListProducts"),
    path('shop/product/create', create_product, name="CreateProduct")
]