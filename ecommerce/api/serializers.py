from rest_framework import serializers
from .models import Produto, Categoria

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto # modelo de origem dos dados
        fields = ["produto_id", "nome", "categoria", "preco", "estoque"] # campos que serão expostos em JSON
        
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome"]