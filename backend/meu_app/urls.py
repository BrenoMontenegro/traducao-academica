from django.urls import path
from . import views
from django.shortcuts import render
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.login_usuario, name='login'),        #minha tela de login
    path('cadastro/', views.cadastrar_usuario, name='cadastro'),
    path('index/', views.index, name='index'),
    path('registrar/', views.registrar_usuario, name='registrar'), #criar
    path('sucesso/', views.sucesso, name = 'sucesso'),
    path('lista/', views.listar_usuarios, name='lista'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar'), #editar
    path('deletar/<int:pk>/', views.deletar_usuario, name='deletar'), #deletar
    path('perfil/<int:pk>/', views.perfil_usuario, name='perfil'),   #visualizar/ler
    path('logout/', views.logout_usuario, name='logout'),
    path('traduzir/', views.traduzir_texto, name="traduzir"),
    path('upload/', views.upload_pdf, name='upload'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)