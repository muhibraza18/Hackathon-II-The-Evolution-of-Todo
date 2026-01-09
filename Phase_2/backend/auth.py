"""
Authentication Utilities
JWT Token Management for Better Auth Integration
"""

from datetime import datetime, timedelta
from typing import Optional
import jwt
from fastapi import HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel
import os

# JWT Configuration
JWT_SECRET = os.getenv("BETTER_AUTH_SECRET")
if not JWT_SECRET:
    raise ValueError("BETTER_AUTH_SECRET environment variable is not set")

JWT_ALGORITHM = "HS256"
JWT_EXPIRATION_DELTA = timedelta(days=7)  # Token expires in 7 days

security = HTTPBearer()

class TokenData(BaseModel):
    user_id: str
    email: str


def create_access_token(data: dict) -> str:
    """
    Create a new JWT access token

    Args:
        data: Dictionary containing user information to encode in the token

    Returns:
        Encoded JWT token as string
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + JWT_EXPIRATION_DELTA
    to_encode.update({"exp": expire, "iat": datetime.utcnow()})
    encoded_jwt = jwt.encode(to_encode, JWT_SECRET, algorithm=JWT_ALGORITHM)
    return encoded_jwt


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)) -> TokenData:
    """
    Verify JWT token and extract user data

    Args:
        credentials: HTTP authorization credentials from request headers

    Returns:
        TokenData object containing user information

    Raises:
        HTTPException: If token is invalid, expired, or cannot be decoded
    """
    token = credentials.credentials

    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
        user_id: str = payload.get("sub")
        email: str = payload.get("email")

        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        return TokenData(user_id=user_id, email=email)
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_current_user_id(token_data: TokenData = Depends(verify_token)) -> str:
    """
    Dependency to get current user ID from JWT token

    Args:
        token_data: Verified token data containing user information

    Returns:
        User ID string
    """
    return token_data.user_id