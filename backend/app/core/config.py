"""إعدادات التطبيق - يتم تحميلها من متغيرات البيئة"""
from typing import List, Union
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    # عام
    DEBUG: bool = False
    SECRET_KEY: str  # لـ JWT
    ENCRYPTION_KEY: str  # لـ AES-256 لتشفير بيانات MT5

    # قاعدة البيانات
    DATABASE_URL: str = "postgresql+asyncpg://mursheed:mursheed@db:5432/mursheed"

    # JWT
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # يوم واحد
    REFRESH_TOKEN_EXPIRE_DAYS: int = 30

    # CORS - في الإنتاج: قائمة مفصولة بفواصل عبر env
    CORS_ORIGINS: Union[str, List[str]] = [
        "http://localhost:3000",
        "http://localhost:5173",
    ]

    # MetaApi - الجسر مع MT5
    METAAPI_TOKEN: str = ""

    # Rate Limiting
    RATE_LIMIT_PER_MINUTE: int = 60

    @field_validator("DATABASE_URL")
    @classmethod
    def normalize_database_url(cls, v: str) -> str:
        """تطبيع رابط قاعدة البيانات: Supabase/Railway يعطي postgresql:// — نحتاج asyncpg"""
        if v.startswith("postgres://"):
            v = v.replace("postgres://", "postgresql+asyncpg://", 1)
        elif v.startswith("postgresql://") and "+asyncpg" not in v:
            v = v.replace("postgresql://", "postgresql+asyncpg://", 1)
        return v

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def parse_cors(cls, v):
        """يقبل قائمة أو سلسلة مفصولة بفواصل من env"""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",") if origin.strip()]
        return v


settings = Settings()
