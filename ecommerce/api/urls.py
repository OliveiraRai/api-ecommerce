from django.urls import path
from .views import list_products, create_product, create_customer, create_seller

urlpatterns = [
    path('products/', list_products, name="ListProducts"),
    path('shop/product/create', create_product, name="CreateProduct"),
    path('create/customer', create_customer, name="CreateCustomer"),
    path('create/seller', create_seller, name="CreateSeller"),
]