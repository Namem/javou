from django.db import models
from django.contrib.auth.models import User

# (Seu modelo Chamado existente fica aqui em cima, sem alterações)
class Chamado(models.Model):
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
        ('EM_ATENDIMENTO', 'Em Atendimento'),
        ('ENCERRADO', 'Encerrado'),
    ]

    PRIORIDADE_CHOICES = [
        ('BAIXA', 'Baixa'),
        ('MEDIA', 'Média'),
        ('ALTA', 'Alta'),
    ]
    CATEGORIA_CHOICES = [
        ('SUPORTE', 'Suporte Técnico'),
        ('INFRA', 'Infraestrutura'),
        ('OUTROS', 'Outros'),
    ]

    titulo = models.CharField("Título", max_length=100)
    
    solicitante = models.ForeignKey(
        User,
        verbose_name="Solicitante",
        on_delete=models.PROTECT,
        related_name='chamados_solicitados'
    )

    descricao = models.TextField("Descrição")
    categoria = models.CharField("Categoria", max_length=50, choices=CATEGORIA_CHOICES)
    prioridade = models.CharField("Prioridade", max_length=20, choices=PRIORIDADE_CHOICES, default='BAIXA')
    
    responsavel = models.ForeignKey(
        User,
        verbose_name="Responsável",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='chamados_responsaveis'
    )
    
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='ABERTO')
    data_abertura = models.DateTimeField("Data de abertura", auto_now_add=True)

    def __str__(self):
        return f"[{self.id}] {self.titulo} ({self.status})"


class Comentario(models.Model):
    chamado = models.ForeignKey(Chamado, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField("Comentário")
    data_criacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['data_criacao'] # Ordena os comentários do mais antigo para o mais novo

    def __str__(self):
        return f'Comentário de {self.autor.username} em {self.chamado.titulo}'
