from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied # Importamos a exceção de permissão negada
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from .models import Chamado
from .forms import ChamadoForm
from .forms import ChamadoForm, ComentarioForm
from .models import Chamado, Comentario
# Função auxiliar para verificar se o usuário é técnico
# Usamos hasattr para evitar erros caso um usuário antigo não tenha perfil
def is_technician(user):
    return hasattr(user, 'profile') and user.profile.is_technician

@login_required
def listar_chamados(request):
    # Primeiro, verificamos o papel do usuário
    if is_technician(request.user):
        # --- LÓGICA PARA TÉCNICOS ---
        # Eles veem tudo e podem filtrar e ordenar como antes.
        sort = request.GET.get('sort', 'data_abertura')
        direction = request.GET.get('direction', 'desc')
        
        chamados_list = Chamado.objects.all()

        # Filtros
        status = request.GET.get('status')
        prioridade = request.GET.get('prioridade')
        responsavel_nome = request.GET.get('responsavel_nome')
        busca = request.GET.get('busca')

        if status:
            chamados_list = chamados_list.filter(status=status.upper())
        if prioridade:
            chamados_list = chamados_list.filter(prioridade=prioridade.upper())
        if responsavel_nome:
            chamados_list = chamados_list.filter(responsavel__username__icontains=responsavel_nome)
        if busca:
            if busca.isdigit():
                chamados_list = chamados_list.filter(id=busca)
            else:
                chamados_list = chamados_list.filter(titulo__icontains=busca)

        order = f"{'-' if direction == 'desc' else ''}{sort}"
        chamados_list = chamados_list.order_by(order)

        responsaveis = User.objects.filter(profile__is_technician=True) # Mostra apenas técnicos como opção de filtro
        
        context = {
            'responsaveis': responsaveis,
            'filtros': {'status': status, 'prioridade': prioridade, 'responsavel_nome': responsavel_nome, 'busca': busca,},
            'ordenacao': {'sort': sort, 'direction': direction,},
        }

    else:
        # --- LÓGICA PARA USUÁRIOS COMUNS ---
        # Eles veem apenas uma lista simples de chamados abertos ou em atendimento.
        chamados_list = Chamado.objects.filter(status__in=['ABERTO', 'EM_ATENDIMENTO']).order_by('-data_abertura')
        context = {} # O contexto para usuários comuns é vazio, sem filtros.

    # Paginação é comum para ambos
    paginator = Paginator(chamados_list, 10) # Aumentei para 10 por página
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Adiciona os objetos paginados ao contexto
    context['chamados'] = page_obj
    context['page_obj'] = page_obj
    
    return render(request, 'chamados/lista.html', context)


@login_required
def novo_chamado(request):
    # Verificação de permissão no início da view
    if not is_technician(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = ChamadoForm(request.POST)
        if form.is_valid():
            # Não precisamos mais do `commit=False` porque o solicitante vem do formulário
            chamado = form.save()
            messages.success(request, f"Chamado #{chamado.id} aberto com sucesso!")
            return redirect('listar_chamados')
    else:
        form = ChamadoForm()
    return render(request, 'chamados/form.html', {'form': form, 'titulo': 'Novo Chamado'})


@login_required
def editar_chamado(request, id):
    # Verificação de permissão
    if not is_technician(request.user):
        raise PermissionDenied

    chamado = get_object_or_404(Chamado, id=id)
    if request.method == 'POST':
        form = ChamadoForm(request.POST, instance=chamado) # Usando o mesmo form por simplicidade
        if form.is_valid():
            form.save()
            messages.success(request, "Chamado atualizado com sucesso!")
            return redirect('listar_chamados')
    else:
        form = ChamadoForm(instance=chamado)
    return render(request, 'chamados/form.html', {'form': form, 'titulo': f'Editar Chamado #{id}'})


@login_required
def assumir_chamado(request, id):
    # Verificação de permissão
    if not is_technician(request.user):
        raise PermissionDenied
        
    chamado = get_object_or_404(Chamado, id=id)
    chamado.responsavel = request.user
    if chamado.status == 'ABERTO':
        chamado.status = 'EM_ATENDIMENTO'
    chamado.save()
    messages.success(request, f"Você assumiu o chamado #{chamado.id}.")
    return redirect('listar_chamados')


@require_POST
@login_required
def encerrar_chamado(request, id):
    # Verificação de permissão
    if not is_technician(request.user):
        raise PermissionDenied
        
    chamado = get_object_or_404(Chamado, id=id)
    chamado.status = 'ENCERRADO'
    chamado.save()
    messages.success(request, f"Chamado #{id} encerrado com sucesso.")
    return redirect('listar_chamados')

@login_required
def detalhe_chamado(request, id):
    # Busca o chamado específico ou retorna um erro 404 se não encontrar.
    chamado = get_object_or_404(Chamado, id=id)
    
    # Busca todos os comentários associados a este chamado.
    comentarios = chamado.comentarios.all()
    
    # Lógica para adicionar um novo comentário
    if request.method == 'POST':
        # Apenas técnicos podem comentar por enquanto
        if not (hasattr(request.user, 'profile') and request.user.profile.is_technician):
            raise PermissionDenied

        form_comentario = ComentarioForm(request.POST)
        if form_comentario.is_valid():
            novo_comentario = form_comentario.save(commit=False)
            novo_comentario.chamado = chamado
            novo_comentario.autor = request.user
            novo_comentario.save()
            messages.success(request, 'Comentário adicionado com sucesso.')
            # Redireciona para a mesma página para mostrar o novo comentário e limpar o form.
            return redirect('detalhe_chamado', id=chamado.id)
    else:
        # Se não for POST, apenas cria um formulário em branco.
        form_comentario = ComentarioForm()

    contexto = {
        'chamado': chamado,
        'comentarios': comentarios,
        'form_comentario': form_comentario,
    }
    
    return render(request, 'chamados/detalhe.html', contexto)