"""
منصة مُرشد - نقطة الدخول الرئيسية
Mursheed Trading Platform - Main Entry Point
"""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from app.core.config import settings
from app.core.database import init_db
from app.api import auth, mt5, analytics, users


@asynccontextmanager
async def lifespan(app: FastAPI):
    """دورة حياة التطبيق - عند البدء والإيقاف"""
    logger.info("🚀 بدء تشغيل منصة مُرشد...")
    await init_db()
    logger.info("✓ قاعدة البيانات جاهزة")
    yield
    logger.info("👋 إيقاف منصة مُرشد")


app = FastAPI(
    title="Mursheed API",
    description="API لمنصة مُرشد العربية للتداول",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# CORS - السماح للواجهة الأمامية
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# تسجيل الـ routes
app.include_router(auth.router, prefix="/api/auth", tags=["المصادقة"])
app.include_router(users.router, prefix="/api/users", tags=["المستخدمون"])
app.include_router(mt5.router, prefix="/api/mt5", tags=["MetaTrader 5"])
app.include_router(analytics.router, prefix="/api/analytics", tags=["التحليلات"])


@app.get("/")
async def root():
    """نقطة فحص الحالة"""
    return {
        "name": "Mursheed API",
        "version": "1.0.0",
        "status": "running",
        "message": "أهلاً بك في منصة مُرشد",
    }


@app.get("/health")
async def health_check():
    """فحص صحة الخدمة"""
    return {"status": "healthy"}


if __name__ == "__main__":
    import os
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=settings.DEBUG,
    )
