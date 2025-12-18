# Controllers

API controllers and route handlers for the FastAPI Boilerplate.

## Base Controller

### Controller Structure

```python
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from app.core.database import get_db
from app.schemas import BaseSchema
from app.services import BaseService

class BaseController:
    def __init__(self, service: BaseService):
        self.service = service
        self.router = APIRouter()
        self._register_routes()

    def _register_routes(self):
        raise NotImplementedError("Subclasses must implement _register_routes")
```

## User Controller

### User Routes

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.user import UserCreate, UserUpdate, UserResponse
from app.services.user import UserService
from app.models.user import User

class UserController(BaseController):
    def __init__(self, service: UserService):
        super().__init__(service)

    def _register_routes(self):
        self.router.post("/", response_model=UserResponse)(self.create)
        self.router.get("/me", response_model=UserResponse)(self.get_me)
        self.router.get("/{user_id}", response_model=UserResponse)(self.get)
        self.router.put("/{user_id}", response_model=UserResponse)(self.update)
        self.router.delete("/{user_id}")(self.delete)

    async def create(self, user: UserCreate, db: Session = Depends(get_db)):
        return await self.service.create(db, user)

    async def get_me(self, current_user: User = Depends(get_current_user)):
        return current_user

    async def get(self, user_id: int, db: Session = Depends(get_db)):
        return await self.service.get(db, user_id)

    async def update(
        self,
        user_id: int,
        user: UserUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        if current_user.id != user_id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return await self.service.update(db, user_id, user)

    async def delete(
        self,
        user_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        if current_user.id != user_id and not current_user.is_superuser:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return await self.service.delete(db, user_id)
```

## Post Controller

### Post Routes

```python
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.core.database import get_db
from app.core.auth import get_current_user
from app.schemas.post import PostCreate, PostUpdate, PostResponse
from app.services.post import PostService
from app.models.user import User

class PostController(BaseController):
    def __init__(self, service: PostService):
        super().__init__(service)

    def _register_routes(self):
        self.router.post("/", response_model=PostResponse)(self.create)
        self.router.get("/", response_model=List[PostResponse])(self.list)
        self.router.get("/{post_id}", response_model=PostResponse)(self.get)
        self.router.put("/{post_id}", response_model=PostResponse)(self.update)
        self.router.delete("/{post_id}")(self.delete)

    async def create(
        self,
        post: PostCreate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        return await self.service.create(db, post, current_user.id)

    async def list(
        self,
        skip: int = 0,
        limit: int = 100,
        db: Session = Depends(get_db)
    ):
        return await self.service.list(db, skip, limit)

    async def get(self, post_id: int, db: Session = Depends(get_db)):
        return await self.service.get(db, post_id)

    async def update(
        self,
        post_id: int,
        post: PostUpdate,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        return await self.service.update(db, post_id, post, current_user.id)

    async def delete(
        self,
        post_id: int,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
    ):
        return await self.service.delete(db, post_id, current_user.id)
```

## Error Handling

### Custom Exceptions

```python
from fastapi import HTTPException, status

class NotFoundException(HTTPException):
    def __init__(self, detail: str = "Resource not found"):
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=detail
        )

class UnauthorizedException(HTTPException):
    def __init__(self, detail: str = "Not authenticated"):
        super().__init__(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail
        )

class ForbiddenException(HTTPException):
    def __init__(self, detail: str = "Not enough permissions"):
        super().__init__(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=detail
        )
```
