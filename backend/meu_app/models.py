from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now

class Usuario(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    senha = models.CharField(max_length=100)

    def __str__(self):
        return self.nome

class TextoOriginal(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    data_envio = models.DateTimeField(auto_now_add=True)

class ResumoGerado(models.Model):
    texto_original = models.ForeignKey(TextoOriginal, on_delete=models.CASCADE)
    resumo = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)
    foi_exportado_pdf = models.BooleanField(default=False)

class SessaoEstudo(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    inicio = models.DateTimeField(default=now)
    fim = models.DateTimeField(null=True, blank=True)

    def duracao_em_minutos(self):
        if self.fim:
            return (self.fim - self.inicio).total_seconds() / 60
        return 0

