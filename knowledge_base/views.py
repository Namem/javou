from django.shortcuts import render, get_object_or_404
from .models import CategoriaArtigo, Artigo
from django.contrib.auth.decorators import login_required
from django.db.models import Count, Q

@login_required
def lista_categorias(request):
    """
    View para a página inicial da Base de Conhecimento.
    Lista todas as categorias de artigos.
    """
    categorias = CategoriaArtigo.objects.annotate(
        num_artigos_publicados=Count('artigos', filter=Q(artigos__status='publicado'))
    ).order_by('nome')

    contexto = {
        'categorias': categorias,
    }
    return render(request, 'knowledge_base/lista_categorias.html', contexto)

@login_required
def lista_artigos_por_categoria(request, categoria_slug):
    """
    Lista todos os artigos publicados de uma categoria específica.
    """
    categoria = get_object_or_404(CategoriaArtigo, slug=categoria_slug)
    artigos = Artigo.objects.filter(categoria=categoria, status='publicado')
    contexto = {
        'categoria': categoria,
        'artigos': artigos
    }
    return render(request, 'knowledge_base/lista_artigos_por_categoria.html', contexto)

@login_required
def detalhe_artigo(request, slug):
    """
    Exibe um único artigo completo.
    """
    artigo = get_object_or_404(Artigo, slug=slug, status='publicado')
    contexto = {
        'artigo': artigo,
    }
    return render(request, 'knowledge_base/detalhe_artigo.html', contexto)