# FastAPI Boilerplate

A modern, production-ready FastAPI boilerplate with a structure similar to Laravel.

## Features

- User authentication with JWT
- SQLAlchemy ORM
- Alembic database migrations
- Pydantic models and validation
- Environment configuration
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
│   │       └── api.py        # API router
│   ├── core/                 # Core functionality
│   │   ├── config.py         # Configuration
│   │   └── security.py       # Security utilities
│   ├── database/             # Database configuration
│   │   └── base.py           # Database base
│   ├── models/               # SQLAlchemy models
│   │   └── user.py           # User model
│   └── schemas/              # Pydantic schemas
│       ├── token.py          # Token schemas
│       └── user.py           # User schemas
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

5. Run database migrations:
```bash
alembic upgrade head
```

6. Start the development server:
```bash
python main.py
```

The API will be available at http://localhost:8000
API documentation will be available at http://localhost:8000/docs

## API Endpoints

### Authentication
- POST /api/v1/auth/register - Register a new user
- POST /api/v1/auth/login - Login and get access token

### Users
- GET /api/v1/users/me - Get current user
- PUT /api/v1/users/me - Update current user
- GET /api/v1/users - Get all users

## Development

### Running Tests
```bash
pytest
```

### Creating Migrations
```bash
alembic revision --autogenerate -m "description"
```

### Applying Migrations
```bash
alembic upgrade head
```

## Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details. 