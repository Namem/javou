from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.urls import reverse

class CategoriaArtigo(models.Model):
    nome = models.CharField("Nome da Categoria", max_length=100, unique=True)
    slug = models.SlugField("URL (slug)", max_length=100, unique=True, blank=True, 
                            help_text="Endereço único para a categoria, gerado automaticamente se deixado em branco.")

    class Meta:
        verbose_name = "Categoria de Artigo"
        verbose_name_plural = "Categorias de Artigos"
        ordering = ['nome']

    def save(self, *args, **kwargs):
        # Gera o slug automaticamente a partir do nome se ele não existir
        if not self.slug:
            self.slug = slugify(self.nome)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome

class Artigo(models.Model):
    STATUS_CHOICES = (
        ('rascunho', 'Rascunho'),
        ('publicado', 'Publicado'),
    )

    titulo = models.CharField("Título do Artigo", max_length=200)
    slug = models.SlugField("URL (slug)", max_length=200, unique=True, blank=True,
                            help_text="Endereço único para o artigo, gerado automaticamente se deixado em branco.")
    categoria = models.ForeignKey(CategoriaArtigo, on_delete=models.PROTECT, related_name='artigos', verbose_name="Categoria")
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='artigos_escritos', verbose_name="Autor")
    conteudo = models.TextField("Conteúdo do Artigo")
    status = models.CharField("Status", max_length=10, choices=STATUS_CHOICES, default='rascunho')
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Artigo"
        verbose_name_plural = "Artigos"
        ordering = ['-data_criacao']

    def save(self, *args, **kwargs):
        # Gera o slug automaticamente a partir do título se ele não existir
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo
    
    def get_absolute_url(self):
        # Gera a URL para um artigo específico (útil no admin)
        return reverse("knowledge_base:detalhe_artigo", kwargs={"slug": self.slug})