from django.core.mail import send_mail
from django.shortcuts import render, redirect
from . import forms, models
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.conf import settings


# Checa se usuario está logado ou não e o envia para pagina correta
def home_view(request):
    if request.user.is_authenticated:
        return HttpResponseRedirect('afterlogin')
    return render(request, 'painel/index.html')


# Verifica se usuario é gerente
def is_manager(user):
    usr = models.UserExtra.objects.get(user=user)
    result = usr.manager
    return result


# Verifica qual é o tipo de usuario logado e o envia para o dashboard correto
def afterlogin_view(request):
    if is_manager(request.user):
        return redirect('manager-dashboard-view')
    else:
        return redirect('user-dashboard-view')


# Sobre a empresa
def aboutus_view(request):
    return render(request, 'painel/aboutus.html')


# Formulario de contato com a empresa
def contactus_view(request):
    sub = forms.ContactusForm()
    if request.method == 'POST':
        sub = forms.ContactusForm(request.POST)
        if sub.is_valid():
            email = sub.cleaned_data['Email']
            name = sub.cleaned_data['Nome']
            message = sub.cleaned_data['Mensagem']
            send_mail(f"Pastelaria: Feedback de {name} ({email})", message, settings.EMAIL_HOST_USER, settings.EMAIL_RECEIVING_USER,
                      fail_silently=False)
            return render(request, 'painel/contactussuccess.html')
    return render(request, 'painel/contactus.html', {'form': sub})


# Dashboard do gerente
@login_required(login_url='userlogin')
@user_passes_test(is_manager)
def manager_dashboard_view(request):
    usr = models.UserExtra.objects.get(user=request.user)
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    return render(request, 'painel/manager/dashboard.html', {'usr': usr, 'avatar': avatar})


# Dashboard do usuario comum
@login_required(login_url='userlogin')
def user_dashboard_view(request):
    usr = models.UserExtra.objects.get(user=request.user)
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    return render(request, 'painel/user/dashboard.html', {'usr': usr, 'avatar': avatar})


# Lista de tarefas para o usuario
@login_required(login_url='userlogin')
def user_task_view(request):
    usr = models.User.objects.get(id=request.user.id)  # Captura qual é o usuario
    cl = models.Task.objects.filter(user=usr)  # Filtra apenas as atividades do usuario
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    return render(request, 'painel/user/list_task.html', {'list': cl, 'avatar': avatar})


# Verifica status da tarefa e altera
@login_required(login_url='userlogin')
def task_done_view(request, pk):
    cl = models.Task.objects.get(id=pk)
    if cl.done:
        print('ja foi concluido')
    else:
        cl.done = True  # Informa que a tarefa foi concluida
        cl.save()  # Salva a informação
        # Enviar e-mail de conclusão para o gerente que criou a tarefa
        email = cl.created_by.user.email
        name = cl.user.first_name
        message = f"Olá {name}! " \
                  f"A tarefa ({cl.message}) com prazo de até {cl.end_at} " \
                  f"foi concluida pelo usuario {cl.user.first_name}"
        send_mail(f"Pastelaria: Tarefa concluida pelo usuario {name}",  # Titulo
                  message,  # Mensagem
                  settings.EMAIL_HOST_USER,  # Host
                  [email],  # Quem irá receber
                  fail_silently=False)
    return redirect('user-task-view')


# Lista de tarefas criadas pelo gerente
@login_required(login_url='userlogin')
@user_passes_test(is_manager)
def list_task_manager_view(request):
    manager = models.UserExtra.objects.get(user=request.user)  # Captura qual UserExtra é o do usuario gerente
    cl = models.Task.objects.filter(created_by=manager)  # Filtra apenas as atividades que o gerente criou
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    return render(request, 'painel/manager/list_task.html', {'list': cl, 'avatar': avatar})


# Criar nova tarefa
@login_required(login_url='userlogin')
@user_passes_test(is_manager)
def new_task_view(request):
    form = forms.TaskForm()
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    mydict = {'form': form, 'avatar': avatar}
    if request.method == 'POST':
        form = forms.TaskForm(request.POST)
        if form.is_valid():
            f2 = form.save(commit=False)
            manager = models.UserExtra.objects.get(user=request.user)
            f2.created_by = manager
            u2 = f2.save()
            # Enviar e-mail para o usuario informando sobre a nova tarefa
            email = f2.user.email
            name = f2.user.first_name
            message = f"Olá {name}! " \
                      f"A tarefa ({f2.message}) foi criada pelo gerente {manager.user.first_name} para você " \
                      f"com prazo de conclusão até {f2.end_at}"
            send_mail(f"Pastelaria: Nova tarefa criada por {manager.user.first_name}",  # Titulo
                      message,  # Mensagem
                      settings.EMAIL_HOST_USER,  # Host
                      [email],  # Quem irá receber
                      fail_silently=False)
        return redirect('list-task-manager-view')

    return render(request, 'painel/manager/new_task.html', context=mydict)


# Lista de usuarios cadastrados
@login_required(login_url='userlogin')
@user_passes_test(is_manager)
def list_user_view(request):
    cl = models.User.objects.filter()
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    return render(request, 'painel/manager/list_user.html', {'list': cl, 'avatar': avatar})


# Criar novo usuario
@login_required(login_url='userlogin')
@user_passes_test(is_manager)
def new_user_view(request):
    form1 = forms.UserForm()
    form2 = forms.UserExtraForm()
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    mydict = {'form1': form1, 'form2': form2, 'avatar': avatar}
    if request.method == 'POST':
        form2 = forms.UserExtraForm(request.POST)
        user = User.objects.create_user(request.POST.get('email'), request.POST.get('email'),
                                        request.POST.get('password'))
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.save()
        if form2.is_valid():
            f2 = form2.save(commit=False)
            f2.user = user
            user2 = f2.save()
        return redirect('afterlogin')

    return render(request, 'painel/manager/new_user.html', context=mydict)


# Configurações de usuario comum
@login_required(login_url='userlogin')
def user_config_view(request):
    # Informações do Django
    usr = models.User.objects.get(id=request.user.id)
    dt = {'id': usr.id,
          'first_name': usr.first_name,
          'last_name': usr.last_name,
          'username': usr.username,
          'email': usr.email
    }
    form = forms.UserForm(initial=dt)
    # Informações extras
    us2 = models.UserExtra.objects.get(user=request.user)
    dt2 = {'mobile': us2.mobile, 'phone': us2.phone, 'address': us2.address}
    form2 = forms.UserExtraForm(initial=dt2)
    # Une os dois formularios
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    mydict = {'form1': form, 'form2': form2, 'avatar': avatar}
    if request.method == 'POST':
        # User
        usr.first_name = request.POST.get('first_name')
        usr.last_name = request.POST.get('last_name')
        usr.email = request.POST.get('username')
        usr.username = request.POST.get('username')
        usr.save()
        # UserExtra
        cl = models.UserExtra.objects.get(user=request.user)
        cl.phone = request.POST.get('phone')
        cl.mobile = request.POST.get('mobile')
        cl.address = request.POST.get('address')
        cl.save()
        return redirect('afterlogin')

    return render(request, 'painel/user/config.html', context=mydict)


# Configurações de usuario manager
@login_required(login_url='userlogin')
@user_passes_test(is_manager)
def manager_config_view(request):
    # Informações do Django
    usr = models.User.objects.get(id=request.user.id)
    dt = {'id': usr.id,
          'first_name': usr.first_name,
          'last_name': usr.last_name,
          'username': usr.username,
          'email': usr.email
    }
    form = forms.UserForm(initial=dt)
    # Informações extras
    us2 = models.UserExtra.objects.get(user=request.user)
    dt2 = {'mobile': us2.mobile, 'phone': us2.phone, 'address': us2.address}
    form2 = forms.UserExtraForm(initial=dt2)
    # Une os dois formularios
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    mydict = {'form1': form, 'form2': form2, 'avatar': avatar}
    if request.method == 'POST':
        # User
        usr.first_name = request.POST.get('first_name')
        usr.last_name = request.POST.get('last_name')
        usr.email = request.POST.get('username')
        usr.username = request.POST.get('username')
        usr.save()
        # UserExtra
        cl = models.UserExtra.objects.get(user=request.user)
        cl.phone = request.POST.get('phone')
        cl.mobile = request.POST.get('mobile')
        cl.address = request.POST.get('address')
        cl.save()
        return redirect('afterlogin')

    return render(request, 'painel/manager/config.html', context=mydict)


# Upload foto do usuario gerente
def upload_manager_avatar_view(request):
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    if request.method == 'POST':  # Checa se usuario enviou uma foto
        us = models.UserExtra.objects.get(user=request.user)  # Captura qual UserExtra do usuario
        us.avatar.save('{0}_avatar.jpg'.format(request.user.first_name), request.FILES['userimg'])  # Salva foto
        us.save()
        return redirect('afterlogin')
    else:
        form = forms.UserAvatarForm()
    return render(request, 'painel/manager/upload_avatar.html', {'form': form, 'avatar': avatar})


# Upload foto do usuario comum
def upload_user_avatar_view(request):
    avatar = models.UserExtra.objects.filter(user=request.user).values_list('avatar', flat=True)  # Foto do usuario
    if request.method == 'POST':  # Checa se usuario enviou uma foto
        us = models.UserExtra.objects.get(user=request.user)  # Captura qual UserExtra do usuario
        us.avatar.save('{0}_avatar.jpg'.format(request.user.first_name), request.FILES['userimg'])  # Salva foto
        us.save()
        return redirect('afterlogin')
    else:
        form = forms.UserAvatarForm()
    return render(request, 'painel/user/upload_avatar.html', {'form': form, 'avatar': avatar})