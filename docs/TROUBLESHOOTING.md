# 🆘 حل المشاكل الشائعة

## Backend ما يشتغل

### المشكلة: `connection refused` على Postgres
```bash
# تحقق من حالة Postgres
docker-compose logs db

# تأكد من بدء Postgres قبل Backend
docker-compose down
docker-compose up -d db redis
sleep 5
docker-compose up -d backend
```

### المشكلة: `ImportError` أو module not found
```bash
docker-compose build --no-cache backend
docker-compose up -d backend
```

---

## Frontend ما يتصل بالـ Backend

### تحقق من CORS
في `backend/app/core/config.py` تأكد من:
```python
CORS_ORIGINS = ["http://localhost:3000", "http://localhost:5173"]
```

### تحقق من VITE_API_URL
في `.env`:
```
VITE_API_URL=http://localhost:8000/api
```

---

## MT5 ما يربط

### رسالة: `Failed to connect to MT5`

#### الأسباب المحتملة:
1. **بيانات خاطئة**
   - تأكد من رقم الحساب وكلمة المرور
   - اسم السيرفر يكتب بالضبط زي ما يظهر في تطبيق MT5

2. **MetaApi Token غير صالح**
   ```bash
   # تحقق من القيمة
   docker-compose exec backend env | grep METAAPI
   ```

3. **الباقة المجانية في MetaApi**
   - الباقة المجانية تدعم حسابين فقط
   - تحقق من لوحة تحكم MetaApi

4. **السيرفر غير مدعوم**
   - بعض الوسطاء الصغار غير مدعومين في MetaApi
   - جرب وسيط آخر مثل XM أو Exness

---

## الأداء بطيء

### إعادة بناء Docker images محسنة
```bash
docker-compose down
docker-compose build --no-cache
docker-compose up -d
```

### تنظيف الذاكرة
```bash
docker system prune -a
```

---

## الأمان

### استبدال المفاتيح الافتراضية
**لا تستخدم القيم الافتراضية في الإنتاج!**

```bash
# توليد مفاتيح قوية
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

### تفعيل HTTPS
في الإنتاج، استخدم reverse proxy مثل nginx أو caddy:
```nginx
server {
    listen 443 ssl;
    server_name mursheed.sa;
    ssl_certificate /etc/ssl/cert.pem;
    ssl_certificate_key /etc/ssl/key.pem;

    location / {
        proxy_pass http://localhost:3000;
    }
    location /api/ {
        proxy_pass http://localhost:8000;
    }
}
```

---

## رسائل خطأ شائعة

### `بيانات الاعتماد غير صالحة`
- الـ token انتهت صلاحيته
- سجل دخول من جديد

### `حساب MT5 غير موجود`
- تحقق من account_id
- تأكد من ربط الحساب أولاً

### `فشل تنفيذ الصفقة`
- تحقق من ساعات السوق (الفوركس مغلق نهاية الأسبوع)
- تحقق من حجم الصفقة (لا يقل عن 0.01 lot)
- تحقق من Stop Loss / Take Profit (يجب أن تكون منطقية)

---

## للمزيد من المساعدة

- توثيق MetaApi: https://metaapi.cloud/docs/
- توثيق FastAPI: https://fastapi.tiangolo.com/
- مجتمع MQL5: https://www.mql5.com/en/forum
