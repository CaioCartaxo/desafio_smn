from django.db import models
from django.contrib.auth.models import User


def get_first_name(self):  # Define o usuario pelo nome
    return self.first_name


User.add_to_class("__str__", get_first_name)


class UserExtra(models.Model):  # Informações do usuario
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)  # Chave com User do Django
    joindate = models.DateField(auto_now_add=True, blank=True)  # Data de cadastro
    phone = models.CharField(max_length=15, null=True, blank=True)  # Número de telefone fixo
    mobile = models.CharField(max_length=15, null=True, blank=True)  # Número de telefone movel
    born = models.DateField(auto_now_add=False, blank=True, null=True)  # Nascimento
    address = models.CharField(max_length=256, null=True, blank=True)  # Endereço
    manager = models.BooleanField(null=True, blank=True)  # Flag para sinalizar que usuario é gerente
    avatar = models.ImageField(default='default.png')  # Foto do usuario

    def __str__(self):
        return self.user.first_name

    @property
    def get_id(self):
        return self.user.id

    @property
    def get_name(self):
        return self.user.first_name + " " + self.user.last_name


class Task(models.Model):  # Atividades dos usuarios
    created_by = models.ForeignKey(UserExtra, on_delete=models.CASCADE, blank=True)  # Gerente que criou
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)  # Usuario da atividade
    message = models.CharField(max_length=256, null=True, blank=True)  # Mensagem
    created_at = models.DateField(auto_now_add=True, blank=True, null=True)  # Data de criação da atividade
    end_at = models.DateField(auto_now_add=False, blank=True, null=True)  # Data de entrega
    done = models.BooleanField('Completo', default=False)  # Flag que sinaliza se foi concluido

    def __str__(self):
        return self.message

