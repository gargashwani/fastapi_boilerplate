# Requirements

System requirements and dependencies for the FastAPI Boilerplate project.

## System Requirements

### Minimum Requirements

*   Python 3.8 or higher
*   MySQL 5.7 or higher (with mysqlclient package)
*   PostgreSQL 12+ (alternative database with psycopg2-binary package)
*   Redis (for caching and background tasks)
*   4GB RAM minimum
*   2GB free disk space

### Recommended Requirements

*   Python 3.10 or higher
*   MySQL 8.0 or higher
*   Redis 6.0 or higher
*   8GB RAM or more
*   SSD storage

## Core Dependencies

### Main Packages

```text
fastapi==0.109.2
uvicorn==0.27.1
sqlalchemy==2.0.27
pydantic==2.6.1
python-jose==3.3.0
passlib==1.7.4
python-multipart==0.0.9
alembic==1.13.1
celery==5.3.6
redis==5.0.1
# Database drivers (install one based on your database choice)
mysqlclient==2.2.4  # For MySQL
psycopg2-binary==2.9.10  # For PostgreSQL
```

### Development Dependencies

```text
pytest==8.0.0
pytest-cov==4.1.0
black==24.1.1
isort==5.13.2
flake8==7.0.0
mypy==1.8.0
pre-commit==3.6.0
```

## Optional Dependencies

### Additional Features

*   Email Support (SMTP)
*   File Storage (AWS S3, Local)
*   Monitoring (Prometheus, Grafana)
*   Logging (ELK Stack)
*   API Documentation (Swagger UI, ReDoc)

## Compatibility

### Operating Systems

*   Linux (Ubuntu, Debian, CentOS)
*   macOS
*   Windows (with WSL recommended)

### Database Support

*   MySQL 5.7+
*   PostgreSQL 12+
*   SQLite (development only)
```
