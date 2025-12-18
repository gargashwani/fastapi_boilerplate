import strawberry
from datetime import datetime
from typing import Optional

@strawberry.type
class UserType:
    id: int
    email: str
    full_name: Optional[str]
    is_active: bool
    is_superuser: bool
    created_at: datetime
    updated_at: datetime
