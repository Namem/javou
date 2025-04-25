from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from chamados.models import Chamado
from django.utils import timezone
from django.utils.timezone import localdate

@login_required
def dashboard(request):
    hoje = timezone.now().date()
    total_abertos = Chamado.objects.filter(status='ABERTO').count()
    total_encerrados = Chamado.objects.filter(status='ENCERRADO').count()
    abertos_hoje = Chamado.objects.filter(data_abertura__date=localdate(), status='ABERTO').count()
    total_em_atendimento = Chamado.objects.filter(status='EM_ATENDIMENTO').count()



    contexto = {
        'total_abertos': total_abertos,
        'total_encerrados': total_encerrados,
        'abertos_hoje': abertos_hoje,
        'total_em_atendimento': total_em_atendimento,
    }

    return render(request, 'dashboard/index.html', contexto)
