from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict, Any
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
    Extended with due_date, priority, tags, recurring_config, and relationship fields.
    """
    __tablename__ = "task"

    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id", index=True)
    title: str = Field(min_length=1, max_length=200)
    description: Optional[str] = Field(default=None, max_length=1000)
    completed: bool = Field(default=False, index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

    # New fields for advanced features
    due_date: Optional[datetime] = Field(default=None, index=True)
    priority: Optional[str] = Field(default=None, max_length=20, index=True)  # low, medium, high, urgent
    tags: Optional[str] = Field(default=None, max_length=1000)  # JSON string of tags array
    recurring_config: Optional[str] = Field(default=None, max_length=1000)  # JSON string of recurring config
    next_occurrence_id: Optional[str] = Field(default=None, max_length=100, index=True)
    parent_task_id: Optional[int] = Field(default=None, foreign_key="task.id", index=True)
    original_task_id: Optional[int] = Field(default=None, foreign_key="task.id", index=True)

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

    @classmethod
    def validate_priority(cls, priority: Optional[str]) -> bool:
        """Validate that priority is one of the allowed values."""
        if priority is None:
            return True
        return priority in ["low", "medium", "high", "urgent"]

    @classmethod
    def validate_tags(cls, tags: Optional[str]) -> bool:
        """Validate that tags JSON string represents an array with reasonable length."""
        if tags is None:
            return True
        try:
            import json
            parsed_tags = json.loads(tags)
            if not isinstance(parsed_tags, list):
                return False
            return len(parsed_tags) <= 10  # Limit to 10 tags
        except (json.JSONDecodeError, TypeError):
            return False

    @classmethod
    def validate_due_date(cls, due_date: Optional[datetime]) -> bool:
        """Validate that due date is in the future if provided."""
        if due_date is None:
            return True
        return due_date > datetime.utcnow()

    @classmethod
    def validate_recurring_config(cls, recurring_config: Optional[str]) -> bool:
        """Validate recurring configuration JSON string."""
        if recurring_config is None:
            return True
        try:
            import json
            config = json.loads(recurring_config)
            if not isinstance(config, dict):
                return False

            # Validate required fields
            if "type" not in config or config["type"] not in ["daily", "weekly", "monthly"]:
                return False

            if "interval" not in config or not isinstance(config["interval"], int) or config["interval"] <= 0:
                return False

            return True
        except (json.JSONDecodeError, TypeError):
            return False


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

class Reminder(SQLModel, table=True):
    """
    Represents a scheduled notification for a task with a specific due time.
    Used for Phase V - Redpanda Cloud Integration with real-time reminders.
    """
    __tablename__ = "reminders"
    
    id: Optional[int] = Field(default=None, primary_key=True)
    task_id: int = Field(foreign_key="task.id", ondelete="CASCADE")
    user_id: int = Field(foreign_key="user.id", ondelete="CASCADE")
    due_time: datetime = Field(index=True)
    status: str = Field(default="pending")  # pending, sent, failed
    event_published: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    sent_at: Optional[datetime] = None
    error_message: Optional[str] = None
    retry_count: int = Field(default=0)
    
    @classmethod
    def validate_status(cls, status: str) -> bool:
        """Validate that status is one of the allowed values."""
        return status in ["pending", "sent", "failed"]
