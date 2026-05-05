# 🛠️ دليل الإعداد التفصيلي

## الخطوة 1: المتطلبات الأساسية

### تثبيت Docker
- **Mac/Windows**: حمّل [Docker Desktop](https://www.docker.com/products/docker-desktop/)
- **Linux**: `curl -fsSL https://get.docker.com | sh`

### التحقق
```bash
docker --version
docker-compose --version
```

---

## الخطوة 2: حساب MetaApi.cloud (مهم!)

MetaApi هو الجسر اللي يربط منصتك بـ MT5. بدونه، النظام ما يشتغل.

### إنشاء الحساب
1. روح [metaapi.cloud](https://metaapi.cloud)
2. اضغط **Sign Up** وأنشئ حساب
3. الباقة المجانية تكفي للاختبار

### الحصول على API Token
1. سجل دخولك في لوحة التحكم
2. روح **API Tokens**
3. اضغط **Generate Token**
4. اختر الصلاحيات: `mt-manager-api:rest:public:*` و `mt-account-api:rest:public:*`
5. انسخ الـ Token (بيظهر مرة واحدة فقط!)

### ضع Token في .env
```bash
METAAPI_TOKEN=your-actual-token-here
```

---

## الخطوة 3: حساب MT5 للاختبار

### خيار 1: حساب Demo مجاني (موصى به للتطوير)
1. روح [XM Global](https://www.xm.com) أو [Exness](https://www.exness.com)
2. سجل حساب Demo
3. ستصلك:
   - **Login**: رقم الحساب
   - **Password**: كلمة المرور
   - **Server**: اسم السيرفر (مثل `XMGlobal-MT5-Demo`)

### خيار 2: حسابك الفعلي
استخدم بيانات حسابك في MT5، لكن انتبه:
- **استخدم Investor Password** (للمراقبة فقط) للاختبار الأولي
- الـ Master Password يسمح بالتداول الفعلي - استخدمه فقط بعد التأكد

---

## الخطوة 4: إعداد المشروع

### 1. توليد المفاتيح السرية

في الـ Terminal:
```bash
# مفتاح JWT
python3 -c "import secrets; print('SECRET_KEY=' + secrets.token_urlsafe(32))"

# مفتاح التشفير
python3 -c "import secrets; print('ENCRYPTION_KEY=' + secrets.token_urlsafe(32))"
```

### 2. إنشاء .env
```bash
cp .env.example .env
```

### 3. تعديل .env
افتح `.env` بأي محرر وضع:
- `SECRET_KEY` من الخطوة 1
- `ENCRYPTION_KEY` من الخطوة 1
- `METAAPI_TOKEN` من خطوة MetaApi

---

## الخطوة 5: التشغيل

### تشغيل كل شيء
```bash
docker-compose up -d
```

### مراقبة الـ logs
```bash
docker-compose logs -f
```

### التحقق من الحالة
```bash
docker-compose ps
```

يجب أن تشاهد:
- ✅ mursheed-db (postgres)
- ✅ mursheed-redis
- ✅ mursheed-backend
- ✅ mursheed-frontend

---

## الخطوة 6: التجربة الأولى

1. افتح http://localhost:3000
2. اضغط **ابدأ مجاناً**
3. أنشئ حساب في "مُرشد"
4. ستوجه تلقائياً لربط MT5
5. أدخل بيانات حساب MT5 Demo
6. انتظر 30-60 ثانية للربط
7. ستوجه للوحة التحكم

---

## الأوامر المفيدة

```bash
# إيقاف
docker-compose down

# إيقاف مع حذف البيانات
docker-compose down -v

# إعادة بناء بعد تغيير الكود
docker-compose up -d --build

# تنفيذ أمر داخل Backend
docker-compose exec backend bash
docker-compose exec backend pytest

# قاعدة البيانات
docker-compose exec db psql -U mursheed -d mursheed
```

---

## التطوير بدون Docker (متقدم)

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

ملاحظة: تحتاج PostgreSQL و Redis مشغلين محلياً.
