# ⏱️ Build Your First API in 5 Minutes

Welcome! This tutorial will show you how to build a production-ready "Books" API using the FastAPI Boilerplate.

## 1. Create a Migration
Let's create a table for our books.

```bash
uv run python artisan make:migration create_books_table
```

Edit the generated file in `alembic/versions/` and add the `books` table:

```python
def upgrade() -> None:
    op.create_table(
        "books",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("title", sa.String(255), nullable=False),
        sa.Column("author", sa.String(255), nullable=False),
    )
```

Run the migration:
```bash
uv run python artisan migrate
```

## 2. Create the Model
Create `app/models/book.py`:

```python
from sqlalchemy import Column, Integer, String
from app.core.database import Base

class Book(Base):
    __tablename__ = "books"
    id = Column(Integer, primary_key=True)
    title = Column(String)
    author = Column(String)
```

## 3. Create the Schema
Create `app/schemas/book.py`:

```python
from pydantic import BaseModel

class BookCreate(BaseModel):
    title: str
    author: str

class BookResponse(BookCreate):
    id: int
    class Config:
        from_attributes = True
```

## 4. Create the Controller
Run the Artisan command to generate a controller:

```bash
uv run python artisan make:controller BookController
```

Implement the `create` logic in `app/api/v1/controllers/book.py`:

```python
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.models.book import Book
from app.schemas.book import BookCreate, BookResponse

router = APIRouter()

@router.post("/", response_model=BookResponse)
def create_book(book: BookCreate, db: Session = Depends(get_db)):
    db_book = Book(**book.model_dump())
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book
```

## 5. Register the Routes
Add to `routes/api.py`:

```python
from app.api.v1.controllers.book import router as book_router

router.include_router(book_router, prefix="/books", tags=["Books"])
```

## 🎉 Done!
Go to [http://localhost:8000/docs](http://localhost:8000/docs) to test your new API!

---

> [!TIP]
> Use `uv run python artisan make:controller --resource` to generate a full CRUD controller automatically!
