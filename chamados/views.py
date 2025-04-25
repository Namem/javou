from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Chamado
from .forms import ChamadoForm

@login_required
def listar_chamados(request):
    status = request.GET.get('status')
    hoje = request.GET.get('abertos_hoje')

    chamados = Chamado.objects.all()

    if status:
        chamados = chamados.filter(status=status.upper())

    if hoje:
        from django.utils.timezone import localdate
        chamados = chamados.filter(data_abertura__date=localdate())

    chamados = chamados.order_by('-data_abertura')
    return render(request, 'chamados/lista.html', {'chamados': chamados})


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

@login_required
def encerrar_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    chamado.status = 'ENCERRADO'
    chamado.save()
    messages.info(request, f"Chamado #{id} encerrado.")
    return redirect('listar_chamados')
