from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from .serializers import ProdutoSerializer, CategoriaSerializer, ClienteSerializer, VendedorSerializer, VendaSerializer, ItensVendaSerializer
from .models import Produto, Categoria, Cliente, Vendedor, Venda, ItensVenda
import bcrypt, uuid
from datetime import date

class ProdutoAPITestCase(APITestCase):
    def setUp(self):
        self.categoria = Categoria.objects.create(nome='Periférico')
        self.produto = Produto.objects.create(
            nome = "Mouse Gamer",
            categoria = self.categoria,
            preco = 80,
            estoque = 5,
        )
        
        self.url_list = reverse('produto-list')
        self.url_detail = reverse('produto-detail', kwargs={'pk': self.produto.produto_id})
        
        password = b'myPassword0'
        salt = bcrypt.gensalt()
        
        self.password = bcrypt.hashpw(password=password, salt=salt)
        
        self.seller = Vendedor.objects.create(
            nome = "John Doe",
            cpnj_cpf = "00.000.000/0000-00",
            celular = "(00) 00000-0000",
            email = "john.doe@example.com",
            senha = self.password,
        )
        
    ### POV do cliente (GET)
    
    def test_customer_can_list_products(self):
        response = self.client.get(self.url_list)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['nome'], "Mouse Gamer")
        self.assertEqual(response.data[0]['categoria'], "Periférico")
        
    def test_customer_can_see_product_detail(self):
        response = self.client.get(self.url_detail)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['nome'], "Mouse Gamer")
    
    def test_nonexisting_product_returns_404(self):
        nonexisting_product = uuid.uuid4
        invalid_url = reverse(self.url_detail, kwargs={'pk': nonexisting_product})
        
        response = self.client.get(invalid_url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
    ### POV do vendedor (POST, PUT, PATCH, DELETE)
    
    def test_autheticated_seller_can_create_products(self):
        self.client.force_authenticate(self.seller)
        
        new_product = {
            "nome": "Teclado Mecânico",
            "categoria": self.categoria,
            "preco": 120,
            "estoque": 4,
        }
        
        response = self.client.post(self.url_list, new_product, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Produto.objects.filter(nome="Teclado Mecânico").exists())
        
    def test_validation_error_when_price_is_less_or_equal_than_0(self):
        self.client.force_authenticate(self.seller)
        
        invalid_product = {
            "nome": "Teclado Mecânico",
            "categoria": self.categoria,
            "preco": -10,
            "estoque": 4,
        }
        
        response = self.client.post(self.url_list, invalid_product, format='json')
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('preco', response.data)
        self.assertEqual(response.data['preco'][0], "O preço do produto deve ser maior que zero.")