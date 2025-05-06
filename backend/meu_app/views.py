from django.shortcuts import render, redirect, get_object_or_404
from .models import Usuario
from django.http import HttpResponse

def registrar_usuario(request):
    if request.method == 'POST':
        nome = request.POST.get('nome')
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        usuario = Usuario(nome=nome, email=email, senha=senha)
        usuario.save()

        return redirect('sucesso')

    return render(request, 'meu_app/registro.html')

def listar_usuarios(request):
    usuarios = Usuario.objects.all()
    return render(request, 'meu_app/lista.html', {'usuarios': usuarios})

def editar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        usuario.nome = request.POST.get('nome')
        usuario.email = request.POST.get('email')
        usuario.senha = request.POST.get('senha')
        usuario.save()

        return redirect('sucesso')

    return render(request, 'meu_app/registro.html', {'usuario': usuario})

def deletar_usuario(request, pk):
    usuario = get_object_or_404(Usuario, pk=pk)

    if request.method == 'POST':
        usuario.delete()
        return redirect('sucesso')

    return render(request, 'meu_app/confirma_exclusao.html', {'usuario': usuario})

def perfil_usuario(request):
    usuario = Usuario.objects.first()
    return render(request, 'meu_app/perfil.html', {'usuario': usuario})