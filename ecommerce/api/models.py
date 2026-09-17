from django.db import models
import uuid
import datetime

# Create your models here.
class Vendedores(models.Model):
    vendedor = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    cnpj_cpf = models.CharField(max_length=18)
    celular = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    senha = models.CharField(max_length=128) # will be hashed
    
class Clientes(models.Model):
    cliente_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    cpf = models.CharField(max_length=14)
    celular = models.CharField(max_length=15)
    email = models.EmailField(max_length=255)
    senha = models.CharField(max_length=128) # will be hashed
    
class Venda(models.Model):
    venda_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    cliente = models.ForeignKey(Clientes, on_delete=models.PROTECT)
    vendedor = models.ForeignKey(Vendedores, on_delete=models.PROTECT)
    data_venda = models.DateField(auto_now_add=True)
    total_venda = models.DecimalField(max_digits=8, decimal_places=2)
    
class Produtos(models.Model):
    produto_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=255)
    categoria = models.ForeignKey('Categoria', on_delete=models.PROTECT)
    preco = models.DecimalField(max_digits=8, decimal_places=2)
    estoque = models.IntegerField(default=0)
    
class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    
class ItensVenda(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    venda = models.ForeignKey(Venda, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produtos, on_delete=models.PROTECT)
    quantidade = models.IntegerField()
    valor_praticado = models.DecimalField(max_digits=8, decimal_places=2)