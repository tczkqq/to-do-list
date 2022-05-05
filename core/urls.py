from django.contrib import admin
from django.urls import path
from . import views

app_name = "core"

urlpatterns = [
    path('', views.home_view, name='home'),
    path('employee/<int:id>', views.detail_view, name='detail'),
    path('api/task/<int:id>', views.task, name='task'),
    path('api/tasks', views.tasks_list, name='tasks')
    
    
    
]
