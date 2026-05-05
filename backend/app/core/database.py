"""إعداد قاعدة البيانات - SQLAlchemy Async"""
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """القاعدة الأساسية لكل النماذج"""
    pass


def _build_engine_kwargs() -> dict:
    """خيارات المحرك - تمكين SSL للقواعد السحابية (Supabase/Neon/Railway)"""
    kwargs = {
        "echo": settings.DEBUG,
        "pool_pre_ping": True,
        "pool_size": 5,
        "max_overflow": 10,
    }
    url = settings.DATABASE_URL
    if any(host in url for host in ("supabase.co", "supabase.com", "neon.tech", "railway")):
        kwargs["connect_args"] = {"ssl": "require"}
    return kwargs


engine = create_async_engine(settings.DATABASE_URL, **_build_engine_kwargs())

async_session_maker = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


async def init_db():
    """إنشاء الجداول إن لم توجد - آمن للإنتاج (يعتمد IF NOT EXISTS)"""
    from app.models import user, mt5_account, trade  # noqa
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def get_db() -> AsyncSession:
    """Dependency للحصول على جلسة قاعدة بيانات"""
    async with async_session_maker() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
