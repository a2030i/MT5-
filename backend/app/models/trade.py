"""نموذج الصفقات (للتسجيل المحلي والتحليل)"""
from datetime import datetime
from sqlalchemy import String, Float, DateTime, ForeignKey, Integer, func
from sqlalchemy.orm import Mapped, mapped_column
import uuid

from app.core.database import Base


class Trade(Base):
    """سجل الصفقات (نسخة محلية للتحليل السريع)"""
    __tablename__ = "trades"

    id: Mapped[str] = mapped_column(
        String(36), primary_key=True, default=lambda: str(uuid.uuid4())
    )
    user_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("users.id", ondelete="CASCADE"), nullable=False
    )
    mt5_account_id: Mapped[str] = mapped_column(
        String(36), ForeignKey("mt5_accounts.id", ondelete="CASCADE"), nullable=False
    )

    # معرف الصفقة في MT5
    mt5_ticket: Mapped[int] = mapped_column(Integer, nullable=False, index=True)

    symbol: Mapped[str] = mapped_column(String(20), nullable=False, index=True)
    type: Mapped[str] = mapped_column(String(10), nullable=False)  # BUY/SELL
    volume: Mapped[float] = mapped_column(Float, nullable=False)

    open_price: Mapped[float] = mapped_column(Float, nullable=False)
    close_price: Mapped[float] = mapped_column(Float, nullable=True)
    stop_loss: Mapped[float] = mapped_column(Float, nullable=True)
    take_profit: Mapped[float] = mapped_column(Float, nullable=True)

    profit: Mapped[float] = mapped_column(Float, default=0.0)
    commission: Mapped[float] = mapped_column(Float, default=0.0)
    swap: Mapped[float] = mapped_column(Float, default=0.0)

    open_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    close_time: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=True)

    status: Mapped[str] = mapped_column(String(20), default="open")  # open/closed

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )

    def __repr__(self) -> str:
        return f"<Trade {self.symbol} {self.type} {self.volume}>"
