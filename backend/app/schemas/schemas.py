"""Pydantic schemas - للتحقق من البيانات"""
from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# === المصادقة ===
class UserRegister(BaseModel):
    """طلب إنشاء حساب"""
    email: EmailStr
    full_name: str = Field(..., min_length=3, max_length=255)
    phone: Optional[str] = Field(None, pattern=r"^\+?[0-9\s\-]+$")
    password: str = Field(..., min_length=8, max_length=100)


class UserLogin(BaseModel):
    """طلب تسجيل دخول"""
    email: EmailStr
    password: str


class TokenResponse(BaseModel):
    """استجابة الـ token"""
    access_token: str
    token_type: str = "bearer"
    expires_in: int  # بالثواني


class UserResponse(BaseModel):
    """بيانات المستخدم"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    email: str
    full_name: str
    phone: Optional[str] = None
    is_verified: bool
    has_2fa: bool
    created_at: datetime


# === MT5 ===
class MT5ConnectRequest(BaseModel):
    """طلب ربط حساب MT5"""
    login: str = Field(..., description="رقم الحساب")
    password: str = Field(..., description="كلمة المرور")
    server: str = Field(..., description="اسم السيرفر مثل XMGlobal-MT5")
    nickname: Optional[str] = Field(None, max_length=100, description="اسم تعريفي اختياري")


class MT5AccountResponse(BaseModel):
    """معلومات حساب MT5"""
    model_config = ConfigDict(from_attributes=True)

    id: str
    nickname: Optional[str] = None
    login: str
    server: str
    broker_name: Optional[str] = None
    is_demo: bool
    connection_status: str
    last_sync: Optional[datetime] = None
    created_at: datetime


class AccountInfo(BaseModel):
    """معلومات الرصيد من MT5"""
    balance: float
    equity: float
    margin: float
    free_margin: float
    margin_level: float
    currency: str
    leverage: int
    profit: float


# === التداول ===
class TradeRequest(BaseModel):
    """طلب تنفيذ صفقة"""
    symbol: str = Field(..., description="الرمز مثل EURUSD")
    type: str = Field(..., pattern="^(BUY|SELL)$", description="نوع الصفقة")
    volume: float = Field(..., gt=0, le=100, description="حجم الصفقة")
    stop_loss: Optional[float] = Field(None, description="وقف الخسارة")
    take_profit: Optional[float] = Field(None, description="جني الأرباح")
    comment: Optional[str] = Field(None, max_length=255)


class Position(BaseModel):
    """صفقة مفتوحة"""
    ticket: int
    symbol: str
    type: str
    volume: float
    open_price: float
    current_price: float
    stop_loss: Optional[float] = None
    take_profit: Optional[float] = None
    profit: float
    swap: float
    commission: float
    open_time: datetime


class HistoricalTrade(BaseModel):
    """صفقة من السجل"""
    ticket: int
    symbol: str
    type: str
    volume: float
    open_price: float
    close_price: float
    profit: float
    open_time: datetime
    close_time: datetime


# === التحليلات ===
class PerformanceStats(BaseModel):
    """إحصائيات الأداء"""
    total_trades: int
    winning_trades: int
    losing_trades: int
    win_rate: float  # نسبة مئوية
    total_profit: float
    total_loss: float
    net_profit: float
    profit_factor: float
    max_drawdown: float
    average_win: float
    average_loss: float
