from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Produto
from .serializers import ProdutoSerializer, ClienteSerializer, VendedorSerializer

# Listagem de Produtos
@api_view(["GET"]) 
def list_products(request):
    # Não é necessário validação, pois o rest_framework 
    # retornará uma lista vazia [] com status 200 OK    
    products = Produto.objects.all()
    
    # many=True faz o rest_framework lidar com os dados 
    # de products como uma lista, seja vazia ou não
    serializer = ProdutoSerializer(products, many=True)
    
    # retorna [], [{}], ou [{}, ...]
    return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(["POST"])
def create_product(request):
    # deserializa request com 'request.data'
    serializer = ProdutoSerializer(data=request.data)
    
    # validação básica
    if serializer.is_valid():
        serializer.save() # save() salva no db
        return Response(serializer.data, status=status.HTTP_201_CREATED) # retorno de acordo com a realidade
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST) # retorno de acordo com a realidade

@api_view(["POST"])
def create_customer(request):
    serializer = ClienteSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)

@api_view(["POST"])
def create_seller(request):
    serializer = VendedorSerializer(data=request.data)
    
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    return Response(serializer.data, status=status.HTTP_400_BAD_REQUEST)