from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('<slug:workspace_slug>/', views.list, name='list'),
    path('<slug:workspace_slug>/<int:pk>/', views.detail, name='detail'),
]
