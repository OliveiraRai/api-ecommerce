from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import ProdutoSerializer, CategoriaSerializer, ClienteSerializer, VendedorSerializer, VendaSerializer, ItensVendaSerializer
from .models import Produto, Categoria, Cliente, Vendedor, Venda, ItensVenda
import bcrypt
from datetime import date

## testes dos models

class CategoriaSerializerTestCase(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(
            nome = "Periférico",
        )
        
    def test_categoria_serializer_retorna_nome(self):
        serializer = CategoriaSerializer(instance=self.categoria)
        data = serializer.data
        
        self.assertEqual(data["nome"], "Periférico")
        self.assertIn("id", data)

class ProdutoSerializerTestCase(APITestCase):
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

class ClienteSerializerTestCase(APITestCase):
    def setUp(self):
        password = b'MinhaSenha22'
        salt = bcrypt.gensalt()
        
        self.hashed_pw = bcrypt.hashpw(password=password, salt=salt)
    
        self.cliente = Cliente.objects.create(
            nome = "Jair Messias Bolsonaro",
            cpf = "555.555.555-55",
            celular = "(55) 55555-5555",
            email = "jair.bolsonaro@gmail.com",
            senha = self.hashed_pw
        )
        
    def test_cliente_serializer_cria_cliente(self):
        serializer = ClienteSerializer(self.cliente)
        data = serializer.data
        
        self.assertEqual(data["nome"], self.cliente.nome)
        self.assertEqual(data["cpf"], self.cliente.cpf)
        self.assertEqual(data["celular"], self.cliente.celular)
        self.assertEqual(data["email"], self.cliente.email)
        self.assertEqual(data["senha"], str(self.hashed_pw))
        self.assertEqual(data["criado_em"], str(date.today()))
        self.assertIn("cliente_id", data)

class VendedorSerializerTestCase(APITestCase):
    def setUp(self):
        password = b'MinhaSenha13'
        salt = bcrypt.gensalt()
    
        self.hashed_pw = bcrypt.hashpw(password=password, salt=salt)
    
        self.vendedor = Vendedor.objects.create(
            nome = "Luíz Inácio Lula da Silva",
            cnpj_cpf = "555.555.555-54",
            celular = "(55) 55555-5554",
            email = "lula.silva@gmail.com",
            senha = self.hashed_pw
        )
    
    def test_vendedor_serializer_cria_vendedor(self):
        serializer = VendedorSerializer(self.vendedor)
        data = serializer.data
    
        self.assertEqual(data["nome"], self.vendedor.nome)
        self.assertEqual(data["cnpj_cpf"], self.vendedor.cnpj_cpf)
        self.assertEqual(data["celular"], self.vendedor.celular)
        self.assertEqual(data["email"], self.vendedor.email)
        self.assertEqual(data["senha"], str(self.hashed_pw))
        self.assertEqual(data["criado_em"], str(date.today()))
        self.assertIn("vendedor_id", data)
        
class VendaSerializerTestCase(APITestCase):
    def setUp(self):
        # cliente
        password_1 = b'MinhaSenha22'
        salt_1 = bcrypt.gensalt()
        
        self.hashed_pw = bcrypt.hashpw(password=password_1, salt=salt_1)
        
        self.cliente = Cliente.objects.create(
            nome = "Jair Messias Bolsonaro",
            cpf = "555.555.555-55",
            celular = "(55) 55555-5555",
            email = "jair.bolsonaro@gmail.com",
            senha = self.hashed_pw
        )
        # vendedor
        password_2 = b'MinhaSenha13'
        salt_2 = bcrypt.gensalt()
        
        self.hashed_pw = bcrypt.hashpw(password=password_2, salt=salt_2)
        
        self.vendedor = Vendedor.objects.create(
            nome = "Luíz Inácio Lula da Silva",
            cnpj_cpf = "555.555.555-54",
            celular = "(55) 55555-5554",
            email = "lula.silva@gmail.com",
            senha = self.hashed_pw
        )
        # categoria
        self.categoria = Categoria.objects.create(nome = "Periférico")
        # produto
        self.produto = Produto.objects.create(
            nome = "Teclado Mecânico",
            categoria = self.categoria,
            preco = 200,
            estoque = 5,
        )
        
        self.quantity = 2
        # venda
        self.venda = Venda.objects.create(
            cliente = self.cliente,
            vendedor = self.vendedor,
            total_venda = self.produto.preco * self.quantity,
        )
        
        self.itens_venda = ItensVenda.objects.create(
            venda = self.venda,
            produto = self.produto,
            quantidade = self.quantity,
            valor_praticado = self.produto.preco 
        )
        
    def test_venda_serializer_cria_venda_e_itens_venda(self):
        # venda
        venda_serializer = VendaSerializer(self.venda)
        venda_data = venda_serializer.data
        
        # itens_venda
        itens_venda_serializer = ItensVendaSerializer(self.itens_venda)
        itens_venda_data = itens_venda_serializer.data
        
        # venda - testes
        self.assertEqual(venda_data["cliente"], self.cliente.cliente_id)
        self.assertEqual(venda_data["vendedor"], self.vendedor.vendedor_id)
        self.assertEqual(venda_data["data_venda"], str(date.today()))
        self.assertEqual(venda_data["total_venda"], '400.00')
        self.assertIn("venda_id", venda_data)
        
        # itens_venda - testes
        self.assertEqual(itens_venda_data["venda"], self.venda.venda_id)
        self.assertEqual(itens_venda_data["produto"], self.produto.produto_id)
        self.assertEqual(itens_venda_data["quantidade"], self.quantity)
        self.assertEqual(itens_venda_data["valor_praticado"], '200.00')
        self.assertIn("item_id", itens_venda_data)
        
## testes das rotas

class ListarProdutosTestCase(APITestCase):
    def setUp(self):
        # reverse usa o name="" de uma url para manter um código DRY (Don't Repeat Yourself)
        self.url = reverse('ListProducts')
        
        # criar categoria para o produto
        self.categoria = Categoria.objects.create(nome="Periférico")
        
        # criar produto
        self.produto = Produto.objects.create(
            nome = "Teclado Mecânico",
            categoria = self.categoria,
            preco = 200,
            estoque = 1,
        )
        
    def test_listar_produtos_retorna_lista_vazia(self):
        response = self.client.get(self.url, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Produto.objects.count(), 1)

class CriarProdutoTestCase(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome="Periférico")
        self.categoria_serialized = CategoriaSerializer(self.categoria)
        self.data = self.categoria_serialized.data
        
        self.url = reverse('CreateProduct')
        self.dados = {
            "nome": "Teclado Mecânico",
            "categoria": self.data["id"],
            "preco": 200,
            "estoque": 1,
        }
        
    def test_criar_produto_retorna_id(self):
        response = self.client.post(self.url, self.dados, format='json')
        data = response.data
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("produto_id", data)