"""endpoints التحليلات"""
from fastapi import APIRouter, HTTPException, status
from sqlalchemy import select

from app.api.deps import CurrentUser, DbSession
from app.models.mt5_account import MT5Account
from app.schemas.schemas import PerformanceStats
from app.services.metaapi_service import metaapi_service


router = APIRouter()


@router.get("/{account_id}/performance", response_model=PerformanceStats)
async def get_performance(
    account_id: str,
    user: CurrentUser,
    db: DbSession,
    days: int = 30,
):
    """حساب إحصائيات الأداء من سجل الصفقات"""
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

    # جلب السجل
    trades = await metaapi_service.get_history(
        account.metaapi_account_id, days=days
    )

    # الإحصائيات
    total = len(trades)
    if total == 0:
        return PerformanceStats(
            total_trades=0, winning_trades=0, losing_trades=0,
            win_rate=0, total_profit=0, total_loss=0, net_profit=0,
            profit_factor=0, max_drawdown=0, average_win=0, average_loss=0,
        )

    winning = [t for t in trades if t.profit > 0]
    losing = [t for t in trades if t.profit < 0]

    total_profit = sum(t.profit for t in winning)
    total_loss = abs(sum(t.profit for t in losing))
    net_profit = total_profit - total_loss

    return PerformanceStats(
        total_trades=total,
        winning_trades=len(winning),
        losing_trades=len(losing),
        win_rate=round(len(winning) / total * 100, 2) if total else 0,
        total_profit=round(total_profit, 2),
        total_loss=round(total_loss, 2),
        net_profit=round(net_profit, 2),
        profit_factor=round(total_profit / total_loss, 2) if total_loss > 0 else 0,
        max_drawdown=0,  # يحتاج حساب أعمق
        average_win=round(total_profit / len(winning), 2) if winning else 0,
        average_loss=round(total_loss / len(losing), 2) if losing else 0,
    )
