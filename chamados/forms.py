from django import forms
from django.contrib.auth.models import User
from .models import Chamado, Comentario

# O formulário que era 'ChamadoForm' foi renomeado para ser específico para técnicos.
class TecnicoChamadoForm(forms.ModelForm):
    # Mostra apenas usuários que NÃO são técnicos na lista de solicitantes
    solicitante = forms.ModelChoiceField(
        queryset=User.objects.filter(profile__is_technician=False),
        label="Solicitante (Cliente)",
        help_text="Selecione o usuário para quem este chamado está sendo aberto."
    )
    anexo_arquivo = forms.FileField(label="Anexar Arquivo", required=False)

    class Meta:
        model = Chamado
        fields = ['titulo', 'solicitante', 'descricao', 'categoria', 'prioridade']


# Este é o novo formulário, mais simples, para o cliente final.
class ClienteChamadoForm(forms.ModelForm):
    anexo_arquivo = forms.FileField(label="Anexar Arquivo", required=False)

    class Meta:
        model = Chamado
        # Note que não há o campo 'solicitante' aqui
        fields = ['titulo', 'descricao', 'categoria', 'prioridade']


# O formulário de comentário continua o mesmo
class ComentarioForm(forms.ModelForm):
    anexo_arquivo = forms.FileField(label="Anexar Arquivo", required=False)
    is_internal = forms.BooleanField(
        label="Marcar como nota interna (visível apenas para técnicos)", 
        required=False
    )
    class Meta:
        model = Comentario
        fields = ['texto', 'is_internal']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Adicione seu comentário aqui...'})
        }