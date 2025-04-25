from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chamado
from .forms import ChamadoForm
from django.contrib.auth.models import User
from django.utils.timezone import localdate
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST

@login_required
def listar_chamados(request):
    sort = request.GET.get('sort', 'data_abertura')
    direction = request.GET.get('direction', 'desc')

    chamados = Chamado.objects.all()

    # Filtros
    status = request.GET.get('status')
    prioridade = request.GET.get('prioridade')
    responsavel_nome = request.GET.get('responsavel_nome')
    busca = request.GET.get('busca')

    if status:
        chamados = chamados.filter(status=status.upper())

    if prioridade:
        chamados = chamados.filter(prioridade=prioridade.upper())

    if responsavel_nome:
        chamados = chamados.filter(responsavel__username__icontains=responsavel_nome)

    if busca:
        if busca.isdigit():
            chamados = chamados.filter(id=busca)
        else:
            chamados = chamados.filter(titulo__icontains=busca)

    order = f"{'-' if direction == 'desc' else ''}{sort}"
    chamados = chamados.order_by(order)

    responsaveis = User.objects.all()

    # Paginação
    paginator = Paginator(chamados, 5)  # 5 chamados por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'chamados/lista.html', {
        'chamados': page_obj,
        'responsaveis': responsaveis,
        'filtros': {
            'status': status,
            'prioridade': prioridade,
            'responsavel_nome': responsavel_nome,
            'busca': busca,
        },
        'ordenacao': {
            'sort': sort,
            'direction': direction,
        },
        'page_obj': page_obj,
    })


@login_required
def assumir_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    chamado.responsavel = request.user
    if chamado.status == 'ABERTO':
        chamado.status = 'EM_ATENDIMENTO'
    chamado.save()
    messages.success(request, f"Você assumiu o chamado #{chamado.id}.")
    return redirect('listar_chamados')


@login_required
def novo_chamado(request):
    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            chamado = form.save(commit=False)
            chamado.status = 'ABERTO'
            chamado.save()
            messages.success(request, "Chamado aberto com sucesso!")
            return redirect('listar_chamados')
    else:
        form = ChamadoForm()
    return render(request, 'chamados/form.html', {'form': form, 'titulo': 'Novo Chamado'})

@login_required
def editar_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    if request.method == 'POST':
        form = ChamadoForm(request.POST, instance=chamado)
        if form.is_valid():
            form.save()
            messages.success(request, "Chamado atualizado com sucesso!")
            return redirect('listar_chamados')
    else:
        form = ChamadoForm(instance=chamado)
    return render(request, 'chamados/form.html', {'form': form, 'titulo': f'Editar Chamado #{id}'})

@require_POST
@login_required
def encerrar_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    chamado.status = 'ENCERRADO'
    chamado.save()
    messages.success(request, f"Chamado #{id} encerrado com sucesso.")
    return redirect('listar_chamados')
