# UniCRM AI - To'liq Qo'llanma

> Sun'iy intellekt bilan qurollangan zamonaviy CRM/ERP SaaS platformasi

---

## 📚 MUNDARIJA

1. [Loyiha Haqida](#loyiha-haqida)
2. [Asosiy Tushunchalar](#asosiy-tushunchalar)
3. [Loyiha Arxitekturasi](#loyiha-arxitekturasi)
4. [Modullar va Ularning Vazifalari](#modullar-va-ularning-vazifalari)
5. [Qanday Ishlaydi](#qanday-ishlaydi)
6. [Foydalanish Senariylari](#foydalanish-senariylari)
7. [Texnik Tafsilotlar](#texnik-tafsilotlar)
8. [Keyingi Qadamlar](#keyingi-qadamlar)

---

## 🎯 LOYIHA HAQIDA

### UniCRM AI Nima?

**UniCRM AI** - bu kichik va o'rta biznes uchun mo'ljallangan, sun'iy intellekt yordamida boyitilgan barcha-turidagi CRM (Customer Relationship Management) va ERP (Enterprise Resource Planning) tizimi.

### Asosiy Maqsad

- Mijozlar bilan ishlashni soddalashtirish
- Buyurtmalarni avtomatik boshqarish
- Business tahlillarini AI yordamida chuqurlashtirish
- Telegram bot orqali har qayerdan boshqarish
- Workspace (ish joyi) tizimi orqali bir nechta biznesni boshqarish

### Kimlar Uchun?

| Sector | Foydalanish |
|--------|-------------|
| 🍽️ **Restoran/Kafe** | Buyurtmalar, mijozlar, hisob-kitoblar |
| 🛍️ **Do'kon** | Savdo, mijozlar bazasi, ombor |
| 💼 **Xizmat Ko'rsatish** | Buyurtmalar, mijozlar, hisob-fakturalar |
| 🏢 **Korporatsiya** | Multi-departament boshqaruvi |
| 🎓 **Ta'lim** | Talabalar, to'lovlar, darslar |

---

## 💡 ASOSIY TUSHUNCHALAR

### 1. Workspace (Ish Joyi)

**Workspace** - bu sizning biznesingiz yoki loyihangiz uchun alohida "ko'rinma joy". Har bir workspace o'ziga xos:

- **Mijozlar bazasi**
- **Buyurtmalar**
- **A'zolar** (xodimlar)
- **Sozlamalar**
- **Modullar** (faol/neytral)

**Misol:**
```
Ahmad
├── "Ahmad Restoran" workspace
│   ├── 150 mijoz
│   ├── 450 buyurtma
│   ├── 5 xodim
│   └── Modullar: Orders, Clients, Products
│
└── "Ahmad Shop" workspace
    ├── 80 mijoz
    ├── 120 buyurtma
    ├── 2 xodim
    └── Modullar: Orders, Clients
```

### 2. Multi-Tenancy (Ko'p Kirish)

Tizim **multi-tenant** arxitektura asosida ishlaydi:

- Har bir foydalanuvchi bir nechta workspace yaratishi mumkin
- Har bir workspace ma'lumotlari ajratilgan
- Xodimlar workspace ichida rollarga ega:
  - **Owner** - Egasi (to'liq huquq)
  - **Admin** - Boshqaruvchi (deyarli to'liq)
  - **Manager** - Menecer (cheklangan)
  - **Member** - A'zo (minimal)

### 3. Modullar Tizimi

Workspace ichida turli modullarni yoqish/o'chirish mumkin:

| Modul | Vazifasi | Status |
|-------|----------|--------|
| **Orders** | Buyurtmalar boshqaruvi | ✅ Faol |
| **Clients** | Mijozlar bazasi | ✅ Faol |
| **Products** | Mahsulotlar ombori | ✅ Faol |
| **Invoices** | Hisob-fakturalar | ⏳ Keyinchalik |
| **Tasks** | Vazifalar | ⏳ Keyinchalik |
| **Calendar** | Kun tartibi | ⏳ Keyinchalik |
| **Reports** | Tahliliy hisobotlar | ⏳ Keyinchalik |

### 4. AI (Sun'iy Intellekt)

**OpenAI API** integratsiyasi orqali:

- **Kunlik hisobotlar** - Statistikalar va tavsiyalar
- **Mijoz tahlili** - Har bir mijoz uchun AI insights
- **Avtomatik email** - Marketing va eslatma xatlari
- **Tavsiyalar** - Business o'sishi uchun strategiyalar

> **Qiziqarli:** OpenAI kaliti bo'lmasa ham **demo mode** ishlaydi - barcha funksiyalar mavjud, lekin AI statik javob beradi.

### 5. Telegram Bot & WebApp

**Telegram bot** orqali tizimni telefoningizdan boshqarish:

```
/start          - Workspace tanlash
/dashboard      - Statistikani ko'rish
/clients        - Mijozlar ro'yxati
/orders         - Buyurtmalar
/workspace      - Yangi workspace yaratish
/help           - Yordam
```

**Telegram WebApp** - bu Telegram ichida ochiladigan mobil interfeys:

- To'liq dashboard
- Tezkor buyurtma yaratish
- Mijoz qo'shish
- Real-time ma'lumotlar

---

## 🏗️ LOYIHA ARXITEKTURASI

### Umumiy Struktura

```
┌─────────────────────────────────────────────────────────┐
│                    FRONTEND LAYER                        │
├─────────────────────────────────────────────────────────┤
│  Django Templates  │  HTMX  │  Alpine.js  │  Tailwind   │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    BACKEND LAYER                         │
├─────────────────────────────────────────────────────────┤
│            Django 5.1 (Python)                           │
├──────────────┬──────────────┬──────────────┬────────────┤
│  Accounts    │  Workspaces  │  Dashboard   │  Modules   │
│  (Auth)      │  (Tenancy)   │  (Stats)     │  (Config)  │
├──────────────┼──────────────┼──────────────┼────────────┤
│  Clients     │  Orders      │  AI Features │  Telegram  │
│  (CRM)       │  (ERP)       │  (OpenAI)    │  (Bot)     │
└──────────────┴──────────────┴──────────────┴────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│                    DATA LAYER                            │
├─────────────────────────────────────────────────────────┤
│          SQLite3 (Dev) / PostgreSQL (Prod)               │
└─────────────────────────────────────────────────────────┘
```

### Ma'lumotlar Oqimi (Data Flow)

```
1. Foydalanuvchi → Django View → Model → Database
2. Database → Model → View → Template → Frontend
3. HTMX → AJAX → View → Partial HTML → DOM Update
4. Telegram Bot → Webhook → View → Model → Response
```

### Xavfsizlik (Security)

| Qatlam | Himoya |
|--------|--------|
| **Authentication** | Django allauth, Session-based |
| **Authorization** | Workspace membership, Roles |
| **CSRF** | Django CSRF tokens |
| **SQL Injection** | Django ORM (avtomatik) |
| **XSS** | Django template escaping |
| **Telegram Auth** | HMAC validation |

---

## 📦 MODULLAR VA ULARNING VAZIFALARI

### 1. Accounts (Foydalanuvchilar)

**Vazifasi:** Foydalanuvchilarni ro'yxatdan o'tkazish va autentifikatsiya

**Xususiyatlar:**
- ✅ Email/Username bilan ro'yxatdan o'tish
- ✅ Telegram autentifikatsiya
- ✅ Profil boshqaruvi
- ✅ Parolni tiklash
- ✅ Email tasdiqlash

**Modellar:**
```python
User:
├── username
├── email
├── telegram_id (Telegram uchun)
├── avatar
└── is_owner (Superuser flag)
```

### 2. Workspaces (Ish Joylari)

**Vazifasi:** Multi-tenancy va bizneslarni ajratish

**Xususiyatlar:**
- ✅ Workspace yaratish/tahrirlish
- ✅ A'zolar qo'shish/chiqarish
- ✅ Rollar (Owner, Admin, Manager, Member)
- ✅ Modullarni yoqish/o'chirish
- ✅ Plan tizimi (Free, Starter, Business, Premium)

**Modellar:**
```python
Workspace:
├── name
├── slug (URL uchun)
├── owner (User)
├── plan (Free/Starter/Business/Premium)
├── status (Trial/Active/Suspended/Expired)
└── logo

WorkspaceMember:
├── workspace
├── user
├── role (owner/admin/manager/member)
└── joined_at

Module:
├── workspace
├── module_type (orders/clients/products...)
├── is_enabled
└── settings (JSON)
```

### 3. Clients (Mijozlar)

**Vazifasi:** Mijozlar bazasi (CRM)

**Xususiyatlar:**
- ✅ Mijoz qo'shish/tahrirlash/o'chirish
- ✅ Telefon, email, Telegram username
- ✅ Teglar (tags)
- ✅ Eslatmalar (notes)
- ✅ Mijoz manbasi (Telegram, Website, Call...)
- ✅ Buyurtmalar tarixi

**Modellar:**
```python
Client:
├── workspace
├── first_name, last_name
├── email, phone
├── telegram_id, telegram_username
├── source (telegram/website/referral/call/other)
├── tags (comma-separated)
├── notes
├── created_by (User)
└── created_at, updated_at
```

**Foydalanish Senariysi:**
```
1. Yangi mijoz qo'shish
   ├─> Ism, telefon, email kiritish
   ├─> Manbani tanlash (Telegram, Website...)
   └─> Teglar qo'shish (VIP, Yangi, Doimiy...)

2. Mijozni qidirish
   ├─> Ism bo'yicha
   ├─> Telefon bo'yicha
   └─> Teg bo'yicha

3. Mijoz tarixini ko'rish
   ├─> Barcha buyurtmalar
   ├─> Jami xarajat
   └─> Oxirgi aloqa
```

### 4. Orders (Buyurtmalar)

**Vazifasi:** Buyurtmalarni boshqarish (ERP)

**Xususiyatlar:**
- ✅ Buyurtma yaratish
- ✅ Statuslar (Pending, Processing, Completed, Cancelled, Refunded)
- ✅ Mahsulotlar (OrderItems)
- ✅ Hisob-kitoblar
- ✅ Buyurtma raqami (ORD-XXXX)
- ✅ Eslatmalar

**Modellar:**
```python
Order:
├── workspace
├── order_number (ORD-XXXX)
├── client (ForeignKey)
├── status (pending/processing/completed...)
├── total_amount
├── notes
├── created_by (User)
└── created_at, updated_at

OrderItem:
├── order
├── name (mahsulot nomi)
├── quantity
└── unit_price
```

**Buyurtma Jarayoni:**
```
1. Buyurtma yaratish
   ├─> Mijoz tanlash
   ├─> Mahsulotlar qo'shish
   ├─> Summa avtomatik hisoblash
   └─> Status: Pending

2. Buyurtmani qayta ishlash
   ├─> Status: Processing
   ├─> Mahsulotlarni tayyorlash
   └─> Eslatmalar qo'shish

3. Buyurtmani yakunlash
   ├─> Status: Completed
   ├─> To'lov qabul qilish
   └─> Mijozga xabar

4. Agar muammo bo'lsa
   ├─> Status: Cancelled yoki Refunded
   └─> Sabab yozish
```

### 5. Dashboard (Boshqaruv Paneli)

**Vazifasi:** Umumiy statistikani ko'rish

**Xususiyatlar:**
- ✅ Real-time statistika
- ✅ Chart.js grafiklar
- ✅ Top mijozlar
- ✅ AI-generated insights
- ✅ Tezkor amallar

**Ko'rsatkichlar:**
```
Dashboard Cards:
├── Jami Mijozlar
├── Jami Buyurtmalar
├── Aktiv Buyurtmalar
├── Umumiy Tushum
└── AI Insights

Grafiklar:
├── So'nggi 30 kunlik buyurtmalar
├── Mijozlar o'sishi
└── Top 5 mijozlar
```

### 6. AI Features (Sun'iy Intellekt)

**Vazifasi:** Business tahlillari va tavsiyalar

**Xususiyatlar:**
- ✅ Kunlik hisobotlar (Daily Report)
- ✅ Haftalik hisobotlar (Weekly Report)
- ✅ Mijoz tahlillari (Client Insights)
- ✅ AI Tavsiyalari
- ✅ OpenAI integratsiya

**AI Hisobot Misoli:**
```
🤖 AI Kunlik Hisobot

📊 Umumiy Ko'rsatkichlar:
• Jami mijozlar: 150
• Jami buyurtmalar: 450

📅 Bugungi Statistikasi:
• Bugungi buyurtmalar: 12
• Bugungi tushum: 2,500,000 so'm

💡 AI Tavsiyalari:
1. Mijozlar bazangiz o'smoqda, tabriklaymiz!
2. Buyurtmalar sonini oshirish uchun marketing kampaniyasini boshlang
3. Telegram bot orqali mijozlar bilan aloqani kuchaytiring

⚡ Keyingi Qadamlar:
• Yangi mijozlar qo'shing
• Buyurtmalarni kuzatib boring
• Hisobotlarni tahlil qiling
```

### 7. Telegram Bot

**Vazifasi:** Tizimni telefoningizdan boshqarish

**Komandalar:**
```
/start          - Boshlash, workspace tanlash
/dashboard      - Statistikani ko'rish
/clients        - Mijozlar ro'yxati
/orders         - Buyurtmalar ro'yxati
/workspace      - Yangi workspace yaratish
/help           - Yordam
```

**WebApp:**
```
Telegram ichida:
├── Dashboard ko'rish
├── Tezkor buyurtma yaratish
├── Mijoz qo'shish
└── Real-time ma'lumotlar
```

---

## 🔄 QANDAY ISHLAYDI

### 1. Foydalanuvchi Ro'yxatdan O'tish

```
1. /accounts/signup/ ga o'ting
2. Username va email kiriting
3. Parol tanlang
4. Ro'yxatdan o'ting
5. Dashboard ga yo'naltiriladi
```

### 2. Workspace Yaratish

```
1. Dashboard sahifasida "Yangi Workspace" tugmasini bosing
2. Workspace nomini kiriting (masalan: "Mening Restoran")
3. Yaratish tugmasini bosing
4. Workspace avtomatik yaratiladi va sizning workspace member bo'lasiz
5. Default modullar yoqiladi (Orders, Clients, Products)
```

### 3. Mijoz Qo'shish

```
1. Clients moduli sahifasiga o'ting
2. "Mijoz Qo'shish" tugmasini bosing
3. Ma'lumotlarni kiriting:
   ├─> Ism, familiya
   ├─> Telefon
   ├─> Email
   ├─> Telegram username (ixtiyoriy)
   ├─> Manbani tanlash
   └─> Teglar qo'shish
4. Saqlash
```

### 4. Buyurtma Yaratish

```
1. Orders moduli sahifasiga o'ting
2. "Buyurtma Yaratish" tugmasini bosing
3. Mijozni tanlang
4. Mahsulotlar qo'shing:
   ├─> Mahsulot nomi
   ├─> Soni
   ├─> Narx
5. Summa avtomatik hisoblanadi
6. Status tanlang (Pending/Processing...)
7. Eslatma qo'shing (ixtiyoriy)
8. Saqlash
```

### 5. AI Hisobot Olish

```
1. AI Reports sahifasiga o'ting
2. "Kunlik Hisobot" tugmasini bosing
3. AI avtomatik:
   ├─> Statistikani yig'adi
   ├─> Trendlarni tahlil qiladi
   ├─> Tavsiyalar beradi
   └─> Hisobotni ko'rsatadi
```

### 6. Telegram Bot Orqali Ishlash

```
1. Telegram'da botni toping
2. /start bosing
3. Workspace tanlang
4. Komandalardan foydalaning:
   ├─ /dashboard - Statistikani ko'rish
   ├─ /clients - Mijozlar
   ├─ /orders - Buyurtmalar
5. WebApp tugmasini bosib to'liq interfeysni oching
```

---

## 📋 FOYDALANISH SENARIYLARI

### Senariy 1: Restoran Egosi

**Ahmad** - yangi restoran ochdi. U UniCRM AI dan foydalangan holda:

```
1. Workspace yaratdi: "Ahmad Restoran"
2. 3 xodim qo'shdi (Manager, Kashir, Ofitsiant)
3. Mijozlar bazasini boshladi
4. Har bir buyurtmani tizimga kiritadi
5. Kunlik AI hisobotni o'qiydi
6. Telegram bot orqali restoranda bo'lmaganda ham buyurtmalarni kuzatadi

Natija:
✅ Barcha buyurtmalar tartibli
✅ Mijozlar bazasi mavjud
✅ Xodimlar mas'uliyati aniq
✅ Daromad tahlili qulay
```

### Senariy 2: Onlayn Do'kon

**Zarina** - onlayn kiyim do'koni ochdi:

```
1. Workspace: "Zarina Fashion"
2. Mijozlar bazasi (Telegram'dan kelganlar)
3. Buyurtmalarni kiritadi
4. Statuslarni kuzatadi (Pending → Processing → Completed)
5. Mijozlarga Telegram orqali xabar beradi
6. Haftalik AI hisobot bilan savdoni tahlil qiladi

Natija:
✅ Buyurtmalar tartibli
✅ Mijozlar qaytadi (loyallik)
✅ Savdo trendlari aniq
✅ Vaqt tejaldi
```

### Senariy 3: Xizmat Ko'rsatish Shirkati

**Aziz** - IT xizmatlari ko'rsatadi:

```
1. Workspace: "Aziz IT Services"
2. Har bir mijoz uchun alohida kartochka
3. Har bir loyiha = buyurtma
4. Hisob-fakturalar (kelajakda)
5. Xodimlarga vazifa taqsimot
6. AI orqali mijozlarga eslatma

Natija:
✅ Barcha loyihalar kuzatiladi
✅ Mijozlar bilan aloqa tartibli
✅ To'lovlar nazoratida
```

---

## 🔧 TEXNIK TAFSİLOTLAR

### Backend Stack

```python
Framework: Django 5.1
Database: SQLite3 (Dev) / PostgreSQL (Prod)
Authentication: django-allauth
Background Tasks: Celery + Redis
AI: OpenAI API
Telegram: python-telegram-bot v20+
```

### Frontend Stack

```javascript
Templates: Django Templates
Dynamic: HTMX + Alpine.js
UI: Tailwind CSS + DaisyUI
Charts: Chart.js
Icons: Font Awesome
```

### Ma'lumotlar Bazasi

```sql
-- Asosiy jadvallar
User (accounts)
├── id, username, email, telegram_id, avatar...

Workspace (workspaces)
├── id, name, slug, owner_id, plan, status...

WorkspaceMember (workspaces)
├── workspace_id, user_id, role, joined_at...

Client (clients)
├── id, workspace_id, first_name, last_name...
├── email, phone, telegram_id, source, tags...

Order (orders)
├── id, workspace_id, order_number, client_id...
├── status, total_amount, notes...

OrderItem (orders)
├── id, order_id, name, quantity, unit_price...

AISummary (ai_features)
├── id, workspace_id, summary_type, content...
```

### API Endpoints

```
Dashboard API:
GET /dashboard/api/stats/          - Umumiy statistika
GET /dashboard/api/top-clients/    - Top mijozlar
GET /dashboard/api/orders-chart/   - Grafik ma'lumotlari

Clients API:
GET /clients/{workspace_slug}/     - Mijozlar ro'yxati
POST /clients/{workspace_slug}/    - Mijoz yaratish
GET /clients/{workspace_slug}/{id}/ - Mijoz detallari

Orders API:
GET /orders/{workspace_slug}/      - Buyurtmalar ro'yxati
POST /orders/{workspace_slug}/     - Buyurtma yaratish
GET /orders/{workspace_slug}/{id}/ - Buyurtma detallari

AI API:
GET /ai/{workspace_slug}/daily-summary/     - Kunlik hisobot
GET /ai/{workspace_slug}/client/{id}/insights/ - Mijoz tahlili
```

### Xavfsizlik

```python
# CSRF Protection
{% csrf_token %}  # Har bir formada

# Authorization
@login_required  # View decorator
WorkspaceMember.objects.get(user=request.user)  # Workspace access

# Data Isolation
Client.objects.filter(workspace=workspace)  # Har doim workspace bo'yicha filtrlash
```

---

## 🚀 KEYINGI QADAMLAR

### 1. Production Deployment

```bash
# PostgreSQL o'rnatish
pip install psycopg2-binary

# .env sozlash
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=unicrm_ai
DATABASE_USER=postgres
DATABASE_PASSWORD=your_password
DATABASE_HOST=localhost
DATABASE_PORT=5432

# Static files
python manage.py collectstatic

# Gunicorn
gunicorn apps.core.wsgi:application --bind 0.0.0.0:8000
```

### 2. Payment Integration

```python
# Click, Payme integratsiyasi
# Hisob-fakturalar
# Avtomatik to'lovlar
```

### 3. Advanced Features

```
- [ ] Email notifications (SMTP)
- [ ] SMS notifications
- [ ] Export to Excel/PDF
- [ ] Mobile app (React Native)
- [ ] Advanced analytics
- [ ] Multi-language (uz/en/ru)
- [ ] API for third-party apps
- [ ] Webhooks
- [ ] Real-time updates (WebSockets)
```

### 4. Scaling

```
- Load balancer
- Database replication
- Redis cache
- CDN for static files
- Docker containerization
- Kubernetes orchestration
```

---

## 📞 YORDAM VA QO'LLAB-QUVVATLASH

### Muammolar

Agar muammo yuzaga kelsa:

1. **Loglarni tekshiring**
   ```bash
   python manage.py runserver  # Console output
   ```

2. **Database tekshirish**
   ```bash
   python manage.py shell
   >>> from apps.accounts.models import User
   >>> User.objects.all()
   ```

3. **Migratsiyalar**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

### Foydali Buyruqlar

```bash
# Server
python manage.py runserver

# Bot
python apps/telegram_bot/bot.py

# Superuser
python manage.py createsuperuser

# Shell
python manage.py shell

# Static files
python manage.py collectstatic

# Tests
python manage.py test
```

---

## 📄 LİSENSİYA

MIT License - To'liq ochiq kod

---

## 👥 MUALLIFLAR

**NLP-Core-Team**

🌐 [nlp-core-team.com](https://nlp-core-team.com)

---

## 🎓 O'QISH MATERIALLARI

### Django

- [Django Documentation](https://docs.djangoproject.com/)
- [Django Templates](https://docs.djangoproject.com/en/stable/topics/templates/)
- [Django ORM](https://docs.djangoproject.com/en/stable/topics/db/queries/)

### Frontend

- [HTMX Documentation](https://htmx.org/docs/)
- [Alpine.js Guide](https://alpinejs.dev/start-here)
- [Tailwind CSS](https://tailwindcss.com/docs)
- [DaisyUI Components](https://daisyui.com/components/)

### AI

- [OpenAI API](https://platform.openai.com/docs)
- [python-telegram-bot](https://docs.python-telegram-bot.org/)

---

**UniCRM AI** - Biznesingizni avtomatlashtiring, vaqtingizni tejang! 🚀

*Oxirgi yangilanish: 2024*
