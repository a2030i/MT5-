# 🚀 دليل النشر للإنتاج

## ⚠️ قبل الإطلاق

### الجانب القانوني (السعودية)
- [ ] استشارة محامي متخصص في الأنظمة المالية
- [ ] الحصول على ترخيص CMA (أو شراكة مع وسيط مرخص)
- [ ] التزام بنظام حماية البيانات (PDPL)
- [ ] إعداد سياسة خصوصية وشروط استخدام

### الجانب التقني
- [ ] تغيير كل المفاتيح الافتراضية
- [ ] تفعيل HTTPS
- [ ] إعداد نسخ احتياطية يومية
- [ ] إعداد monitoring وlogging
- [ ] اختبار penetration testing
- [ ] إعداد rate limiting

---

## خيارات النشر

### 1. AWS (موصى به للإنتاج)
- **Frontend**: CloudFront + S3
- **Backend**: ECS أو EC2
- **Database**: RDS PostgreSQL
- **Redis**: ElastiCache

### 2. DigitalOcean (مناسب للـ MVP)
- **Droplet** بـ 4GB RAM
- **Managed Database** PostgreSQL
- **Managed Redis**

### 3. STC Cloud / علي بابا (للسعودية)
- متوافق مع متطلبات SDAIA
- بيانات داخل المملكة

---

## النشر على Production

### 1. تجهيز السيرفر
```bash
# Ubuntu 22.04
sudo apt update && sudo apt upgrade -y
curl -fsSL https://get.docker.com | sh
sudo apt install docker-compose-plugin nginx certbot
```

### 2. استنساخ المشروع
```bash
git clone <your-repo> mursheed
cd mursheed
```

### 3. إعداد .env للإنتاج
```bash
# مفاتيح قوية!
SECRET_KEY=<32+ random chars>
ENCRYPTION_KEY=<32+ random chars>
DEBUG=False

# Production database
DATABASE_URL=postgresql+asyncpg://user:pass@your-db-host:5432/mursheed

# Production Redis
REDIS_URL=redis://your-redis-host:6379/0

# Production MetaApi (paid plan)
METAAPI_TOKEN=<your-paid-token>

# CORS - فقط الدومينات المسموح بها
CORS_ORIGINS=["https://mursheed.sa"]
```

### 4. nginx + SSL
```nginx
# /etc/nginx/sites-available/mursheed
server {
    listen 80;
    server_name mursheed.sa www.mursheed.sa;
    return 301 https://$host$request_uri;
}

server {
    listen 443 ssl http2;
    server_name mursheed.sa;

    ssl_certificate /etc/letsencrypt/live/mursheed.sa/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/mursheed.sa/privkey.pem;

    # Frontend
    location / {
        proxy_pass http://localhost:3000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection 'upgrade';
        proxy_set_header Host $host;
    }

    # Backend
    location /api/ {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### 5. SSL مع Let's Encrypt
```bash
sudo certbot --nginx -d mursheed.sa -d www.mursheed.sa
```

### 6. التشغيل
```bash
docker-compose -f docker-compose.prod.yml up -d
sudo systemctl restart nginx
```

---

## المراقبة والصيانة

### Logs
```bash
# Backend logs
docker-compose logs -f backend

# Postgres logs
docker-compose logs -f db
```

### النسخ الاحتياطية
```bash
# سكربت يومي
docker-compose exec db pg_dump -U mursheed > backup_$(date +%Y%m%d).sql
```

### مراقبة الصحة
أضف endpoint للمراقبة:
```bash
curl https://mursheed.sa/api/health
```

---

## Performance Optimization

### Backend
- تفعيل **gunicorn** workers بدل uvicorn المباشر:
```bash
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker
```

- تفعيل **Redis caching** للبيانات المتكررة

### Frontend
- بناء production:
```bash
npm run build
```
- خدمة الملفات الثابتة عبر CDN

### Database
- إضافة indexes على الجداول المستخدمة بكثرة
- تفعيل query caching

---

## التوسع (Scaling)

عند زيادة المستخدمين:

1. **استخدم Load Balancer** أمام Backend
2. **شغل عدة instances** من Backend
3. **استخدم Read Replicas** لـ PostgreSQL
4. **انقل إلى Kubernetes** للمرونة الكاملة

---

## مراجع

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [Docker in Production](https://docs.docker.com/config/containers/start-containers-automatically/)
- [PostgreSQL Backup](https://www.postgresql.org/docs/current/backup.html)
