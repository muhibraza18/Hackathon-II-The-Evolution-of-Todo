from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from datetime import datetime, timedelta
import re
import uuid


class User(SQLModel, table=True):
    """
    Represents a registered user with credentials and profile information.
    """
    __tablename__ = "user"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str = Field(min_length=1)
    name: Optional[str] = Field(default=None, max_length=100)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def validate_email(cls, email: str) -> bool:
        """Validate email format."""
        pattern = r'^[^@]+@[^@]+\.[^@]+$'
        return bool(re.match(pattern, email))

    @classmethod
    def validate_password(cls, password: str) -> bool:
        """Validate password strength (min 8 chars, 1 upper, 1 lower, 1 digit, 1 special)."""
        if len(password) < 8:
            return False

        has_upper = any(c.isupper() for c in password)
        has_lower = any(c.islower() for c in password)
        has_digit = any(c.isdigit() for c in password)
        has_special = any(not c.isalnum() for c in password)

        return has_upper and has_lower and has_digit and has_special


class SessionModel(SQLModel, table=True):
    """
    Represents an active user session with token validation and expiration.
    """
    __tablename__ = "session"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    token: str = Field(unique=True, index=True, min_length=32)
    expires_at: datetime
    created_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def generate_expiration(cls, days: int = 7) -> datetime:
        """Generate expiration datetime based on number of days."""
        return datetime.utcnow() + timedelta(days=days)

    @classmethod
    def is_valid(cls, expires_at: datetime) -> bool:
        """Check if session is still valid (not expired)."""
        return datetime.utcnow() < expires_at


class Task(SQLModel, table=True):
    """
    Represents a user's todo item with title, description, completion status, and timestamps.
    Associated with a specific user via user_id.
    """
    __tablename__ = "task"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    @classmethod
    def validate_title(cls, title: str) -> bool:
        """Validate that title is not empty and within length constraints."""
        return 1 <= len(title) <= 200

    @classmethod
    def validate_description(cls, description: Optional[str]) -> bool:
        """Validate that description is within length constraints if provided."""
        if description is None:
            return True
        return len(description) <= 1000


class Conversation(SQLModel, table=True):
    """
    Represents a logical grouping of messages between a user and the AI assistant.
    Associated with a specific user via user_id.
    """
    __tablename__ = "conversation"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # Relationship to messages with cascade delete
    messages: List["Message"] = Relationship(
        back_populates="conversation",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    @classmethod
    def validate_user_id(cls, user_id: int) -> bool:
        """Validate that user_id is not empty."""
        return user_id > 0


class Message(SQLModel, table=True):
    """
    Represents individual exchanges within a conversation, with role indicating
    sender (user or assistant) and content of the message. Belongs to a specific conversation and user.
    """
    __tablename__ = "message"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    conversation_id: int = Field(foreign_key="conversation.id", index=True)
    role: str = Field(description="Must be 'user', 'assistant', or 'tool'")
    content: str = Field(min_length=1)
    created_at: datetime = Field(default_factory=datetime.utcnow, index=True)

    # Relationship to conversation
    conversation: Optional[Conversation] = Relationship(back_populates="messages")

    @classmethod
    def validate_role(cls, role: str) -> bool:
        """Validate that role is 'user', 'assistant', or 'tool'."""
        return role in ["user", "assistant", "tool"]

    @classmethod
    def validate_content(cls, content: str) -> bool:
        """Validate that content is not empty."""
        return len(content) > 0