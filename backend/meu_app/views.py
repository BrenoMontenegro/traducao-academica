import os
import requests
import fitz
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from .forms import UsuarioForm
from django.http import FileResponse
from django.core.files.storage import default_storage

DEEPL_API_KEY = "e209052d-4ff1-4a0a-b2f8-cfb6ae173c07:fx"

def registrar_usuario(request):
    if request.method == 'POST':
        print("Dados enviados:", request.POST)
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = Usuario(nome=nome, email=email, senha=senha)
        usuario.save()

        return redirect('sucesso')

    return render(request, 'meu_app/registro.html')

def sucesso(request):
    return render(request, 'meu_app/sucesso.html')

def login_usuario(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        try:
            usuario = Usuario.objects.get(email=email, senha=senha)
            request.session['usuario_id'] = usuario.id
            return redirect('index')

        except Usuario.DoesNotExist:
            return render(request, 'meu_app/login.html', {
                'erro': 'Email ou senha inválidos.',
                'email': email  
            })

    return render(request, 'meu_app/login.html')

def cadastrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        if Usuario.objects.filter(email=email).exists():
            return render(request, 'meu_app/cadastro.html', {'erro': 'Esse e-mail já está em uso.'})

        usuario = Usuario.objects.create(nome=nome, email=email, senha=senha)
        request.session['usuario_id'] = usuario.id  
        return redirect('index')  

    return render(request, 'meu_app/cadastro.html')

def index(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    print("ID da sessão:", request.session.get('usuario_id'))
    usuario = get_object_or_404(Usuario, pk=usuario_id)
    return render(request, 'meu_app/index.html', {'usuario': usuario})

def logout_usuario(request):
    request.session.flush()
    return redirect('login')


def listar_usuarios(request):
    return redirect('index')


def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('sucesso')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'meu_app/registro.html', {'form': form})

def deletar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        usuario.delete()
        request.session.flush()
        return redirect('login')

    return redirect('perfil', pk=pk)

def perfil_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'meu_app/perfil.html', {'usuario': usuario})


@csrf_exempt  
def traduzir_texto(request):
    if request.method == "POST":
        texto = request.POST.get("texto")
        origem = request.POST.get("origem", "EN")
        destino = request.POST.get("destino", "PT")

        url = "https://api-free.deepl.com/v2/translate"
        headers = {
            "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
        }
        data = {
            "text": texto,
            "source_lang": origem.upper(),
            "target_lang": destino.upper()
        }

        response = requests.post(url, data=data, headers=headers)

        if response.status_code == 200:
            traducao = response.json()["translations"][0]["text"]
            return render(request, "meu_app/index.html", {"traducao": traducao, "original": texto})
        else:
            return render(request, "meu_app/index.html", {"erro": "Erro ao traduzir o texto."})

    return render(request, "meu_app/index.html")


@csrf_exempt
def upload_pdf(request):
    usuario_id = request.session.get('usuario_id')
    usuario = Usuario.objects.get(pk=usuario_id) if usuario_id else None
    

    if request.method == 'POST' and request.FILES.get('arquivo_pdf'):
        pdf = request.FILES['arquivo_pdf']
        caminho = default_storage.save(pdf.name, pdf)

        
        texto_extraido = ""
        with fitz.open(default_storage.path(caminho)) as doc:
            for pagina in doc:
                texto_extraido += pagina.get_text()

    
        url = "https://api-free.deepl.com/v2/translate"
        headers = {
            "Authorization": f"DeepL-Auth-Key {DEEPL_API_KEY}"
        }
        data = {
            "text": texto_extraido,  
            "target_lang": "PT"
        }

        response = requests.post(url, data=data, headers=headers)
        

        if response.status_code == 200:
            texto_traduzido = response.json()["translations"][0]["text"]
            novo_pdf_path = os.path.join("media", "pdf_traduzido.pdf")
            doc_traduzido = fitz.open()
            page = doc_traduzido.new_page()
            page.insert_text((72, 72), texto_traduzido, fontsize=11)
            doc_traduzido.save(novo_pdf_path)

            return render(request, 'meu_app/index.html', {
                'usuario': usuario,
                'texto_original': texto_extraido,
                'traducao': texto_traduzido,
                'pdf_url': '/' + novo_pdf_path
            })

        else:
            return render(request, 'meu_app/index.html', {
                'usuario': usuario,
                'erro': 'Erro na tradução.'
            })

    return render(request, 'meu_app/index.html', {'usuario': usuario})