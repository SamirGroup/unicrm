from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.db import models
from datetime import datetime
from apps.workspaces.models import Workspace, WorkspaceMember
from apps.clients.models import Client
from apps.orders.models import Order
from apps.ai_features.models import AISummary

@login_required
def reports(request):
    """AI Reports view"""
    membership = WorkspaceMember.objects.filter(user=request.user).first()
    workspace = membership.workspace if membership else None
    
    context = {
        'workspace': workspace,
    }
    return render(request, 'ai_features/reports.html', context)

@login_required
def generate_daily_summary(request, workspace_slug):
    """Generate daily AI summary (Demo version)"""
    from apps.workspaces.models import Workspace
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    
    # Get stats
    total_clients = Client.objects.filter(workspace=workspace).count()
    total_orders = Order.objects.filter(workspace=workspace).count()
    today_orders = Order.objects.filter(
        workspace=workspace,
        created_at__date=datetime.now().date()
    ).count()
    today_revenue = Order.objects.filter(
        workspace=workspace,
        created_at__date=datetime.now().date()
    ).aggregate(total=models.Sum('total_amount'))['total'] or 0
    
    # Generate demo AI summary
    summary_content = f"""🤖 **AI Kunlik Hisobot**

📊 **Umumiy Ko'rsatkichlar:**
• Jami mijozlar: {total_clients}
• Jami buyurtmalar: {total_orders}

📅 **Bugungi Statistikasi:**
• Bugungi buyurtmalar: {today_orders}
• Bugungi tushum: {today_revenue} so'm

💡 **AI Tavsiyalari:**
1. Mijozlar bazangiz o'smoqda, tabriklaymiz!
2. Buyurtmalar sonini oshirish uchun marketing kampaniyasini boshlang
3. Telegram bot orqali mijozlar bilan aloqani kuchaytiring

⚡ **Keyingi Qadamlar:**
• Yangi mijozlar qo'shing
• Buyurtmalarni kuzatib boring
• Hisobotlarni tahlil qiling

*Bu demo versiya. To'liq AI xususiyatlar OpenAI API ulangandan keyin ishlaydi.*"""
    
    # Save summary
    summary = AISummary.objects.create(
        workspace=workspace,
        summary_type='daily',
        content=summary_content
    )
    
    return render(request, 'ai_features/summary_partial.html', {'summary': summary})

@login_required
def generate_client_insights(request, workspace_slug, client_id):
    """Generate AI insights for specific client (Demo)"""
    from apps.workspaces.models import Workspace
    workspace = get_object_or_404(Workspace, slug=workspace_slug)
    client = get_object_or_404(Client, pk=client_id, workspace=workspace)
    
    order_count = client.orders.count()
    total_spent = client.orders.aggregate(total=models.Sum('total_amount'))['total'] or 0
    
    insights = f"""🤖 **AI Mijoz Tahlili**

👤 **{client.full_name}**

📈 **Faoliyat:**
• Buyurtmalar soni: {order_count}
• Jami xarajat: {total_spent} so'm
• Manbasi: {client.get_source_display}

💡 **Tavsiyalar:**
1. {client.full_name} sizning faol mijozingiz
2. Maxsus takliflar yuboring
3. Doimiy mijoz dasturiga qo'shing

*Bu demo versiya.*"""
    
    return JsonResponse({'insights': insights})
