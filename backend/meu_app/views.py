from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from django.http import HttpResponse
from .forms import UsuarioForm
from django.contrib.auth.decorators import login_required

def registrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = Usuario(nome=nome, email=email, senha=senha)
        usuario.save()

        return redirect('sucesso')

    return render(request, 'meu_app/registro.html')

def sucesso(request):
    return render(request, 'meu_app/sucesso.html')

@login_required
def index(request):
    return render(request, 'meu_app/index.html', {'usuario': request.user})

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'meu_app/lista.html', {'usuarios': usuarios})


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
        return redirect('sucesso')

    return render(request, 'meu_app/confirma_exclusao.html', {'usuario': usuario})

def perfil_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)
    return render(request, 'meu_app/perfil.html', {'usuario': usuario})