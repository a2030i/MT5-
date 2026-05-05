# CLAUDE.md

هذا الملف يوجه Claude Code عند العمل على هذا المشروع.

## 📋 نظرة عامة على المشروع

**مُرشد (Mursheed)** — منصة تداول عربية تربط حسابات MetaTrader 5 وتقدم واجهة عربية واضحة بديلة لـ MT5 المعقد.

### المستخدم المستهدف
متداولون عرب (السوق السعودي بالتحديد) يستخدمون MT5 ويعانون من تعقيد الواجهة الأصلية.

### الهدف
طبقة عربية فوق MT5 تتيح للمستخدم:
- ربط حسابه في MT5 بسهولة
- تنفيذ صفقات شراء/بيع
- متابعة الصفقات والأداء
- نسخ صفقات من متداولين محترفين

---

## 🏗️ المعمارية

```
┌────────────────────────────────────┐
│  Frontend: React + Vite + TS       │
│  (واجهة عربية RTL داكنة)            │
└─────────────┬──────────────────────┘
              │ REST + WebSocket
┌─────────────▼──────────────────────┐
│  Backend: FastAPI + Python 3.11    │
│  - JWT Auth                        │
│  - PostgreSQL (SQLAlchemy)         │
│  - Redis (Cache + Sessions)        │
└─────────────┬──────────────────────┘
              │
┌─────────────▼──────────────────────┐
│  MetaApi.cloud (سحابي)              │
│  بديل عن MetaTrader5 Python package  │
│  لأنه يدعم الحسابات المتعددة سحابياً │
└────────────────────────────────────┘
```

### لماذا MetaApi بدلاً من MetaTrader5 Python package؟
- المكتبة الرسمية تشتغل على Windows فقط وتحتاج تيرمنال مفتوح
- MetaApi خدمة سحابية تدعم آلاف الحسابات بنفس الوقت
- REST + WebSocket متاح من أي نظام تشغيل
- Free Tier متاح للتجربة

---

## 🗂️ هيكل المشروع

```
mursheed-cloud/
├── backend/                # FastAPI Backend
│   ├── app/
│   │   ├── api/           # REST endpoints
│   │   ├── core/          # config, security, db
│   │   ├── models/        # SQLAlchemy models
│   │   ├── schemas/       # Pydantic schemas
│   │   └── services/      # Business logic + MetaApi integration
│   ├── tests/
│   ├── requirements.txt
│   ├── Dockerfile
│   └── main.py
├── frontend/              # React + Vite + TypeScript
│   ├── src/
│   │   ├── pages/         # كل صفحة في ملف
│   │   ├── components/    # مكونات قابلة لإعادة الاستخدام
│   │   ├── services/      # API client (axios)
│   │   └── styles/        # CSS موحد (RTL + داكن)
│   ├── package.json
│   ├── vite.config.ts
│   └── Dockerfile
├── docker-compose.yml     # تشغيل كامل المشروع
├── .env.example
└── README.md
```

---

## 🚀 أوامر التطوير الشائعة

### تشغيل المشروع كاملاً (موصى به)
```bash
docker-compose up -d
# Frontend: http://localhost:3000
# Backend:  http://localhost:8000
# API Docs: http://localhost:8000/docs
```

### تشغيل Backend فقط
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
# venv\Scripts\activate   # Windows
pip install -r requirements.txt
uvicorn main:app --reload
```

### تشغيل Frontend فقط
```bash
cd frontend
npm install
npm run dev
```

### تشغيل الاختبارات
```bash
cd backend
pytest tests/ -v
```

### إنشاء migration جديد
```bash
cd backend
alembic revision --autogenerate -m "وصف التغيير"
alembic upgrade head
```

---

## ⚠️ تحذيرات مهمة جداً

### 1. الجانب القانوني (السعودية)
هذا المشروع يقدم خدمات تداول. في السعودية:
- **هيئة السوق المالية (CMA)** تشترط ترخيصاً لأي نشاط تداول
- لا تطلق المنصة قبل الحصول على ترخيص أو شراكة مع وسيط مرخص
- استشر محامياً متخصصاً قبل أي إطلاق تجاري

### 2. الأمان حساس جداً
- بيانات MT5 (كلمات المرور) **يجب** أن تشفر بـ AES-256 قبل التخزين
- لا تسجل كلمات المرور في الـ logs أبداً
- استخدم HTTPS فقط في الإنتاج
- فعّل rate limiting على endpoints الحساسة

### 3. أموال حقيقية
عند ربط حسابات حقيقية، أي خطأ ممكن يكلف المستخدم خسائر مالية فعلية:
- اختبر دائماً على حسابات Demo أولاً
- أضف confirmation للصفقات الكبيرة
- سجّل كل عملية تداول للمراجعة

---

## 📐 معايير الكود (Code Standards)

### Python (Backend)
- استخدم type hints دائماً
- اتبع PEP 8
- وثّق الدوال بـ docstrings عربية
- اختبر كل endpoint جديد

### TypeScript (Frontend)
- لا تستخدم `any` إلا للضرورة القصوى
- كل صفحة في ملف منفصل
- استخدم functional components + hooks
- النصوص العربية في ملف i18n منفصل (للتوسع لاحقاً)

### الأسماء
- متغيرات وأسماء الملفات: إنجليزية (snake_case للـ Python، camelCase للـ TS)
- النصوص الظاهرة للمستخدم: عربية فقط
- التعليقات: عربية مفضلة (لتوضيح المنطق)

---

## 🎨 نظام التصميم

التصميم محدد في `frontend/src/styles/design-system.css`:
- **خلفية داكنة**: `#0a0e1a`
- **اللون الرئيسي**: `#00d68f` (أخضر زمردي)
- **الخطوط**: Reem Kufi (عناوين) + IBM Plex Sans Arabic (نصوص)
- **RTL** بالكامل
- **Mobile-first** responsive

لا تغيّر نظام التصميم بدون موافقة صريحة.

---

## 🔌 نقاط نهاية API الأساسية

```
POST   /api/auth/register          إنشاء حساب
POST   /api/auth/login             تسجيل دخول
POST   /api/mt5/connect            ربط حساب MT5
GET    /api/mt5/account            معلومات الحساب
GET    /api/mt5/positions          الصفقات المفتوحة
POST   /api/mt5/trade              تنفيذ صفقة
DELETE /api/mt5/positions/{id}     إغلاق صفقة
GET    /api/mt5/history            سجل الصفقات
GET    /api/analytics/performance  تحليل الأداء
```

التفاصيل الكاملة في `backend/app/api/`.

---

## ✅ المهام الفورية (TODO)

عند البدء بالتطوير، نفذ بهذا الترتيب:
1. اقرأ `docs/SETUP.md` للإعداد الأولي
2. شغّل `docker-compose up` وتأكد من عمل البيئة
3. سجّل في MetaApi.cloud واحصل على API token (مجاني للبداية)
4. ضع المتغيرات في `.env`
5. شغّل migrations الأولية
6. ابدأ بتطوير endpoint واحد ثم الواجهة المقابلة

---

## 🆘 عند المشاكل

- **Backend ما يشتغل؟** تأكد من تشغيل PostgreSQL و Redis
- **Frontend ما يتصل بـ Backend؟** افحص CORS settings في `backend/app/core/config.py`
- **MT5 ما يربط؟** افحص MetaApi credentials و server name
- مشاكل أخرى → راجع `docs/TROUBLESHOOTING.md`
