from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import ProdutoViewSet

# DRF cria um CRUD base (GET, POST, PUT, PATCH, DELETE)
router = DefaultRouter()
router.register(r'produtos', ProdutoViewSet, basename="produto") # criação

urlpatterns = [
    path('', include(router.urls))
] # oficialização