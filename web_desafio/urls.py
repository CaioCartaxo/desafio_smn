from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from core import views
from django.contrib.auth.views import LoginView, LogoutView
from web_desafio import settings

urlpatterns = [
    # Core
    path('admin/', admin.site.urls),
    path('', views.home_view, name=''),
    # Login de usuario
    path('userlogin', LoginView.as_view(template_name='painel/userlogin.html')),
    # Redireciona usuario para dashboard correta
    path('afterlogin', views.afterlogin_view, name='afterlogin'),
    # Logout do usuario
    path('logout', LogoutView.as_view(template_name='painel/index.html'), name='logout'),
    # Dashboard dos usuarios
    path('manager/dashboard', views.manager_dashboard_view, name='manager-dashboard-view'),
    path('user/dashboard', views.user_dashboard_view, name='user-dashboard-view'),
    # Informações sobre a pastelaria
    path('aboutus', views.aboutus_view),
    path('contactus', views.contactus_view),
    # Configurações do usuario
    path('manager/config', views.manager_config_view, name='manager-setting-view'),
    path('manager/upload_avatar', views.upload_manager_avatar_view, name='manager-upload-avatar-view'),
    path('user/config', views.user_config_view, name='user-setting-view'),
    path('user/upload_avatar', views.upload_user_avatar_view, name='user-upload-avatar-view'),
    # Gerenciar usuarios
    path('manager/list_user', views.list_user_view, name='list-user-view'),
    path('manager/new_user', views.new_user_view, name='new-user-view'),
    # Atividades dos gerentes
    path('manager/list_task', views.list_task_manager_view, name='list-task-manager-view'),
    path('manager/new_task', views.new_task_view, name='new-task-view'),
    # Tarefas do usuario
    path('user/list_task', views.user_task_view, name='user-task-view'),
    # Concluir tarefa
    path('user/done_task/<int:pk>', views.task_done_view, name='task-done-view'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # Permite acesso publico as imagens de usuario
