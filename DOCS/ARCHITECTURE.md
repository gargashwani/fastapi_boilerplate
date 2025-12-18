# Architecture

Project structure and design patterns used in the FastAPI Boilerplate.

## Project Structure

### Directory Layout

```text
fastapi_boilerplate/
├── app/
│   ├── api/
│   │   └── v1/
│   │       ├── controllers/
│   │       └── api.py
│   ├── controllers/
│   ├── core/
│   │   ├── config.py
│   │   ├── database.py
│   │   └── security.py
│   ├── models/
│   ├── schemas/
│   └── services/
├── alembic/
│   └── versions/
├── docs/
├── tests/
└── .env
```

## Design Patterns

### Repository Pattern

The repository pattern is used to abstract the data layer, making it easier to swap out implementations or test the application.

```python
class UserRepository:
    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: int) -> Optional[User]:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> Optional[User]:
        return self.db.query(User).filter(User.email == email).first()
```

### Service Layer

The service layer contains business logic and orchestrates operations between repositories and other services.

```python
class UserService:
    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def create_user(self, user_data: UserCreate) -> User:
        if await self.user_repository.get_by_email(user_data.email):
            raise HTTPException(
                status_code=400,
                detail="Email already registered"
            )
        return await self.user_repository.create(user_data)
```

## Dependency Injection

### FastAPI Dependencies

FastAPI's dependency injection system is used to manage dependencies and provide them to route handlers.

```python
async def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=UserResponse)
async def create_user(
    user: UserCreate,
    db: Session = Depends(get_db),
    user_service: UserService = Depends()
):
    return await user_service.create_user(user)
```

## Error Handling

### Custom Exception Handler

```python
from fastapi import Request, status
from fastapi.responses import JSONResponse
from app.core.exceptions import CustomException

@app.exception_handler(CustomException)
async def custom_exception_handler(request: Request, exc: CustomException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "detail": exc.detail,
            "error_code": exc.error_code
        }
    )
```
