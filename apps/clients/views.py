from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from .models import Client

@login_required
def list(request, workspace_slug):
    """Client list view"""
    from apps.workspaces.models import Workspace
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    clients = Client.objects.filter(workspace=workspace).order_by('-created_at')
    return render(request, 'clients/list.html', {'workspace': workspace, 'clients': clients})

@login_required
def detail(request, workspace_slug, pk):
    """Client detail view"""
    from apps.workspaces.models import Workspace
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    client = get_object_or_404(Client, pk=pk, workspace=workspace)
    return render(request, 'clients/detail.html', {'workspace': workspace, 'client': client})
