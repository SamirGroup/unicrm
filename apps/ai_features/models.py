from django.db import models
from apps.workspaces.models import Workspace

class AISummary(models.Model):
    """AI-generated summaries"""
    SUMMARY_TYPES = [
        ('client', 'Client Summary'),
        ('order', 'Order Summary'),
        ('daily', 'Daily Report'),
        ('weekly', 'Weekly Report'),
    ]
    
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='ai_summaries')
    summary_type = models.CharField(max_length=50, choices=SUMMARY_TYPES)
    content = models.TextField()
    related_object_id = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.summary_type} - {self.created_at}"
