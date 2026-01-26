"""
Simple mock MCP server to unblock the main application.
This mimics the expected behavior of the real MCP server.
"""
import asyncio
from aiohttp import web, hdrs
import json
import logging
from typing import Dict, Any, Optional

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# In-memory storage for tasks (temporary solution)
tasks_db = []
next_task_id = 1


async def add_task_handler(request):
    """Handle add_task requests"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        title = data.get('title')
        description = data.get('description')

        global next_task_id

        # Validate inputs
        if not user_id:
            return web.json_response({"error": "user_id is required"}, status=400)

        if not title:
            return web.json_response({"error": "title is required"}, status=400)

        if not title.strip():
            return web.json_response({"error": "title cannot be empty"}, status=400)

        if len(title) > 200:
            return web.json_response({"error": "title exceeds maximum length of 200 characters"}, status=400)

        if description and len(description) > 1000:
            return web.json_response({"error": "description exceeds maximum length of 1000 characters"}, status=400)

        # Create task
        task = {
            "id": next_task_id,
            "user_id": int(user_id),
            "title": title.strip(),
            "description": description.strip() if description else None,
            "completed": False,
            "created_at": "2026-01-15T23:59:59"
        }

        tasks_db.append(task)
        task_copy = task.copy()
        next_task_id += 1

        # Remove user_id from response to match expected format
        del task_copy["user_id"]

        logger.info(f"Task {task_copy['id']} created for user {user_id}")
        return web.json_response({
            "task_id": task_copy["id"],
            "status": "created",
            "title": task_copy["title"]
        })
    except ValueError as e:
        logger.error(f"Invalid user_id format: {data.get('user_id') if 'data' in locals() else 'unknown'}")
        return web.json_response({"error": "Invalid user_id format"}, status=400)
    except Exception as e:
        logger.error(f"Failed to create task: {e}")
        return web.json_response({"error": "Failed to create task"}, status=500)


async def list_tasks_handler(request):
    """Handle list_tasks requests"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        status = data.get('status', 'all')

        # Validate inputs
        if not user_id:
            return web.json_response({"error": "user_id is required"}, status=400)

        if status not in ["all", "pending", "completed"]:
            return web.json_response({"error": "status must be 'all', 'pending', or 'completed'"}, status=400)

        user_id_int = int(user_id)

        # Filter tasks for the user
        user_tasks = [task for task in tasks_db if task["user_id"] == user_id_int]

        # Apply status filter
        if status == "pending":
            user_tasks = [task for task in user_tasks if not task["completed"]]
        elif status == "completed":
            user_tasks = [task for task in user_tasks if task["completed"]]

        # Format response
        formatted_tasks = []
        for task in user_tasks:
            formatted_task = {
                "id": task["id"],
                "title": task["title"],
                "description": task["description"],
                "completed": task["completed"],
                "created_at": task["created_at"]
            }
            formatted_tasks.append(formatted_task)

        logger.info(f"Found {len(formatted_tasks)} tasks for user {user_id}")
        return web.json_response(formatted_tasks)
    except ValueError:
        logger.error(f"Invalid user_id format: {data.get('user_id') if 'data' in locals() else 'unknown'}")
        return web.json_response({"error": "Invalid user_id format"}, status=400)
    except Exception as e:
        logger.error(f"Failed to retrieve tasks: {e}")
        return web.json_response({"error": "Failed to retrieve tasks"}, status=500)


async def complete_task_handler(request):
    """Handle complete_task requests"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        task_id = data.get('task_id')

        # Validate inputs
        if not user_id:
            return web.json_response({"error": "user_id is required"}, status=400)

        if not task_id:
            return web.json_response({"error": "task_id is required"}, status=400)

        user_id_int = int(user_id)
        task_id_int = int(task_id)

        # Find the task
        task = None
        for t in tasks_db:
            if t["user_id"] == user_id_int and t["id"] == task_id_int:
                task = t
                break

        if not task:
            return web.json_response({"error": f"Task {task_id_int} not found"}, status=404)

        # Update task as completed
        task["completed"] = True

        logger.info(f"Task {task_id_int} marked as completed for user {user_id}")
        return web.json_response({
            "task_id": task["id"],
            "status": "completed",
            "title": task["title"]
        })
    except ValueError:
        logger.error(f"Invalid input format: user_id={data.get('user_id')}, task_id={data.get('task_id')}")
        return web.json_response({"error": "Invalid user_id or task_id format"}, status=400)
    except Exception as e:
        logger.error(f"Failed to complete task {task_id}: {e}")
        return web.json_response({"error": "Failed to complete task"}, status=500)


async def delete_task_handler(request):
    """Handle delete_task requests"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        task_id = data.get('task_id')

        # Validate inputs
        if not user_id:
            return web.json_response({"error": "user_id is required"}, status=400)

        if not task_id:
            return web.json_response({"error": "task_id is required"}, status=400)

        user_id_int = int(user_id)
        task_id_int = int(task_id)

        # Find and remove the task
        task_index = None
        for i, t in enumerate(tasks_db):
            if t["user_id"] == user_id_int and t["id"] == task_id_int:
                task_index = i
                break

        if task_index is None:
            return web.json_response({"error": f"Task {task_id_int} not found"}, status=404)

        task = tasks_db.pop(task_index)

        logger.info(f"Task {task_id_int} deleted for user {user_id}")
        return web.json_response({
            "task_id": task["id"],
            "status": "deleted",
            "title": task["title"]
        })
    except ValueError:
        logger.error(f"Invalid input format: user_id={data.get('user_id')}, task_id={data.get('task_id')}")
        return web.json_response({"error": "Invalid user_id or task_id format"}, status=400)
    except Exception as e:
        logger.error(f"Failed to delete task {task_id}: {e}")
        return web.json_response({"error": "Failed to delete task"}, status=500)


async def update_task_handler(request):
    """Handle update_task requests"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        task_id = data.get('task_id')
        title = data.get('title')
        description = data.get('description')

        # Validate inputs
        if not user_id:
            return web.json_response({"error": "user_id is required"}, status=400)

        if not task_id:
            return web.json_response({"error": "task_id is required"}, status=400)

        if not title and not description:
            return web.json_response({"error": "At least one field (title or description) required"}, status=400)

        if title and not title.strip():
            return web.json_response({"error": "title cannot be empty"}, status=400)

        if title and len(title) > 200:
            return web.json_response({"error": "title exceeds maximum length of 200 characters"}, status=400)

        if description and len(description) > 1000:
            return web.json_response({"error": "description exceeds maximum length of 1000 characters"}, status=400)

        user_id_int = int(user_id)
        task_id_int = int(task_id)

        # Find the task
        task = None
        for t in tasks_db:
            if t["user_id"] == user_id_int and t["id"] == task_id_int:
                task = t
                break

        if not task:
            return web.json_response({"error": f"Task {task_id_int} not found"}, status=404)

        # Update fields if provided
        if title is not None:
            task["title"] = title.strip()
        if description is not None:
            task["description"] = description.strip()

        logger.info(f"Task {task_id_int} updated for user {user_id}")
        return web.json_response({
            "task_id": task["id"],
            "status": "updated",
            "title": task["title"]
        })
    except ValueError:
        logger.error(f"Invalid input format: user_id={data.get('user_id')}, task_id={data.get('task_id')}")
        return web.json_response({"error": "Invalid user_id or task_id format"}, status=400)
    except Exception as e:
        logger.error(f"Failed to update task {task_id}: {e}")
        return web.json_response({"error": "Failed to update task"}, status=500)


async def health_handler(request):
    """Health check endpoint"""
    return web.json_response({"status": "healthy", "timestamp": "2026-01-15T23:59:59"})


def create_app():
    """Create the aiohttp web application"""
    app = web.Application()

    # Add routes for the expected MCP endpoints
    app.router.add_post('/add_task', add_task_handler)
    app.router.add_post('/list_tasks', list_tasks_handler)
    app.router.add_post('/complete_task', complete_task_handler)
    app.router.add_post('/delete_task', delete_task_handler)
    app.router.add_post('/update_task', update_task_handler)
    app.router.add_get('/health', health_handler)

    return app


if __name__ == '__main__':
    app = create_app()
    logger.info("Starting mock MCP server on port 8001...")
    web.run_app(app, host='localhost', port=8001)