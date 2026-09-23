from rest_framework import serializers
from .models import Produto, Categoria, Cliente, Vendedor, Venda, ItensVenda

class ProdutoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Produto # modelo de origem dos dados
        fields = ["produto_id", "nome", "categoria", "preco", "estoque"] # campos que serão expostos em JSON
        
class CategoriaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Categoria
        fields = ["id", "nome"]
        
class ClienteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Cliente
        fields = ["cliente_id", "nome", "cpf", "celular", "email", "senha", "criado_em"]
        
class VendedorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vendedor
        fields = ["vendedor_id", "nome", "cnpj_cpf", "celular", "email", "senha", "criado_em"]
        
class VendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Venda
        fields = ["venda_id", "cliente", "vendedor", "data_venda", "total_venda"]
        
class ItensVendaSerializer(serializers.ModelSerializer):
    class Meta:
        model = ItensVenda
        fields = ["item_id", "venda", "produto", "quantidade", "valor_praticado"]