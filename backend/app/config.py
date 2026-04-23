from functools import lru_cache
from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://admin:cont123456@localhost:5432/contabilidad"
    SECRET_KEY: str = "django-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7
    
    POSTGRES_HOST: str = "localhost"
    POSTGRES_DB: str = "contabilidad"
    POSTGRES_USER: str = "admin"
    POSTGRES_PASSWORD: str = "cont123456"
    
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()