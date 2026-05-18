from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from apps.workspaces.models import Workspace, WorkspaceMember
from apps.clients.models import Client
from apps.orders.models import Order
from apps.ai_features.models import AISummary

@login_required
def index(request):
    """Main dashboard view"""
    # Get user's workspace
    membership = WorkspaceMember.objects.filter(user=request.user).first()
    workspace = membership.workspace if membership else None
    
    context = {
        'workspace': workspace,
    }
    return render(request, 'dashboard/index.html', context)

@login_required
def stats_api(request):
    """API endpoint for dashboard stats"""
    membership = WorkspaceMember.objects.filter(user=request.user).first()
    if not membership:
        return JsonResponse({'error': 'No workspace'}, status=404)
    
    workspace = membership.workspace
    
    stats = {
        'clients': Client.objects.filter(workspace=workspace).count(),
        'orders': Order.objects.filter(workspace=workspace).count(),
        'active_orders': Order.objects.filter(workspace=workspace, status='processing').count(),
        'revenue': str(Order.objects.filter(workspace=workspace).aggregate(
            total=Sum('total_amount')
        )['total'] or 0),
        'clients_growth': 12,
        'ai_insights': 5,
    }
    
    return JsonResponse(stats)

@login_required
def top_clients_api(request):
    """API endpoint for top clients"""
    membership = WorkspaceMember.objects.filter(user=request.user).first()
    if not membership:
        return JsonResponse([], safe=False)
    
    workspace = membership.workspace
    
    top_clients = Client.objects.filter(
        workspace=workspace
    ).annotate(
        order_count=Count('orders'),
        total=Sum('orders__total_amount')
    ).order_by('-total')[:5]
    
    data = []
    for client in top_clients:
        data.append({
            'id': client.id,
            'name': client.full_name,
            'order_count': client.order_count or 0,
            'total': str(client.total or 0),
        })
    
    return JsonResponse(data, safe=False)

@login_required
def orders_chart_api(request):
    """API endpoint for orders chart data"""
    membership = WorkspaceMember.objects.filter(user=request.user).first()
    if not membership:
        return JsonResponse({'labels': [], 'values': []})
    
    workspace = membership.workspace
    
    # Get last 30 days order counts
    from django.utils import timezone
    from datetime import timedelta
    
    now = timezone.now()
    labels = []
    values = []
    
    for i in range(30):
        date = now - timedelta(days=i)
        labels.append(date.strftime('%d.%m'))
        count = Order.objects.filter(
            workspace=workspace,
            created_at__date=date.date()
        ).count()
        values.append(count)
    
    return JsonResponse({
        'labels': list(reversed(labels)),
        'values': list(reversed(values)),
    })

@login_required
def daily_ai_summary(request):
    """HTMX endpoint for daily AI summary"""
    membership = WorkspaceMember.objects.filter(user=request.user).first()
    if not membership:
        return render(request, 'ai_features/summary_partial.html', {'summary': None})
    
    workspace = membership.workspace
    
    # Get latest summary or generate placeholder
    summary = AISummary.objects.filter(
        workspace=workspace,
        summary_type='daily'
    ).order_by('-created_at').first()
    
    return render(request, 'ai_features/summary_partial.html', {'summary': summary})
