"""
الأمان - JWT والتشفير
- JWT للمصادقة
- AES-256 لتشفير بيانات MT5 الحساسة
"""
import base64
from datetime import datetime, timedelta, timezone
from typing import Optional

from cryptography.fernet import Fernet
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.config import settings


# تشفير كلمات المرور
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    """تشفير كلمة المرور"""
    return pwd_context.hash(password)


def verify_password(plain: str, hashed: str) -> bool:
    """التحقق من كلمة المرور"""
    return pwd_context.verify(plain, hashed)


# JWT Tokens
def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """إنشاء access token"""
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {"sub": str(subject), "exp": expire, "type": "access"}
    return jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.JWT_ALGORITHM)


def decode_token(token: str) -> Optional[dict]:
    """فك تشفير الـ token"""
    try:
        return jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.JWT_ALGORITHM])
    except JWTError:
        return None


# AES-256 - لتشفير بيانات MT5 الحساسة (كلمات المرور)
def _get_cipher() -> Fernet:
    """الحصول على مفتاح التشفير"""
    # تحويل المفتاح لصيغة Fernet
    key = settings.ENCRYPTION_KEY.encode()
    if len(key) != 44:  # Fernet key length in base64
        # توليد مفتاح متوافق من السر
        import hashlib
        key = base64.urlsafe_b64encode(hashlib.sha256(key).digest())
    return Fernet(key)


def encrypt_sensitive(data: str) -> str:
    """تشفير بيانات حساسة (مثل كلمة مرور MT5)"""
    cipher = _get_cipher()
    return cipher.encrypt(data.encode()).decode()


def decrypt_sensitive(encrypted: str) -> str:
    """فك تشفير بيانات حساسة"""
    cipher = _get_cipher()
    return cipher.decrypt(encrypted.encode()).decode()
