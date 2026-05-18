from django.db import models
from apps.accounts.models import User
from apps.workspaces.models import Workspace

class SubscriptionPlan(models.Model):
    """Subscription plans"""
    PLAN_TYPES = [
        ('monthly', 'Monthly'),
        ('yearly', 'Yearly'),
    ]
    
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    duration_days = models.IntegerField()
    features = models.TextField(help_text="Features list, one per line")
    is_active = models.BooleanField(default=True)
    
    def __str__(self):
        return f"{self.name} - {self.price} UZS"

class Subscription(models.Model):
    """Workspace subscription"""
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('expired', 'Expired'),
        ('pending', 'Pending Payment'),
        ('suspended', 'Suspended'),
    ]
    
    workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE, related_name='subscription')
    plan = models.ForeignKey(SubscriptionPlan, on_delete=models.SET_NULL, null=True)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    start_date = models.DateField()
    end_date = models.DateField()
    auto_renew = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.workspace.name} - {self.plan.name}"
    
    @property
    def is_active(self):
        return self.status == 'active'
    
    @property
    def days_remaining(self):
        from datetime import date, timedelta
        today = date.today()
        if self.end_date > today:
            return (self.end_date - today).days
        return 0
    
    def extend(self, days):
        """Extend subscription by days"""
        from datetime import date, timedelta
        if self.end_date < date.today():
            self.end_date = date.today() + timedelta(days=days)
        else:
            self.end_date += timedelta(days=days)
        self.save()

class Payment(models.Model):
    """Payment records"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    
    METHOD_CHOICES = [
        ('click', 'Click'),
        ('payme', 'Payme'),
        ('cash', 'Cash'),
        ('card', 'Card'),
    ]
    
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    method = models.CharField(max_length=20, choices=METHOD_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    transaction_id = models.CharField(max_length=255, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Payment {self.id} - {self.amount} UZS"
    
    def complete(self, transaction_id=''):
        """Mark payment as completed"""
        self.status = 'completed'
        self.payment_date = models.timezone.now()
        self.transaction_id = transaction_id
        self.save()
        
        # Extend subscription
        if self.subscription.plan:
            self.subscription.extend(self.subscription.plan.duration_days)
            self.subscription.status = 'active'
            self.subscription.save()

class PaymentReminder(models.Model):
    """Payment reminders"""
    subscription = models.ForeignKey(Subscription, on_delete=models.CASCADE, related_name='reminders')
    message = models.TextField()
    sent_at = models.DateTimeField(null=True, blank=True)
    is_sent = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Reminder for {self.subscription.workspace.name}"
