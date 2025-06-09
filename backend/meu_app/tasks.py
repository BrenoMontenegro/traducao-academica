from celery import shared_task
from .models import TextoOriginal, ResumoGerado
from .services.ia import gerar_insight_local
from django.core.mail import send_mail
from django.conf import settings

@shared_task
def gerar_resumo(texto_id):
    texto = TextoOriginal.objects.get(id=texto_id)
    resumo = gerar_insight_local(texto.conteudo)

    ResumoGerado.objects.create(
        texto_original=texto,
        resumo=resumo
    )
@shared_task   
def enviar_email_welcome(email, nome, senha):
    if len(senha) <=4:
        senha_censurada = '*' * len(senha)
    else:
        senha_censurada = senha[:2] + '*' * (len(senha) - 4) + senha [-2:]
        
    assunto = "Bem vindo ao Gerador de Resumo!"
    mensagem = f"""
Olá, {nome},

Seu cadastro foi realizado com sucesso!

Aqui estão seus dados de acesso:

Email: {email}
Senha: {senha_censurada}

Att,
Equipe Peso Pleno

"""

    send_mail(
        assunto,
        mensagem,
        settings.DEFAULT_FROM_EMAIL,
        [email],
        fail_silently = False
    )