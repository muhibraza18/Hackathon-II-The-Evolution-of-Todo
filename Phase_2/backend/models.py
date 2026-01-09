"""
SQLModel Models
Task CRUD Operations with Authentication
"""

from typing import Optional
from sqlmodel import Field, SQLModel
from datetime import datetime
from uuid import uuid4


class UserBase(SQLModel):
    """Base model with shared fields for User"""
    email: str = Field(unique=True, index=True, min_length=5, max_length=200)


class UserCreate(UserBase):
    """Schema for user creation"""
    password: str = Field(min_length=8, max_length=200)


class UserUpdate(SQLModel):
    """Schema for user updates"""
    email: Optional[str] = Field(default=None, min_length=5, max_length=200)


class UserResponse(UserBase):
    """Schema for user responses"""
    id: str
    created_at: datetime
    updated_at: datetime


class User(UserBase, table=True):
    """
    User entity for authentication.

    Attributes:
        id: Unique user identifier (UUID string)
        email: User email (unique, indexed)
        password_hash: Hashed password
        created_at: Timestamp when user was created
        updated_at: Timestamp when user was last updated
    """
    __tablename__ = "users"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    password_hash: str = Field(max_length=500)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


class TaskBase(SQLModel):
    """Base model with shared fields"""
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskCreate(TaskBase):
    """Schema for task creation"""
    pass  # user_id will come from JWT token


class TaskUpdate(SQLModel):
    """Schema for task updates"""
    title: Optional[str] = Field(default=None, min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)


class TaskResponse(TaskBase):
    """Schema for task responses"""
    id: str
    user_id: str
    completed: bool
    created_at: datetime
    updated_at: datetime


class Task(TaskBase, table=True):
    """
    Task entity representing a todo item.

    Attributes:
        id: Unique task identifier (UUID string)
        user_id: User identifier (foreign key to users table)
        title: Task title (1-200 characters)
        description: Task description (0-1000 characters, optional)
        completed: Task completion status (boolean)
        created_at: Timestamp when task was created
        updated_at: Timestamp when task was last updated
    """
    __tablename__ = "tasks"

    id: str = Field(default_factory=lambda: str(uuid4()), primary_key=True)
    user_id: str = Field(index=True, foreign_key="users.id")  # Now properly references users table
    completed: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
