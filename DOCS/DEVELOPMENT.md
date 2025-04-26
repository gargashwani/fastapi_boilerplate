# Development Guide

## Project Setup

### Prerequisites
- Python 3.8+
- PostgreSQL
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

1. Create a PostgreSQL database:
```bash
createdb fastapi_boilerplate
```

2. Run migrations:
```bash
alembic upgrade head
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
   - Ensure PostgreSQL is running
   - Verify database exists

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