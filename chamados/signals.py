from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from .models import Comentario
from .models import Comentario, Chamado 

@receiver(post_save, sender=Comentario)
def enviar_notificacao_por_email(sender, instance, created, **kwargs):
    if created:
        comentario = instance
        chamado = comentario.chamado
        
        autor_e_tecnico = hasattr(comentario.autor, 'profile') and comentario.autor.profile.is_technician
        
        if autor_e_tecnico and comentario.autor != chamado.solicitante:
            assunto = f"Nova atualização no seu chamado #{chamado.id}: {chamado.titulo}"
            email_remetente = settings.DEFAULT_FROM_EMAIL or 'suporte@helpdesk.com'
            email_destinatario = [chamado.solicitante.email]
            
            contexto = {
                'solicitante_nome': chamado.solicitante.username,
                'chamado_id': chamado.id,
                'chamado_titulo': chamado.titulo,
                'comentario_texto': comentario.texto,
                'autor_comentario': comentario.autor.username,
                'chamado_url': f"http://127.0.0.1:8000/chamados/{chamado.id}/",
                'assunto': assunto
            }

            # ===================================================================
            # INÍCIO DA MODIFICAÇÃO
            # ===================================================================
            # Renderiza a versão em texto puro (fallback)
            mensagem_texto = render_to_string('emails/notificacao_comentario_corpo.txt', contexto)
            
            # Renderiza a versão em HTML
            mensagem_html = render_to_string('emails/notificacao_comentario.html', contexto)
            # ===================================================================
            # FIM DA MODIFICAÇÃO
            # ===================================================================

            print(f"Enviando e-mail de notificação para {email_destinatario[0]}...")
            
            send_mail(
                subject=assunto,
                message=mensagem_texto, # Corpo em texto puro
                from_email=email_remetente,
                recipient_list=email_destinatario,
                html_message=mensagem_html, # Corpo em HTML
                fail_silently=False,
            )


@receiver(post_save, sender=Chamado)
def enviar_notificacao_novo_chamado(sender, instance, created, **kwargs):
    # 'instance' é o objeto Chamado que foi salvo.
    # 'created' é True se for um novo registro.
    if created:
        chamado = instance
        assunto = f"Seu chamado #{chamado.id} foi aberto com sucesso!"
        mensagem = (
            f"Olá, {chamado.solicitante.username}.\n\n"
            f"Recebemos sua solicitação e um novo chamado foi aberto com os seguintes detalhes:\n\n"
            f"ID do Chamado: {chamado.id}\n"
            f"Título: {chamado.titulo}\n\n"
            f"Um de nossos técnicos irá assumir seu caso em breve.\n"
            f"Você pode acompanhar o status do seu chamado aqui: http://127.0.0.1:8000/chamados/{chamado.id}/\n\n"
            "Atenciosamente,\nEquipe de Suporte Helpdesk"
        )
        email_remetente = settings.DEFAULT_FROM_EMAIL or 'suporte@helpdesk.com'
        email_destinatario = [chamado.solicitante.email]

        print(f"Enviando e-mail de NOVO CHAMADO para {email_destinatario[0]}...")
        
        send_mail(
            assunto,
            mensagem,
            email_remetente,
            email_destinatario,
            fail_silently=False,
        )