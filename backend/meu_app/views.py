import os
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from .forms import UsuarioForm
from .tasks import gerar_resumo
from .models import TextoOriginal, ResumoGerado, Usuario
from .tasks import gerar_resumo
from django.contrib import messages

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

    usuario = get_object_or_404(Usuario, pk=usuario_id)

    if request.method == "POST":
        titulo = request.POST["titulo"]
        conteudo = request.POST["conteudo"]

        usuario = Usuario.objects.get(id=request.session['usuario_id'])

        texto = TextoOriginal.objects.create(
            usuario=usuario,
            titulo=titulo,
            conteudo=conteudo
        )

        gerar_resumo.delay(texto.id)
        messages.success(request, "Resumo sendo gerado! Isso pode levar alguns minutos.")
        return redirect("index")

    usuario = Usuario.objects.get(id=request.session['usuario_id'])

    resumos = ResumoGerado.objects.filter(texto_original__usuario=usuario).order_by("-data_criacao")

    return render(request, "meu_app/index.html", {
        "usuario": usuario,
        "resumos": resumos
    })

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

def enviar_texto(request):
    if request.method == 'POST':
        conteudo = request.POST['conteudo']
        titulo = request.POST['titulo']
        texto = TextoOriginal.objects.create(usuario=request.user, titulo=titulo, conteudo=conteudo)
        gerar_resumo.delay(texto.id)  
        return redirect('resumos')
    
def listar_resumos(request):
    resumos = ResumoGerado.objects.filter(texto_original__usuario=request.user)
    return render(request, 'meu_app/lista_resumos.html', {'resumos': resumos})
    
def deletar_resumo(request, resumo_id):
    resumo = get_object_or_404(ResumoGerado, id=resumo_id)

    if request.method == "POST":
        resumo.delete()
        messages.success(request, "Resumo deletado com sucesso.")
        return redirect('index')

    return redirect('index')
    
def meus_resumos(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = get_object_or_404(Usuario, id=usuario_id)
    resumos = ResumoGerado.objects.filter(texto_original__usuario=usuario).order_by('-data_criacao')

    return render(request, 'meu_app/lista_resumos.html', {
        'resumos': resumos,
        'usuario': usuario  # <-- ESSENCIAL!
    })


