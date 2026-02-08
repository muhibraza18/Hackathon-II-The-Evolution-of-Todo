from sqlmodel import select, func
from sqlalchemy.exc import IntegrityError
from typing import List, Optional
from datetime import datetime, timedelta
from .database.models import Task, Conversation, Message, Reminder
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy import and_, or_, text


# Task CRUD Operations
async def create_task(db_session: AsyncSession, user_id: str, title: str, description: Optional[str] = None, completed: bool = False,
                     due_date: Optional[datetime] = None, priority: Optional[str] = None, tags: Optional[str] = None,
                     recurring_config: Optional[str] = None) -> Task:
    """
    Create a new task for a user.

    Args:
        db_session: Database session
        user_id: ID of the user creating the task
        title: Title of the task
        description: Optional description of the task
        completed: Whether the task is completed (default: False)
        due_date: Optional due date for the task
        priority: Optional priority level (low, medium, high, urgent)
        tags: Optional JSON string of tags array
        recurring_config: Optional JSON string of recurring configuration

    Returns:
        Created Task object
    """
    # Validate new fields
    if not Task.validate_priority(priority):
        raise ValueError(f"Invalid priority: {priority}")
    if not Task.validate_tags(tags):
        raise ValueError(f"Invalid tags: {tags}")
    if not Task.validate_due_date(due_date):
        raise ValueError(f"Invalid due date: {due_date}")
    if not Task.validate_recurring_config(recurring_config):
        raise ValueError(f"Invalid recurring config: {recurring_config}")

    task = Task(
        user_id=user_id,
        title=title,
        description=description,
        completed=completed,
        due_date=due_date,
        priority=priority,
        tags=tags,
        recurring_config=recurring_config
    )
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task


async def get_tasks(db_session: AsyncSession, user_id: str, completed: Optional[bool] = None, search: Optional[str] = None) -> List[Task]:
    """
    Get all tasks for a user, optionally filtered by completion status and search term.

    Args:
        db_session: Database session
        user_id: ID of the user whose tasks to retrieve
        completed: Optional filter for completion status
        search: Optional search term to match against title and description

    Returns:
        List of Task objects
    """
    query = select(Task).where(Task.user_id == user_id)

    if completed is not None:
        query = query.where(Task.completed == completed)

    # Add search functionality
    if search:
        search_term = f"%{search}%"
        query = query.where(
            or_(
                Task.title.ilike(search_term),
                Task.description.ilike(search_term) if Task.description is not None else False
            )
        )

    query = query.order_by(Task.created_at.desc())

    result = await db_session.exec(query)
    return result.all()


async def search_tasks(db_session: AsyncSession, user_id: str, search_term: str,
                      completed: Optional[bool] = None,
                      priority: Optional[str] = None,
                      due_before: Optional[datetime] = None,
                      due_after: Optional[datetime] = None) -> List[Task]:
    """
    Search tasks with multiple filters.

    Args:
        db_session: Database session
        user_id: ID of the user whose tasks to search
        search_term: Term to search for in title and description
        completed: Optional filter for completion status
        priority: Optional filter for priority
        due_before: Optional filter for due date before this date
        due_after: Optional filter for due date after this date

    Returns:
        List of matching Task objects
    """
    query = select(Task).where(Task.user_id == user_id)

    # Add search term filter
    if search_term:
        search_pattern = f"%{search_term}%"
        query = query.where(
            or_(
                Task.title.ilike(search_pattern),
                Task.description.ilike(search_pattern) if Task.description is not None else False
            )
        )

    # Add filters
    if completed is not None:
        query = query.where(Task.completed == completed)

    if priority is not None:
        query = query.where(Task.priority == priority)

    if due_before is not None:
        query = query.where(Task.due_date <= due_before)

    if due_after is not None:
        query = query.where(Task.due_date >= due_after)

    query = query.order_by(Task.created_at.desc())

    result = await db_session.exec(query)
    return result.all()


async def get_task_by_id(db_session: AsyncSession, task_id: int, user_id: str) -> Optional[Task]:
    """
    Get a specific task by ID for a user.

    Args:
        db_session: Database session
        task_id: ID of the task to retrieve
        user_id: ID of the user (for authorization)

    Returns:
        Task object if found, None otherwise
    """
    query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
    result = await db_session.exec(query)
    return result.first()


async def update_task(db_session: AsyncSession, task_id: int, user_id: str, title: Optional[str] = None,
                     description: Optional[str] = None, completed: Optional[bool] = None,
                     due_date: Optional[datetime] = None, priority: Optional[str] = None,
                     tags: Optional[str] = None, recurring_config: Optional[str] = None) -> Optional[Task]:
    """
    Update a task for a user.

    Args:
        db_session: Database session
        task_id: ID of the task to update
        user_id: ID of the user (for authorization)
        title: New title (optional)
        description: New description (optional)
        completed: New completion status (optional)
        due_date: New due date (optional)
        priority: New priority level (optional)
        tags: New tags JSON string (optional)
        recurring_config: New recurring config JSON string (optional)

    Returns:
        Updated Task object if successful, None if not found
    """
    task = await get_task_by_id(db_session, task_id, user_id)
    if not task:
        return None

    if title is not None:
        task.title = title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed
    if due_date is not None:
        if not Task.validate_due_date(due_date):
            raise ValueError(f"Invalid due date: {due_date}")
        task.due_date = due_date
    if priority is not None:
        if not Task.validate_priority(priority):
            raise ValueError(f"Invalid priority: {priority}")
        task.priority = priority
    if tags is not None:
        if not Task.validate_tags(tags):
            raise ValueError(f"Invalid tags: {tags}")
        task.tags = tags
    if recurring_config is not None:
        if not Task.validate_recurring_config(recurring_config):
            raise ValueError(f"Invalid recurring config: {recurring_config}")
        task.recurring_config = recurring_config

    task.updated_at = func.now()
    db_session.add(task)
    await db_session.commit()
    await db_session.refresh(task)
    return task


async def delete_task(db_session: AsyncSession, task_id: int, user_id: str) -> bool:
    """
    Delete a task for a user.

    Args:
        db_session: Database session
        task_id: ID of the task to delete
        user_id: ID of the user (for authorization)

    Returns:
        True if deletion was successful, False otherwise
    """
    task = await get_task_by_id(db_session, task_id, user_id)
    if not task:
        return False

    await db_session.delete(task)
    await db_session.commit()
    return True


# Conversation CRUD Operations
async def create_conversation(db_session: AsyncSession, user_id: str) -> Conversation:
    """
    Create a new conversation for a user.

    Args:
        db_session: Database session
        user_id: ID of the user creating the conversation

    Returns:
        Created Conversation object
    """
    conversation = Conversation(user_id=user_id)
    db_session.add(conversation)
    await db_session.commit()
    await db_session.refresh(conversation)
    return conversation


async def get_conversations(db_session: AsyncSession, user_id: str) -> List[Conversation]:
    """
    Get all conversations for a user.

    Args:
        db_session: Database session
        user_id: ID of the user whose conversations to retrieve

    Returns:
        List of Conversation objects
    """
    query = select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.created_at.desc())
    result = await db_session.exec(query)
    return result.all()


async def get_conversation_by_id(db_session: AsyncSession, conversation_id: int, user_id: str) -> Optional[Conversation]:
    """
    Get a specific conversation by ID for a user.

    Args:
        db_session: Database session
        conversation_id: ID of the conversation to retrieve
        user_id: ID of the user (for authorization)

    Returns:
        Conversation object if found, None otherwise
    """
    query = select(Conversation).where(Conversation.id == conversation_id, Conversation.user_id == user_id)
    result = await db_session.exec(query)
    return result.first()


async def delete_conversation(db_session: AsyncSession, conversation_id: int, user_id: str) -> bool:
    """
    Delete a conversation for a user (and all associated messages due to cascade delete).

    Args:
        db_session: Database session
        conversation_id: ID of the conversation to delete
        user_id: ID of the user (for authorization)

    Returns:
        True if deletion was successful, False otherwise
    """
    conversation = await get_conversation_by_id(db_session, conversation_id, user_id)
    if not conversation:
        return False

    await db_session.delete(conversation)
    await db_session.commit()
    return True


# Message CRUD Operations
async def create_message(db_session: AsyncSession, user_id: str, conversation_id: int, role: str, content: str) -> Message:
    """
    Create a new message in a conversation.

    Args:
        db_session: Database session
        user_id: ID of the user creating the message
        conversation_id: ID of the conversation
        role: Role of the sender ('user' or 'assistant')
        content: Content of the message

    Returns:
        Created Message object
    """
    message = Message(user_id=user_id, conversation_id=conversation_id, role=role, content=content)
    db_session.add(message)
    await db_session.commit()
    await db_session.refresh(message)
    return message


async def get_messages_by_conversation(db_session: AsyncSession, conversation_id: int, user_id: str) -> List[Message]:
    """
    Get all messages in a conversation for a user.

    Args:
        db_session: Database session
        conversation_id: ID of the conversation
        user_id: ID of the user (for authorization)

    Returns:
        List of Message objects
    """
    query = select(Message).where(
        Message.conversation_id == conversation_id,
        Message.user_id == user_id
    ).order_by(Message.created_at.asc())

    result = await db_session.exec(query)
    return result.all()


async def get_message_by_id(db_session: AsyncSession, message_id: int, user_id: str) -> Optional[Message]:
    """
    Get a specific message by ID for a user.

    Args:
        db_session: Database session
        message_id: ID of the message to retrieve
        user_id: ID of the user (for authorization)

    Returns:
        Message object if found, None otherwise
    """
    query = select(Message).where(Message.id == message_id, Message.user_id == user_id)
    result = await db_session.exec(query)
    return result.first()

# Reminder CRUD Operations for Phase V - Redpanda Cloud Integration
async def create_reminder(db_session: AsyncSession, task_id: int, user_id: int, due_time: datetime) -> "Reminder":
    """
    Create a reminder for a task with a specific due time.
    
    Args:
        db_session: Database session
        task_id: ID of the task to create reminder for
        user_id: ID of the user who owns the task
        due_time: When the reminder should trigger (UTC timestamp)
        
    Returns:
        Created Reminder object
    """
    from .database.models import Reminder
    
    reminder = Reminder(task_id=task_id, user_id=user_id, due_time=due_time)
    db_session.add(reminder)
    await db_session.commit()
    await db_session.refresh(reminder)
    return reminder


async def get_pending_reminders(db_session: AsyncSession, user_id: int, within_minutes: int = 5) -> List["Reminder"]:
    """
    Get all pending reminders for a user that are due within the specified time window.
    
    Args:
        db_session: Database session
        user_id: ID of the user
        within_minutes: Only return reminders due within this many minutes
        
    Returns:
        List of Reminder objects
    """
    from .database.models import Reminder
    from sqlalchemy import and_
    
    time_window = datetime.utcnow() + timedelta(minutes=within_minutes)
    
    query = select(Reminder).where(
        and_(
            Reminder.user_id == user_id,
            Reminder.status == "pending",
            Reminder.due_time <= time_window
        )
    ).order_by(Reminder.due_time.asc())
    
    result = await db_session.exec(query)
    return result.all()


async def get_reminder_by_task_id(db_session: AsyncSession, task_id: int, user_id: int) -> Optional["Reminder"]:
    """
    Get a reminder by task ID.
    
    Args:
        db_session: Database session
        task_id: ID of the task
        user_id: ID of the user (for authorization)
        
    Returns:
        Reminder object if found, None otherwise
    """
    from .database.models import Reminder
    
    query = select(Reminder).where(Reminder.task_id == task_id, Reminder.user_id == user_id)
    result = await db_session.exec(query)
    return result.first()


async def mark_reminder_sent(db_session: AsyncSession, reminder_id: int, user_id: int) -> Optional["Reminder"]:
    """
    Mark a reminder as sent.
    
    Args:
        db_session: Database session
        reminder_id: ID of the reminder
        user_id: ID of the user (for authorization)
        
    Returns:
        Updated Reminder object if found, None otherwise
    """
    from .database.models import Reminder
    
    query = select(Reminder).where(Reminder.id == reminder_id, Reminder.user_id == user_id)
    result = await db_session.exec(query)
    reminder = result.first()
    
    if reminder:
        reminder.status = "sent"
        reminder.sent_at = datetime.utcnow()
        db_session.add(reminder)
        await db_session.commit()
        await db_session.refresh(reminder)
    
    return reminder
