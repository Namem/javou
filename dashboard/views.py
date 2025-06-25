from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from chamados.models import Chamado
from django.db.models import Count
from django.utils.translation import gettext as _

# Função auxiliar para traduzir os status (já existe)
def traduzir_status(status_dict):
    mapa_status = {
        'ABERTO': _('Aberto'),
        'EM_ATENDIMENTO': _('Em Atendimento'),
        'ENCERRADO': _('Encerrado'),
    }
    return mapa_status.get(status_dict['status'], status_dict['status'])

@login_required
def dashboard(request):
    # Contagens gerais
    total_chamados = Chamado.objects.count()
    total_abertos = Chamado.objects.filter(status='ABERTO').count()
    total_em_atendimento = Chamado.objects.filter(status='EM_ATENDIMENTO').count()
    total_encerrados = Chamado.objects.filter(status='ENCERRADO').count()

    # Dados para o gráfico de status (já existe)
    status_data = Chamado.objects.values('status').annotate(total=Count('status')).order_by('status')
    labels_status = [traduzir_status(item) for item in status_data]
    data_status = [item['total'] for item in status_data]


    categoria_data = Chamado.objects.values('categoria').annotate(total=Count('categoria')).order_by('categoria')
    
    # Prepara os dados para o Chart.js
    labels_categoria = [dict(Chamado.CATEGORIA_CHOICES).get(item['categoria'], item['categoria']) for item in categoria_data]
    data_categoria = [item['total'] for item in categoria_data]


    contexto = {
        'total_chamados': total_chamados,
        'total_abertos': total_abertos,
        'total_em_atendimento': total_em_atendimento,
        'total_encerrados': total_encerrados,
        'labels_status': labels_status,
        'data_status': data_status,
        # Adiciona os novos dados ao contexto
        'labels_categoria': labels_categoria,
        'data_categoria': data_categoria,
    }

    return render(request, 'dashboard/index.html', contexto)