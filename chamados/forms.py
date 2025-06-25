from django import forms
from django.contrib.auth.models import User
from .models import Chamado, Comentario # Certifique-se de importar o Comentario

class ChamadoForm(forms.ModelForm):
    solicitante = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Solicitante (Cliente)",
        help_text="Selecione o usuário para quem este chamado está sendo aberto."
    )

    anexo_arquivo = forms.FileField(
        label="Anexar Arquivo",
        required=False, # O anexo não é obrigatório
        help_text="Anexe um print, log ou outro documento relevante."
    )

    class Meta:
        model = Chamado
        fields = ['titulo', 'solicitante', 'descricao', 'categoria', 'prioridade']



class ComentarioForm(forms.ModelForm):
    anexo_arquivo = forms.FileField(label="Anexar Arquivo", required=False)

    is_internal = forms.BooleanField(
        label="Marcar como nota interna (visível apenas para técnicos)", 
        required=False
    )

    class Meta:
        model = Comentario
        # O único campo que o usuário preencherá é o texto do comentário.
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Adicione seu comentário aqui...'})
        }


