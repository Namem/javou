from django.urls import path
from . import views

app_name = 'knowledge_base'

urlpatterns = [
    # Ex: /kb/
    path('', views.lista_categorias, name='lista_categorias'),
    
    # Ex: /kb/problemas-de-impressora/
    path('<slug:categoria_slug>/', views.lista_artigos_por_categoria, name='lista_artigos_por_categoria'),
    
    # Ex: /kb/artigo/como-instalar-nova-impressora/
    path('artigo/<slug:slug>/', views.detalhe_artigo, name='detalhe_artigo'),
]