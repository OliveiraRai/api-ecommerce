from rest_framework import serializers
from .models import Produto, Categoria, Cliente, Vendedor, Venda, ItensVenda

class ProdutoSerializer(serializers.ModelSerializer):
    # verifica se tal categoria existe, como uma constraint
    category_id = serializers.PrimaryKeyRelatedField(
        queryset = Produto.objects.all(),
        source = 'categoria',
        write_only = True
    )
    # possibila leitura de nomes amigáveis
    category_name = serializers.CharField(source='categoria.nome', read_only=True)
    
    class Meta:
        model = Produto # modelo de origem dos dados
        fields = ["produto_id", 
                  "nome", 
                  "categoria", 
                  "preco", 
                  "estoque"
                  ] # campos que serão expostos em JSON]
        
        read_only_fields = ["produto_id"]
        
    def validate_price(self, value):
        if value <= 0:
            raise serializers.ValidationError("O preço do produto deve ser maior que zero.")
        return value
        
    def validate_stock(self, value):
        if value < 0:
            raise serializers.ValidationError("O estoque não pode ser negativo.")
        return value
        
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