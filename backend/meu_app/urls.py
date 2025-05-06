from django.urls import path
from . import views

urlpatterns = [
    path('registrar/', views.registrar_usuario, name='registrar'),
    path('sucesso/', lambda r: render(r, 'meu_app/sucesso.html'), name='sucesso'),
    path('lista/', views.listar_usuarios, name='lista'),
    path('editar/<int:pk>/', views.editar_usuario, name='editar'),
    path('deletar/<int:pk>/', views.deletar_usuario, name='deletar'),
    path('perfil/', views.perfil_usuario, name='perfil'),
]
