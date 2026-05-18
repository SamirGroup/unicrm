from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.utils.text import slugify
from django.contrib import messages
from .models import Workspace, WorkspaceMember, Module
from apps.admin_panel.models import ModulePrice, Contract

@login_required
def index(request):
    """Workspace list view"""
    workspaces = WorkspaceMember.objects.filter(user=request.user).select_related('workspace')
    return render(request, 'workspaces/index.html', {'memberships': workspaces})

@login_required
def create(request):
    """Create new workspace with module selection"""
    # Barcha mavjud modullarni olish
    available_modules = ModulePrice.objects.filter(is_active=True).order_by('category', 'name')
    
    if request.method == 'POST':
        name = request.POST.get('name')
        selected_modules = request.POST.getlist('modules')  # Tanlangan modullar
        
        if name:
            with transaction.atomic():
                # Workspace yaratish
                workspace = Workspace.objects.create(
                    name=name,
                    slug=slugify(name) + '-' + str(request.user.id),
                    owner=request.user,
                    plan='business',
                    status='active'
                )
                
                # Owner qo'shish
                WorkspaceMember.objects.create(
                    workspace=workspace,
                    user=request.user,
                    role='owner'
                )
                
                # Tanlangan modullarni yaratish
                default_modules = ['orders', 'clients', 'products']
                all_modules = list(set(default_modules + selected_modules))
                
                for mod_type in all_modules:
                    Module.objects.create(
                        workspace=workspace,
                        module_type=mod_type,
                        is_enabled=True
                    )
                
                # Agar shartnoma mavjud bo'lsa, modullarni yangilash
                try:
                    contract = Contract.objects.get(workspace=workspace)
                    contract.allowed_modules = all_modules
                    contract.recalculate_monthly_fee()
                    messages.success(request, f'Workspace yaratildi! Oylik to\'lov: {contract.monthly_fee} so\'m')
                except Contract.DoesNotExist:
                    # Agar shartnoma yo'q bo'lsa, shartnoma yaratish (admin panel orqali)
                    messages.success(request, 'Workspace muvaffaqiyatli yaratildi!')
                
            return redirect('/workspace/')
    
    # Modullarni kategoriyalar bo'yicha guruhlash
    from collections import defaultdict
    modules_by_category = defaultdict(list)
    for mod in available_modules:
        modules_by_category[mod.get_category_display()].append(mod)
    
    context = {
        'modules_by_category': dict(modules_by_category),
        'available_modules': available_modules,
    }
    
    return render(request, 'workspaces/create.html', context)

@login_required
def settings(request, workspace_slug):
    """Workspace settings view"""
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    membership = WorkspaceMember.objects.filter(workspace=workspace, user=request.user).first()
    
    if not membership:
        return redirect('/workspace/')
    
    return render(request, 'workspaces/settings.html', {'workspace': workspace, 'membership': membership})

@login_required
def members(request, workspace_slug):
    """Workspace members view"""
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    memberships = WorkspaceMember.objects.filter(workspace=workspace).select_related('user')
    
    return render(request, 'workspaces/members.html', {'workspace': workspace, 'memberships': memberships})

@login_required
def modules(request, workspace_slug):
    """Workspace modules view"""
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    modules = Module.objects.filter(workspace=workspace)
    
    return render(request, 'workspaces/modules.html', {'workspace': workspace, 'modules': modules})

@require_http_methods(['POST'])
@login_required
def toggle_module(request, workspace_slug, module_type):
    """Toggle module enable/disable"""
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    module = get_object_or_404(Module, workspace=workspace, module_type=module_type)
    
    module.is_enabled = not module.is_enabled
    module.save()
    
    return JsonResponse({'success': True, 'is_enabled': module.is_enabled})
