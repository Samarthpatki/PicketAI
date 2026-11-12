from datetime import datetime, timedelta, timezone
import bcrypt
from datetime import timedelta
from typing import Any
import jwt

from app.core.config import settings

def hash_password(password:str) -> str:
    """Hashes a plain text password using bcrypt with a generated salt."""
    password_bytes = password.encode("utf-8")
    salt = bcrypt.gensalt()
    hashed_bytes = bcrypt.hashpw(password_bytes , salt)
    return hashed_bytes.decode("utf-8")

def verify_password(plain_password:str, hashed_password:str) -> bool:
        """Verifies a plain password against the stored bcrypt hash."""
        try:
            return bcrypt.checkpw(
                plain_password.encode("utf-8"),
                hashed_password.encode("utf-8")
            )
        except:
            return False

def create_access_token(subject:str |Any , expires_delta:timedelta| None=None) -> str:
    """Encdoes subject (eg. user ID) into a signed JWT with an expiration timestamp"""
    if expires_delta is not None :
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )
    payload = {
        "exp": expire,
        "sub" : str(subject)
    }

    return jwt.encode(
        payload,
        settings.JWT_SECRET_KEY,
        algorithm=settings.JWT_ALGORITHM
    )
