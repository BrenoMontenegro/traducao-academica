from django.urls import path
from . import views
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_usuario, name='login'),        
    path('cadastro/', views.cadastrar_usuario, name='cadastro'),
    path('home/', views.pagina_principal, name='home'),
    path('index/', views.index, name='index'),
    path('registrar/', views.registrar_usuario, name='registrar'), 
    path('sucesso/', views.sucesso, name = 'sucesso'),
    path('lista/', views.listar_usuarios, name='lista'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar'), 
    path('deletar/<int:pk>/', views.deletar_usuario, name='deletar'), 
    path('perfil/<int:pk>/', views.perfil_usuario, name='perfil'),   
    path('logout/', views.logout_usuario, name='logout'),
    path('deletar-resumo/<int:resumo_id>/', views.deletar_resumo, name='deletar_resumo'),
    path('meus-resumos/', views.meus_resumos, name='meus_resumos'),
    path('historico/', views.historico, name='historico'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('tempo-estudo-ao-vivo/', views.tempo_estudo_ao_vivo, name='tempo_estudo_ao_vivo'),
    path('obter_tempo_estudado_hoje/', views.obter_tempo_estudado_hoje, name='obter_tempo_estudado_hoje'),
    path('tarefas/', views.quadro_tarefas, name='tarefas'),
    path('tarefas/<int:id>/deletar/', views.deletar_tarefa, name='deletar_tarefa'),
    path('tarefas/<int:id>/mover/', views.mover_tarefa, name='mover_tarefa'),
    path('atualizar-status/', views.atualizar_status, name='atualizar_status'),
    path('deletar-tarefa/<int:id>/', views.deletar_tarefa, name='deletar_tarefa'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])
