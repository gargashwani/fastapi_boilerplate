import strawberry
from typing import List, Optional
from strawberry.types import Info
from sqlalchemy.orm import Session

from app.graphql.types import UserType
from app.models.user import User
from app.core.database import SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@strawberry.type
class Query:
    @strawberry.field
    def me(self, info: Info) -> Optional[UserType]:
        # Placeholder for actual auth logic
        # In a real app, we'd get the user from info.context
        return None

    @strawberry.field
    def users(self, info: Info) -> List[UserType]:
        db = SessionLocal()
        try:
            users = db.query(User).all()
            return [
                UserType(
                    id=user.id,
                    email=user.email,
                    full_name=user.full_name,
                    is_active=user.is_active,
                    is_superuser=user.is_superuser,
                    created_at=user.created_at,
                    updated_at=user.updated_at
                ) for user in users
            ]
        finally:
            db.close()

schema = strawberry.Schema(query=Query)
