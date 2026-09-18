from django.test import TestCase
from .serializers import ProdutoSerializer, CategoriaSerializer
from .models import Produto, Categoria

class CategoriaSerializerTestCase(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome = "Periférico",
        )
        
    def test_categoria_serializer_retorna_nome(self):
        serializer = CategoriaSerializer(instance=self.categoria)
        data = serializer.data
        
        self.assertEqual(data["nome"], "Periférico")
        self.assertIn("id", data)

class ProdutoSerializerTestCase(TestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome = "Periférico")
        
        self.produto = Produto.objects.create(
            nome = "Teclado Mecânico",
            categoria = self.categoria,
            preco = 200,
            estoque = 5,
        )
        
    def test_produto_serializer_retorna_campos(self):
        serializer = ProdutoSerializer(instance=self.produto)
        data = serializer.data
        formatted_number = f"{200:.2f}"
        
        self.assertEqual(data["nome"], "Teclado Mecânico")
        self.assertEqual(data["categoria"], self.categoria.id)
        self.assertEqual(data["preco"], formatted_number)
        self.assertEqual(data["estoque"], 5)
        self.assertIn("produto_id", data)