# UniCRM AI - To'lov Tizimi (Subscription System)

## 📋 Umumiy Ma'lumot

Bu tizim workspace'larni ijaraga berish va avtomatik to'lovni boshqarish uchun mo'ljallangan.

## 🎯 Asosiy Funksiyalar

### 1. **Shartnoma Tuzish**
- Admin foydalanuvchiga login/parol beradi
- Foydalanuvchi ro'yxatdan o'tadi
- Workspace yaratadi yoki mavjud workspace'ga ulanadi

### 2. **Abonent To'lovi**
- Oylik yoki yillik to'lov
- Avtomatik to'lov eslatmalari
- To'lov amalga oshirilganda avtomatik uzaytirish

### 3. **To'lov Tugaganda**
- Avtomatik suspenziya (to'xtatib turish)
- Ma'lumotlar saqlanadi
- To'lov qilingandan keyin avtomatik tiklanadi

### 4. **Ma'lumotlarni Saqlash**
- To'lov tugasa ham barcha ma'lumotlar saqlanadi
- Workspace suspenzda bo'lsa ham o'qish mumkin (o'zgartirish yo'q)
- To'lov qilingandan keyin to'liq tiklanadi

## 🏗️ Arxitektura

### Modellar

#### 1. SubscriptionPlan (Obuna Plani)
```python
SubscriptionPlan:
├── name (Plani nomi)
├── slug (URL uchun)
├── price (Narxi)
├── duration_days (Muddat kun)
├── features (Imkoniyatlar)
└── is_active (Faolmi)
```

**Misol Plani:**
- **Basic** - 50,000 UZS/oy
- **Pro** - 150,000 UZS/oy
- **Enterprise** - 300,000 UZS/oy

#### 2. Subscription (Abonament)
```python
Subscription:
├── workspace (Workspace)
├── plan (Plan)
├── status (active/expired/pending/suspended)
├── start_date (Boshlanish)
├── end_date (Tugash)
└── auto_renew (Avtomatik yangilash)
```

#### 3. Payment (To'lov)
```python
Payment:
├── subscription (Abonament)
├── amount (Summa)
├── method (click/payme/cash/card)
├── status (pending/completed/failed)
├── transaction_id (Tranzaksiya ID)
└── payment_date (To'lov sanasi)
```

#### 4. PaymentReminder (Eslatma)
```python
PaymentReminder:
├── subscription (Abonament)
├── message (Xabar)
├── sent_at (Yuborilgan)
└── is_sent (Yuborilganmi)
```

## 🔄 Ish Jarayoni

### 1. Yangi Foydalanuvchi

```
1. Admin shartnoma tuzadi
2. Login/parol beradi
3. Foydalanuvchi kiradi
4. Workspace yaratadi
5. Plan tanlaydi
6. To'lovni amalga oshiradi
7. Workspace faollashadi
```

### 2. To'lov Amalga Oshirish

```
1. Foydalanuvchi plan tanlaydi
2. To'lov yaratiladi (status: pending)
3. To'lov tugmani bosadi
4. Click/Payme'ga yo'naltiriladi
5. To'lov muvaffaqiyatli
6. Callback qabul qiladi
7. Payment status: completed
8. Subscription uzaytiriladi
9. Workspace status: active
```

### 3. To'lov Tugaganda

```
1. End_date kuni keladi
2. Avtomatik tekshiruv
3. Status: suspended
4. Ma'lumotlar saqlanadi
5. Foydalanuvchi faqat o'qiy oladi
6. Eslatma yuboriladi
```

### 4. To'lov Qilingandan Keyin

```
1. Yangi to'lov amalga oshiriladi
2. Payment completed
3. Subscription uzaytiriladi
4. Status: active
5. To'liq kirish tiklanadi
6. Barcha ma'lumotlar mavjud
```

## 🔧 Texnik Implementatsiya

### API Endpoints

```
GET  /subscription/                    - Dashboard
POST /subscription/activate/{ws}/{plan}/ - Plan aktivatsiya
GET  /subscription/payment/success/{id}/ - To'lov muvaffaqiyatli
POST /subscription/reminder/{id}/      - Eslatma yuborish
```

### Avtomatik Tekshiruv

```python
def auto_check_expiration():
    """Har kuni ishlaydi"""
    today = date.today()
    
    # Tugaganlarni suspenz qilish
    expired = Subscription.objects.filter(
        end_date__lt=today,
        status='active'
    )
    for sub in expired:
        sub.status = 'suspended'
        sub.save()
    
    # 3 kundan keyin tugaydiganlar
    expiring_soon = Subscription.objects.filter(
        end_date__gte=today,
        end_date__lte=today + timedelta(days=3),
        status='active'
    )
    for sub in expiring_soon:
        # Eslatma yuborish
        send_reminder(sub)
```

### To'lov Integratsiyasi

#### Click Integratsiya
```python
def click_payment(subscription):
    """Click'ga to'lov so'rovi"""
    url = "https://www.click.uz/pay"
    data = {
        'amount': subscription.plan.price,
        'merchant_id': settings.CLICK_MERCHANT_ID,
        'transaction_param': subscription.id,
        'return_url': f'/subscription/payment/success/{subscription.id}/'
    }
    return requests.post(url, data=data)
```

#### Payme Integratsiya
```python
def payme_payment(subscription):
    """Payme'ga to'lov so'rovi"""
    url = "https://check.paycom.uz/service/create.transaction"
    data = {
        'amount': int(subscription.plan.price * 100),  # Qopamda
        'currency': 'UZS',
        'merchant_transaction_id': str(subscription.id),
        'merchant_id': settings.PAYME_MERCHANT_ID
    }
    return requests.post(url, json=data)
```

## 📊 Boshqaruv Paneli

### Admin uchun

```
1. Barcha workspace'lar
2. Har birining statusi
3. To'lov tarixi
4. Eslatmalar yuborish
5. Qo'lda uzaytirish
```

### Foydalanuvchi uchun

```
1. O'z workspace'i
2. Subscription statusi
3. Qolgan kunlar
4. To'lov qilish
5. To'lov tarixi
```

## 🔐 Xavfsizlik

- Har bir workspace o'z ma'lumotlarini ko'radi
- Faqat owner/admin to'lov qilishi mumkin
- To'lov tranzaksiya ID bilan tekshiriladi
- CSRF protection
- Login/parol autentifikatsiya

## 📱 Telegram Bot Integratsiya

```
/subscription      - Statusni ko'rish
/pay              - To'lov qilish
/renew            - Yangilash
```

## 💡 Misol Senariy

```
1. Admin Ahmad bilan shartnoma tuzadi
2. Login: ahmad, Parol: abc123
3. Ahmad kiradi
4. "Ahmad Restoran" workspace yaratadi
5. Pro plan tanlaydi (150,000 UZS/oy)
6. Click orqali to'lov qiladi
7. 30 kun faol
8. 3 kunga qoldi -> Eslatma
9. Tugadi -> Suspended
10. Ma'lumotlar saqlandi
11. Ahmad to'lov qiladi
12. Workspace tiklandi
13. Barcha mijozlar va buyurtmalar saqlangan
```

## 🚀 Keyingi Qadamlar

- [ ] Click/Payme to'liq integratsiya
- [ ] Telegram bot orqali to'lov
- [ ] SMS eslatmalar
- [ ] Email eslatmalar
- [ ] Chegirmalar tizimi
- [ ] Avtomatik invoicelar
- [ ] To'lov rejasi (plan)

---

**Muhim:** Ma'lumotlar hech qachon o'chirilmaydi, faqat kirish cheklanadi!
