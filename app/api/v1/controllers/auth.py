from datetime import timedelta
from typing import Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.core import security
from app.core.broadcasting import broadcast
from app.core.database import get_db
from app.events.user_events import UserCreated
from app.jobs.tasks import process_user_data, send_welcome_email
from app.models.user import User
from app.schemas.token import TokenWithUser
from app.schemas.user import UserCreate, UserResponse
from config import settings

router = APIRouter()


@router.post("/login", response_model=TokenWithUser)
def login(
    db: Session = Depends(get_db), form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    OAuth2 compatible token login, get an access token and user information for future requests
    """
    user = User.authenticate(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=settings.JWT_EXPIRATION)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
        "user": user,
    }


@router.post("/register", response_model=UserResponse)
def register(
    *,
    db: Session = Depends(get_db),
    user_in: UserCreate,
) -> Any:
    """
    Create new user.
    Returns user information only. Use /login endpoint to get authorization token.
    """
    user = User.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = User.create(db, obj_in=user_in)

    # Queue background tasks
    send_welcome_email.delay(user.id)
    process_user_data.delay(user.id)

    # Example: Broadcast user created event
    event = UserCreated(user)
    broadcast().event(event)

    return user
