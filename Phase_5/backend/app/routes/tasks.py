from fastapi import APIRouter, Depends, HTTPException, Query, Body, Request
from typing import Optional, List
from datetime import datetime
import json
from pydantic import BaseModel

from ..database.connection import get_async_db_session
from sqlmodel.ext.asyncio.session import AsyncSession
from ..database.models import Task
from .. import crud
from ..services.event_publisher import EventPublisher
from ..schemas.events import TaskCreatedEvent, TaskUpdatedEvent, TaskCompletedEvent, TaskDeletedEvent
from ..auth.middleware import get_current_user_id, get_current_user_id_dependency

router = APIRouter()


class CreateTaskRequest(BaseModel):
    title: str
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    recurring_config: Optional[dict] = None


class UpdateTaskRequest(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[str] = None
    priority: Optional[str] = None
    tags: Optional[List[str]] = None
    recurring_config: Optional[dict] = None
    completed: Optional[bool] = None


@router.post("/tasks")
async def create_task(
    task_data: CreateTaskRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_db_session)
):
    """
    Create a new task with advanced features (due date, priority, tags, recurring config).
    """
    from ..services.tag_service import TagService
    from ..services.priority_service import PriorityService
    from ..services.due_date_service import DueDateService
    from ..services.recurring_task_service import RecurringTaskService
    from ..services.reminder_scheduler import ReminderScheduler

    # Get user_id from request state (set by auth middleware)
    user_id = get_current_user_id(request)

    # Validate priority
    if task_data.priority and not PriorityService.validate_priority(task_data.priority):
        raise HTTPException(status_code=400, detail=f"Invalid priority: {task_data.priority}")

    # Validate tags
    tags_json = None
    if task_data.tags:
        tags_json = TagService.serialize_tags(task_data.tags)

    # Validate due date
    due_datetime = None
    if task_data.due_date:
        try:
            due_datetime = datetime.fromisoformat(task_data.due_date.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid due date format")

        if not DueDateService.validate_due_date(due_datetime):
            raise HTTPException(status_code=400, detail="Due date must be in the future")

    # Validate recurring config
    recurring_json = None
    if task_data.recurring_config:
        is_valid = await RecurringTaskService.validate_recurring_config(task_data.recurring_config)
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid recurring configuration")
        recurring_json = json.dumps(task_data.recurring_config)

    # Create task via CRUD
    task = await crud.create_task(
        db_session=db,
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        due_date=due_datetime,
        priority=task_data.priority,
        tags=tags_json,
        recurring_config=recurring_json
    )

    # Schedule reminder for task with due date
    if task.due_date:
        await ReminderScheduler.schedule_reminder_for_task(task, db)

    # Publish event
    event_payload = {
        "event_type": "task.created",
        "task_id": str(task.id) if task.id else None,
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "payload": {
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "priority": task.priority,
            "tags": json.loads(task.tags) if task.tags else [],
            "recurring_config": json.loads(task.recurring_config) if task.recurring_config else {},
            "status": "pending"
        }
    }

    await EventPublisher.publish_event(
        event_type=event_payload["event_type"],
        data=event_payload["payload"],
        task_id=event_payload.get("task_id"),
        user_id=event_payload.get("user_id")
    )

    return task


@router.get("/tasks")
async def get_tasks(
    request: Request,
    db: AsyncSession = Depends(get_async_db_session),
    completed: Optional[bool] = Query(None),
    priority: Optional[str] = Query(None),
    tag: Optional[str] = Query(None),
    due_before: Optional[str] = Query(None),
    due_after: Optional[str] = Query(None),
    overdue_only: Optional[bool] = Query(False),
    sort_by: Optional[str] = Query("created_at"),
    sort_order: Optional[str] = Query("desc"),
    page: Optional[int] = Query(1),
    limit: Optional[int] = Query(20)
):
    """
    Get tasks with filtering, sorting, and pagination support.
    Includes overdue_only filter for performance optimization.
    """
    from ..services.tag_service import TagService
    from ..services.priority_service import PriorityService
    from ..services.due_date_service import DueDateService

    # Get user_id from request state (set by auth middleware)
    user_id = get_current_user_id(request)

    # Validate inputs
    if priority and not PriorityService.validate_priority(priority):
        raise HTTPException(status_code=400, detail=f"Invalid priority: {priority}")

    due_before_dt = None
    if due_before:
        try:
            due_before_dt = datetime.fromisoformat(due_before.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid due_before date format")

    due_after_dt = None
    if due_after:
        try:
            due_after_dt = datetime.fromisoformat(due_after.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid due_after date format")

    if sort_by not in ["created_at", "updated_at", "due_date", "priority"]:
        raise HTTPException(status_code=400, detail="Invalid sort_by parameter")

    if sort_order not in ["asc", "desc"]:
        raise HTTPException(status_code=400, detail="Invalid sort_order parameter")

    # Get tasks via CRUD - only get pending tasks for overdue filter (performance)
    if overdue_only:
        tasks = await crud.get_tasks(db_session=db, user_id=user_id, completed=False)
    else:
        tasks = await crud.get_tasks(db_session=db, user_id=user_id, completed=completed)

    # Apply additional filters
    filtered_tasks = []
    now = datetime.utcnow()

    for task in tasks:
        # Priority filter
        if priority and task.priority != priority:
            continue

        # Tag filter
        if tag:
            task_tags = TagService.parse_tags(task.tags)
            if tag not in task_tags:
                continue

        # Due date filters
        if due_before_dt and task.due_date and task.due_date > due_before_dt:
            continue

        if due_after_dt and task.due_date and task.due_date < due_after_dt:
            continue

        # Overdue filter (for performance)
        if overdue_only:
            if not task.due_date or task.due_date >= now or task.completed:
                continue

        filtered_tasks.append(task)

    # Apply sorting
    if sort_by == "priority":
        from ..services.priority_service import PriorityService
        filtered_tasks = await PriorityService.sort_tasks_by_priority(filtered_tasks, ascending=(sort_order == "asc"))
    elif sort_by == "due_date":
        # Sort by due date, with None values last
        filtered_tasks.sort(key=lambda x: (x.due_date is None, x.due_date), reverse=(sort_order != "asc"))
    elif sort_by == "created_at":
        filtered_tasks.sort(key=lambda x: x.created_at, reverse=(sort_order == "desc"))
    elif sort_by == "updated_at":
        filtered_tasks.sort(key=lambda x: x.updated_at, reverse=(sort_order == "desc"))

    # Apply pagination (page starts at 1)
    start_idx = (page - 1) * limit
    end_idx = min(start_idx + limit, len(filtered_tasks))
    paginated_tasks = filtered_tasks[start_idx:end_idx]

    # Return structured response matching frontend expectations
    return {
        "tasks": paginated_tasks,
        "total": len(filtered_tasks),
        "page": page,
        "limit": limit
    }


@router.put("/tasks/{task_id}")
async def update_task(
    task_id: int,
    task_data: UpdateTaskRequest,
    request: Request,
    db: AsyncSession = Depends(get_async_db_session)
):
    """
    Update an existing task with advanced features.
    """
    from ..services.tag_service import TagService
    from ..services.priority_service import PriorityService
    from ..services.due_date_service import DueDateService
    from ..services.recurring_task_service import RecurringTaskService
    from ..services.reminder_scheduler import ReminderScheduler

    # Get user_id from request state (set by auth middleware)
    user_id = get_current_user_id(request)

    # Validate priority
    if task_data.priority and not PriorityService.validate_priority(task_data.priority):
        raise HTTPException(status_code=400, detail=f"Invalid priority: {task_data.priority}")

    # Validate tags
    tags_json = None
    if task_data.tags:
        tags_json = TagService.serialize_tags(task_data.tags)

    # Validate due date
    due_datetime = None
    if task_data.due_date:
        try:
            due_datetime = datetime.fromisoformat(task_data.due_date.replace('Z', '+00:00'))
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid due date format")

        if not DueDateService.validate_due_date(due_datetime):
            raise HTTPException(status_code=400, detail="Due date must be in the future")

    # Validate recurring config
    recurring_json = None
    if task_data.recurring_config:
        is_valid = await RecurringTaskService.validate_recurring_config(task_data.recurring_config)
        if not is_valid:
            raise HTTPException(status_code=400, detail="Invalid recurring configuration")
        recurring_json = json.dumps(task_data.recurring_config)

    # Update task via CRUD
    task = await crud.update_task(
        db_session=db,
        task_id=task_id,
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        completed=task_data.completed,
        due_date=due_datetime,
        priority=task_data.priority,
        tags=tags_json,
        recurring_config=recurring_json
    )

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Reschedule or cancel reminder based on task changes
    if task.completed:
        # Task was completed, cancel any scheduled reminder
        await ReminderScheduler.cancel_scheduled_reminder(str(task.id))
    elif task.due_date:
        # Task has a due date (possibly updated), reschedule reminder
        await ReminderScheduler.reschedule_reminder(task, db)

    # Publish event
    event_payload = {
        "event_type": "task.updated",
        "task_id": str(task.id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "payload": {
            "title": task.title,
            "description": task.description,
            "due_date": task.due_date.isoformat() if task.due_date else None,
            "priority": task.priority,
            "tags": json.loads(task.tags) if task.tags else [],
            "recurring_config": json.loads(task.recurring_config) if task.recurring_config else {},
            "status": "completed" if task.completed else "pending"
        }
    }

    await EventPublisher.publish_event(
        event_type=event_payload["event_type"],
        data=event_payload["payload"],
        task_id=event_payload.get("task_id"),
        user_id=event_payload.get("user_id")
    )

    return task


@router.patch("/tasks/{task_id}/complete")
async def complete_task(task_id: int, request: Request, db: AsyncSession = Depends(get_async_db_session)):
    """
    Complete a task and handle recurring task generation if applicable.
    """
    from ..services.recurring_task_service import RecurringTaskService
    from ..services.reminder_scheduler import ReminderScheduler

    # Get user_id from request state (set by auth middleware)
    user_id = get_current_user_id(request)

    # First, get the task to check if it's recurring
    task = await crud.get_task_by_id(db_session=db, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Update task to completed
    updated_task = await crud.update_task(
        db_session=db,
        task_id=task_id,
        user_id=user_id,
        completed=True
    )

    if not updated_task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Cancel any scheduled reminder since task is now completed
    await ReminderScheduler.cancel_scheduled_reminder(str(task_id))

    # Handle recurring task logic
    next_occurrence_id = None
    if task.recurring_config:
        next_task = await RecurringTaskService.create_next_occurrence(db, task)
        if next_task:
            next_occurrence_id = str(next_task.id)

    # Publish completion event
    event_payload = {
        "event_type": "task.completed",
        "task_id": str(updated_task.id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "payload": {
            "title": updated_task.title,
            "due_date": updated_task.due_date.isoformat() if updated_task.due_date else None,
            "priority": updated_task.priority,
            "tags": json.loads(updated_task.tags) if updated_task.tags else [],
            "next_occurrence_id": next_occurrence_id
        }
    }

    await EventPublisher.publish_event(
        event_type=event_payload["event_type"],
        data=event_payload["payload"],
        task_id=event_payload.get("task_id"),
        user_id=event_payload.get("user_id")
    )

    return updated_task


@router.get("/tasks/{task_id}")
async def get_task(task_id: int, request: Request, db: AsyncSession = Depends(get_async_db_session)):
    """
    Get a specific task by ID.
    """
    # Get user_id from request state (set by auth middleware)
    user_id = get_current_user_id(request)

    task = await crud.get_task_by_id(db_session=db, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


@router.delete("/tasks/{task_id}")
async def delete_task(task_id: int, request: Request, db: AsyncSession = Depends(get_async_db_session)):
    """
    Delete a task.
    """
    from ..services.reminder_scheduler import ReminderScheduler

    # Get user_id from request state (set by auth middleware)
    user_id = get_current_user_id(request)

    # Check if task exists and belongs to user
    task = await crud.get_task_by_id(db_session=db, task_id=task_id, user_id=user_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Delete the task
    success = await crud.delete_task(db_session=db, task_id=task_id, user_id=user_id)
    if not success:
        raise HTTPException(status_code=500, detail="Failed to delete task")

    # Cancel any scheduled reminder for the deleted task
    await ReminderScheduler.cancel_scheduled_reminder(str(task_id))

    # Publish deletion event
    event_payload = {
        "event_type": "task.deleted",
        "task_id": str(task_id),
        "user_id": str(user_id),
        "timestamp": datetime.utcnow().isoformat(),
        "payload": {
            "title": task.title
        }
    }

    await EventPublisher.publish_event(
        event_type=event_payload["event_type"],
        data=event_payload["payload"],
        task_id=event_payload.get("task_id"),
        user_id=event_payload.get("user_id")
    )

    return {"message": "Task deleted successfully"}