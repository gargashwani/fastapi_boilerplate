from typing import List, Optional
from pydantic_settings import BaseSettings
from pydantic import AnyHttpUrl, validator
from functools import lru_cache

class Settings(BaseSettings):
    # Database Configuration
    # Options: postgresql, postgres, mysql, mysql+pymysql
    # Similar to Laravel's DB_CONNECTION
    DB_CONNECTION: str = "postgresql"
    DB_HOST: str = "localhost"
    DB_PORT: int = 5432  # PostgreSQL default port (use 3306 for MySQL, 8889 for MAMP MySQL)
    DB_DATABASE: str = "fastapi_boilerplate"
    DB_USERNAME: str = "postgres"
    DB_PASSWORD: str = "postgres"
    
    # Optional: MySQL Unix Socket (for MAMP or local MySQL)
    DB_UNIX_SOCKET: Optional[str] = None
    
    # Optional: PostgreSQL SSL Mode (require, prefer, allow, disable)
    DB_SSL_MODE: Optional[str] = None

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
    
    # Cache Configuration
    CACHE_PREFIX: str = "cache:"
    CACHE_DEFAULT_TTL: int = 3600  # 1 hour in seconds
    CACHE_SERIALIZER: str = "json"  # Options: json, pickle

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

    # Celery Configuration (Message Queue)
    # These will be auto-generated from Redis config if not set
    CELERY_BROKER_URL: Optional[str] = None
    CELERY_RESULT_BACKEND: Optional[str] = None
    CELERY_WORKER_CONCURRENCY: int = 4
    CELERY_TASK_TIME_LIMIT: int = 1800
    CELERY_TASK_SOFT_TIME_LIMIT: int = 1200

    # Logging Configuration
    LOG_LEVEL: str = "INFO"
    LOG_FILE: str = "logs/app.log"
    LOG_MAX_SIZE: int = 10485760
    LOG_BACKUP_COUNT: int = 5
    
    # Scheduler Configuration
    APP_TIMEZONE: str = "UTC"  # Default timezone for scheduled tasks
    
    # Broadcasting Configuration
    BROADCAST_DRIVER: str = "redis"  # Options: redis, pusher, ably, log, null
    BROADCAST_CONNECTION: str = "default"  # Connection name for broadcasting
    
    # Pusher Configuration (for pusher driver)
    PUSHER_APP_ID: Optional[str] = None
    PUSHER_APP_KEY: Optional[str] = None
    PUSHER_APP_SECRET: Optional[str] = None
    PUSHER_APP_CLUSTER: str = "mt1"
    PUSHER_HOST: Optional[str] = None
    PUSHER_PORT: int = 443
    PUSHER_SCHEME: str = "https"
    PUSHER_ENCRYPTED: bool = True
    
    # Ably Configuration (for ably driver)
    ABLY_KEY: Optional[str] = None

    # Filesystem Configuration
    FILESYSTEM_DISK: str = "local"  # Options: local, s3, ftp, sftp
    FILESYSTEM_ROOT: str = "storage/app"  # Local storage root directory (private)
    FILESYSTEM_PUBLIC_ROOT: str = "public/storage"  # Public storage root directory (publicly accessible)
    FILESYSTEM_URL: Optional[str] = None  # Public URL for local storage (defaults to APP_URL/storage)
    
    # AWS S3 Configuration (for s3 disk)
    AWS_ACCESS_KEY_ID: Optional[str] = None
    AWS_SECRET_ACCESS_KEY: Optional[str] = None
    AWS_DEFAULT_REGION: str = "us-east-1"
    AWS_BUCKET: Optional[str] = None
    AWS_ENDPOINT: Optional[str] = None  # Optional: for S3-compatible services (e.g., DigitalOcean Spaces)
    
    # FTP Configuration (for ftp disk)
    FTP_HOST: str = "localhost"
    FTP_PORT: int = 21
    FTP_USERNAME: Optional[str] = None
    FTP_PASSWORD: Optional[str] = None
    
    # SFTP Configuration (for sftp disk)
    SFTP_HOST: str = "localhost"
    SFTP_PORT: int = 22
    SFTP_USERNAME: Optional[str] = None
    SFTP_PASSWORD: Optional[str] = None
    SFTP_KEY: Optional[str] = None  # Path to SSH private key

    class Config:
        env_file = ".env"
        case_sensitive = True

@lru_cache()
def get_settings() -> Settings:
    return Settings()

settings = get_settings() 