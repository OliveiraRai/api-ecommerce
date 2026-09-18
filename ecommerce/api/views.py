from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Produto
from .serializers import ProdutoSerializer

@api_view(["GET"]) # rota só aceita leitura (GET)
def list_products(request):
    products = Produto.objects.all()
    translator = ProdutoSerializer(products, many=True)
    return Response(translator.data)
    