from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from chamados.models import Chamado
from django.utils import timezone
from django.utils.timezone import localdate
from django.db.models import Count
from django.contrib.auth.models import User

@login_required
def dashboard(request):
    hoje = timezone.now().date()
    total_abertos = Chamado.objects.filter(status='ABERTO').count()
    total_encerrados = Chamado.objects.filter(status='ENCERRADO').count()
    abertos_hoje = Chamado.objects.filter(data_abertura__date=localdate(), status='ABERTO').count()
    total_em_atendimento = Chamado.objects.filter(status='EM_ATENDIMENTO').count()

    ranking = (
        User.objects
        .annotate(qtd_chamados=Count('chamado'))
        .order_by('-qtd_chamados')[:10]
    )

    labels = [user.username for user in ranking]
    data = [user.qtd_chamados for user in ranking]

    contexto = {
        'total_abertos': total_abertos,
        'total_encerrados': total_encerrados,
        'abertos_hoje': abertos_hoje,
        'total_em_atendimento': total_em_atendimento,
        'labels': labels,
        'data': data,
    }

    return render(request, 'dashboard/index.html', contexto)
