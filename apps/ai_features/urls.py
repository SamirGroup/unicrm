from django.urls import path
from django.shortcuts import render
from . import views

app_name = 'ai'

urlpatterns = [
    path('reports/', views.reports, name='reports'),
    path('<slug:workspace_slug>/daily-summary/', views.generate_daily_summary, name='generate_daily_summary'),
    path('<slug:workspace_slug>/client/<int:client_id>/insights/', views.generate_client_insights, name='generate_client_insights'),
]
