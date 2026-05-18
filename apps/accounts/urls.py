from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('profile/', views.profile, name='profile'),
    # Boshqa custom view'lar shu yerga qo'shiladi
]
