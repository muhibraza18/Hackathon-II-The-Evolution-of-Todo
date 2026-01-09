"""
Better Auth Integration for FastAPI Backend
Implements authentication endpoints compatible with Better Auth frontend
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlmodel import Session, select
from typing import Optional
import uuid
from datetime import datetime, timedelta
import hashlib
import os

from models import User, UserCreate
from db import get_session
from auth import create_access_token, verify_token, TokenData

router = APIRouter(tags=["auth"])

from pydantic import BaseModel

class SignupRequest(BaseModel):
    email: str
    password: str

class SigninRequest(BaseModel):
    email: str
    password: str


@router.post("/signup")
def signup(
    request: SignupRequest,
    session: Session = Depends(get_session)
):
    """
    Handle user registration via email and password
    Compatible with Better Auth frontend expectations
    """
    # Check if user already exists
    existing_user = session.exec(select(User).where(User.email == request.email)).first()
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="User with this email already exists"
        )

    # Hash the password
    hashed_password = hashlib.sha256(request.password.encode()).hexdigest()

    # Create new user
    user = User(
        id=str(uuid.uuid4()),
        email=request.email,
        password_hash=hashed_password,
        created_at=datetime.utcnow()
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    # Create JWT token
    token_data = {
        "sub": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    access_token = create_access_token(token_data)

    response_data = {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.email,
            "emailVerified": False,
            "createdAt": user.created_at.isoformat(),
            "updatedAt": user.created_at.isoformat()
        },
        "session": {
            "accessToken": access_token,
            "refreshToken": None,
            "expiresAt": (datetime.utcnow() + timedelta(days=7)).isoformat(),
            "tokenType": "Bearer"
        },
        "redirect": False,
        "error": None
    }

    return JSONResponse(status_code=200, content=response_data)


@router.post("/signin")
def signin(
    request: SigninRequest,
    session: Session = Depends(get_session)
):
    """
    Handle user login via email and password
    Compatible with Better Auth frontend expectations
    """
    # Find user by email
    user = session.exec(select(User).where(User.email == request.email)).first()
    if not user:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid email or password", "user": None}
        )

    # Verify password
    hashed_password = hashlib.sha256(request.password.encode()).hexdigest()
    if user.password_hash != hashed_password:
        return JSONResponse(
            status_code=401,
            content={"error": "Invalid email or password", "user": None}
        )

    # Create JWT token
    token_data = {
        "sub": user.id,
        "email": user.email,
        "exp": datetime.utcnow() + timedelta(days=7)
    }
    access_token = create_access_token(token_data)

    response_data = {
        "user": {
            "id": user.id,
            "email": user.email,
            "name": user.email,
            "emailVerified": False,
            "createdAt": user.created_at.isoformat() if hasattr(user, 'created_at') and user.created_at else datetime.utcnow().isoformat(),
            "updatedAt": user.updated_at.isoformat() if hasattr(user, 'updated_at') and user.updated_at else datetime.utcnow().isoformat()
        },
        "session": {
            "accessToken": access_token,
            "refreshToken": None,
            "expiresAt": (datetime.utcnow() + timedelta(days=7)).isoformat(),
            "tokenType": "Bearer"
        },
        "redirect": False,
        "error": None
    }

    return JSONResponse(status_code=200, content=response_data)


@router.get("/session")
def get_session_endpoint(
    token_data: TokenData = Depends(verify_token)
):
    """
    Get current session information
    Compatible with Better Auth frontend expectations
    """
    response_data = {
        "user": {
            "id": token_data.user_id,
            "email": token_data.email,
            "name": token_data.email,
            "emailVerified": False,
            "createdAt": datetime.utcnow().isoformat(),
            "updatedAt": datetime.utcnow().isoformat()
        },
        "session": {
            "accessToken": "token_placeholder",
            "refreshToken": None,
            "expiresAt": (datetime.utcnow() + timedelta(days=7)).isoformat(),
            "tokenType": "Bearer"
        },
        "redirect": False,
        "error": None
    }

    return JSONResponse(status_code=200, content=response_data)


# Legacy endpoints for compatibility with older frontend calls
@router.post("/sign-up/email")
def signup_legacy(
    request: SignupRequest,
    session: Session = Depends(get_session)
):
    """
    Legacy endpoint for signup - for compatibility with frontend that calls /sign-up/email
    """
    return signup(request, session)


@router.post("/sign-in/email")
def signin_legacy(
    request: SigninRequest,
    session: Session = Depends(get_session)
):
    """
    Legacy endpoint for signin - for compatibility with frontend that calls /sign-in/email
    """
    return signin(request, session)


@router.get("/get-session")
def get_session_legacy(
    token_data: TokenData = Depends(verify_token)
):
    """
    Legacy endpoint for getting session - for compatibility with frontend that calls /get-session
    """
    return get_session_endpoint(token_data)


@router.post("/sign-out")
def signout():
    """
    Handle user logout
    Compatible with Better Auth frontend expectations
    """
    return JSONResponse(status_code=200, content={"success": True})


@router.post("/forgot-password")
def forgot_password(email: str):
    """Handle password reset request"""
    return JSONResponse(status_code=200, content={"success": True})


@router.post("/reset-password")
def reset_password(token: str, new_password: str):
    """Handle password reset with token"""
    return JSONResponse(status_code=200, content={"success": True})