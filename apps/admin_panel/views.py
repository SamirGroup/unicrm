from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.contrib import messages
from django.db.models import Sum, Count, Q
from django.utils import timezone
from datetime import datetime, timedelta, date
from decimal import Decimal

from apps.accounts.models import User
from apps.workspaces.models import Workspace, WorkspaceMember, Module
from apps.clients.models import Client
from apps.orders.models import Order
from .models import SuperAdmin, Contract, PaymentLog, ModulePrice

# ==================== AUTHENTICATION ====================

def admin_login(request):
    """Super admin login page"""
    # Agar allaqachon kirgan bo'lsa, dashboardga yo'naltirish
    if request.session.get('is_super_admin'):
        return redirect('admin_panel:dashboard')
    
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        
        if not username or not password:
            messages.error(request, 'Login va parolni kiriting!')
            return render(request, 'admin_panel/login.html')
        
        try:
            admin = SuperAdmin.objects.get(username=username, is_active=True)
            if admin.check_password(password):
                request.session['is_super_admin'] = True
                request.session['admin_id'] = admin.id
                request.session['admin_username'] = admin.username
                messages.success(request, 'Xush kelibsiz, Admin!')
                return redirect('admin_panel:dashboard')
            else:
                messages.error(request, 'Noto\'g\'ri parol!')
        except SuperAdmin.DoesNotExist:
            messages.error(request, 'Bunday admin topilmadi!')
        except Exception as e:
            messages.error(request, f'Tizimda xatolik: {str(e)}')
    
    return render(request, 'admin_panel/login.html')

def admin_logout(request):
    """Super admin logout"""
    if request.method == 'POST':
        request.session.flush()
        messages.success(request, 'Tizimdan muvaffaqiyatli chiqdingiz!')
        return redirect('admin_panel:login')
    
    # GET so'rov uchun tasdiqlash sahifasi
    return render(request, 'admin_panel/logout.html')

def admin_required(view_func):
    """Decorator to check if user is super admin"""
    def wrapper(request, *args, **kwargs):
        if not request.session.get('is_super_admin'):
            messages.error(request, 'Iltimos, avval kiring!')
            return redirect('admin_panel:login')
        return view_func(request, *args, **kwargs)
    return wrapper

# ==================== DASHBOARD ====================

@admin_required
def dashboard(request):
    """Super admin dashboard with statistics"""
    
    # Umumiy statistika
    total_contracts = Contract.objects.count()
    active_contracts = Contract.objects.filter(status='active').count()
    pending_contracts = Contract.objects.filter(status='pending').count()
    expired_contracts = Contract.objects.filter(status='expired').count()
    suspended_contracts = Contract.objects.filter(status='suspended').count()
    
    total_users = User.objects.count()
    total_workspaces = Workspace.objects.count()
    total_clients = Client.objects.count()
    total_orders = Order.objects.count()
    
    # Tushum statistikasi
    today = date.today()
    
    # Kunlik tushum
    daily_revenue = PaymentLog.objects.filter(
        status='completed',
        payment_date__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Haftalik tushum
    week_start = today - timedelta(days=today.weekday())
    weekly_revenue = PaymentLog.objects.filter(
        status='completed',
        payment_date__date__gte=week_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Oylik tushum
    month_start = today.replace(day=1)
    monthly_revenue = PaymentLog.objects.filter(
        status='completed',
        payment_date__date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Jami tushum
    total_revenue = PaymentLog.objects.filter(
        status='completed'
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    # Qarzdorlik
    total_debt = Contract.objects.aggregate(total=Sum('total_debt'))['total'] or 0
    
    # So'nggi to'lovlar
    recent_payments = PaymentLog.objects.select_related('contract').order_by('-created_at')[:10]
    
    # So'nggi shartnomalar
    recent_contracts = Contract.objects.select_related('workspace', 'owner_user').order_by('-created_at')[:10]
    
    # Grafik ma'lumotlari - oxirgi 30 kun
    chart_labels = []
    chart_data = []
    for i in range(29, -1, -1):
        day = today - timedelta(days=i)
        chart_labels.append(day.strftime('%d.%m'))
        day_revenue = PaymentLog.objects.filter(
            status='completed',
            payment_date__date=day
        ).aggregate(total=Sum('amount'))['total'] or 0
        chart_data.append(float(day_revenue))
    
    context = {
        'total_contracts': total_contracts,
        'active_contracts': active_contracts,
        'pending_contracts': pending_contracts,
        'expired_contracts': expired_contracts,
        'suspended_contracts': suspended_contracts,
        'total_users': total_users,
        'total_workspaces': total_workspaces,
        'total_clients': total_clients,
        'total_orders': total_orders,
        'daily_revenue': daily_revenue,
        'weekly_revenue': weekly_revenue,
        'monthly_revenue': monthly_revenue,
        'total_revenue': total_revenue,
        'total_debt': total_debt,
        'recent_payments': recent_payments,
        'recent_contracts': recent_contracts,
        'chart_labels': chart_labels,
        'chart_data': chart_data,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/dashboard.html', context)

# ==================== CONTRACTS ====================

@admin_required
def contracts_list(request):
    """Barcha shartnomalar ro'yxati"""
    status_filter = request.GET.get('status', '')
    search = request.GET.get('search', '')
    
    contracts = Contract.objects.select_related('workspace', 'owner_user')
    
    if status_filter:
        contracts = contracts.filter(status=status_filter)
    
    if search:
        contracts = contracts.filter(
            Q(organization_name__icontains=search) |
            Q(contract_number__icontains=search) |
            Q(owner_user__username__icontains=search)
        )
    
    contracts = contracts.order_by('-created_at')
    
    context = {
        'contracts': contracts,
        'status_filter': status_filter,
        'search': search,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/contracts.html', context)

@admin_required
def contract_create(request):
    """Yangi shartnoma yaratish"""
    if request.method == 'POST':
        # Foydalanuvchi ma'lumotlari
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email', '')
        first_name = request.POST.get('first_name', '')
        last_name = request.POST.get('last_name', '')
        
        # Tashkilot ma'lumotlari
        org_name = request.POST.get('organization_name')
        workspace_name = request.POST.get('workspace_name', org_name)
        
        # Shartnoma ma'lumotlari
        contract_number = request.POST.get('contract_number')
        contract_date = request.POST.get('contract_date')
        start_date = request.POST.get('start_date')
        end_date = request.POST.get('end_date')
        monthly_fee = request.POST.get('monthly_fee', 0)
        
        # Modullar
        allowed_modules = request.POST.getlist('modules')
        
        try:
            # 1. Foydalanuvchi yaratish
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                first_name=first_name,
                last_name=last_name,
                is_owner=True
            )
            
            # 2. Workspace yaratish
            from django.utils.text import slugify
            workspace = Workspace.objects.create(
                name=workspace_name,
                slug=slugify(workspace_name) + '-' + str(user.id),
                owner=user,
                plan='business',
                status='active'
            )
            
            # 3. Workspace member yaratish
            WorkspaceMember.objects.create(
                workspace=workspace,
                user=user,
                role='owner'
            )
            
            # 4. Default modullar
            default_modules = ['orders', 'clients', 'products']
            for mod_type in default_modules:
                Module.objects.create(
                    workspace=workspace,
                    module_type=mod_type,
                    is_enabled=mod_type in allowed_modules
                )
            
            # 5. Shartnoma yaratish
            contract = Contract.objects.create(
                organization_name=org_name,
                workspace=workspace,
                owner_user=user,
                contract_number=contract_number,
                contract_date=contract_date,
                start_date=start_date,
                end_date=end_date,
                monthly_fee=monthly_fee,
                status='active',
                allowed_modules=allowed_modules
            )
            
            messages.success(request, f'Shartnoma {contract_number} muvaffaqiyatli yaratildi!')
            return redirect('admin_panel:contracts')
            
        except Exception as e:
            messages.error(request, f'Xatolik yuz berdi: {str(e)}')
    
    # Mavjud modullar
    available_modules = [
        {'type': 'orders', 'name': 'Buyurtmalar', 'price': 50000},
        {'type': 'clients', 'name': 'Mijozlar', 'price': 50000},
        {'type': 'products', 'name': 'Mahsulotlar', 'price': 30000},
        {'type': 'invoices', 'name': 'Hisob-fakturalar', 'price': 40000},
        {'type': 'tasks', 'name': 'Vazifalar', 'price': 30000},
        {'type': 'calendar', 'name': 'Kalendar', 'price': 20000},
        {'type': 'reports', 'name': 'Hisobotlar', 'price': 50000},
    ]
    
    context = {
        'available_modules': available_modules,
        'today': date.today().isoformat(),
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/contract_form.html', context)

@admin_required
def contract_detail(request, pk):
    """Shartnoma detallari"""
    contract = get_object_or_404(Contract, pk=pk)
    payments = contract.payments.order_by('-created_at')
    
    context = {
        'contract': contract,
        'payments': payments,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/contract_detail.html', context)

@admin_required
def contract_edit(request, pk):
    """Shartnomani tahrirlash"""
    contract = get_object_or_404(Contract, pk=pk)
    
    if request.method == 'POST':
        contract.organization_name = request.POST.get('organization_name')
        contract.contract_number = request.POST.get('contract_number')
        contract.contract_date = request.POST.get('contract_date')
        contract.start_date = request.POST.get('start_date')
        contract.end_date = request.POST.get('end_date')
        contract.monthly_fee = request.POST.get('monthly_fee', 0)
        contract.status = request.POST.get('status')
        contract.allowed_modules = request.POST.getlist('modules')
        contract.notes = request.POST.get('notes', '')
        contract.save()
        
        messages.success(request, 'Shartnoma yangilandi!')
        return redirect('admin_panel:contract_detail', pk=pk)
    
    available_modules = [
        {'type': 'orders', 'name': 'Buyurtmalar'},
        {'type': 'clients', 'name': 'Mijozlar'},
        {'type': 'products', 'name': 'Mahsulotlar'},
        {'type': 'invoices', 'name': 'Hisob-fakturalar'},
        {'type': 'tasks', 'name': 'Vazifalar'},
        {'type': 'calendar', 'name': 'Kalendar'},
        {'type': 'reports', 'name': 'Hisobotlar'},
    ]
    
    context = {
        'contract': contract,
        'available_modules': available_modules,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/contract_edit.html', context)

# ==================== PAYMENTS ====================

@admin_required
def payments_list(request):
    """Barcha to'lovlar ro'yxati"""
    status_filter = request.GET.get('status', '')
    
    payments = PaymentLog.objects.select_related('contract').order_by('-created_at')
    
    if status_filter:
        payments = payments.filter(status=status_filter)
    
    # Tushumlar statistikasi
    today = date.today()
    
    daily_revenue = PaymentLog.objects.filter(
        status='completed',
        payment_date__date=today
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    week_start = today - timedelta(days=today.weekday())
    weekly_revenue = PaymentLog.objects.filter(
        status='completed',
        payment_date__date__gte=week_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    month_start = today.replace(day=1)
    monthly_revenue = PaymentLog.objects.filter(
        status='completed',
        payment_date__date__gte=month_start
    ).aggregate(total=Sum('amount'))['total'] or 0
    
    context = {
        'payments': payments,
        'status_filter': status_filter,
        'daily_revenue': daily_revenue,
        'weekly_revenue': weekly_revenue,
        'monthly_revenue': monthly_revenue,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/payments.html', context)

@admin_required
def payment_add(request, contract_id):
    """Yangi to'lov qo'shish"""
    contract = get_object_or_404(Contract, pk=contract_id)
    
    if request.method == 'POST':
        amount = request.POST.get('amount')
        payment_method = request.POST.get('payment_method')
        period_start = request.POST.get('period_start')
        period_end = request.POST.get('period_end')
        notes = request.POST.get('notes', '')
        
        payment = PaymentLog.objects.create(
            contract=contract,
            amount=amount,
            payment_method=payment_method,
            status='completed',
            payment_date=timezone.now(),
            period_start=period_start,
            period_end=period_end,
            notes=notes
        )
    
        # Shartnoma to'lovlarini yangilash
        contract.total_paid = Decimal(contract.total_paid) + Decimal(amount)
        contract.total_debt = max(0, Decimal(contract.total_debt) - Decimal(amount))
        
        # Agar qarzdorlik 0 bo'lsa, statusni active qilish
        if contract.total_debt <= 0:
            contract.status = 'active'
            if contract.workspace:
                contract.workspace.status = 'active'
                contract.workspace.save()
        
        contract.save()
        
        messages.success(request, 'To\'lov muvaffaqiyatli qo\'shildi!')
        return redirect('admin_panel:payments')
    
    context = {
        'contract': contract,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/payment_form.html', context)

# ==================== USERS ====================

@admin_required
def users_list(request):
    """Barcha foydalanuvchilar ro'yxati"""
    search = request.GET.get('search', '')
    
    users = User.objects.all().order_by('-date_joined')
    
    if search:
        users = users.filter(
            Q(username__icontains=search) |
            Q(email__icontains=search) |
            Q(first_name__icontains=search) |
            Q(last_name__icontains=search)
        )
    
    context = {
        'users': users,
        'search': search,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/users.html', context)

@admin_required
def user_detail(request, pk):
    """Foydalanuvchi detallari"""
    user = get_object_or_404(User, pk=pk)
    workspaces = Workspace.objects.filter(owner=user)
    contract = Contract.objects.filter(owner_user=user).first()
    
    context = {
        'user_obj': user,
        'workspaces': workspaces,
        'contract': contract,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/user_detail.html', context)

# ==================== MODULES ====================

@admin_required
def modules_list(request):
    """Modullar ro'yxati va narxlari"""
    modules = ModulePrice.objects.all().order_by('category', 'name')
    
    # Kategoriyalar bo'yicha guruhlash
    from collections import defaultdict
    modules_by_category = defaultdict(list)
    for mod in modules:
        modules_by_category[mod.get_category_display()].append(mod)
    
    context = {
        'modules': modules,
        'modules_by_category': dict(modules_by_category),
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/modules.html', context)

@admin_required
def module_edit(request, pk):
    """Modul narxini tahrirlash"""
    module = get_object_or_404(ModulePrice, pk=pk)
    
    if request.method == 'POST':
        module.name = request.POST.get('name')
        module.price = request.POST.get('price')
        module.description = request.POST.get('description')
        module.is_active = request.POST.get('is_active') == 'on'
        module.save()
        
        messages.success(request, 'Modul yangilandi!')
        return redirect('admin_panel:modules')
    
    context = {
        'module': module,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/module_form.html', context)

# ==================== PROFILE ====================

@admin_required
def profile(request):
    """Super admin profili"""
    admin = get_object_or_404(SuperAdmin, pk=request.session.get('admin_id'))
    
    if request.method == 'POST':
        admin.full_name = request.POST.get('full_name', '')
        admin.email = request.POST.get('email', '')
        admin.phone = request.POST.get('phone', '')
        
        # Parolni o'zgartirish
        current_password = request.POST.get('current_password')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')
        
        if current_password and new_password:
            if admin.check_password(current_password):
                if new_password == confirm_password:
                    admin.set_password(new_password)
                    messages.success(request, 'Parol muvaffaqiyatli o\'zgartirildi!')
                else:
                    messages.error(request, 'Yangi parollar mos kelmadi!')
            else:
                messages.error(request, 'Joriy parol noto\'g\'ri!')
        
        admin.save()
        messages.success(request, 'Profil yangilandi!')
        return redirect('admin_panel:profile')
    
    context = {
        'admin': admin,
        'admin_username': request.session.get('admin_username'),
    }
    
    return render(request, 'admin_panel/profile.html', context)

# ==================== AUTO CHECK ====================

def auto_check_contracts():
    """Shartnomalarni avtomatik tekshirish - Cron job yoki Celery bilan chaqiriladi"""
    today = date.today()
    
    # Muddati tugagan shartnomalar
    expired = Contract.objects.filter(end_date__lt=today, status='active')
    for contract in expired:
        contract.status = 'expired'
        contract.save()
        
        if contract.workspace:
            contract.workspace.status = 'expired'
            contract.workspace.save()
    
    # 3 kundan keyin tugaydigan shartnomalar
    expiring_soon = Contract.objects.filter(
        end_date__gte=today,
        end_date__lte=today + timedelta(days=3),
        status='active'
    )
    for contract in expiring_soon:
        # To'lov eslatmasi yaratish
        PaymentLog.objects.create(
            contract=contract,
            amount=contract.monthly_fee,
            status='pending',
            period_start=today,
            period_end=contract.end_date,
            notes='Avtomatik yaratilgan - abonent to\'lovi'
        )
    
    # To'lov qilmaganlar (7 kunlik grace period)
    pending_payments = PaymentLog.objects.filter(
        status='pending',
        created_at__lte=timezone.now() - timedelta(days=7)
    )
    for payment in pending_payments:
        payment.contract.status = 'suspended'
        payment.contract.save()
        if payment.contract.workspace:
            payment.contract.workspace.status = 'suspended'
            payment.contract.workspace.save()
