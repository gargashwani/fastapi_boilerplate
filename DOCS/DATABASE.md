# Database

Database configuration and models for the FastAPI Boilerplate.

## Database Configuration

### Environment Variables

```env
# Database Configuration
DATABASE_URL=mysql://user:password@localhost/db_name
# or for PostgreSQL
# DATABASE_URL=postgresql://user:password@localhost/db_name

# Database Pool Settings
DB_POOL_SIZE=5
DB_MAX_OVERFLOW=10
DB_POOL_TIMEOUT=30
DB_POOL_RECYCLE=1800
```

### Database Connection

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

engine = create_engine(
    settings.DATABASE_URL,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    pool_recycle=settings.DB_POOL_RECYCLE
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

## Database Migrations

### Creating Migrations

```bash
# Create new migration
python3 artisan make-migration "migration message"

# Run migrations
python3 artisan migrate

# Rollback last migration
python3 artisan rollback

# Show migration history
python3 artisan migrate:status
```

## Database Models

### Base Model

```python
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
```

### User Model

```python
from sqlalchemy import Column, String, Boolean
from app.core.database import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
```

## Database Transactions

### Transaction Management

```python
from contextlib import contextmanager
from sqlalchemy.orm import Session

@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
        db.commit()
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()
```
