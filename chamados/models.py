from django.db import models
from django.contrib.auth.models import User

class Chamado(models.Model):
    STATUS_CHOICES = [
        ('ABERTO', 'Aberto'),
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
    descricao = models.TextField("Descrição")
    categoria = models.CharField("Categoria", max_length=50, choices=CATEGORIA_CHOICES)
    prioridade = models.CharField("Prioridade", max_length=20, choices=PRIORIDADE_CHOICES, default='BAIXA')
    responsavel = models.ForeignKey(User, verbose_name="Responsável", on_delete=models.SET_NULL, null=True, blank=True)
    status = models.CharField("Status", max_length=20, choices=STATUS_CHOICES, default='ABERTO')
    data_abertura = models.DateTimeField("Data de abertura", auto_now_add=True)

    def __str__(self):
        return f"[{self.id}] {self.titulo} ({self.status})"
