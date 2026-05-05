"""نموذج حساب MT5"""
from datetime import datetime
from sqlalchemy import String, Boolean, DateTime, ForeignKey, Text, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
import uuid
from typing import TYPE_CHECKING

from app.core.database import Base

if TYPE_CHECKING:
    from app.models.user import User


class MT5Account(Base):
    """حسابات MT5 المرتبطة"""
    __tablename__ = "mt5_accounts"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )

    # معرف MetaApi (يُنشأ بعد ربط الحساب)
    metaapi_account_id: Mapped[str] = mapped_column(String(255), nullable=True)

    # بيانات الحساب
    nickname: Mapped[str] = mapped_column(String(100), nullable=True)  # اسم تعريفي
    login: Mapped[str] = mapped_column(String(50), nullable=False)  # رقم الحساب
    server: Mapped[str] = mapped_column(String(255), nullable=False)  # السيرفر
    broker_name: Mapped[str] = mapped_column(String(255), nullable=True)

    # كلمة المرور مشفرة بـ AES-256
    encrypted_password: Mapped[str] = mapped_column(Text, nullable=False)

    # نوع الحساب
    is_demo: Mapped[bool] = mapped_column(Boolean, default=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    # الحالة
    last_sync: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)
    connection_status: Mapped[str] = mapped_column(
        String(20), default="pending"  # pending, connected, error
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    # علاقات
    user: Mapped["User"] = relationship("User", back_populates="mt5_accounts")

    def __repr__(self) -> str:
        return f"<MT5Account login={self.login} server={self.server}>"
