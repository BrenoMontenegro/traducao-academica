from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from .forms import UsuarioForm

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