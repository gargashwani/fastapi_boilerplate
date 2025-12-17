# FastAPI Boilerplate

A modern, production-ready FastAPI boilerplate with a structure similar to Laravel.

## Features

- User authentication with JWT
- SQLAlchemy ORM with PostgreSQL & MySQL support
- Alembic database migrations
- Redis caching (Laravel-like Cache facade)
- Redis message queue with Celery
- Pydantic models and validation
- Environment configuration (Laravel-like)
- CORS support
- Type hints
- API documentation with Swagger UI

## Project Structure

```
fastapi_boilerplate/
├── alembic/                  # Database migrations
│   ├── versions/             # Migration files
│   ├── env.py                # Migration environment
│   └── script.py.mako        # Migration template
├── app/                      # Application package
│   ├── api/                  # API routes
│   │   └── v1/               # API version 1
│   │       ├── endpoints/    # API endpoints
│   │       │   ├── auth.py   # Authentication endpoints
│   │       │   └── users.py  # User endpoints
│   │       └── api.py        # API router
│   ├── core/                 # Core functionality
│   │   ├── config.py         # Configuration settings
│   │   ├── database.py       # Database configuration (PostgreSQL & MySQL)
│   │   ├── cache.py          # Redis caching (Laravel-like)
│   │   ├── celery_app.py     # Celery configuration
│   │   ├── security.py       # Security utilities (JWT, password hashing)
│   │   ├── middlewares.py    # Custom middlewares
│   │   ├── policies.py       # Authorization policies
│   │   └── gates.py          # Authorization gates
│   ├── models/               # SQLAlchemy models
│   │   └── user.py           # User model
│   ├── schemas/              # Pydantic schemas
│   │   ├── token.py          # Token schemas
│   │   └── user.py           # User schemas
│   └── workers/              # Background tasks
│       └── tasks.py          # Celery tasks
├── DOCS/                     # Documentation
│   ├── REDIS_USAGE.md        # Redis caching & message queue guide
│   ├── ENVIRONMENT.md        # Environment variables guide
│   └── DEVELOPMENT.md        # Development guide
├── tests/                    # Test files
├── .env.example              # Example environment variables
├── alembic.ini               # Alembic configuration
├── main.py                   # Application entry point
├── requirements.txt          # Python dependencies
└── README.md                 # Project documentation
```

## Getting Started

1. Clone the repository:
```bash
git clone https://github.com/yourusername/fastapi_boilerplate.git
cd fastapi_boilerplate
```

2. Create a virtual environment and activate it:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Copy the example environment file and configure it:
```bash
cp .env.example .env
```

5. Configure your database in `.env` file:
   - **PostgreSQL** (default):
     ```env
     DB_CONNECTION=postgresql
     DB_HOST=localhost
     DB_PORT=5432
     DB_DATABASE=fastapi_boilerplate
     DB_USERNAME=postgres
     DB_PASSWORD=postgres
     ```
   
   - **MySQL**:
     ```env
     DB_CONNECTION=mysql+pymysql
     DB_HOST=localhost
     DB_PORT=3306
     DB_DATABASE=fastapi_boilerplate
     DB_USERNAME=root
     DB_PASSWORD=root
     # Optional: For MAMP
     # DB_UNIX_SOCKET=/Applications/MAMP/tmp/mysql/mysql.sock
     ```

6. Run database migrations:
```bash
alembic upgrade head
```

7. Start the development server:
```bash
python main.py
```

The API will be available at http://localhost:8000
API documentation will be available at http://localhost:8000/docs

## API Endpoints

### Authentication
- `POST /api/v1/auth/register` - Register a new user
- `POST /api/v1/auth/login` - Login and get access token

### Users
- `GET /api/v1/users/me` - Get current user
- `PUT /api/v1/users/me` - Update current user
- `GET /api/v1/users` - Get all users (admin only)
- `GET /api/v1/users/{user_id}` - Get specific user
- `DELETE /api/v1/users/{user_id}` - Delete user (admin only)

### Documentation
- `GET /docs` - Swagger UI documentation
- `GET /redoc` - ReDoc documentation
- `GET /` - API welcome message

## Configuration

### Database Selection

The boilerplate supports both **PostgreSQL** and **MySQL**. Switch between them by changing `DB_CONNECTION` in your `.env` file:

**PostgreSQL (Default):**
```env
DB_CONNECTION=postgresql
DB_HOST=localhost
DB_PORT=5432
DB_DATABASE=fastapi_boilerplate
DB_USERNAME=postgres
DB_PASSWORD=postgres
```

**MySQL:**
```env
DB_CONNECTION=mysql+pymysql
DB_HOST=localhost
DB_PORT=3306
DB_DATABASE=fastapi_boilerplate
DB_USERNAME=root
DB_PASSWORD=root
# Optional: For MAMP
# DB_UNIX_SOCKET=/Applications/MAMP/tmp/mysql/mysql.sock
```

The same SQLAlchemy models work with both databases - no code changes needed!

### Redis Configuration

Redis is used for both **caching** and **message queue**. Configure in `.env`:

```env
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=

# Cache Configuration
CACHE_PREFIX=cache:
CACHE_DEFAULT_TTL=3600
CACHE_SERIALIZER=json
```

## Development

### Prerequisites

- Python 3.8+
- PostgreSQL or MySQL
- Redis (for caching and message queue)
- pip and virtualenv

### Running the Development Server

```bash
python main.py
```

The API will be available at:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### Database Migrations

```bash
# Create a new migration
alembic revision --autogenerate -m "description"

# Apply migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1
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

### Using Redis Cache

The boilerplate provides a Laravel-like caching interface:

```python
from app.core.cache import cache

# Basic operations
cache().put("key", "value", ttl=3600)
value = cache().get("key")
cache().forget("key")

# Cache-aside pattern (recommended)
user = cache().remember(
    f"user:{user_id}",
    ttl=300,
    callback=lambda: User.get(db, id=user_id)
)

# Advanced operations
cache().increment("counter")
cache().forever("key", "value")
tagged = cache().tags("users")
```

See [Redis Usage Guide](DOCS/REDIS_USAGE.md) for comprehensive examples.

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

**Using Tasks:**
```python
from app.workers.tasks import send_welcome_email

# Queue a background task
send_welcome_email.delay(user.id)
```

### Running Tests

```bash
# Run all tests
pytest

# With coverage
pytest --cov=app
```

## Documentation

- [Redis Usage Guide](DOCS/REDIS_USAGE.md) - Caching and message queue
- [Environment Variables](DOCS/ENVIRONMENT.md) - Complete configuration guide
- [Development Guide](DOCS/DEVELOPMENT.md) - Development workflow and best practices

## Key Features Explained

### Database Support
- **PostgreSQL & MySQL**: Switch databases via configuration - same ORM, same code
- **Alembic Migrations**: Version-controlled database schema changes
- **Connection Pooling**: Optimized database connections

### Redis Caching
- **Laravel-like API**: Familiar `cache().get()`, `cache().put()`, `cache().remember()` methods
- **Automatic Serialization**: JSON and pickle support
- **Tagged Cache**: Group related cache keys
- **TTL Support**: Automatic expiration

### Message Queue
- **Celery Integration**: Background task processing
- **Redis Backend**: Fast and reliable message broker
- **Task Monitoring**: Flower dashboard included
- **Retry Logic**: Built-in task retry support

### Security
- **JWT Authentication**: Secure token-based auth
- **Password Hashing**: bcrypt password encryption
- **Authorization**: Policy and Gate-based access control
- **CORS Support**: Configurable cross-origin requests
- **Rate Limiting**: Built-in request throttling

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 