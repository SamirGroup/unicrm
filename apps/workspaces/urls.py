from django.urls import path
from . import views

app_name = 'workspaces'

urlpatterns = [
    path('', views.index, name='index'),
    path('create/', views.create, name='create'),
    path('<slug:workspace_slug>/settings/', views.settings, name='settings'),
    path('<slug:workspace_slug>/members/', views.members, name='members'),
    path('<slug:workspace_slug>/modules/', views.modules, name='modules'),
    path('<slug:workspace_slug>/modules/<str:module_type>/toggle/', views.toggle_module, name='toggle_module'),
]
