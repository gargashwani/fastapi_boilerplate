# Models

Data models and relationships for the FastAPI Boilerplate.

## Base Model

### Common Fields

```python
from sqlalchemy import Column, Integer, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class BaseModel(Base):
    __abstract__ = True
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, default=func.now(), onupdate=func.now())
```

## User Model

### User Fields

```python
from sqlalchemy import Column, String, Boolean, DateTime
from app.core.database import BaseModel

class User(BaseModel):
    __tablename__ = "users"

    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    last_login = Column(DateTime, nullable=True)
```

## Post Model

### Post Fields

```python
from sqlalchemy import Column, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import BaseModel

class Post(BaseModel):
    __tablename__ = "posts"

    title = Column(String, index=True)
    content = Column(Text)
    author_id = Column(Integer, ForeignKey("users.id"))
    
    author = relationship("User", back_populates="posts")
```

## Model Relationships

### One-to-Many

```python
# User model
class User(BaseModel):
    # ... other fields ...
    posts = relationship("Post", back_populates="author")

# Post model
class Post(BaseModel):
    # ... other fields ...
    author_id = Column(Integer, ForeignKey("users.id"))
    author = relationship("User", back_populates="posts")
```

### Many-to-Many

```python
# Association table
post_tags = Table(
    "post_tags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("posts.id")),
    Column("tag_id", Integer, ForeignKey("tags.id"))
)

# Post model
class Post(BaseModel):
    # ... other fields ...
    tags = relationship("Tag", secondary=post_tags, back_populates="posts")

# Tag model
class Tag(BaseModel):
    __tablename__ = "tags"
    name = Column(String, unique=True)
    posts = relationship("Post", secondary=post_tags, back_populates="tags")
```

## Model Methods

### Common Methods

```python
from sqlalchemy.orm import Session
from typing import Optional

class User(BaseModel):
    # ... fields ...

    @classmethod
    def get_by_email(cls, db: Session, email: str) -> Optional["User"]:
        return db.query(cls).filter(cls.email == email).first()

    @classmethod
    def get_by_id(cls, db: Session, id: int) -> Optional["User"]:
        return db.query(cls).filter(cls.id == id).first()

    def update(self, db: Session, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.commit()
        db.refresh(self)
        return self
```
