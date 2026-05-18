from django.urls import path
from . import views

app_name = 'subscriptions'

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('activate/<slug:workspace_slug>/<slug:plan_slug>/', views.activate_plan, name='activate_plan'),
    path('payment/success/<int:payment_id>/', views.payment_callback, name='payment_callback'),
    path('reminder/<int:subscription_id>/', views.send_reminder, name='send_reminder'),
]
