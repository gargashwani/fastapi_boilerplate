# Redis Usage Guide

This guide explains how to use Redis for both **caching** and **message queue** (Celery) in this FastAPI boilerplate.

## Table of Contents

1. [Redis Configuration](#redis-configuration)
2. [Caching](#caching)
3. [Message Queue (Celery)](#message-queue-celery)
4. [Examples](#examples)

## Redis Configuration

### Environment Variables

Configure Redis in your `.env` file:

```env
# Redis Configuration
REDIS_HOST=localhost
REDIS_PORT=6379
REDIS_DB=0
REDIS_PASSWORD=  # Optional, leave empty if no password

# Cache Configuration
CACHE_PREFIX=cache:
CACHE_DEFAULT_TTL=3600  # Default TTL in seconds (1 hour)
CACHE_SERIALIZER=json   # Options: json, pickle
```

### Connection

Redis is used for:
- **Caching**: Store frequently accessed data
- **Message Queue**: Background task processing with Celery

## Caching

The boilerplate provides a Laravel-like caching interface through `app.core.cache`.

### Basic Usage

```python
from app.core.cache import cache

# Store a value
cache().put("key", "value", ttl=3600)  # TTL in seconds

# Get a value
value = cache().get("key")
value = cache().get("key", default="default_value")  # With default

# Check if key exists
if cache().has("key"):
    print("Key exists")

# Delete a value
cache().forget("key")

# Clear all cache
cache().flush()
```

### Remember Pattern (Cache-Aside)

The `remember` method is very useful - it gets from cache or executes a callback:

```python
from app.core.cache import cache
from app.models.user import User

# Get user from cache, or fetch from DB if not cached
user = cache().remember(
    f"user:{user_id}",
    ttl=300,  # 5 minutes
    callback=lambda: User.get(db, id=user_id)
)
```

### Advanced Operations

```python
# Store forever (no expiration)
cache().forever("key", "value")

# Add only if key doesn't exist
cache().add("key", "value", ttl=3600)

# Get and delete (pull)
value = cache().pull("key", default=None)

# Increment/Decrement numeric values
cache().increment("counter", amount=1)
cache().decrement("counter", amount=1)
```

### Tagged Cache

Group related cache keys:

```python
# Create tagged cache
tagged = cache().tags("users", "profile")

# Operations use tags automatically
tagged.put("user:1", user_data, ttl=3600)
tagged.get("user:1")
tagged.flush()  # Flush all keys with these tags
```

### Real-World Example

```python
from fastapi import Depends
from app.core.cache import cache
from app.core.database import get_db
from app.models.user import User

@router.get("/users/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    # Try cache first
    cache_key = f"user:{user_id}"
    user = cache().get(cache_key)
    
    if user is None:
        # Cache miss - fetch from database
        user = User.get(db, id=user_id)
        if user:
            # Store in cache for 5 minutes
            cache().put(cache_key, user, ttl=300)
    
    return user

@router.put("/users/{user_id}")
def update_user(user_id: int, db: Session = Depends(get_db)):
    user = User.update(db, ...)
    
    # Invalidate cache after update
    cache().forget(f"user:{user_id}")
    
    return user
```

## Message Queue (Celery)

Celery uses Redis as both the message broker and result backend.

### Configuration

Celery automatically uses Redis configuration from your `.env`:

```env
# Celery will use Redis settings automatically
# Or you can override:
CELERY_BROKER_URL=redis://localhost:6379/0
CELERY_RESULT_BACKEND=redis://localhost:6379/0
```

### Creating Tasks

Tasks are defined in `app/workers/tasks.py`:

```python
from app.core.celery_app import celery_app

@celery_app.task(name="send_email")
def send_email_task(email: str, subject: str, body: str):
    """Send email asynchronously."""
    # Your email sending logic here
    print(f"Sending email to {email}")
    return {"status": "sent"}

@celery_app.task(name="process_data")
def process_data_task(data_id: int):
    """Process data asynchronously."""
    # Your processing logic here
    return {"processed": data_id}
```

### Calling Tasks

```python
from app.workers.tasks import send_email_task, process_data_task

# Call task asynchronously
result = send_email_task.delay("user@example.com", "Subject", "Body")

# Get task result (blocking)
task_result = result.get(timeout=10)

# Call task with ETA (execute at specific time)
from datetime import datetime, timedelta
send_email_task.apply_async(
    args=["user@example.com", "Subject", "Body"],
    eta=datetime.utcnow() + timedelta(hours=1)
)

# Call task with countdown (execute after delay)
send_email_task.apply_async(
    args=["user@example.com", "Subject", "Body"],
    countdown=300  # Execute after 5 minutes
)
```

### Running Celery Worker

Start the Celery worker:

```bash
celery -A app.core.celery_app worker --loglevel=info
```

For development with auto-reload:

```bash
celery -A app.core.celery_app worker --loglevel=info --reload
```

### Monitoring with Flower

Flower is included for monitoring Celery tasks:

```bash
celery -A app.core.celery_app flower
```

Access at: http://localhost:5555

### Example: Background Email Sending

```python
# In your endpoint
from app.workers.tasks import send_welcome_email

@router.post("/register")
def register(user_data: UserCreate):
    user = User.create(db, obj_in=user_data)
    
    # Send welcome email in background
    send_welcome_email.delay(user.id)
    
    return user
```

## Examples

### Example 1: Caching Database Queries

```python
from app.core.cache import cache
from app.models.user import User

def get_active_users(db: Session):
    """Get active users with caching."""
    return cache().remember(
        "users:active",
        ttl=600,  # 10 minutes
        callback=lambda: User.get_multi(db, skip=0, limit=100)
    )
```

### Example 2: Cache Invalidation on Update

```python
@router.put("/users/{user_id}")
def update_user(user_id: int, db: Session = Depends(get_db)):
    user = User.update(db, ...)
    
    # Invalidate related cache
    cache().forget(f"user:{user_id}")
    cache().forget("users:active")  # Invalidate list cache
    
    return user
```

### Example 3: Using Cache Tags

```python
# Cache with tags
tagged = cache().tags("users")
tagged.put("profile:1", profile_data, ttl=3600)
tagged.put("settings:1", settings_data, ttl=3600)

# Flush all user-related cache
tagged.flush()  # Removes both profile:1 and settings:1
```

### Example 4: Background Task with Retry

```python
from celery import Task
from app.core.celery_app import celery_app

class RetryTask(Task):
    """Task with automatic retry on failure."""
    autoretry_for = (Exception,)
    retry_kwargs = {'max_retries': 3, 'countdown': 60}

@celery_app.task(base=RetryTask, name="process_payment")
def process_payment_task(payment_id: int):
    """Process payment with automatic retry."""
    # Your payment processing logic
    pass
```

## Best Practices

1. **Cache Keys**: Use descriptive, namespaced keys (e.g., `user:123`, `users:active`)
2. **TTL**: Set appropriate TTL based on data freshness requirements
3. **Cache Invalidation**: Always invalidate cache on data updates
4. **Error Handling**: Cache failures shouldn't break your application
5. **Monitoring**: Use Flower to monitor Celery tasks
6. **Connection Pooling**: Redis connection pooling is handled automatically

## Troubleshooting

### Redis Connection Error

```python
# Check Redis connection
from app.core.cache import cache
try:
    cache().put("test", "value")
    print("Redis connected!")
except Exception as e:
    print(f"Redis error: {e}")
```

### Celery Not Processing Tasks

1. Check if Celery worker is running
2. Verify Redis connection
3. Check Celery logs for errors
4. Ensure tasks are imported in `celery_app.py`

## Additional Resources

- [Redis Documentation](https://redis.io/documentation)
- [Celery Documentation](https://docs.celeryproject.org/)
- [FastAPI Background Tasks](https://fastapi.tiangolo.com/tutorial/background-tasks/)

