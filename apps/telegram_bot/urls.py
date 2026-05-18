from django.urls import path
from . import views

app_name = 'telegram_bot'

urlpatterns = [
    path('miniapp/', views.telegram_miniapp_view, name='miniapp'),
    path('auth/', views.telegram_auth_view, name='auth'),
]
