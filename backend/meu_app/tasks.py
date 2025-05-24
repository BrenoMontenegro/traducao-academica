from celery import shared_task
from .models import TextoOriginal, ResumoGerado
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.text_rank import TextRankSummarizer

@shared_task
def gerar_resumo(texto_id):
    print(f"CELERY >>> RESUMO RECEBIDO PARA TEXTO ID: {texto_id}")
    texto = TextoOriginal.objects.get(id=texto_id)

    parser = PlaintextParser.from_string(texto.conteudo, Tokenizer("portuguese"))
    summarizer = TextRankSummarizer()
    frases = summarizer(parser.document, 3)  

    resumo_final = " ".join(str(sentenca) for sentenca in frases)

    ResumoGerado.objects.create(
        texto_original=texto,
        resumo=resumo_final
    )

    print(f"✅ RESUMO GERADO para texto ID: {texto_id}")