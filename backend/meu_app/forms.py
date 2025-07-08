from django import forms
from .models import Usuario
from django.db import models
from .models import Tarefa

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nome', 'email', 'senha']
        widgets = {
            'senha': forms.PasswordInput()
        }

class TarefaForm(forms.ModelForm):  
    class Meta:
        model = Tarefa
        fields = ['titulo', 'descricao', 'status', 'data']
        widgets = {
            'titulo': forms.TextInput(attrs={'class': 'form-control'}),
            'descricao': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'status': forms.Select(attrs={'class': 'form-select'}),
            'data': forms.DateInput(attrs={'type': 'date', 'class': 'form-control'}),
        }