from django.contrib import admin
from .models import CategoriaArtigo, Artigo

@admin.register(CategoriaArtigo)
class CategoriaArtigoAdmin(admin.ModelAdmin):
    """
    Configuração de administração para o modelo CategoriaArtigo.
    """
    list_display = ('nome', 'slug')
    search_fields = ('nome',)
    # Esta linha garante que o slug seja preenchido a partir do nome
    prepopulated_fields = {'slug': ('nome',)}

@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    """
    Configuração de administração para o modelo Artigo.
    """
    list_display = ('titulo', 'categoria', 'status', 'autor', 'data_atualizacao')
    list_filter = ('status', 'categoria', 'autor')
    search_fields = ('titulo', 'conteudo')
    # Esta linha garante que o slug seja preenchido a partir do título
    prepopulated_fields = {'slug': ('titulo',)}
    date_hierarchy = 'data_criacao'
    list_editable = ('status', 'categoria')