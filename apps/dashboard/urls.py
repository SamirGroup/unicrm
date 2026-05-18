from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('', views.index, name='index'),
    path('api/stats/', views.stats_api, name='stats_api'),
    path('api/top-clients/', views.top_clients_api, name='top_clients_api'),
    path('api/orders-chart/', views.orders_chart_api, name='orders_chart_api'),
    path('api/ai/daily-summary/', views.daily_ai_summary, name='daily_summary'),
]
