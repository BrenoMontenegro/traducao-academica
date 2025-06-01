from celery import shared_task
from .models import TextoOriginal, ResumoGerado
from .services.ia import gerar_insight_local  

@shared_task
def gerar_resumo(texto_id):
    texto = TextoOriginal.objects.get(id=texto_id)
    resumo = gerar_insight_local(texto.conteudo)

    ResumoGerado.objects.create(
        texto_original=texto,
        resumo=resumo
    )