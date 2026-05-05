"""
endpoints التعامل مع MT5
- ربط حساب
- جلب الرصيد والصفقات
- تنفيذ الصفقات
- إغلاق الصفقات
- جلب السجل
"""
from typing import List
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.core.security import encrypt_sensitive, decrypt_sensitive
from app.models.mt5_account import MT5Account
from app.schemas.schemas import (
    MT5ConnectRequest,
    MT5AccountResponse,
    AccountInfo,
    Position,
    HistoricalTrade,
    TradeRequest,
)
from app.services.metaapi_service import metaapi_service


router = APIRouter()


@router.post("/connect", response_model=MT5AccountResponse, status_code=status.HTTP_201_CREATED)
async def connect_mt5_account(
    data: MT5ConnectRequest,
    user: CurrentUser,
    db: DbSession,
):
    """ربط حساب MT5 جديد"""
    # التحقق من عدم وجود حساب مكرر
    existing = await db.execute(
        select(MT5Account).where(
            MT5Account.user_id == user.id,
            MT5Account.login == data.login,
            MT5Account.server == data.server,
        )
    )
    if existing.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="هذا الحساب مرتبط بالفعل",
        )

    # ربط الحساب في MetaApi
    try:
        metaapi_id = await metaapi_service.provision_account(
            login=data.login,
            password=data.password,
            server=data.server,
            nickname=data.nickname,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e),
        )

    # حفظ في قاعدة البيانات (كلمة المرور مشفرة)
    account = MT5Account(
        user_id=user.id,
        metaapi_account_id=metaapi_id,
        nickname=data.nickname,
        login=data.login,
        server=data.server,
        encrypted_password=encrypt_sensitive(data.password),
        connection_status="connected",
        is_demo="demo" in data.server.lower() or "trial" in data.server.lower(),
    )
    db.add(account)
    await db.commit()
    await db.refresh(account)

    return account


@router.get("/accounts", response_model=List[MT5AccountResponse])
async def list_mt5_accounts(user: CurrentUser, db: DbSession):
    """قائمة حسابات MT5 المرتبطة"""
    result = await db.execute(
        select(MT5Account).where(MT5Account.user_id == user.id)
    )
    return result.scalars().all()


async def _get_user_mt5_account(account_id: str, user: CurrentUser, db: DbSession) -> MT5Account:
    """التحقق من ملكية الحساب وإرجاعه"""
    result = await db.execute(
        select(MT5Account).where(
            MT5Account.id == account_id,
            MT5Account.user_id == user.id,
        )
    )
    account = result.scalar_one_or_none()
    if not account:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="حساب MT5 غير موجود",
        )
    return account


@router.get("/{account_id}/info", response_model=AccountInfo)
async def get_mt5_account_info(account_id: str, user: CurrentUser, db: DbSession):
    """جلب معلومات الرصيد"""
    account = await _get_user_mt5_account(account_id, user, db)
    return await metaapi_service.get_account_info(account.metaapi_account_id)


@router.get("/{account_id}/positions", response_model=List[Position])
async def get_mt5_positions(account_id: str, user: CurrentUser, db: DbSession):
    """جلب الصفقات المفتوحة"""
    account = await _get_user_mt5_account(account_id, user, db)
    return await metaapi_service.get_positions(account.metaapi_account_id)


@router.post("/{account_id}/trade")
async def execute_mt5_trade(
    account_id: str,
    trade: TradeRequest,
    user: CurrentUser,
    db: DbSession,
):
    """تنفيذ صفقة شراء أو بيع"""
    account = await _get_user_mt5_account(account_id, user, db)

    try:
        result = await metaapi_service.execute_trade(
            metaapi_account_id=account.metaapi_account_id,
            request=trade,
        )
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل تنفيذ الصفقة: {str(e)}",
        )


@router.delete("/{account_id}/positions/{ticket}")
async def close_mt5_position(
    account_id: str,
    ticket: int,
    user: CurrentUser,
    db: DbSession,
):
    """إغلاق صفقة"""
    account = await _get_user_mt5_account(account_id, user, db)

    try:
        result = await metaapi_service.close_position(
            metaapi_account_id=account.metaapi_account_id,
            ticket=ticket,
        )
        return {"success": True, "result": result}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"فشل إغلاق الصفقة: {str(e)}",
        )


@router.get("/{account_id}/history", response_model=List[HistoricalTrade])
async def get_mt5_history(
    account_id: str,
    user: CurrentUser,
    db: DbSession,
    days: int = 30,
):
    """جلب سجل الصفقات"""
    account = await _get_user_mt5_account(account_id, user, db)
    return await metaapi_service.get_history(account.metaapi_account_id, days=days)


@router.delete("/{account_id}", status_code=status.HTTP_204_NO_CONTENT)
async def disconnect_mt5_account(
    account_id: str,
    user: CurrentUser,
    db: DbSession,
):
    """إلغاء ربط حساب MT5"""
    account = await _get_user_mt5_account(account_id, user, db)
    await db.delete(account)
    await db.commit()
