from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.decorators.http import require_POST
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings

from .models import Chamado, Comentario, Anexo
from .forms import TecnicoChamadoForm, ClienteChamadoForm, ComentarioForm

# Função auxiliar para verificar se o usuário é técnico
def is_technician(user):
    return hasattr(user, 'profile') and user.profile.is_technician


@login_required
def listar_chamados(request):
    """
    Lista os chamados.
    - Técnicos veem todos os chamados.
    - Clientes veem apenas os seus próprios chamados.
    Também passa o formulário correto para o modal de 'Novo Chamado'.
    """
    if is_technician(request.user):
        chamados_list = Chamado.objects.all().order_by('-data_abertura')
        context = {'form': TecnicoChamadoForm()}
    else:
        chamados_list = Chamado.objects.filter(solicitante=request.user).order_by('-data_abertura')
        context = {'form': ClienteChamadoForm()}
    
    context['chamados'] = chamados_list
    return render(request, 'chamados/lista.html', context)


@login_required
def novo_chamado(request):
    """
    Cria um novo chamado. Usa um formulário para técnicos e outro para clientes.
    """
    if is_technician(request.user):
        form_class = TecnicoChamadoForm
    else:
        form_class = ClienteChamadoForm

    if request.method == 'POST':
        form = form_class(request.POST, request.FILES)
        if form.is_valid():
            chamado = form.save(commit=False)
            
            if not is_technician(request.user):
                chamado.solicitante = request.user
            
            chamado.save()

            arquivo_anexado = form.cleaned_data.get('anexo_arquivo')
            if arquivo_anexado:
                Anexo.objects.create(chamado=chamado, arquivo=arquivo_anexado)

            messages.success(request, f"Chamado #{chamado.id} aberto com sucesso!")
            return redirect('chamados:detalhe_chamado', id=chamado.id)
    else:
        form = form_class()

    return render(request, 'chamados/form.html', {'form': form, 'titulo': 'Novo Chamado'})


@login_required
def detalhe_chamado(request, id):
    """
    Exibe os detalhes de um chamado, seu histórico de comentários e anexos.
    Também processa a adição de novos comentários.
    """
    chamado = get_object_or_404(Chamado, id=id)
    
    # Permissão: Ou você é técnico, ou o chamado é seu.
    if not is_technician(request.user) and chamado.solicitante != request.user:
        raise PermissionDenied

    comentarios = chamado.comentarios.all()
    
    if request.method == 'POST':
        # Apenas técnicos podem comentar por enquanto
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
            return redirect('chamados:detalhe_chamado', id=chamado.id)
    else:
        form_comentario = ComentarioForm()
        
    contexto = {
        'chamado': chamado,
        'comentarios': comentarios,
        'form_comentario': form_comentario,
    }
    
    return render(request, 'chamados/detalhe.html', contexto)


@login_required
def editar_chamado(request, id):
    """
    Edita um chamado existente. Apenas para técnicos.
    """
    if not is_technician(request.user):
        raise PermissionDenied

    chamado = get_object_or_404(Chamado, id=id)
    if request.method == 'POST':
        # Usamos o TecnicoChamadoForm para garantir que todos os campos estejam disponíveis
        form = TecnicoChamadoForm(request.POST, request.FILES, instance=chamado)
        if form.is_valid():
            form.save()
            # Lógica para anexos na edição pode ser adicionada aqui se necessário
            messages.success(request, "Chamado atualizado com sucesso!")
            return redirect('chamados:detalhe_chamado', id=chamado.id)
    else:
        form = TecnicoChamadoForm(instance=chamado)
        
    return render(request, 'chamados/form.html', {'form': form, 'titulo': f'Editar Chamado #{id}'})


@login_required
def assumir_chamado(request, id):
    """
    Atribui o chamado ao técnico logado.
    """
    if not is_technician(request.user):
        raise PermissionDenied
        
    chamado = get_object_or_404(Chamado, id=id)
    chamado.responsavel = request.user
    if chamado.status == 'ABERTO':
        chamado.status = 'EM_ATENDIMENTO'
    chamado.save()
    messages.success(request, f"Você assumiu o chamado #{chamado.id}.")
    return redirect('chamados:listar_chamados')


@require_POST
@login_required
def encerrar_chamado(request, id):
    """
    Muda o status do chamado para 'ENCERRADO' e notifica o cliente.
    """
    if not is_technician(request.user):
        raise PermissionDenied
        
    chamado = get_object_or_404(Chamado, id=id)
    chamado.status = 'ENCERRADO'
    chamado.save()
    
    # Lógica de e-mail de encerramento
    assunto = f"Seu chamado #{chamado.id} foi encerrado."
    mensagem = (
        f"Olá, {chamado.solicitante.username}.\n\n"
        f"Seu chamado '{chamado.titulo}' foi marcado como resolvido e encerrado por nossa equipe.\n\n"
        f"Agradecemos o seu contato.\nEquipe de Suporte Resolve AI"
    )
    email_remetente = settings.DEFAULT_FROM_EMAIL or 'suporte@resolveai.com'
    email_destinatario = [chamado.solicitante.email]

    send_mail(
        assunto,
        mensagem,
        email_remetente,
        email_destinatario,
        fail_silently=False,
    )
    
    messages.success(request, f"Chamado #{id} encerrado com sucesso.")
    return redirect('chamados:listar_chamados')