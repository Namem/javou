from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.core.paginator import Paginator
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Chamado, Comentario, Anexo
from .forms import ChamadoForm, ComentarioForm


# Função auxiliar para verificar se o usuário é técnico
def is_technician(user):
    return hasattr(user, 'profile') and user.profile.is_technician

@login_required
def listar_chamados(request):
    # Primeiro, verificamos o papel do usuário
    if is_technician(request.user):
        # --- LÓGICA PARA TÉCNICOS ---
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

        responsaveis = User.objects.filter(profile__is_technician=True)
        
        context = {
            'responsaveis': responsaveis,
            'filtros': {'status': status, 'prioridade': prioridade, 'responsavel_nome': responsavel_nome, 'busca': busca},
            'ordenacao': {'sort': sort, 'direction': direction},
            'form': ChamadoForm() # Adiciona o form para o modal
        }
    else:
        # --- LÓGICA PARA USUÁRIOS COMUNS ---
        chamados_list = Chamado.objects.filter(status__in=['ABERTO', 'EM_ATENDIMENTO']).order_by('-data_abertura')
        context = {}

    # A paginação foi removida para simplificar a integração com o DataTables, que tem sua própria paginação.
    # Se você não estiver usando DataTables, pode adicionar o Paginator de volta aqui.
    context['chamados'] = chamados_list
    
    return render(request, 'chamados/lista.html', context)

@login_required
def novo_chamado(request):
    if not is_technician(request.user):
        raise PermissionDenied

    if request.method == 'POST':
        form = ChamadoForm(request.POST, request.FILES)
        if form.is_valid():
            chamado = form.save()
            
            arquivo_anexado = form.cleaned_data.get('anexo_arquivo')
            if arquivo_anexado:
                Anexo.objects.create(chamado=chamado, arquivo=arquivo_anexado)

            messages.success(request, f"Chamado #{chamado.id} aberto com sucesso!")
            # MODIFICAÇÃO: Usar o nome da URL com namespace
            return redirect('chamados:listar_chamados')
    else:
        form = ChamadoForm()

    return render(request, 'chamados/form.html', {'form': form, 'titulo': 'Novo Chamado'})

@login_required
def editar_chamado(request, id):
    if not is_technician(request.user):
        raise PermissionDenied

    chamado = get_object_or_404(Chamado, id=id)
    if request.method == 'POST':
        # Aqui você poderia usar um formulário de edição diferente se quisesse
        form = ChamadoForm(request.POST, request.FILES, instance=chamado)
        if form.is_valid():
            form.save()
            messages.success(request, "Chamado atualizado com sucesso!")
            # MODIFICAÇÃO: Usar o nome da URL com namespace
            return redirect('chamados:detalhe_chamado', id=chamado.id)
    else:
        form = ChamadoForm(instance=chamado)
    return render(request, 'chamados/form.html', {'form': form, 'titulo': f'Editar Chamado #{id}'})

@login_required
def assumir_chamado(request, id):
    if not is_technician(request.user):
        raise PermissionDenied
        
    chamado = get_object_or_404(Chamado, id=id)
    chamado.responsavel = request.user
    if chamado.status == 'ABERTO':
        chamado.status = 'EM_ATENDIMENTO'
    chamado.save()
    messages.success(request, f"Você assumiu o chamado #{chamado.id}.")
    # MODIFICAÇÃO: Usar o nome da URL com namespace
    return redirect('chamados:listar_chamados')

@require_POST
@login_required
def encerrar_chamado(request, id):
    if not is_technician(request.user):
        raise PermissionDenied
        
    chamado = get_object_or_404(Chamado, id=id)
    chamado.status = 'ENCERRADO'
    chamado.save()

    assunto = f"Seu chamado #{chamado.id} foi encerrado."
    mensagem = (
        f"Olá, {chamado.solicitante.username}.\n\n"
        f"Seu chamado '{chamado.titulo}' foi marcado como resolvido e encerrado por nossa equipe.\n\n"
        "Agradecemos o seu contato.\nEquipe de Suporte Resolve AI"
    )
    email_remetente = settings.DEFAULT_FROM_EMAIL or 'suporte@resolveai.com'
    email_destinatario = [chamado.solicitante.email]

    print(f"Enviando e-mail de CHAMADO ENCERRADO para {email_destinatario[0]}...")

    send_mail(
        assunto,
        mensagem,
        email_remetente,
        email_destinatario,
        fail_silently=False,
    )

    messages.success(request, f"Chamado #{id} encerrado com sucesso.")
    # MODIFICAÇÃO: Usar o nome da URL com namespace
    return redirect('chamados:listar_chamados')

@login_required
def detalhe_chamado(request, id):
    chamado = get_object_or_404(Chamado, id=id)
    comentarios = chamado.comentarios.all()
    
    if request.method == 'POST':
        if not is_technician(request.user):
            raise PermissionDenied
        
        form_comentario = ComentarioForm(request.POST, request.FILES)
        if form_comentario.is_valid():
            novo_comentario = form_comentario.save(commit=False)
            novo_comentario.chamado = chamado
            novo_comentario.autor = request.user
            novo_comentario.is_internal = form_comentario.cleaned_data.get('is_internal')
            novo_comentario.save()

            arquivo_anexado = form_comentario.cleaned_data.get('anexo_arquivo')
            if arquivo_anexado:
                Anexo.objects.create(comentario=novo_comentario, arquivo=arquivo_anexado)
            
            messages.success(request, 'Comentário adicionado com sucesso.')
            # MODIFICAÇÃO: Usar o nome da URL com namespace
            return redirect('chamados:detalhe_chamado', id=chamado.id)
    else:
        form_comentario = ComentarioForm()
        
    contexto = {
        'chamado': chamado,
        'comentarios': comentarios,
        'form_comentario': form_comentario,
    }
    
    return render(request, 'chamados/detalhe.html', contexto)