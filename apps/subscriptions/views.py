from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import SubscriptionPlan, Subscription, Payment, PaymentReminder
from apps.workspaces.models import Workspace, WorkspaceMember

@login_required
def dashboard(request):
    """Subscription dashboard"""
    memberships = WorkspaceMember.objects.filter(user=request.user).select_related('workspace__subscription')
    
    context = {
        'memberships': memberships,
    }
    return render(request, 'subscriptions/dashboard.html', context)

@login_required
def activate_plan(request, workspace_slug, plan_slug):
    """Activate subscription plan"""
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    membership = WorkspaceMember.objects.filter(workspace=workspace, user=request.user).first()
    
    if not membership or membership.role not in ['owner', 'admin']:
        return JsonResponse({'error': 'Unauthorized'}, status=403)
    
    plan = get_object_or_404(SubscriptionPlan, slug=plan_slug, is_active=True)
    
    # Check if subscription exists
    subscription, created = Subscription.objects.get_or_create(
        workspace=workspace,
        defaults={
            'plan': plan,
            'start_date': timezone.now().date(),
            'end_date': timezone.now().date() + timedelta(days=plan.duration_days),
            'status': 'pending'
        }
    )
    
    if not created:
        subscription.plan = plan
        subscription.start_date = timezone.now().date()
        subscription.end_date = timezone.now().date() + timedelta(days=plan.duration_days)
        subscription.status = 'pending'
        subscription.save()
    
    # Create payment
    payment = Payment.objects.create(
        subscription=subscription,
        amount=plan.price,
        method='click'  # Default method
    )
    
    return JsonResponse({
        'success': True,
        'payment_id': payment.id,
        'amount': str(plan.price),
        'message': 'To\'lovni amalga oshirish uchun quyidagi havolaga o\'ting'
    })

@login_required
def payment_callback(request, payment_id):
    """Payment callback handler"""
    payment = get_object_or_404(Payment, id=payment_id)
    
    # Mark as completed
    payment.complete()
    
    # Extend subscription
    if payment.subscription.plan:
        payment.subscription.extend(payment.subscription.plan.duration_days)
        payment.subscription.status = 'active'
        payment.subscription.save()
    
    return render(request, 'subscriptions/payment_success.html', {
        'payment': payment
    })

@require_http_methods(['POST'])
@login_required
def send_reminder(request, subscription_id):
    """Send payment reminder"""
    subscription = get_object_or_404(Subscription, id=subscription_id)
    
    reminder = PaymentReminder.objects.create(
        subscription=subscription,
        message=f"Sizning workspace subscription'ingiz yaqinlashmoqda. Iltimos, to'lovni amalga oshiring.",
        is_sent=True,
        sent_at=timezone.now()
    )
    
    return JsonResponse({'success': True, 'reminder_id': reminder.id})

def auto_check_expiration():
    """Background task to check expired subscriptions"""
    from datetime import date
    today = date.today()
    
    # Check expired subscriptions
    expired = Subscription.objects.filter(end_date__lt=today, status='active')
    for sub in expired:
        sub.status = 'suspended'
        sub.save()
        
        # Create reminder
        PaymentReminder.objects.create(
            subscription=sub,
            message="Subscription muddati tugadi. Iltimos, to'lovni amalga oshiring.",
        )
    
    # Check expiring soon (within 3 days)
    expiring_soon = Subscription.objects.filter(
        end_date__gte=today,
        end_date__lte=today + timedelta(days=3),
        status='active'
    )
    for sub in expiring_soon:
        PaymentReminder.objects.create(
            subscription=sub,
            message=f"Sizning subscription'ingiz {sub.days_remaining} kundan keyin tugaydi.",
        )
