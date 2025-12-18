import hashlib
from datetime import datetime, timedelta, timezone
from typing import Any

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from jose.exceptions import JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.core.database import get_db
from config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")

# Bcrypt has a 72-byte limit. For longer passwords, we pre-hash with SHA-256
# This allows passwords of any length while maintaining security
BCRYPT_MAX_LENGTH = 72


def create_access_token(
    subject: str | Any, expires_delta: timedelta | None = None
) -> str:
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRATION)
    to_encode = {"exp": expire, "sub": str(subject)}
    encoded_jwt = jwt.encode(
        to_encode, settings.JWT_SECRET, algorithm=settings.JWT_ALGORITHM
    )
    return encoded_jwt


def _prepare_password_for_bcrypt(password: str) -> str:
    """
    Prepare password for bcrypt hashing.
    Bcrypt has a 72-byte limit, so for longer passwords we pre-hash with SHA-256.
    This allows passwords of any length while maintaining security.

    Args:
        password: Plain text password

    Returns:
        Password ready for bcrypt (either original or SHA-256 hash)
    """
    password_bytes = password.encode("utf-8")

    # If password is 72 bytes or less, use it directly
    if len(password_bytes) <= BCRYPT_MAX_LENGTH:
        return password

    # For longer passwords, pre-hash with SHA-256
    # This creates a 32-byte hash (64 hex characters) which is well under the limit
    sha256_hash = hashlib.sha256(password_bytes).hexdigest()
    return sha256_hash


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against a hash.
    Handles passwords longer than 72 bytes by pre-hashing.

    Args:
        plain_password: Plain text password to verify
        hashed_password: Bcrypt hash to verify against

    Returns:
        True if password matches, False otherwise
    """
    prepared_password = _prepare_password_for_bcrypt(plain_password)
    return pwd_context.verify(prepared_password, hashed_password)


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    Handles passwords longer than 72 bytes by pre-hashing with SHA-256.

    Args:
        password: Plain text password to hash

    Returns:
        Bcrypt hash of the password
    """
    prepared_password = _prepare_password_for_bcrypt(password)
    return pwd_context.hash(prepared_password)


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> "User":
    from app.models.user import User

    try:
        payload = jwt.decode(
            token, settings.JWT_SECRET, algorithms=[settings.JWT_ALGORITHM]
        )
        user_id = payload.get("sub")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
            )
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
        )
    user = User.get(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user
