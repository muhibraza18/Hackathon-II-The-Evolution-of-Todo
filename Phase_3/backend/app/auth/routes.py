"""
Authentication routes for Todo AI Chatbot.

This module contains all authentication-related API endpoints including
registration, login, logout, and user information retrieval.
"""

from fastapi import APIRouter, Depends, HTTPException, Request
from sqlmodel import Session, select
from typing import Dict, Any
from datetime import datetime, timedelta

from ..database.models import User, SessionModel
from ..database.connection import get_db_session
from .utils import (
    hash_password, 
    verify_password, 
    generate_session_token, 
    validate_email, 
    validate_password_strength
)

router = APIRouter(prefix="/api/auth", tags=["auth"])


@router.post("/register")
async def register(
    request: Request,
    db: Session = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Register a new user with email, password, and optional name.

    Args:
        request: HTTP request containing user registration data
        db: Database session

    Returns:
        Dict containing user_id, email, and session token
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")
    name = data.get("name", "").strip() if data.get("name") else None

    # Validate email format
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    # Validate password strength
    password_validation = validate_password_strength(password)
    if not password_validation['strong']:
        raise HTTPException(
            status_code=400, 
            detail=password_validation.get('message', 'Password does not meet requirements')
        )

    # Validate name length if provided
    if name and len(name) > 100:
        raise HTTPException(status_code=400, detail="Name exceeds maximum length of 100 characters")

    # Check if email already exists
    statement = select(User).where(User.email == email)
    existing_user = db.exec(statement).first()
    
    if existing_user:
        raise HTTPException(status_code=409, detail="Email already registered")

    try:
        # Hash the password
        password_hash = hash_password(password)

        # Create new user
        user = User(
            email=email,
            password_hash=password_hash,
            name=name,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )

        # Add user to database
        db.add(user)
        db.commit()
        db.refresh(user)

        # Generate a session token
        session_token = generate_session_token()
        expires_at = datetime.utcnow() + timedelta(days=7)

        # Create session record
        session = SessionModel(
            user_id=user.id,
            token=session_token,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )

        # Add session to database
        db.add(session)
        db.commit()
        db.refresh(session)  # Refresh to ensure we have the latest data from DB

        # Return success response
        return {
            "user_id": str(user.id),
            "email": user.email,
            "token": session.token  # Return token from the session object
        }
    
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Registration failed: {str(e)}")


@router.post("/login")
async def login(
    request: Request,
    db: Session = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Authenticate user with email and password.

    Args:
        request: HTTP request containing email and password
        db: Database session

    Returns:
        Dict containing user_id, session token, and expiration
    """
    try:
        data = await request.json()
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid JSON format")

    email = data.get("email", "").strip().lower()
    password = data.get("password", "")

    if not email or not password:
        raise HTTPException(status_code=400, detail="Email and password are required")

    # Verify email format
    if not validate_email(email):
        raise HTTPException(status_code=400, detail="Invalid email format")

    try:
        # Find user by email
        statement = select(User).where(User.email == email)
        user = db.exec(statement).first()

        if not user or not verify_password(password, user.password_hash):
            raise HTTPException(status_code=401, detail="Invalid credentials")

        # Generate a new session token
        session_token = generate_session_token()
        expires_at = datetime.utcnow() + timedelta(days=7)

        # Create session record
        session = SessionModel(
            user_id=user.id,
            token=session_token,
            expires_at=expires_at,
            created_at=datetime.utcnow()
        )

        # Add session to database
        db.add(session)
        db.commit()
        db.refresh(session)  # Refresh to ensure we have the latest data from DB

        # Return success response
        return {
            "user_id": str(user.id),
            "email": user.email,
            "token": session.token,  # Return token from the session object
            "expires_at": expires_at.isoformat()
        }
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Login failed: {str(e)}")


@router.post("/logout")
async def logout(
    request: Request,
    db: Session = Depends(get_db_session)
) -> Dict[str, str]:
    """
    Invalidate the current user session.

    Args:
        request: HTTP request with Authorization header containing session token
        db: Database session

    Returns:
        Dict with success message
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header[7:].strip()  # Remove "Bearer " prefix

    try:
        # Find session by token
        statement = select(SessionModel).where(SessionModel.token == token)
        session = db.exec(statement).first()

        if not session:
            raise HTTPException(status_code=401, detail="Invalid session token")

        # Delete the session
        db.delete(session)
        db.commit()

        return {"message": "Logged out successfully"}
    
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Logout failed: {str(e)}")


@router.get("/me")
async def get_current_user(
    request: Request,
    db: Session = Depends(get_db_session)
) -> Dict[str, Any]:
    """
    Retrieve information about the currently authenticated user.

    Args:
        request: HTTP request with Authorization header containing session token
        db: Database session

    Returns:
        Dict containing user information
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.lower().startswith("bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid Authorization header")

    token = auth_header[7:].strip()  # Remove "Bearer " prefix

    try:
        # Find session by token
        statement = select(SessionModel).where(SessionModel.token == token)
        session = db.exec(statement).first()

        if not session:
            raise HTTPException(status_code=401, detail="Invalid session token")

        # Check if session is still valid (not expired)
        if session.expires_at < datetime.utcnow():
            # Session has expired - delete it from database
            db.delete(session)
            db.commit()
            raise HTTPException(status_code=401, detail="Session has expired")

        # Get user information
        user_statement = select(User).where(User.id == session.user_id)
        user = db.exec(user_statement).first()

        if not user:
            raise HTTPException(status_code=404, detail="User not found")

        return {
            "user_id": str(user.id),
            "email": user.email,
            "name": user.name
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get user: {str(e)}")