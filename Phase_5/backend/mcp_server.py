import asyncio
import logging
import os
from contextlib import asynccontextmanager
from datetime import datetime
from typing import List, Optional

from dotenv import load_dotenv
from mcp.server import Server
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from database import get_db_session
from models import Task

# Load environment variables
load_dotenv()

# Configure logging
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)

# Initialize MCP server
server = Server("todo-mcp-server")


@server.tool()
async def add_task(user_id: str, title: str, description: Optional[str] = None):
    """
    Create a new task in the database

    Args:
        user_id: User identifier
        title: Task title (max 200 chars)
        description: Task details (max 1000 chars, optional)

    Returns:
        Dictionary with task_id, status, and title
    """
    logger.info(f"add_task called for user {user_id}")

    # Validate inputs
    if not user_id:
        return {"error": "user_id is required"}

    if not title:
        return {"error": "title is required"}

    if not title.strip():
        return {"error": "title cannot be empty"}

    if len(title) > 200:
        return {"error": "title exceeds maximum length of 200 characters"}

    if description and len(description) > 1000:
        return {"error": "description exceeds maximum length of 1000 characters"}

    try:
        # Convert user_id to integer for database storage
        user_id_int = int(user_id)

        async with get_db_session() as session:
            # Create new task
            task = Task(
                user_id=user_id_int,
                title=title.strip(),
                description=description.strip() if description else None
            )

            session.add(task)
            await session.commit()
            await session.refresh(task)

            logger.info(f"Task {task.id} created for user {user_id}")
            return {
                "task_id": task.id,
                "status": "created",
                "title": task.title
            }
    except ValueError:
        logger.error(f"Invalid user_id format: {user_id}")
        return {"error": "Invalid user_id format"}
    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        return {"error": "Failed to create task"}


@server.tool()
async def list_tasks(user_id: str, status: Optional[str] = "all"):
    """
    Retrieve tasks from database based on filter

    Args:
        user_id: User identifier
        status: Filter by "all", "pending", or "completed" (default: "all")

    Returns:
        List of task dictionaries
    """
    logger.info(f"list_tasks called for user {user_id} with status {status}")

    # Validate inputs
    if not user_id:
        return {"error": "user_id is required"}

    if status not in ["all", "pending", "completed"]:
        return {"error": "status must be 'all', 'pending', or 'completed'"}

    try:
        # Convert user_id to integer for database query
        user_id_int = int(user_id)

        async with get_db_session() as session:
            # Build query based on status filter
            query = select(Task).where(Task.user_id == user_id_int)

            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)

            # Execute query
            result = await session.exec(query)
            tasks = result.all()

            # Format response
            formatted_tasks = []
            for task in tasks:
                formatted_tasks.append({
                    "id": task.id,
                    "title": task.title,
                    "description": task.description,
                    "completed": task.completed,
                    "created_at": task.created_at.isoformat()
                })

            logger.info(f"Found {len(formatted_tasks)} tasks for user {user_id}")
            return formatted_tasks
    except ValueError:
        logger.error(f"Invalid user_id format: {user_id}")
        return {"error": "Invalid user_id format"}
    except Exception as e:
        logger.error(f"Failed to retrieve tasks: {e}")
        return {"error": "Failed to retrieve tasks"}


@server.tool()
async def complete_task(user_id: str, task_id: int):
    """
    Mark a specific task as completed

    Args:
        user_id: User identifier
        task_id: Task ID to complete

    Returns:
        Dictionary with task_id, status, and title
    """
    logger.info(f"complete_task called for user {user_id}, task {task_id}")

    # Validate inputs
    if not user_id:
        return {"error": "user_id is required"}

    if not task_id:
        return {"error": "task_id is required"}

    try:
        # Convert user_id to integer for database query
        user_id_int = int(user_id)

        async with get_db_session() as session:
            # Find the task
            query = select(Task).where(Task.user_id == user_id_int, Task.id == task_id)
            result = await session.exec(query)
            task = result.first()

            if not task:
                return {"error": f"Task {task_id} not found"}

            # Update task as completed
            task.completed = True
            session.add(task)
            await session.commit()
            await session.refresh(task)

            logger.info(f"Task {task.id} marked as completed for user {user_id}")
            return {
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            }
    except ValueError:
        logger.error(f"Invalid user_id format: {user_id}")
        return {"error": "Invalid user_id format"}
    except Exception as e:
        logger.error(f"Failed to complete task {task_id}: {e}")
        return {"error": "Failed to complete task"}


@server.tool()
async def delete_task(user_id: str, task_id: int):
    """
    Remove a task from database

    Args:
        user_id: User identifier
        task_id: Task ID to delete

    Returns:
        Dictionary with task_id, status, and title
    """
    logger.info(f"delete_task called for user {user_id}, task {task_id}")

    # Validate inputs
    if not user_id:
        return {"error": "user_id is required"}

    if not task_id:
        return {"error": "task_id is required"}

    try:
        # Convert user_id to integer for database query
        user_id_int = int(user_id)

        async with get_db_session() as session:
            # Find the task
            query = select(Task).where(Task.user_id == user_id_int, Task.id == task_id)
            result = await session.exec(query)
            task = result.first()

            if not task:
                return {"error": f"Task {task_id} not found"}

            # Delete the task
            await session.delete(task)
            await session.commit()

            logger.info(f"Task {task.id} deleted for user {user_id}")
            return {
                "task_id": task.id,
                "status": "deleted",
                "title": task.title
            }
    except ValueError:
        logger.error(f"Invalid user_id format: {user_id}")
        return {"error": "Invalid user_id format"}
    except Exception as e:
        logger.error(f"Failed to delete task {task_id}: {e}")
        return {"error": "Failed to delete task"}


@server.tool()
async def update_task(user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None):
    """
    Modify task title or description

    Args:
        user_id: User identifier
        task_id: Task ID to update
        title: New title (max 200 chars, optional)
        description: New description (max 1000 chars, optional)

    Returns:
        Dictionary with task_id, status, and title
    """
    logger.info(f"update_task called for user {user_id}, task {task_id}")

    # Validate inputs
    if not user_id:
        return {"error": "user_id is required"}

    if not task_id:
        return {"error": "task_id is required"}

    if not title and not description:
        return {"error": "At least one field (title or description) required"}

    if title and not title.strip():
        return {"error": "title cannot be empty"}

    if title and len(title) > 200:
        return {"error": "title exceeds maximum length of 200 characters"}

    if description and len(description) > 1000:
        return {"error": "description exceeds maximum length of 1000 characters"}

    try:
        # Convert user_id to integer for database query
        user_id_int = int(user_id)

        async with get_db_session() as session:
            # Find the task
            query = select(Task).where(Task.user_id == user_id_int, Task.id == task_id)
            result = await session.exec(query)
            task = result.first()

            if not task:
                return {"error": f"Task {task_id} not found"}

            # Update fields if provided
            if title is not None:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip()

            session.add(task)
            await session.commit()
            await session.refresh(task)

            logger.info(f"Task {task.id} updated for user {user_id}")
            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            }
    except ValueError:
        logger.error(f"Invalid user_id format: {user_id}")
        return {"error": "Invalid user_id format"}
    except Exception as e:
        logger.error(f"Failed to update task {task_id}: {e}")
        return {"error": "Failed to update task"}


# Health check endpoint
@server.get("/health")
async def health_check():
    """Health check endpoint for the MCP server"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


if __name__ == "__main__":
    port = int(os.getenv("MCP_SERVER_PORT", 8001))
    logger.info(f"Starting MCP server on port {port}")
    server.run(port=port)