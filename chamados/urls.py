from django.urls import path
from . import views

urlpatterns = [
    path('', views.listar_chamados, name='listar_chamados'),
    path('novo/', views.novo_chamado, name='novo_chamado'),
    path('<int:id>/editar/', views.editar_chamado, name='editar_chamado'),
    path('<int:id>/encerrar/', views.encerrar_chamado, name='encerrar_chamado'),
    path('<int:id>/assumir/', views.assumir_chamado, name='assumir_chamado'),

]
