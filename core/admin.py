from django.contrib import admin
from .models import *
from .forms import *


class UserExtraAdmin(admin.ModelAdmin):
    pass


admin.site.register(UserExtra, UserExtraAdmin)


class TaskAdmin(admin.ModelAdmin):
    form = TaskForm
    pass


admin.site.register(Task, TaskAdmin)