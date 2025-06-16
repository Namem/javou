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

    # --- CÓDIGO CORRIGIDO ABAIXO ---
    ranking = (
        User.objects
        .filter(profile__is_technician=True)  # 1. Filtramos para mostrar apenas técnicos no ranking.
        .annotate(qtd_chamados=Count('chamados_responsaveis'))  # 2. Usamos o nome correto da relação.
        .order_by('-qtd_chamados')[:10]
    )
    # --- FIM DO CÓDIGO CORRIGIDO ---

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