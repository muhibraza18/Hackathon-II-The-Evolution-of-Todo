"""
Event schemas for the event-driven architecture.
"""
from datetime import datetime
from typing import Dict, Any, Optional
from pydantic import BaseModel


class BaseEvent(BaseModel):
    """
    Base event schema with common fields for all events.
    """
    event_type: str
    task_id: Optional[str] = None
    user_id: Optional[str] = None
    timestamp: datetime
    payload: Dict[str, Any]


class TaskCreatedEvent(BaseEvent):
    """
    Event schema for task creation events.
    """
    event_type: str = "task.created"
    payload: Dict[str, Any]  # Will contain title, description, due_date, priority, tags, recurring_config, status


class TaskUpdatedEvent(BaseEvent):
    """
    Event schema for task update events.
    """
    event_type: str = "task.updated"
    payload: Dict[str, Any]  # Will contain updated fields


class TaskCompletedEvent(BaseEvent):
    """
    Event schema for task completion events.
    """
    event_type: str = "task.completed"
    payload: Dict[str, Any]  # Will contain title, due_date, priority, tags, next_occurrence_id


class TaskDeletedEvent(BaseEvent):
    """
    Event schema for task deletion events.
    """
    event_type: str = "task.deleted"
    payload: Dict[str, Any]  # Will contain title


class TaskReminderEvent(BaseEvent):
    """
    Event schema for task reminder events.
    """
    event_type: str = "task.reminder"
    payload: Dict[str, Any]  # Will contain title, due_date, priority, notification_method


class TaskReminderEvent(BaseEvent):
    """
    Event schema for task reminder events.
    """
    event_type: str = "task.reminder"
    payload: Dict[str, Any]  # Will contain title, due_date, priority, notification_method


class TaskStatusChangedEvent(BaseEvent):
    """
    Event schema for task status change events.
    """
    event_type: str = "task.status_changed"
    payload: Dict[str, Any]  # Will contain previous_status, new_status