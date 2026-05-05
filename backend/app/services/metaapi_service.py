"""
خدمة MetaApi - الجسر مع MetaTrader 5

تستخدم MetaApi.cloud SDK للتواصل مع حسابات MT5 سحابياً.
هذا أفضل من MetaTrader5 Python package لأن:
1. يدعم آلاف الحسابات بنفس الوقت
2. يشتغل من أي نظام تشغيل
3. لا يحتاج تيرمنال MT5 مفتوح
"""
from typing import List, Optional
from loguru import logger
from metaapi_cloud_sdk import MetaApi

from app.core.config import settings
from app.schemas.schemas import (
    AccountInfo,
    Position,
    HistoricalTrade,
    TradeRequest,
)


class MetaApiService:
    """خدمة التعامل مع MT5 عبر MetaApi"""

    def __init__(self):
        self._api: Optional[MetaApi] = None

    async def _get_api(self) -> MetaApi:
        """الحصول على instance من MetaApi"""
        if self._api is None:
            self._api = MetaApi(settings.METAAPI_TOKEN)
        return self._api

    async def provision_account(
        self,
        login: str,
        password: str,
        server: str,
        nickname: Optional[str] = None,
    ) -> str:
        """
        إنشاء حساب MT5 في MetaApi (الخطوة الأولى للربط).

        Returns:
            metaapi_account_id: معرف الحساب في MetaApi
        """
        api = await self._get_api()

        try:
            account = await api.metatrader_account_api.create_account({
                "name": nickname or f"حساب {login}",
                "type": "cloud",
                "login": login,
                "password": password,
                "server": server,
                "platform": "mt5",
                "magic": 0,
            })

            # نشر الحساب وانتظار الاتصال
            await account.deploy()
            await account.wait_connected()

            logger.info(f"✓ تم ربط حساب MT5 {login} بنجاح")
            return account.id

        except Exception as e:
            logger.error(f"✗ فشل ربط حساب MT5 {login}: {e}")
            raise ValueError(f"فشل الاتصال بـ MT5: {str(e)}")

    async def get_account_info(self, metaapi_account_id: str) -> AccountInfo:
        """جلب معلومات الرصيد"""
        api = await self._get_api()
        account = await api.metatrader_account_api.get_account(metaapi_account_id)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        info = await connection.get_account_information()

        return AccountInfo(
            balance=info["balance"],
            equity=info["equity"],
            margin=info["margin"],
            free_margin=info["freeMargin"],
            margin_level=info.get("marginLevel", 0),
            currency=info["currency"],
            leverage=info["leverage"],
            profit=info.get("profit", 0),
        )

    async def get_positions(self, metaapi_account_id: str) -> List[Position]:
        """جلب الصفقات المفتوحة"""
        api = await self._get_api()
        account = await api.metatrader_account_api.get_account(metaapi_account_id)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        positions_raw = await connection.get_positions()

        return [
            Position(
                ticket=p["id"],
                symbol=p["symbol"],
                type="BUY" if p["type"] == "POSITION_TYPE_BUY" else "SELL",
                volume=p["volume"],
                open_price=p["openPrice"],
                current_price=p["currentPrice"],
                stop_loss=p.get("stopLoss"),
                take_profit=p.get("takeProfit"),
                profit=p["profit"],
                swap=p.get("swap", 0),
                commission=p.get("commission", 0),
                open_time=p["time"],
            )
            for p in positions_raw
        ]

    async def execute_trade(
        self, metaapi_account_id: str, request: TradeRequest
    ) -> dict:
        """تنفيذ صفقة شراء أو بيع"""
        api = await self._get_api()
        account = await api.metatrader_account_api.get_account(metaapi_account_id)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        # تحديد نوع الصفقة
        if request.type == "BUY":
            result = await connection.create_market_buy_order(
                symbol=request.symbol,
                volume=request.volume,
                stop_loss=request.stop_loss,
                take_profit=request.take_profit,
                options={"comment": request.comment or "via Mursheed"},
            )
        else:  # SELL
            result = await connection.create_market_sell_order(
                symbol=request.symbol,
                volume=request.volume,
                stop_loss=request.stop_loss,
                take_profit=request.take_profit,
                options={"comment": request.comment or "via Mursheed"},
            )

        logger.info(f"✓ تم تنفيذ صفقة {request.type} {request.symbol}")
        return result

    async def close_position(
        self, metaapi_account_id: str, ticket: int
    ) -> dict:
        """إغلاق صفقة"""
        api = await self._get_api()
        account = await api.metatrader_account_api.get_account(metaapi_account_id)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        result = await connection.close_position(ticket)
        logger.info(f"✓ تم إغلاق الصفقة #{ticket}")
        return result

    async def get_history(
        self, metaapi_account_id: str, days: int = 30
    ) -> List[HistoricalTrade]:
        """جلب سجل الصفقات"""
        from datetime import datetime, timedelta

        api = await self._get_api()
        account = await api.metatrader_account_api.get_account(metaapi_account_id)
        connection = account.get_rpc_connection()
        await connection.connect()
        await connection.wait_synchronized()

        end_time = datetime.utcnow()
        start_time = end_time - timedelta(days=days)

        deals = await connection.get_deals_by_time_range(start_time, end_time)

        # تجميع الصفقات (deals تأتي كـ open + close)
        trades = []
        for deal in deals:
            if deal.get("entryType") == "DEAL_ENTRY_OUT":  # إغلاق
                trades.append(
                    HistoricalTrade(
                        ticket=deal["positionId"],
                        symbol=deal["symbol"],
                        type="BUY" if deal["type"] == "DEAL_TYPE_SELL" else "SELL",
                        volume=deal["volume"],
                        open_price=deal.get("openPrice", 0),
                        close_price=deal["price"],
                        profit=deal.get("profit", 0),
                        open_time=deal.get("openTime", deal["time"]),
                        close_time=deal["time"],
                    )
                )

        return trades


# Singleton
metaapi_service = MetaApiService()
