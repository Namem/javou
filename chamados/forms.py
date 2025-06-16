from django import forms
from django.contrib.auth.models import User
from .models import Chamado, Comentario # Certifique-se de importar o Comentario

class ChamadoForm(forms.ModelForm):
    solicitante = forms.ModelChoiceField(
        queryset=User.objects.all(),
        label="Solicitante (Cliente)",
        help_text="Selecione o usuário para quem este chamado está sendo aberto."
    )

    class Meta:
        model = Chamado
        fields = ['titulo', 'solicitante', 'descricao', 'categoria', 'prioridade']


# ===================================================================
# A classe abaixo provavelmente está faltando no seu arquivo.
# Adicione-a.
# ===================================================================
class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        # O único campo que o usuário preencherá é o texto do comentário.
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Adicione seu comentário aqui...'})
        }