from django.urls import path
from . import views
from django.shortcuts import render

urlpatterns = [
    path('', views.login_usuario, name='login'),#minha tela de login
    path('cadastro/', views.cadastrar_usuario, name='cadastro'),
    path('index/', views.index, name='index'),
    path('registrar/', views.registrar_usuario, name='registrar'), #criar
    path('sucesso/', views.sucesso, name = 'sucesso'),
    path('lista/', views.listar_usuarios, name='lista'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar'), #editar
    path('deletar/<int:pk>/', views.deletar_usuario, name='deletar'), #deletar
    path('perfil/<int:pk>/', views.perfil_usuario, name='perfil'),   #visualizar/ler
    path('logout/', views.logout_usuario, name='logout'),
]
