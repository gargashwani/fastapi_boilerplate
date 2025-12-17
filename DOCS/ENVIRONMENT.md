# Environment Configuration Guide

This document explains all the environment variables used in the FastAPI boilerplate and their configuration options.

## Database Configuration

### DB_CONNECTION
- **Description**: Database connection type
- **Options**: `postgresql`, `postgres`, `mysql`, `mysql+pymysql`
- **Default**: `postgresql`
- **Note**: The same SQLAlchemy models work with both PostgreSQL and MySQL

### DB_HOST
- **Description**: Database server host address
- **Default**: `localhost`

### DB_PORT
- **Description**: Database server port number
- **Default**: `5432` (PostgreSQL), `3306` (MySQL), `8889` (MAMP MySQL)

### DB_DATABASE
- **Description**: Database name
- **Default**: `fastapi_boilerplate`

### DB_USERNAME
- **Description**: Database username
- **Default**: `postgres` (PostgreSQL), `root` (MySQL)

### DB_PASSWORD
- **Description**: Database password
- **Default**: `postgres` (PostgreSQL), `root` (MySQL)

### DB_UNIX_SOCKET
- **Description**: MySQL Unix socket path (optional)
- **Example**: `/Applications/MAMP/tmp/mysql/mysql.sock`
- **Default**: `None`
- **Note**: Only used for MySQL connections

### DB_SSL_MODE
- **Description**: PostgreSQL SSL mode (optional)
- **Options**: `require`, `prefer`, `allow`, `disable`
- **Default**: `None`
- **Note**: Only used for PostgreSQL connections

## Application Configuration

### APP_NAME
- **Description**: Application name
- **Default**: `FastAPI Boilerplate`

### APP_ENV
- **Description**: Application environment
- **Options**: `local`, `development`, `staging`, `production`
- **Default**: `local`

### APP_DEBUG
- **Description**: Enable/disable debug mode
- **Options**: `true`, `false`
- **Default**: `true`

### APP_URL
- **Description**: Application URL
- **Default**: `http://localhost:8000`

### APP_KEY
- **Description**: Application secret key for encryption
- **Note**: Generate a secure random key for production

## JWT Configuration

### JWT_SECRET
- **Description**: Secret key for JWT token generation
- **Note**: Generate a secure random key for production

### JWT_ALGORITHM
- **Description**: JWT algorithm
- **Options**: `HS256`, `RS256`, etc.
- **Default**: `HS256`

### JWT_EXPIRATION
- **Description**: JWT token expiration time in minutes
- **Default**: `3600` (1 hour)

## Redis Configuration

### REDIS_HOST
- **Description**: Redis server host address
- **Default**: `localhost`

### REDIS_PORT
- **Description**: Redis server port number
- **Default**: `6379`

### REDIS_DB
- **Description**: Redis database number
- **Range**: `0-15`
- **Default**: `0`

### REDIS_PASSWORD
- **Description**: Redis password (if required)
- **Default**: Empty

## Cache Configuration

### CACHE_PREFIX
- **Description**: Prefix for all cache keys
- **Default**: `cache:`
- **Example**: Keys will be stored as `cache:user:123`

### CACHE_DEFAULT_TTL
- **Description**: Default time-to-live for cached items in seconds
- **Default**: `3600` (1 hour)
- **Note**: Can be overridden per cache operation

### CACHE_SERIALIZER
- **Description**: Serialization method for cache values
- **Options**: `json`, `pickle`
- **Default**: `json`
- **Note**: JSON is faster but limited to basic types. Pickle supports all Python objects.

## Rate Limiting Configuration

### RATE_LIMIT
- **Description**: Maximum number of requests allowed per window
- **Default**: `100`

### RATE_LIMIT_WINDOW
- **Description**: Rate limit window in seconds
- **Default**: `60` (1 minute)

## CORS Configuration

### BACKEND_CORS_ORIGINS
- **Description**: Allowed origins for CORS
- **Format**: JSON array of URLs
- **Example**: `["http://localhost:3000","http://localhost:8000"]`

## Email Configuration

### MAIL_HOST
- **Description**: Email server host
- **Default**: `smtp.mailtrap.io`

### MAIL_PORT
- **Description**: Email server port
- **Default**: `2525`

### MAIL_USERNAME
- **Description**: Email username
- **Default**: `null`

### MAIL_PASSWORD
- **Description**: Email password
- **Default**: `null`

### MAIL_ENCRYPTION
- **Description**: Email encryption
- **Options**: `tls`, `ssl`, `none`
- **Default**: `tls`

### MAIL_FROM_ADDRESS
- **Description**: Default sender email
- **Default**: `hello@example.com`

### MAIL_FROM_NAME
- **Description**: Default sender name
- **Default**: `${APP_NAME}`

## Celery Configuration (Message Queue)

### CELERY_BROKER_URL
- **Description**: Celery broker URL (optional)
- **Default**: Auto-generated from Redis settings if not set
- **Format**: `redis://[password@]host:port/db`
- **Note**: If not set, will use Redis configuration from `REDIS_HOST`, `REDIS_PORT`, etc.

### CELERY_RESULT_BACKEND
- **Description**: Celery result backend URL (optional)
- **Default**: Auto-generated from Redis settings if not set
- **Format**: `redis://[password@]host:port/db`
- **Note**: If not set, will use Redis configuration from `REDIS_HOST`, `REDIS_PORT`, etc.

### CELERY_WORKER_CONCURRENCY
- **Description**: Number of worker processes
- **Default**: `4`

### CELERY_TASK_TIME_LIMIT
- **Description**: Hard time limit for tasks in seconds
- **Default**: `1800` (30 minutes)

### CELERY_TASK_SOFT_TIME_LIMIT
- **Description**: Soft time limit for tasks in seconds
- **Default**: `1200` (20 minutes)

## Logging Configuration

### LOG_LEVEL
- **Description**: Log level
- **Options**: `DEBUG`, `INFO`, `WARNING`, `ERROR`, `CRITICAL`
- **Default**: `INFO`

### LOG_FILE
- **Description**: Log file path
- **Default**: `logs/app.log`

### LOG_MAX_SIZE
- **Description**: Maximum log file size in bytes
- **Default**: `10485760` (10MB)

### LOG_BACKUP_COUNT
- **Description**: Number of backup logs to keep
- **Default**: `5`

## Setting Up Environment Variables

1. Copy the `.env.example` file to `.env`:
```bash
cp .env.example .env
```

2. Edit the `.env` file with your configuration:
```bash
nano .env
```

3. For production, make sure to:
   - Set `APP_ENV=production`
   - Set `APP_DEBUG=false`
   - Generate secure random keys for `APP_KEY` and `JWT_SECRET`
   - Configure proper database credentials
   - Set up proper CORS origins
   - Configure email settings
   - Set up Redis for production

## Environment-Specific Configuration

### Local Development
- Use local database
- Enable debug mode
- Use local Redis
- Set CORS to allow local development URLs

### Production
- Use production database
- Disable debug mode
- Use production Redis
- Set proper CORS origins
- Configure proper email settings
- Set up proper logging

## Security Considerations

1. Never commit `.env` files to version control
2. Use strong, random keys for `APP_KEY` and `JWT_SECRET`
3. Use environment-specific configurations
4. Regularly rotate secrets in production
5. Use HTTPS in production
6. Configure proper CORS settings
7. Set up proper rate limiting
8. Use secure database passwords
9. Configure proper Redis security
10. Set up proper email encryption 