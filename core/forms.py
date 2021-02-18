from django import forms
from django.contrib.auth.models import User
from django.forms import Textarea
from . import models


# Informações do usuario
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'password', 'email']


# Informações adicionais do usuario
class UserExtraForm(forms.ModelForm):

    class Meta:
        model = models.UserExtra
        fields = ['user', 'phone', 'mobile', 'born', 'address', 'manager']


# Foto do usuario
class UserAvatarForm(forms.ModelForm):

    class Meta:
        model = models.UserExtra
        fields = ['avatar']


# Atividades
class TaskForm(forms.ModelForm):

    class Meta:
        model = models.Task
        fields = ['created_by', 'user', 'message', 'end_at', 'done']
        widgets = {
            'message': Textarea(attrs={'cols': 19, 'rows': 5})
        }


# E-mail de feedback
class ContactusForm(forms.Form):
    Nome = forms.CharField(max_length=30)
    Email = forms.EmailField()
    Mensagem = forms.CharField(max_length=500, widget=forms.Textarea(attrs={'rows': 3, 'cols': 30}))
