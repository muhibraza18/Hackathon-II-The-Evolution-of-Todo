"""
Reminder routes for Phase V - Redpanda Cloud Integration.
Handles creating and managing task reminders with due times.
"""
from fastapi import APIRouter, HTTPException, Depends, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from typing import List, Optional
from datetime import datetime
from pydantic import BaseModel

from ..crud import (
    create_reminder,
    get_pending_reminders,
    get_reminder_by_task_id,
    mark_reminder_sent,
)
from ..database.connection import get_async_db_session
from ..auth.middleware import get_current_user_id


# Request/Response Models
class ReminderRequest(BaseModel):
    due_time: datetime  # UTC ISO 8601 timestamp


class ReminderResponse(BaseModel):
    reminder_id: int
    task_id: int
    due_time: datetime
    status: str
    event_published: bool = False


class PendingReminderResponse(BaseModel):
    id: int
    task_id: int
    title: str
    due_time: datetime
    priority: Optional[str] = None
    is_overdue: bool = False
    seconds_until_due: int


class PendingRemindersResponse(BaseModel):
    reminders: List[PendingReminderResponse]


router = APIRouter(prefix="/api/reminders", tags=["reminders"])


@router.post("/tasks/{task_id}/reminder", response_model=ReminderResponse)
async def create_task_reminder(
    task_id: int,
    reminder_data: ReminderRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_db_session),
):
    """
    Create or update a reminder for a task.

    When a task with a due time is created/updated, a reminder is automatically scheduled.
    The reminder will trigger a notification at the due time.
    """
    # Get user_id from request state (set by auth middleware)
    user_id = get_current_user_id(request)

    # Check if reminder already exists
    existing = await get_reminder_by_task_id(db, task_id, user_id)

    if existing:
        # Update existing reminder
        existing.due_time = reminder_data.due_time
        existing.status = "pending"
        existing.event_published = False
        db.add(existing)
        await db.commit()
        await db.refresh(existing)
        reminder = existing
    else:
        # Create new reminder
        reminder = await create_reminder(db, task_id, user_id, reminder_data.due_time)

    # TODO: Publish event to Redpanda Cloud (when connectivity is resolved)
    # For now, using in-memory fallback per ADR-003

    return ReminderResponse(
        reminder_id=reminder.id,
        task_id=reminder.task_id,
        due_time=reminder.due_time,
        status=reminder.status,
        event_published=reminder.event_published  # Will be False with in-memory fallback
    )


@router.get("/pending", response_model=PendingRemindersResponse)
async def get_user_pending_reminders(
    request: Request,
    within_minutes: int = 5,
    db: AsyncSession = Depends(get_async_db_session),
):
    """
    Get all pending reminders for the current user that are due soon.

    Args:
        within_minutes: Only return reminders due within this many minutes (default: 5)

    Returns:
        List of pending reminders with task details
    """
    # Get user_id from request state (set by auth middleware)
    user_id = get_current_user_id(request)

    reminders = await get_pending_reminders(db, user_id, within_minutes)

    # Enrich with task details
    from ..crud import get_task_by_id
    from sqlmodel import select
    from ..database.models import Task

    result_reminders = []

    for reminder in reminders:
        # Get the task title and priority
        task_query = select(Task).where(Task.id == reminder.task_id)
        task_result = await db.exec(task_query)
        task = task_result.first()

        if task:
            now = datetime.utcnow()
            is_overdue = reminder.due_time < now
            seconds_until_due = int((reminder.due_time - now).total_seconds())

            result_reminders.append(PendingReminderResponse(
                id=reminder.id,
                task_id=reminder.task_id,
                title=task.title,
                due_time=reminder.due_time,
                priority=task.priority,
                is_overdue=is_overdue,
                seconds_until_due=seconds_until_due
            ))

    return PendingRemindersResponse(reminders=result_reminders)


@router.post("/{reminder_id}/mark-sent")
async def mark_reminder_as_sent(
    reminder_id: int,
    request: Request,
    db: AsyncSession = Depends(get_async_db_session),
):
    """
    Mark a reminder as sent (triggered).

    Called by the reminder scheduler when a notification is delivered.
    """
    # Get user_id from request state (set by auth middleware)
    user_id = get_current_user_id(request)

    reminder = await mark_reminder_sent(db, reminder_id, user_id)

    if not reminder:
        raise HTTPException(status_code=404, detail="Reminder not found")

    return {"status": "marked as sent", "reminder_id": reminder_id}
