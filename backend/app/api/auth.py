"""endpoints المصادقة - تسجيل وتسجيل دخول"""
from datetime import datetime, timezone
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import DbSession
from app.core.config import settings
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
)
from app.models.user import User
from app.schemas.schemas import (
    UserRegister,
    UserLogin,
    TokenResponse,
    UserResponse,
)


router = APIRouter()


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(data: UserRegister, db: DbSession):
    """إنشاء حساب جديد"""
    # التحقق من البريد
    result = await db.execute(select(User).where(User.email == data.email))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="البريد الإلكتروني مستخدم بالفعل",
        )

    # إنشاء المستخدم
    user = User(
        email=data.email,
        full_name=data.full_name,
        phone=data.phone,
        hashed_password=hash_password(data.password),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)

    # إنشاء token
    token = create_access_token(subject=user.id)
    return TokenResponse(
        access_token=token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )


@router.post("/login", response_model=TokenResponse)
async def login(data: UserLogin, db: DbSession):
    """تسجيل الدخول"""
    result = await db.execute(select(User).where(User.email == data.email))
    user = result.scalar_one_or_none()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="البريد الإلكتروني أو كلمة المرور غير صحيحة",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="الحساب غير مفعل",
        )

    # تحديث آخر دخول
    user.last_login = datetime.now(timezone.utc)
    await db.commit()

    # إنشاء token
    token = create_access_token(subject=user.id)
    return TokenResponse(
        access_token=token,
        expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES * 60,
    )
