# UniCRM AI - Django Native Version

**AI-powered Modular CRM/ERP SaaS Platform**

## 🚀 Texnologiyalar Stacki

### Backend
- **Django 5.1** - Asosiy framework
- **SQLite3** - Development database (Production uchun PostgreSQL)
- **python-telegram-bot v20+** - Telegram bot integratsiyasi
- **django-allauth** - Authentication
- **Celery + Redis** - Background tasks
- **OpenAI API** - AI xususiyatlar

### Frontend
- **Django Templates** - Server-side rendering
- **HTMX** - AJAX va dinamik yuklash
- **Alpine.js** - Interaktivlik
- **Tailwind CSS + DaisyUI** - UI/UX
- **Chart.js** - Analytics chartlar

## 📁 Loyiha Strukturasi

```
unicrm_ai/
├── manage.py
├── requirements.txt
├── .env
├── db.sqlite3
├── apps/
│   ├── core/              # Settings, URLs, WSGI
│   ├── accounts/          # User, Authentication
│   ├── workspaces/        # Multi-tenancy
│   ├── dashboard/         # Dashboard views
│   ├── orders/            # Buyurtmalar moduli
│   ├── clients/           # Mijozlar moduli
│   ├── telegram_bot/      # Telegram bot (handlers, bot.py)
│   ├── ai_features/       # AI xususiyatlar (OpenAI)
│   └── modules/           # Modular system
├── templates/             # HTML templates
│   ├── base.html
│   ├── includes/          # navbar, sidebar
│   ├── dashboard/
│   ├── workspaces/
│   ├── clients/
│   ├── orders/
│   ├── telegram/          # Mini App
│   └── ai_features/
├── static/                # CSS, JS, Images
└── media/                 # Uploaded files
```

## ⚙️ O'rnatish

### 1. Talablar
- Python 3.12+
- pip
- Virtual environment (tavsiya etiladi)

### 2. Loyihani klonlash va o'rnatish

```bash
# Virtual environment yaratish
python -m venv venv
venv\Scripts\activate

# Dependencies o'rnatish
pip install -r requirements/base.txt

# Environment variables sozlash
# .env faylini yarating va quyidagi qiymatlarni kiriting:
SECRET_KEY=your-secret-key
DEBUG=True
TELEGRAM_BOT_TOKEN=your-bot-token
BASE_URL=http://localhost:8000
OPENAI_API_KEY=your-openai-key (optional)

# Migratsiyalar
python manage.py makemigrations
python manage.py migrate

# Superuser yaratish
python manage.py createsuperuser

# Serverni ishga tushirish
python manage.py runserver

# Telegram botni ishga tushirish (boshqa terminalda)
python apps/telegram_bot/bot.py
```

## 🎯 Asosiy Xususiyatlar

### 1. Multi-Tenancy (Workspaces)
- Har bir user bir nechta workspace yaratishi mumkin
- Workspace bo'yicha ma'lumotlar ajratilgan
- Turli rollar: Owner, Admin, Manager, Member
- Modullarni yoqish/o'chirish

### 2. Mijozlar Boshqaruvi
- Mijozlar bazasi (CRM)
- Telegram integration
- Teglar va eslatmalar
- Manbalar: Telegram, Website, Referral, Call
- Mijoz tarixi va buyurtmalari

### 3. Buyurtmalar Boshqaruvi
- Buyurtmalar yaratish
- Status tracking (Pending, Processing, Completed, etc.)
- Order items
- Hisob-kitoblar
- Hisob-faktura chop etish

### 4. AI Xususiyatlar (OpenAI)
- AI-generated summaries
- Kunlik hisobotlar
- Mijoz tahlillari
- Tavsiyalar
- **Demo mode** (OpenAI API kaliti bo'lsa to'liq ishlaydi)

### 5. Telegram Bot & WebApp
- To'liq bot funksiyalar
- WebApp integratsiyasi
- Bot orqali buyurtmalar yaratish
- Mijozlar qo'shish
- Dashboard ko'rish
- Mini App mobil interfeys

## 🔐 Authentication

- Django allauth bilan
- Email/Username login
- Telegram WebApp auth
- Session-based authentication

## 📊 Dashboard

- Real-time statistika
- Chart.js bilan analytics
- AI-generated insights
- Top clients ko'rsatish
- HTMX bilan dinamik yuklash

## 🛠️ Development

### Serverni ishga tushirish

```bash
python manage.py runserver
```

### Admin panel

http://localhost:8000/admin/

**Login:** admin  
**Password:** admin123

### Telegram Bot sozlash

1. **BotFather** dan token olish:
   - Telegram'da `@BotFather` ga boring
   - `/newbot` buyrug'ini bering
   - Bot nomini va username kiriting
   - Token olasiz

2. **.env** faylga qo'shish:
```
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
BASE_URL=http://localhost:8000
```

3. Botni ishga tushirish:
```bash
python apps/telegram_bot/bot.py
```

4. **WebApp sozlash** (BotFather):
   - `/setdomain` - domeningizni kiriting
   - `/setmenubutton` - WebApp tugmasini sozlang

### OpenAI Integratsiyasi

OpenAI API kalitini `.env` ga qo'shing:
```
OPENAI_API_KEY=sk-your-openai-api-key
```

Keyin AI xususiyatlar to'liq ishlay boshlaydi. Aks holda demo mode ishlaydi.

## 📱 Telegram Bot Commands

- `/start` - Boshlash / Workspace tanlash
- `/dashboard` - Dashboard ko'rish
- `/clients` - Mijozlar ro'yxati
- `/orders` - Buyurtmalar ro'yxati
- `/workspace` - Workspace boshqaruv
- `/help` - Yordam

## 📄 Template Tuzilmasi

```
templates/
├── base.html              # Asosiy template
├── includes/
│   ├── navbar.html        # Navbar
│   └── sidebar.html       # Sidebar
├── dashboard/
│   └── index.html         # Asosiy dashboard
├── workspaces/
│   ├── create.html        # Workspace yaratish
│   ├── index.html         # Workspace ro'yxati
│   ├── settings.html      # Sozlamalar
│   ├── members.html       # A'zolar
│   └── modules.html       # Modullar
├── clients/
│   ├── list.html          # Mijozlar ro'yxati
│   └── detail.html        # Mijoz detallari
├── orders/
│   ├── list.html          # Buyurtmalar ro'yxati
│   └── detail.html        # Buyurtma detallari
├── telegram/
│   └── miniapp.html       # Telegram Mini App
└── ai_features/
    ├── reports.html       # AI hisobotlar
    └── summary_partial.html # AI summary partial
```

## 📦 Modullar

Tavsiya etilgan modullar:
- ✅ Orders (Buyurtmalar)
- ✅ Clients (Mijozlar)
- ✅ Products (Mahsulotlar)
- ⏳ Invoices (Hisob-fakturalar)
- ⏳ Tasks (Vazifalar)
- ⏳ Calendar (Kundalik)
- ⏳ Reports (Hisobotlar)

## 🚀 Production Deployment

### PostgreSQL o'rnatish

```bash
# requirements/production.txt ga qo'shing
psycopg2-binary==2.9.9

# .env da:
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=unicrm_ai
DATABASE_USER=your_db_user
DATABASE_PASSWORD=your_db_password
DATABASE_HOST=localhost
DATABASE_PORT=5432
```

### Static files to'plash

```bash
python manage.py collectstatic
```

### Gunicorn bilan ishga tushirish

```bash
pip install gunicorn
gunicorn apps.core.wsgi:application --bind 0.0.0.0:8000
```

## 📝 Keyingi Qadamlar

- [ ] Payment integration (Click, Payme)
- [ ] Email notifications (SMTP)
- [ ] SMS notifications
- [ ] API endpoints (Django REST Framework)
- [ ] Mobile app (React Native)
- [ ] Advanced analytics
- [ ] Multi-language support
- [ ] Export to Excel/PDF

## 📄 License

MIT License

## 👥 Authors

**NLP-Core-Team**

🌐 [nlp-core-team.com](https://nlp-core-team.com)

---

**UniCRM AI** - CRM tizimini inqilob qilish! 🚀

*Sun'iy intellekt bilan qurollangan zamonaviy CRM/ERP platformasi*
