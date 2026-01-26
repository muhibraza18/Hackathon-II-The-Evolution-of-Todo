"""
Real MCP Server with Database Integration
This server connects to Neon PostgreSQL and persists all tasks
"""
import asyncio
import logging
import os
import sys
from datetime import datetime
from typing import Optional
from pathlib import Path

from dotenv import load_dotenv
from aiohttp import web
from sqlmodel import select

# Add the backend directory to the Python path
backend_dir = Path(__file__).parent
sys.path.insert(0, str(backend_dir))

# Import database modules - these must exist in backend/app/database/
from app.database.connection import get_db_session_async as get_db_session
from app.database.models import Task

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def add_task_handler(request):
    """Handle add_task requests - Database version"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        title = data.get('title')
        description = data.get('description')

        # Validate inputs
        if not user_id:
            return web.json_response({"error": "user_id is required"}, status=400)

        if not title or not title.strip():
            return web.json_response({"error": "title is required and cannot be empty"}, status=400)

        if len(title) > 200:
            return web.json_response({"error": "title exceeds maximum length of 200 characters"}, status=400)

        if description and len(description) > 1000:
            return web.json_response({"error": "description exceeds maximum length of 1000 characters"}, status=400)

        # Convert user_id to integer
        user_id_int = int(user_id)

        # Create task in database
        async with get_db_session() as session:
            task = Task(
                user_id=user_id_int,
                title=title.strip(),
                description=description.strip() if description else None,
                completed=False
            )

            session.add(task)
            await session.commit()
            await session.refresh(task)

            logger.info(f"✅ DATABASE: Task {task.id} created for user {user_id}")
            
            return web.json_response({
                "task_id": task.id,
                "status": "created",
                "title": task.title
            })

    except ValueError as e:
        logger.error(f"❌ Invalid user_id format: {user_id}")
        return web.json_response({"error": "Invalid user_id format"}, status=400)
    except Exception as e:
        logger.error(f"❌ Failed to create task in database: {e}")
        import traceback
        traceback.print_exc()
        return web.json_response({"error": f"Failed to create task: {str(e)}"}, status=500)


async def list_tasks_handler(request):
    """Handle list_tasks requests - Database version"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        status = data.get('status', 'all')

        if not user_id:
            return web.json_response({"error": "user_id is required"}, status=400)

        if status not in ["all", "pending", "completed"]:
            return web.json_response({"error": "status must be 'all', 'pending', or 'completed'"}, status=400)

        user_id_int = int(user_id)

        async with get_db_session() as session:
            # Build query
            query = select(Task).where(Task.user_id == user_id_int)
            
            if status == "pending":
                query = query.where(Task.completed == False)
            elif status == "completed":
                query = query.where(Task.completed == True)

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
                    "created_at": task.created_at.isoformat() if task.created_at else None
                })

            logger.info(f"✅ DATABASE: Found {len(formatted_tasks)} tasks for user {user_id}")
            return web.json_response(formatted_tasks)

    except ValueError:
        logger.error(f"❌ Invalid user_id format: {user_id}")
        return web.json_response({"error": "Invalid user_id format"}, status=400)
    except Exception as e:
        logger.error(f"❌ Failed to retrieve tasks from database: {e}")
        import traceback
        traceback.print_exc()
        return web.json_response({"error": f"Failed to retrieve tasks: {str(e)}"}, status=500)


async def complete_task_handler(request):
    """Handle complete_task requests - Database version"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        task_id = data.get('task_id')

        if not user_id or not task_id:
            return web.json_response({"error": "user_id and task_id are required"}, status=400)

        user_id_int = int(user_id)
        task_id_int = int(task_id)

        async with get_db_session() as session:
            query = select(Task).where(Task.user_id == user_id_int, Task.id == task_id_int)
            result = await session.exec(query)
            task = result.first()

            if not task:
                return web.json_response({"error": f"Task {task_id_int} not found"}, status=404)

            task.completed = True
            session.add(task)
            await session.commit()
            await session.refresh(task)

            logger.info(f"✅ DATABASE: Task {task.id} completed for user {user_id}")
            return web.json_response({
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            })

    except ValueError:
        logger.error(f"❌ Invalid input format")
        return web.json_response({"error": "Invalid user_id or task_id format"}, status=400)
    except Exception as e:
        logger.error(f"❌ Failed to complete task: {e}")
        import traceback
        traceback.print_exc()
        return web.json_response({"error": f"Failed to complete task: {str(e)}"}, status=500)


async def delete_task_handler(request):
    """Handle delete_task requests - Database version"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        task_id = data.get('task_id')

        if not user_id or not task_id:
            return web.json_response({"error": "user_id and task_id are required"}, status=400)

        user_id_int = int(user_id)
        task_id_int = int(task_id)

        async with get_db_session() as session:
            query = select(Task).where(Task.user_id == user_id_int, Task.id == task_id_int)
            result = await session.exec(query)
            task = result.first()

            if not task:
                return web.json_response({"error": f"Task {task_id_int} not found"}, status=404)

            title = task.title
            await session.delete(task)
            await session.commit()

            logger.info(f"✅ DATABASE: Task {task_id_int} deleted for user {user_id}")
            return web.json_response({
                "task_id": task_id_int,
                "status": "deleted",
                "title": title
            })

    except ValueError:
        logger.error(f"❌ Invalid input format")
        return web.json_response({"error": "Invalid user_id or task_id format"}, status=400)
    except Exception as e:
        logger.error(f"❌ Failed to delete task: {e}")
        import traceback
        traceback.print_exc()
        return web.json_response({"error": f"Failed to delete task: {str(e)}"}, status=500)


async def update_task_handler(request):
    """Handle update_task requests - Database version"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        task_id = data.get('task_id')
        title = data.get('title')
        description = data.get('description')

        if not user_id or not task_id:
            return web.json_response({"error": "user_id and task_id are required"}, status=400)

        if not title and description is None:
            return web.json_response({"error": "At least one field (title or description) required"}, status=400)

        if title and not title.strip():
            return web.json_response({"error": "title cannot be empty"}, status=400)

        if title and len(title) > 200:
            return web.json_response({"error": "title exceeds maximum length"}, status=400)

        if description and len(description) > 1000:
            return web.json_response({"error": "description exceeds maximum length"}, status=400)

        user_id_int = int(user_id)
        task_id_int = int(task_id)

        async with get_db_session() as session:
            query = select(Task).where(Task.user_id == user_id_int, Task.id == task_id_int)
            result = await session.exec(query)
            task = result.first()

            if not task:
                return web.json_response({"error": f"Task {task_id_int} not found"}, status=404)

            if title is not None:
                task.title = title.strip()
            if description is not None:
                task.description = description.strip()

            session.add(task)
            await session.commit()
            await session.refresh(task)

            logger.info(f"✅ DATABASE: Task {task.id} updated for user {user_id}")
            return web.json_response({
                "task_id": task.id,
                "status": "updated",
                "title": task.title
            })

    except ValueError:
        logger.error(f"❌ Invalid input format")
        return web.json_response({"error": "Invalid user_id or task_id format"}, status=400)
    except Exception as e:
        logger.error(f"❌ Failed to update task: {e}")
        import traceback
        traceback.print_exc()
        return web.json_response({"error": f"Failed to update task: {str(e)}"}, status=500)


async def health_handler(request):
    """Health check endpoint"""
    return web.json_response({
        "status": "healthy",
        "server": "database-connected-mcp",
        "port": 8002,
        "timestamp": datetime.utcnow().isoformat()
    })


def create_app():
    """Create the aiohttp web application"""
    app = web.Application()

    # Add routes
    app.router.add_post('/add_task', add_task_handler)
    app.router.add_post('/list_tasks', list_tasks_handler)
    app.router.add_post('/complete_task', complete_task_handler)
    app.router.add_post('/delete_task', delete_task_handler)
    app.router.add_post('/update_task', update_task_handler)
    app.router.add_get('/health', health_handler)

    return app


if __name__ == '__main__':
    app = create_app()
    port = 8002  # Fixed port - different from FastAPI (8000)
    
    logger.info("=" * 60)
    logger.info("🚀 Starting DATABASE-CONNECTED MCP Server")
    logger.info(f"📍 Port: {port}")
    logger.info(f"📊 Database: Neon PostgreSQL (persistent storage)")
    logger.info(f"🔗 Health check: http://localhost:{port}/health")
    logger.info("=" * 60)
    
    web.run_app(app, host='localhost', port=port)