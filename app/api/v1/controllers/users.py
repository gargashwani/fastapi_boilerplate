from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.core.broadcasting import broadcast
from app.core.cache import cache
from app.core.database import get_db
from app.core.policies import UserPolicy
from app.core.security import get_current_user
from app.events.user_events import UserDeleted, UserUpdated
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter()


@router.get("/me", response_model=UserResponse)
def read_user_me(
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserResponse)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Update own user (with cache invalidation and broadcasting example).
    """
    UserPolicy.update(current_user, current_user.id)
    user = User.update(db, db_obj=current_user, obj_in=user_in)

    # Example: Invalidate cache after update
    cache().forget(f"user:{user.id}")

    # Example: Broadcast user update event
    event = UserUpdated(user)
    broadcast().event(event)

    return user


@router.get("/", response_model=list[UserResponse])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Retrieve users.
    """
    UserPolicy.view_any(current_user)
    users = User.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=UserResponse)
def read_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Get a specific user (with caching example).
    """
    UserPolicy.view(current_user, user_id)

    # Example: Cache user data for 5 minutes
    cache_key = f"user:{user_id}"
    
    def get_user_data():
        user = User.get(db, id=user_id)
        if user:
            # Convert User model to UserResponse schema for JSON serialization
            return UserResponse.model_validate(user).model_dump()
        return None
    
    user_data = cache().remember(
        cache_key,
        ttl=300,  # 5 minutes
        callback=get_user_data,
    )

    if not user_data:
        raise HTTPException(status_code=404, detail="User not found")

    return user_data


@router.delete("/{user_id}", response_model=UserResponse)
def delete_user(
    user_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> Any:
    """
    Delete a user (with cache invalidation and broadcasting example).
    """
    user = User.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    UserPolicy.delete(current_user, user.id)

    # Example: Invalidate cache before deletion
    cache().forget(f"user:{user_id}")

    # Example: Broadcast user deletion event
    event = UserDeleted(user_id)
    broadcast().event(event)

    db.delete(user)
    db.commit()
    return user
