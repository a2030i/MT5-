"""اختبارات أساسية للـ API"""
import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_health_check():
    """اختبار صحة الخدمة"""
    from main import app
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "healthy"}


@pytest.mark.asyncio
async def test_root():
    """اختبار الصفحة الرئيسية"""
    from main import app
    async with AsyncClient(app=app, base_url="http://test") as client:
        response = await client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert data["name"] == "Mursheed API"


@pytest.mark.asyncio
async def test_register_validation():
    """اختبار التحقق من بيانات التسجيل"""
    from main import app
    async with AsyncClient(app=app, base_url="http://test") as client:
        # بريد غير صحيح
        response = await client.post("/api/auth/register", json={
            "email": "invalid",
            "full_name": "Test",
            "password": "12345678",
        })
        assert response.status_code == 422
