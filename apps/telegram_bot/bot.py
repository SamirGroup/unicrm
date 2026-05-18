#!/usr/bin/env python
"""
UniCRM AI Telegram Bot
Main bot handler with commands and callbacks
"""

import json
import logging
from telegram import Update, WebAppInfo, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from django.conf import settings
from apps.accounts.models import User
from apps.workspaces.models import Workspace, WorkspaceMember
from apps.clients.models import Client
from apps.orders.models import Order

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.app = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        self.setup_handlers()
    
    def setup_handlers(self):
        """Setup all bot handlers"""
        # Commands
        self.app.add_handler(CommandHandler("start", self.start_command))
        self.app.add_handler(CommandHandler("dashboard", self.dashboard_command))
        self.app.add_handler(CommandHandler("clients", self.clients_command))
        self.app.add_handler(CommandHandler("orders", self.orders_command))
        self.app.add_handler(CommandHandler("help", self.help_command))
        
        # Callback queries
        self.app.add_handler(CallbackQueryHandler(self.button_callback))
        
        # Text messages
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.message_handler))
    
    async def start_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /start command"""
        user = update.effective_user
        
        if not user:
            return
        
        telegram_id = user.id
        
        # Check if user exists
        try:
            db_user = User.objects.get(telegram_id=telegram_id)
            memberships = WorkspaceMember.objects.filter(user=db_user).select_related('workspace')
            
            if memberships.exists():
                # Show workspace selection
                keyboard = []
                for membership in memberships:
                    ws = membership.workspace
                    keyboard.append([
                        InlineKeyboardButton(
                            f"📊 {ws.name}",
                            callback_data=f"workspace_{ws.id}"
                        )
                    ])
                
                keyboard.append([
                    InlineKeyboardButton(
                        "➕ Yangi Workspace",
                        callback_data="new_workspace"
                    )
                ])
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                
                await update.message.reply_text(
                    f"👋 Salom, {user.first_name or user.username}!\n\n"
                    f"UniCRM AI ga xush kelibsiz.\n\n"
                    f"Quyidagi workspace'lardan birini tanlang:",
                    reply_markup=reply_markup
                )
            else:
                # No workspaces - guide to create
                await update.message.reply_text(
                    f"👋 Salom, {user.first_name or user.username}!\n\n"
                    f"UniCRM AI ga xush kelibsiz!\n\n"
                    f"🚀 Boshlash uchun quyidagi buyruqlardan birini bosing:\n\n"
                    f"/workspace - Yangi workspace yaratish\n"
                    f"/help - Yordam",
                    reply_markup=InlineKeyboardMarkup([[
                        InlineKeyboardButton("➕ Workspace Yaratish", callback_data="new_workspace")
                    ]])
                )
                
        except User.DoesNotExist:
            # New user - register
            await self.register_user(update, context)
    
    async def register_user(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Register new Telegram user"""
        user = update.effective_user
        
        db_user = User.objects.create_user(
            username=f"tg_{user.id}",
            telegram_id=user.id,
            telegram_username=user.username or '',
            first_name=user.first_name or '',
            last_name=user.last_name or '',
            is_active=True
        )
        
        await update.message.reply_text(
            f"✅ Siz muvaffaqiyatli ro'yxatdan o'tdingiz, {user.first_name or 'do'stim'}!\n\n"
            f"Endi /workspace buyrug'i bilan workspace yarating yoki /start ni bosing.",
            parse_mode='Markdown'
        )
    
    async def dashboard_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /dashboard command"""
        user = update.effective_user
        telegram_id = user.id
        
        try:
            db_user = User.objects.get(telegram_id=telegram_id)
            membership = WorkspaceMember.objects.filter(user=db_user).first()
            
            if not membership:
                await update.message.reply_text(
                    "❌ Sizda workspace yo'q.\n\n"
                    "Iltimos, avval /workspace buyrug'i bilan workspace yarating.",
                    parse_mode='Markdown'
                )
                return
            
            workspace = membership.workspace
            
            # Get stats
            total_clients = Client.objects.filter(workspace=workspace).count()
            total_orders = Order.objects.filter(workspace=workspace).count()
            pending_orders = Order.objects.filter(workspace=workspace, status='pending').count()
            
            # Get recent orders
            recent_orders = Order.objects.filter(workspace=workspace).order_by('-created_at')[:5]
            
            message = f"📊 *Dashboard - {workspace.name}*\n\n"
            message += f"👥 Mijozlar: *{total_clients}*\n"
            message += f"🛒 Buyurtmalar: *{total_orders}*\n"
            message += f"⏳ Kutilayotgan: *{pending_orders}*\n\n"
            
            if recent_orders:
                message += f"📦 *So'nggi buyurtmalar:*\n"
                for order in recent_orders:
                    client_name = order.client.full_name if order.client else 'Noma\'lum'
                    message += f"• #{order.order_number} - {client_name}\n"
                    message += f"  Status: {order.status}\n"
            
            # WebApp button
            webapp_url = f"{settings.BASE_URL}/telegram/miniapp/?workspace_id={workspace.id}&user_id={telegram_id}"
            keyboard = [[
                InlineKeyboardButton(
                    "🚀 To'liq versiyani ochish",
                    web_app=WebAppInfo(url=webapp_url)
                )
            ]]
            
            await update.message.reply_text(
                message,
                reply_markup=InlineKeyboardMarkup(keyboard),
                parse_mode='Markdown'
            )
            
        except User.DoesNotExist:
            await update.message.reply_text("❌ Foydalanuvchi topilmadi. Iltimos, /start ni bosing.")
    
    async def clients_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /clients command"""
        user = update.effective_user
        telegram_id = user.id
        
        try:
            db_user = User.objects.get(telegram_id=telegram_id)
            membership = WorkspaceMember.objects.filter(user=db_user).first()
            
            if not membership:
                await update.message.reply_text("❌ Workspace topilmadi.")
                return
            
            workspace = membership.workspace
            clients = Client.objects.filter(workspace=workspace).order_by('-created_at')[:10]
            
            if not clients:
                await update.message.reply_text(
                    "📭 Hozircha mijozlar yo'q.\n\n"
                    "To'liq versiyada mijoz qo'shishingiz mumkin.",
                    parse_mode='Markdown'
                )
                return
            
            message = f"👥 *Mijozlar - {workspace.name}*\n\n"
            for i, client in enumerate(clients, 1):
                message += f"{i}. {client.full_name}\n"
                if client.phone:
                    message += f"   📱 {client.phone}\n"
                if client.email:
                    message += f"   ✉️ {client.email}\n"
                message += "\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except User.DoesNotExist:
            await update.message.reply_text("❌ Foydalanuvchi topilmadi.")
    
    async def orders_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /orders command"""
        user = update.effective_user
        telegram_id = user.id
        
        try:
            db_user = User.objects.get(telegram_id=telegram_id)
            membership = WorkspaceMember.objects.filter(user=db_user).first()
            
            if not membership:
                await update.message.reply_text("❌ Workspace topilmadi.")
                return
            
            workspace = membership.workspace
            orders = Order.objects.filter(workspace=workspace).order_by('-created_at')[:10]
            
            if not orders:
                await update.message.reply_text("📭 Hozircha buyurtmalar yo'q.")
                return
            
            message = f"🛒 *Buyurtmalar - {workspace.name}*\n\n"
            for order in orders:
                client_name = order.client.full_name if order.client else 'Noma\'lum'
                message += f"📦 *#{order.order_number}*\n"
                message += f"👤 {client_name}\n"
                message += f"💰 {order.total_amount} so'm\n"
                message += f"📊 {order.status}\n\n"
            
            await update.message.reply_text(message, parse_mode='Markdown')
            
        except User.DoesNotExist:
            await update.message.reply_text("❌ Foydalanuvchi topilmadi.")
    
    async def help_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /help command"""
        help_text = """
🤖 *UniCRM AI - Yordam*

*Asosiy buyruqlar:*
/start - Boshlash / Workspace tanlash
/dashboard - Dashboard ko'rish
/clients - Mijozlar ro'yxati
/orders - Buyurtmalar ro'yxati
/workspace - Workspace boshqaruv
/help - Bu yordam

*WebApp:*
Tugmalarni bosib to'liq versiyani ochishingiz mumkin.

🌐 *Support:* nlp-core-team
        """
        
        await update.message.reply_text(help_text, parse_mode='Markdown')
    
    async def workspace_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle /workspace command"""
        user = update.effective_user
        
        keyboard = InlineKeyboardMarkup([[
            InlineKeyboardButton("➕ Yangi Workspace", callback_data="new_workspace")
        ]])
        
        await update.message.reply_text(
            "🏢 *Workspace Boshqaruv*\n\n"
            "Yangi workspace yaratish uchun quyidagi tugmani bosing:",
            reply_markup=keyboard,
            parse_mode='Markdown'
        )
    
    async def button_callback(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle inline button callbacks"""
        query = update.callback_query
        await query.answer()
        
        data = query.data
        
        if data == "new_workspace":
            await query.edit_message_text(
                "🏢 *Yangi Workspace Yaratish*\n\n"
                "Workspace nomini kiriting:\n"
                "(Masalan: 'Mening Restoran' yoki 'ABC Company')",
                parse_mode='Markdown'
            )
            context.user_data['awaiting_workspace_name'] = True
        
        elif data.startswith("workspace_"):
            workspace_id = data.split("_")[1]
            context.user_data['active_workspace'] = workspace_id
            
            try:
                workspace = Workspace.objects.get(id=workspace_id)
                await query.edit_message_text(
                    f"✅ *{workspace.name}* tanlandi!\n\n"
                    f"Endi /dashboard buyrug'i bilan boshqaruv paneliga o'ting.",
                    parse_mode='Markdown'
                )
            except Workspace.DoesNotExist:
                await query.edit_message_text("❌ Workspace topilmadi.")
    
    async def message_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle text messages"""
        user = update.effective_user
        
        # Check if awaiting workspace name
        if context.user_data.get('awaiting_workspace_name'):
            workspace_name = update.message.text.strip()
            
            if len(workspace_name) < 3:
                await update.message.reply_text(
                    "❌ Workspace nomi juda qisqa.\n"
                    "Iltimos, kamida 3 ta harf kiriting.",
                    parse_mode='Markdown'
                )
                return
            
            from django.utils.text import slugify
            
            # Create workspace
            db_user = User.objects.get(telegram_id=user.id)
            workspace = Workspace.objects.create(
                name=workspace_name,
                slug=slugify(workspace_name) + '-' + str(db_user.id),
                owner=db_user
            )
            
            # Create membership
            WorkspaceMember.objects.create(
                workspace=workspace,
                user=db_user,
                role='owner'
            )
            
            # Create default modules
            from apps.modules.models import Module
            Module.objects.bulk_create([
                Module(workspace=workspace, module_type='orders', is_enabled=True),
                Module(workspace=workspace, module_type='clients', is_enabled=True),
                Module(workspace=workspace, module_type='products', is_enabled=True),
            ])
            
            context.user_data['active_workspace'] = workspace.id
            del context.user_data['awaiting_workspace_name']
            
            await update.message.reply_text(
                f"✅ *{workspace_name}* muvaffaqiyatli yaratildi!\n\n"
                f"🎉 UniCRM AI ga xush kelibsiz!\n\n"
                f"Endi /dashboard buyrug'i bilan boshqaruv paneliga o'ting.",
                parse_mode='Markdown'
            )
            return
        
        # Default response
        await update.message.reply_text(
            "❓ Nima qilishni xohlaysiz?\n\n"
            "Foydalanish uchun /help buyrug'ini bosing."
        )
    
    def run(self):
        """Start the bot"""
        logger.info("Starting Telegram Bot...")
        self.app.run_polling(allowed_updates=Update.ALL_TYPES)

# Initialize bot instance
telegram_bot = TelegramBot()

if __name__ == '__main__':
    telegram_bot.run()
