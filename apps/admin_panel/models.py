from django.db import models
from django.contrib.auth.hashers import make_password, check_password
from apps.accounts.models import User
from apps.workspaces.models import Workspace

class SuperAdmin(models.Model):
    """Super Admin - tizim egasi"""
    username = models.CharField(max_length=150, unique=True)
    password_hash = models.CharField(max_length=255)
    email = models.EmailField(blank=True)
    full_name = models.CharField(max_length=255, blank=True)
    phone = models.CharField(max_length=50, blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def set_password(self, password):
        self.password_hash = make_password(password)
    
    def check_password(self, password):
        return check_password(password, self.password_hash)
    
    def __str__(self):
        return self.username

class Contract(models.Model):
    """Shartnoma - tashkilot bilan tuzilgan kelishuv"""
    STATUS_CHOICES = [
        ('active', 'Faol'),
        ('pending', 'Kutilmoqda'),
        ('expired', 'Muddati tugagan'),
        ('suspended', 'To\'xtatilgan'),
    ]
    
    organization_name = models.CharField(max_length=255)
    workspace = models.OneToOneField(Workspace, on_delete=models.CASCADE, related_name='contract', null=True, blank=True)
    owner_user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='contract', null=True, blank=True)
    
    # Shartnoma ma'lumotlari
    contract_number = models.CharField(max_length=100, unique=True)
    contract_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField()
    
    # To'lov ma'lumotlari
    base_monthly_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0, 
                                            help_text="Asosiy oylik to'lov (modullarsiz)")
    modules_monthly_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0,
                                               help_text="Modullar uchun qo'shimcha to'lov")
    monthly_fee = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_paid = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    total_debt = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    # Status
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    is_auto_renew = models.BooleanField(default=True)
    
    # Modullar - JSONField ichida saqlanadi
    allowed_modules = models.JSONField(default=list, help_text="Ruxsat etilgan modullar ro'yxati")
    
    # Qo'shimcha
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.contract_number} - {self.organization_name}"
    
    def recalculate_monthly_fee(self):
        """Modullar bo'yicha oylik to'lovni qayta hisoblash"""
        from decimal import Decimal
        modules_total = Decimal('0')
        
        for mt in self.allowed_modules:
            try:
                mp = ModulePrice.objects.get(module_type=mt, is_active=True)
                modules_total += mp.price
            except ModulePrice.DoesNotExist:
                pass
        
        self.modules_monthly_fee = modules_total
        self.monthly_fee = self.base_monthly_fee + modules_total
        self.save(update_fields=['modules_monthly_fee', 'monthly_fee'])
    
    def get_modules_detail(self):
        """Modullar tafsilotlarini qaytarish"""
        from decimal import Decimal
        modules = []
        total = Decimal('0')
        
        for mt in self.allowed_modules:
            try:
                mp = ModulePrice.objects.get(module_type=mt)
                modules.append({
                    'type': mt,
                    'name': mp.name,
                    'category': mp.category,
                    'price': mp.price,
                    'icon': mp.icon,
                    'is_active': mp.is_active,
                })
                total += mp.price
            except ModulePrice.DoesNotExist:
                modules.append({
                    'type': mt,
                    'name': mt.replace('_', ' ').title(),
                    'category': 'unknown',
                    'price': 0,
                    'icon': 'puzzle-piece',
                    'is_active': False,
                })
        
        return {
            'modules': modules,
            'total': total,
            'base_fee': self.base_monthly_fee,
            'grand_total': self.monthly_fee,
        }
    
    class Meta:
        ordering = ['-created_at']

class PaymentLog(models.Model):
    """To'lovlar tarixi"""
    STATUS_CHOICES = [
        ('pending', 'Kutilmoqda'),
        ('completed', 'Amalga oshirilgan'),
        ('failed', 'Muvaffaqiyatsiz'),
        ('refunded', 'Qaytarilgan'),
    ]
    
    contract = models.ForeignKey(Contract, on_delete=models.CASCADE, related_name='payments')
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    payment_method = models.CharField(max_length=50, blank=True)
    transaction_id = models.CharField(max_length=255, blank=True)
    payment_date = models.DateTimeField(null=True, blank=True)
    period_start = models.DateField()
    period_end = models.DateField()
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.contract.organization_name} - {self.amount} UZS"
    
    class Meta:
        ordering = ['-created_at']

class ModulePrice(models.Model):
    """Modul narxlari"""
    """Modul narxlari - dinamik modul boshqaruvi"""
    CATEGORY_CHOICES = [
        ('basic', 'Asosiy'),
        ('hr', 'HR Bo\'limi'),
        ('sales', 'Sotuv'),
        ('production', 'Ishlab Chiqarish'),
        ('accounting', 'Buxgalteriya'),
        ('extra', 'Qo\'shimcha'),
    ]
    
    module_type = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='basic')
    price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)
    is_premium = models.BooleanField(default=False)
    icon = models.CharField(max_length=50, default='puzzle-piece', help_text='FontAwesome icon nomi')
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.price} UZS"

    class Meta:
        ordering = ['category', 'name']
