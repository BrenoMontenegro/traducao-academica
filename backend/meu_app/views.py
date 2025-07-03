import os
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from .forms import UsuarioForm
from .tasks import gerar_resumo
from .models import TextoOriginal, ResumoGerado, Usuario
from django.contrib import messages
from .tasks import enviar_email_welcome
from django.contrib.auth.signals import user_logged_in, user_logged_out
from django.dispatch import receiver
from .models import SessaoEstudo, MetaEstudo
from django.db.models import Sum, F, ExpressionWrapper, DurationField
import json
from django.utils.timezone import now
from django.http import JsonResponse

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
            SessaoEstudo.objects.create(usuario=usuario, inicio=now())
            return redirect('home')

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
        
        enviar_email_welcome.delay(email, nome, senha)
        
        return redirect('home')  

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

    resumos = ResumoGerado.objects.filter(texto_original__usuario=usuario).order_by("-data_criacao")[:5]

    return render(request, "meu_app/index.html", {
        "usuario": usuario,
        "resumos": resumos
    })
    
def logout_usuario(request):
    usuario_id = request.session.get('usuario_id')
    
    if usuario_id:
        from django.utils.timezone import now
        try:
            ultima_sessao = SessaoEstudo.objects.filter(usuario_id=usuario_id, fim__isnull=True).last()
            if ultima_sessao:
                ultima_sessao.fim = now()
                ultima_sessao.save()
        except SessaoEstudo.DoesNotExist:
            pass

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


def pagina_principal(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = get_object_or_404(Usuario, pk=usuario_id)
    return render(request, 'meu_app/home.html', {'usuario': usuario})



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
    
def historico(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')
        
    usuario = get_object_or_404(Usuario, pk=usuario_id)  

    resumos = ResumoGerado.objects.filter(texto_original__usuario_id=usuario_id).order_by("-data_criacao")
    return render(request, 'meu_app/historico.html', {
        'resumos': resumos,
        'usuario': usuario
    })
    
def meus_resumos(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = get_object_or_404(Usuario, id=usuario_id)
    resumos = ResumoGerado.objects.filter(texto_original__usuario=usuario).order_by('-data_criacao')

    return render(request, 'meu_app/lista_resumos.html', {
        'resumos': resumos,
        'usuario': usuario  
    })
    
@receiver(user_logged_in)
def iniciar_sessao_estudo(sender, request, user, **kwargs):
    SessaoEstudo.objects.create(usuario=user)

@receiver(user_logged_out)
def encerrar_sessao_estudo(sender, request, user, **kwargs):
    sessao = SessaoEstudo.objects.filter(usuario=user, fim__isnull=True).last()
    if sessao:
        sessao.fim = now()
        sessao.save()
        
def dashboard(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return redirect('login')

    usuario = get_object_or_404(Usuario, pk=usuario_id)

    sessoes = SessaoEstudo.objects.filter(usuario=usuario, fim__isnull=False)
    sessoes = sessoes.annotate(
        duracao=ExpressionWrapper(F('fim') - F('inicio'), output_field=DurationField())
    )
    total_duracao = sessoes.aggregate(total=Sum('duracao'))['total']
    minutos = round(total_duracao.total_seconds() / 60, 2) if total_duracao else 0
    tempo_serializado = json.dumps(minutos)

    metas = MetaEstudo.objects.filter(usuario=usuario)
    
    for meta in metas:
        if meta.tempo_meta > 0:
            progresso = min(100, round((minutos / meta.tempo_meta) * 100))
        else:
            progresso = 0
        meta.progresso = progresso

    mensagens = []

    if request.method == 'POST':
        if 'nova_meta' in request.POST:
            if MetaEstudo.objects.filter(usuario=usuario).count() >= 4:
                mensagens.append("Você já atingiu o limite de 4 metas.")
            else:
                titulo = request.POST.get('titulo')
                tempo_meta = int(request.POST.get('tempo_meta'))
                MetaEstudo.objects.create(usuario=usuario, titulo=titulo, tempo_meta=tempo_meta)
                return redirect('dashboard')

        elif 'atualizar_meta' in request.POST:
            meta_id = request.POST.get('meta_id')
            novo_valor = int(request.POST.get('tempo_meta')) 
            meta = get_object_or_404(MetaEstudo, id=meta_id, usuario=usuario)
            meta.tempo_meta = novo_valor
            meta.save()
            return redirect('dashboard')

        elif 'deletar_meta' in request.POST:
            meta_id = request.POST.get('meta_id')
            MetaEstudo.objects.filter(id=meta_id, usuario=usuario).delete()
            return redirect('dashboard')
            
        if request.method == 'POST':
            if 'zerar_tempo' in request.POST:
                SessaoEstudo.objects.filter(usuario=usuario).delete()
                MetaEstudo.objects.filter(usuario=usuario).update(tempo_realizado=0)
                return redirect('dashboard')
                
        if 'zerar_tempo' in request.POST:
            sessoes.filter(fim__isnull=False).delete()
            return redirect('dashboard')

    return render(request, 'meu_app/dashboard.html', {
        'tempo_total_json': tempo_serializado,
        'tempo_total_minutos': minutos,
        'metas': metas,
        'mensagens': mensagens,
    })

def tempo_estudo_ao_vivo(request):
    usuario_id = request.session.get('usuario_id')
    if not usuario_id:
        return JsonResponse({'erro': 'Usuário não autenticado'}, status=403)

    usuario = get_object_or_404(Usuario, pk=usuario_id)

    sessoes = SessaoEstudo.objects.filter(usuario=usuario, fim__isnull=False).annotate(
        duracao=ExpressionWrapper(F('fim') - F('inicio'), output_field=DurationField())
    )
    duracao_finalizadas = sessoes.aggregate(total=Sum('duracao'))['total']

    sessao_atual = SessaoEstudo.objects.filter(usuario=usuario, fim__isnull=True).order_by('-inicio').first()
    duracao_atual = None
    if sessao_atual:
        duracao_atual = now() - sessao_atual.inicio

    total_segundos = 0
    if duracao_finalizadas:
        total_segundos += duracao_finalizadas.total_seconds()
    if duracao_atual:
        total_segundos += duracao_atual.total_seconds()

    minutos = round(total_segundos / 60, 2)

    return JsonResponse({'tempo_total': minutos})