from django.contrib import admin
from .models import Produto, Categoria

# Register your models here.
@admin.register(Produto)
class ProdutosAdmin(admin.ModelAdmin):
    list_display = ['nome', 'categoria', 'preco', 'estoque']
    search_fields = ('nome', 'categoria__nome',)
    readonly_fields = ('imagem_link',)

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']
    search_fields = ('nome',)