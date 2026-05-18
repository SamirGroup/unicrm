from django.db import models
from apps.workspaces.models import Workspace
from apps.accounts.models import User

class Client(models.Model):
    """Client/Contact model"""
    SOURCE_CHOICES = [
        ('telegram', 'Telegram'),
        ('website', 'Website'),
        ('referral', 'Referral'),
        ('call', 'Call'),
        ('other', 'Other'),
    ]
    
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='clients')
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=50, blank=True)
    telegram_id = models.BigIntegerField(null=True, blank=True)
    telegram_username = models.CharField(max_length=255, blank=True)
    source = models.CharField(max_length=50, choices=SOURCE_CHOICES, default='other')
    tags = models.CharField(max_length=500, blank=True, help_text="Vergul bilan ajratilgan teglar")
    notes = models.TextField(blank=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}".strip()
