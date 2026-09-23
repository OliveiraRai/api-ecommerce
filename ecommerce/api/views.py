from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Produto
from .serializers import ProdutoSerializer

# Listagem de Produtos
@api_view(["GET"]) 
def list_products(request):
    # Não é necessário validação, pois o rest_framework 
    # retornará uma lista vazia [] com status 200 OK
    
    products = Produto.objects.all()
    
    # many=True faz o rest_framework lidar com os dados 
    # de products como uma lista, seja vazia ou não
    translator = ProdutoSerializer(products, many=True)
    
    # retorna [], [{}], ou [{}, ...]
    return Response(translator.data)

# TODO view para criar produto