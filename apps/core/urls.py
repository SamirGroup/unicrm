"""
URL configuration for UniCRM AI project.
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.shortcuts import redirect

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', lambda request: redirect('/dashboard/')),
    
    # Allauth (account/login, account/logout, account/signup)
    path('accounts/', include('allauth.urls')),
    
    # Custom accounts (faqat profile va boshqa custom view'lar)
    path('myaccounts/', include('apps.accounts.urls')),
    
    # App URLs
    path('dashboard/', include('apps.dashboard.urls')),
    path('workspace/', include('apps.workspaces.urls')),
    path('orders/', include('apps.orders.urls')),
    path('clients/', include('apps.clients.urls')),
    path('telegram/', include('apps.telegram_bot.urls')),
    path('ai/', include('apps.ai_features.urls')),
    path('modules/', include('apps.modules.urls')),
    path('subscription/', include('apps.subscriptions.urls')),
    
    # Super Admin
    path('superadmin/', include('apps.admin_panel.urls')),
]

# Static files during development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
