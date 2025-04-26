from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
from functools import lru_cache

class Settings(BaseSettings):
    # Database Configuration
    DB_CONNECTION: str = "postgresql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432
    DB_DATABASE: str = "fastapi_boilerplate"
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "postgres"

    # Application Configuration
    APP_NAME: str = "FastAPI Boilerplate"
    APP_ENV: str = "local"
    APP_DEBUG: bool = True
    APP_URL: str = "http://localhost:8000"
    APP_KEY: str = "your-secret-key-here"

    # JWT Configuration
    JWT_SECRET: str = "your-jwt-secret-key-here"
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRATION: int = 3600

    # Redis Configuration
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None

    # Rate Limiting Configuration
    RATE_LIMIT: int = 100
    RATE_LIMIT_WINDOW: int = 60

    # CORS Configuration
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:8000"]

    # Email Configuration
    MAIL_HOST: str = "smtp.mailtrap.io"
    MAIL_PORT: int = 2525
    MAIL_USERNAME: Optional[str] = None
    MAIL_PASSWORD: Optional[str] = None
    MAIL_ENCRYPTION: str = "tls"
    MAIL_FROM_ADDRESS: str = "hello@example.com"
    MAIL_FROM_NAME: str = "FastAPI Boilerplate"

    # Celery Configuration
    CELERY_BROKER_URL: str = "redis://localhost:6379/0"
    CELERY_RESULT_BACKEND: str = "redis://localhost:6379/0"
    CELERY_WORKER_CONCURRENCY: int = 4
    CELERY_TASK_TIME_LIMIT: int = 1800
    CELERY_TASK_SOFT_TIME_LIMIT: int = 1200

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_SIZE: int = 10485760
    LOG_BACKUP_COUNT: int = 5

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 