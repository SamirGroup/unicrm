from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Order

@login_required
def list(request, workspace_slug):
    """Order list view"""
    from apps.workspaces.models import Workspace
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    orders = Order.objects.filter(workspace=workspace).order_by('-created_at')
    return render(request, 'orders/list.html', {'workspace': workspace, 'orders': orders})

@login_required
def detail(request, workspace_slug, pk):
    """Order detail view"""
    from apps.workspaces.models import Workspace
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    order = get_object_or_404(Order, pk=pk, workspace=workspace)
    return render(request, 'orders/detail.html', {'workspace': workspace, 'order': order})
