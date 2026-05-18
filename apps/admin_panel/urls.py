from django.urls import path
from . import views

app_name = 'admin_panel'

urlpatterns = [
    # Auth
    path('login/', views.admin_login, name='login'),
    path('logout/', views.admin_logout, name='logout'),
    
    # Dashboard
    path('', views.dashboard, name='dashboard'),
    path('dashboard/', views.dashboard, name='dashboard_alt'),
    
    # Contracts
    path('contracts/', views.contracts_list, name='contracts'),
    path('contracts/create/', views.contract_create, name='contract_create'),
    path('contracts/<int:pk>/', views.contract_detail, name='contract_detail'),
    path('contracts/<int:pk>/edit/', views.contract_edit, name='contract_edit'),
    
    # Payments
    path('payments/', views.payments_list, name='payments'),
    path('payments/add/<int:contract_id>/', views.payment_add, name='payment_add'),
    
    # Users
    path('users/', views.users_list, name='users'),
    path('users/<int:pk>/', views.user_detail, name='user_detail'),
    
    # Modules
    path('modules/', views.modules_list, name='modules'),
    path('modules/<int:pk>/edit/', views.module_edit, name='module_edit'),
    
    # Profile
    path('profile/', views.profile, name='profile'),
]
