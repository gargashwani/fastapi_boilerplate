from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.security import get_current_user
from app.core.database import get_db
from app.core.cache import cache
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate
from app.core.policies import UserPolicy

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
    Update own user (with cache invalidation example).
    """
    UserPolicy.update(current_user, current_user.id)
    user = User.update(db, db_obj=current_user, obj_in=user_in)
    
    # Example: Invalidate cache after update
    cache().forget(f"user:{user.id}")
    
    return user

@router.get("/", response_model=List[UserResponse])
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
    user_data = cache().remember(
        cache_key,
        ttl=300,  # 5 minutes
        callback=lambda: User.get(db, id=user_id)
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
    Delete a user (with cache invalidation example).
    """
    user = User.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    UserPolicy.delete(current_user, user.id)
    
    # Example: Invalidate cache before deletion
    cache().forget(f"user:{user_id}")
    
    db.delete(user)
    db.commit()
    return user 