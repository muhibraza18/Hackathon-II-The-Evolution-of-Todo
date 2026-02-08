import json
from datetime import datetime
from typing import Dict, Any, Optional
from app.database.models import Task
from ..services.dapr_client import dapr_client


class EventPublisher:
    """Service for publishing events related to tasks using Dapr pub/sub."""

    @staticmethod
    async def publish_event(event_type: str, data: Dict[str, Any], task_id: Optional[str] = None, user_id: Optional[str] = None):
        """
        Publish an event using Dapr pub/sub.

        Args:
            event_type: Type of event (e.g., 'task.created', 'task.updated', 'task.completed')
            data: Event data payload
            task_id: ID of the task related to the event
            user_id: ID of the user related to the event
        """
        event = {
            "event_type": event_type,
            "task_id": task_id,
            "user_id": user_id,
            "timestamp": datetime.utcnow().isoformat(),
            "data": data
        }

        # Publish event via Dapr pub/sub (topic matches event type)
        topic = event_type  # e.g., "task.created", "task.completed", "task-reminder"
        success = await dapr_client.publish_event("task-pubsub", topic, event)

        if success:
            print(f"EVENT_PUBLISHED VIA DAPR: {event_type} for task {task_id}")
        else:
            print(f"FAILED TO PUBLISH EVENT VIA DAPR: {event_type} for task {task_id}")
            # In a real implementation, we might want to handle the failure appropriately
            # e.g., add to a retry queue or fallback mechanism


async def publish_task_created_event(task: Task):
    """
    Publish an event when a task is created.

    Args:
        task: The created task
    """
    data = {
        "title": task.title,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "priority": task.priority,
        "tags": json.loads(task.tags) if task.tags else [],
    }
    await EventPublisher.publish_event(
        event_type="task.created",
        data=data,
        task_id=str(task.id) if task.id else None,
        user_id=str(task.user_id)
    )


async def publish_task_updated_event(task: Task):
    """
    Publish an event when a task is updated.

    Args:
        task: The updated task
    """
    data = {
        "title": task.title,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "priority": task.priority,
        "tags": json.loads(task.tags) if task.tags else [],
        "status": "completed" if task.completed else "pending"
    }
    await EventPublisher.publish_event(
        event_type="task.updated",
        data=data,
        task_id=str(task.id) if task.id else None,
        user_id=str(task.user_id)
    )


async def publish_task_completed_event(task: Task, next_occurrence_id: Optional[str] = None):
    """
    Publish an event when a task is completed.

    Args:
        task: The completed task
        next_occurrence_id: ID of the next occurrence if it's a recurring task
    """
    data = {
        "title": task.title,
        "due_date": task.due_date.isoformat() if task.due_date else None,
        "priority": task.priority,
        "tags": json.loads(task.tags) if task.tags else [],
        "next_occurrence_id": next_occurrence_id
    }
    await EventPublisher.publish_event(
        event_type="task.completed",
        data=data,
        task_id=str(task.id) if task.id else None,
        user_id=str(task.user_id)
    )


async def publish_task_deleted_event(task_id: str, user_id: str):
    """
    Publish an event when a task is deleted.

    Args:
        task_id: ID of the deleted task
        user_id: ID of the user who deleted the task
    """
    await EventPublisher.publish_event(
        event_type="task.deleted",
        data={},
        task_id=task_id,
        user_id=user_id
    )


async def publish_due_date_reminder_event(task: Task):
    """
    Publish an event when a task's due date is approaching.

    Args:
        task: The task with the approaching due date
    """
    data = {
        "title": task.title,
        "due_date": task.due_date.isoformat() if task.id else None,
        "priority": task.priority,
        "user_id": task.user_id
    }
    await EventPublisher.publish_event(
        event_type="due_date.reminder",
        data=data,
        task_id=str(task.id) if task.id else None,
        user_id=str(task.user_id)
    )


async def publish_recurring_task_generated_event(task: Task, next_task_id: str):
    """
    Publish an event when a recurring task generates a new occurrence.

    Args:
        task: The original recurring task
        next_task_id: ID of the newly generated task
    """
    data = {
        "original_task_id": task.id,
        "original_title": task.title,
        "next_task_id": next_task_id,
        "due_date": task.due_date.isoformat() if task.due_date else None
    }
    await EventPublisher.publish_event(
        event_type="recurring_task.generated",
        data=data,
        task_id=str(task.id) if task.id else None,
        user_id=str(task.user_id)
    )