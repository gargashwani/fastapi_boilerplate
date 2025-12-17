# Development Guide

## Project Setup

### Prerequisites
- Python 3.8+
- PostgreSQL or MySQL
- Redis (for caching and message queue)
- pip
- virtualenv (recommended)

### Environment Setup

1. Create and activate a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
```bash
cp .env.example .env
```
Edit the `.env` file with your configuration.

### Database Setup

**PostgreSQL:**
```bash
createdb fastapi_boilerplate
```

**MySQL:**
```bash
mysql -u root -p
CREATE DATABASE fastapi_boilerplate;
```

2. Configure database in `.env`:
```env
# For PostgreSQL
DB_CONNECTION=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=fastapi_boilerplate
DB_USERNAME=postgres
DB_PASSWORD=postgres

# For MySQL
DB_CONNECTION=mysql+pymysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=fastapi_boilerplate
DB_USERNAME=root
DB_PASSWORD=root
```

3. Run migrations:
```bash
alembic upgrade head
```

### Redis Setup

**macOS (Homebrew):**
```bash
brew install redis
brew services start redis
```

**Docker:**
```bash
docker run -d -p 6379:6379 redis:latest
```

**Linux:**
```bash
sudo apt-get install redis-server
sudo systemctl start redis
```

Verify Redis is running:
```bash
redis-cli ping
# Should return: PONG
```

## Development Workflow

### Running the Development Server
```bash
python main.py
```
The server will be available at http://localhost:8000

### API Documentation
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Database Migrations

#### Creating a new migration
```bash
alembic revision --autogenerate -m "description"
```

#### Applying migrations
```bash
alembic upgrade head
```

#### Rolling back migrations
```bash
alembic downgrade -1  # Roll back one migration
```

### Redis Caching

The boilerplate includes a Laravel-like caching interface:

```python
from app.core.cache import cache

# Store value
cache().put("key", "value", ttl=3600)

# Get value
value = cache().get("key", default=None)

# Cache-aside pattern (recommended)
user = cache().remember(
    f"user:{user_id}",
    ttl=300,
    callback=lambda: User.get(db, id=user_id)
)

# Invalidate cache
cache().forget("key")
```

See [Redis Usage Guide](REDIS_USAGE.md) for more examples.

### Background Tasks (Celery)

**Start Celery Worker:**
```bash
# Development (with auto-reload)
celery -A app.core.celery_app worker --loglevel=info --reload

# Production
celery -A app.core.celery_app worker --loglevel=info
```

**Monitor with Flower:**
```bash
celery -A app.core.celery_app flower
# Access at http://localhost:5555
```

**Create Background Tasks:**
```python
from app.core.celery_app import celery_app

@celery_app.task(name="send_email")
def send_email_task(email: str, subject: str):
    # Your task logic here
    pass

# Call the task
send_email_task.delay("user@example.com", "Hello")
```

### Testing

#### Running tests
```bash
pytest
```

#### Running tests with coverage
```bash
pytest --cov=app
```

## Code Structure

### Adding New Features

1. Create a new model in `app/models/`
2. Create corresponding schemas in `app/schemas/`
3. Create API endpoints in `app/api/v1/endpoints/`
4. Add the new router to `app/api/v1/api.py`
5. Create database migration if needed

### Best Practices

1. Use type hints for all function parameters and return values
2. Write docstrings for all functions and classes
3. Follow PEP 8 style guide
4. Write tests for new features
5. Use Pydantic models for request/response validation
6. Keep business logic in models or services
7. Use dependency injection for database sessions and other dependencies

### Error Handling

- Use FastAPI's built-in HTTPException for error responses
- Create custom exception classes in `app/core/exceptions.py` for specific error cases
- Use Pydantic validation for request data
- Implement proper error logging

### Security

- Always use HTTPS in production
- Implement proper authentication and authorization
- Use environment variables for sensitive data
- Implement rate limiting for API endpoints
- Use secure password hashing
- Implement proper CORS configuration

## Deployment

### Production Setup

1. Set up a production database
2. Configure environment variables for production
3. Set up a reverse proxy (Nginx/Apache)
4. Use a process manager (Gunicorn/Uvicorn)
5. Set up SSL certificates
6. Configure proper logging

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t fastapi_boilerplate .
```

2. Run the container:
```bash
docker run -p 8000:8000 fastapi_boilerplate
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests
5. Submit a pull request

## Troubleshooting

### Common Issues

1. Database connection errors
   - Check database credentials in `.env`
   - Ensure PostgreSQL/MySQL is running
   - Verify database exists
   - For MySQL with MAMP, check `DB_UNIX_SOCKET` path

2. Redis connection errors
   - Ensure Redis is running: `redis-cli ping`
   - Check Redis configuration in `.env`
   - Verify Redis port (default: 6379)

3. Celery worker not processing tasks
   - Ensure Redis is running
   - Check Celery worker is started
   - Verify tasks are imported in `celery_app.py`
   - Check Celery logs for errors

2. Migration errors
   - Check for conflicting migrations
   - Verify database schema matches models

3. Authentication issues
   - Check JWT configuration
   - Verify token expiration
   - Check user credentials

### Getting Help

- Check the documentation
- Search existing issues
- Create a new issue with detailed information
- Join the community chat 