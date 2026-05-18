from django.db import models
from apps.accounts.models import User

class Workspace(models.Model):
    """Workspace model for multi-tenancy"""
    PLAN_CHOICES = [
        ('free', 'Free'),
        ('starter', 'Starter'),
        ('business', 'Business'),
        ('premium', 'Premium'),
    ]
    
    STATUS_CHOICES = [
        ('trial', 'Trial'),
        ('active', 'Active'),
        ('suspended', 'Suspended'),
        ('expired', 'Expired'),
    ]
    
    name = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='owned_workspaces')
    plan = models.CharField(max_length=50, choices=PLAN_CHOICES, default='free')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='trial')
    trial_ends_at = models.DateTimeField(null=True, blank=True)
    subscription_ends_at = models.DateTimeField(null=True, blank=True)
    logo = models.ImageField(upload_to='workspace_logos/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


class WorkspaceMember(models.Model):
    """Workspace membership model"""
    ROLE_CHOICES = [
        ('owner', 'Owner'),
        ('admin', 'Admin'),
        ('manager', 'Manager'),
        ('member', 'Member'),
    ]
    
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='workspace_memberships')
    role = models.CharField(max_length=50, choices=ROLE_CHOICES, default='member')
    joined_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['workspace', 'user']

    def __str__(self):
        return f"{self.user.username} - {self.workspace.name}"


class Module(models.Model):
    """Module enable/disable for workspaces - dinamik modul tizimi"""
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='modules')
    module_type = models.CharField(max_length=50)
    is_enabled = models.BooleanField(default=True)
    settings = models.JSONField(default=dict)
    order = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['workspace', 'module_type']
        ordering = ['order', 'module_type']

    def __str__(self):
        return f"{self.workspace.name} - {self.module_type}"

    @property
    def display_name(self):
        """Modul nomini ModulePrice dan olish"""
        from apps.admin_panel.models import ModulePrice
        try:
            mp = ModulePrice.objects.get(module_type=self.module_type)
            return mp.name
        except ModulePrice.DoesNotExist:
            return self.module_type.replace('_', ' ').title()
    
    @property
    def price(self):
        """Modul narxini ModulePrice dan olish"""
        from apps.admin_panel.models import ModulePrice
        try:
            mp = ModulePrice.objects.get(module_type=self.module_type)
            return mp.price
        except ModulePrice.DoesNotExist:
            return 0
