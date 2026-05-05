"""إعداد قاعدة البيانات - SQLAlchemy Async"""
from urllib.parse import urlparse, unquote
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.core.config import settings


class Base(DeclarativeBase):
    """القاعدة الأساسية لكل النماذج"""
    pass


def _create_engine_for_supabase():
    """
    إنشاء محرك خاص بـ Supabase pooler.
    سبب: الـ pooler يحتاج username يحوي نقطة (postgres.<ref>) وكلمات مرور قد تحوي رموز،
    والاعتماد على تفسير URL يكسر في asyncpg. نمرّر المعطيات مباشرة عبر connect_args.
    """
    url_str = settings.DATABASE_URL
    # إزالة +asyncpg علشان urlparse يفهمها
    parse_target = url_str.replace("postgresql+asyncpg://", "postgresql://", 1)
    parsed = urlparse(parse_target)

    connect_args = {
        "host": parsed.hostname,
        "port": parsed.port or 5432,
        "user": unquote(parsed.username or ""),
        "password": unquote(parsed.password or ""),
        "database": (parsed.path or "/postgres").lstrip("/"),
        "ssl": "require",
        "statement_cache_size": 0,  # ضروري لـ Supabase pooler
    }

    return create_async_engine(
        "postgresql+asyncpg://",
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
        connect_args=connect_args,
    )


def _create_engine_default():
    """محرك عادي للقواعد المحلية"""
    return create_async_engine(
        settings.DATABASE_URL,
        echo=settings.DEBUG,
        pool_pre_ping=True,
        pool_size=5,
        max_overflow=10,
    )


_url = settings.DATABASE_URL
if "supabase" in _url or "pooler" in _url:
    engine = _create_engine_for_supabase()
else:
    engine = _create_engine_default()

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
