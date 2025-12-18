# Services

Business logic and data access layer for the FastAPI Boilerplate.

## Base Service

### Service Structure

```python
from typing import List, Optional, Type, TypeVar
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.models.base import BaseModel as DBModel
from app.core.exceptions import NotFoundException

ModelType = TypeVar("ModelType", bound=DBModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)

class BaseService:
    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def get(self, db: Session, id: int) -> Optional[ModelType]:
        obj = db.query(self.model).filter(self.model.id == id).first()
        if not obj:
            raise NotFoundException()
        return obj

    async def list(
        self,
        db: Session,
        skip: int = 0,
        limit: int = 100
    ) -> List[ModelType]:
        return db.query(self.model).offset(skip).limit(limit).all()

    async def create(
        self,
        db: Session,
        obj_in: CreateSchemaType
    ) -> ModelType:
        obj_data = obj_in.dict()
        db_obj = self.model(**obj_data)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: Session,
        id: int,
        obj_in: UpdateSchemaType
    ) -> ModelType:
        db_obj = await self.get(db, id)
        update_data = obj_in.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_obj, field, value)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def delete(self, db: Session, id: int) -> None:
        db_obj = await self.get(db, id)
        db.delete(db_obj)
        db.commit()
```

## User Service

### User Operations

```python
from typing import Optional
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from app.models.user import User
from app.schemas.user import UserCreate, UserUpdate
from app.core.exceptions import NotFoundException
from app.core.security import get_password_hash, verify_password

class UserService(BaseService):
    def __init__(self):
        super().__init__(User)
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def get_by_email(self, db: Session, email: str) -> Optional[User]:
        return db.query(User).filter(User.email == email).first()

    async def create(self, db: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            full_name=obj_in.full_name,
            is_active=True
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def authenticate(
        self,
        db: Session,
        email: str,
        password: str
    ) -> Optional[User]:
        user = await self.get_by_email(db, email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    async def update(
        self,
        db: Session,
        id: int,
        obj_in: UserUpdate
    ) -> User:
        if obj_in.password:
            hashed_password = get_password_hash(obj_in.password)
            obj_in = obj_in.copy(update={"hashed_password": hashed_password})
        return await super().update(db, id, obj_in)
```

## Post Service

### Post Operations

```python
from typing import List, Optional
from sqlalchemy.orm import Session

from app.models.post import Post
from app.schemas.post import PostCreate, PostUpdate
from app.core.exceptions import NotFoundException, ForbiddenException

class PostService(BaseService):
    def __init__(self):
        super().__init__(Post)

    async def create(
        self,
        db: Session,
        obj_in: PostCreate,
        author_id: int
    ) -> Post:
        db_obj = Post(
            title=obj_in.title,
            content=obj_in.content,
            author_id=author_id
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    async def update(
        self,
        db: Session,
        id: int,
        obj_in: PostUpdate,
        author_id: int
    ) -> Post:
        post = await self.get(db, id)
        if post.author_id != author_id:
            raise ForbiddenException()
        return await super().update(db, id, obj_in)

    async def delete(
        self,
        db: Session,
        id: int,
        author_id: int
    ) -> None:
        post = await self.get(db, id)
        if post.author_id != author_id:
            raise ForbiddenException()
        await super().delete(db, id)
```

## Service Dependencies

### Dependency Injection

```python
from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.services.user import UserService
from app.services.post import PostService

def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService()

def get_post_service(db: Session = Depends(get_db)) -> PostService:
    return PostService()
```
