"""
Minimal MCP Server for DigitalOcean Kubernetes Deployment
Standalone version with direct database connection
"""
import asyncio
import logging
import os
import json
from datetime import datetime
from typing import Optional

from dotenv import load_dotenv
from aiohttp import web, ClientSession
import asyncpg
from aiohttp import web

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Database connection
DATABASE_URL = os.getenv("DATABASE_URL")
BACKEND_API_URL = os.getenv("BACKEND_API_URL", "http://backend-service:8000")

# Pool for database connections
db_pool = None


async def init_db_pool():
    """Initialize the database connection pool"""
    global db_pool
    try:
        # Parse DATABASE_URL and create connection
        # Format: postgresql+asyncpg://user:pass@host:port/db
        db_url = DATABASE_URL.replace("postgresql+asyncpg://", "postgresql://")
        logger.info(f"🔗 Connecting to database...")

        db_pool = await asyncpg.create_pool(
            db_url,
            min_size=1,
            max_size=10,
            command_timeout=60
        )
        logger.info("✅ Database pool created successfully")
        return db_pool
    except Exception as e:
        logger.error(f"❌ Failed to create database pool: {e}")
        return None


async def close_db_pool():
    """Close the database connection pool"""
    global db_pool
    if db_pool:
        await db_pool.close()
        logger.info("🔌 Database pool closed")


async def execute_query(query: str, *args):
    """Execute a database query"""
    global db_pool
    if not db_pool:
        raise Exception("Database pool not initialized")

    async with db_pool.acquire() as conn:
        return await conn.fetch(query, *args)


# Health check endpoint
async def health_handler(request):
    """Health check endpoint"""
    db_status = "connected" if db_pool else "disconnected"
    return web.json_response({
        "status": "healthy",
        "service": "mcp-server",
        "database": db_status,
        "backend_api": BACKEND_API_URL
    })


# List tasks endpoint
async def list_tasks_handler(request):
    """Handle list_tasks requests from chat agent"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        status = data.get('status', 'all')

        if not user_id:
            return web.json_response({"error": "user_id is required"}, status=400)

        # Build query based on status filter (table name is 'task' not 'tasks')
        if status == "completed":
            query = "SELECT * FROM task WHERE user_id = $1 AND completed = true ORDER BY created_at DESC"
        elif status == "pending":
            query = "SELECT * FROM task WHERE user_id = $1 AND completed = false ORDER BY created_at DESC"
        else:  # 'all'
            query = "SELECT * FROM task WHERE user_id = $1 ORDER BY created_at DESC"

        rows = await execute_query(query, int(user_id))

        tasks = []
        for row in rows:
            tasks.append({
                "id": row['id'],
                "title": row['title'],
                "description": row.get('description'),
                "completed": row['completed'],
                "due_date": row.get('due_date').isoformat() if row.get('due_date') else None,
                "priority": row.get('priority'),
                "tags": row.get('tags'),
                "created_at": row['created_at'].isoformat() if row.get('created_at') else None
            })

        logger.info(f"✅ Listed {len(tasks)} tasks for user {user_id}")
        return web.json_response(tasks)

    except Exception as e:
        logger.error(f"❌ Error in list_tasks: {e}")
        return web.json_response({"error": str(e)}, status=500)


# Add task endpoint
async def add_task_handler(request):
    """Handle add_task requests - inserts directly into database"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        title = data.get('title')

        if not user_id or not title:
            return web.json_response({"error": "user_id and title are required"}, status=400)

        # Build the insert query for the 'task' table
        # Note: using 'task' not 'tasks' - table is singular
        query = """
            INSERT INTO task (user_id, title, description, completed, created_at, updated_at, due_date, priority, tags)
            VALUES ($1, $2, $3, $4, NOW(), NOW(), $5, $6, $7)
            RETURNING id, user_id, title, description, completed, created_at, updated_at, due_date, priority, tags
        """

        # Parse due_date if provided
        due_date = None
        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
            except ValueError:
                pass  # Keep due_date as None if invalid format

        # Convert tags list to JSON string if provided
        tags_json = None
        if data.get('tags'):
            import json
            tags_json = json.dumps(data['tags'])

        row = await execute_query(
            query,
            int(user_id),
            title,
            data.get('description'),
            False,  # completed defaults to False
            due_date,
            data.get('priority'),
            tags_json
        )

        if row:
            task = row[0]
            logger.info(f"✅ Task created: {task['id']}")
            return web.json_response({
                "id": task['id'],
                "user_id": task['user_id'],
                "title": task['title'],
                "description": task.get('description'),
                "completed": task['completed'],
                "created_at": task['created_at'].isoformat() if task.get('created_at') else None,
                "updated_at": task['updated_at'].isoformat() if task.get('updated_at') else None,
                "due_date": task.get('due_date').isoformat() if task.get('due_date') else None,
                "priority": task.get('priority'),
                "tags": task.get('tags')
            })
        else:
            return web.json_response({"error": "Failed to create task"}, status=500)

    except Exception as e:
        logger.error(f"❌ Error in add_task: {e}")
        return web.json_response({"error": str(e)}, status=500)


# Complete task endpoint
async def complete_task_handler(request):
    """Handle complete_task requests - updates database directly"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        task_id = data.get('task_id')

        if not user_id or not task_id:
            return web.json_response({"error": "user_id and task_id are required"}, status=400)

        # Update task to completed
        query = """
            UPDATE task
            SET completed = true, updated_at = NOW()
            WHERE id = $1 AND user_id = $2
            RETURNING id, user_id, title, description, completed, created_at, updated_at, due_date, priority, tags
        """

        rows = await execute_query(query, int(task_id), int(user_id))

        if rows:
            task = rows[0]
            logger.info(f"✅ Task {task_id} completed")
            return web.json_response({
                "id": task['id'],
                "user_id": task['user_id'],
                "title": task['title'],
                "description": task.get('description'),
                "completed": task['completed'],
                "created_at": task['created_at'].isoformat() if task.get('created_at') else None,
                "updated_at": task['updated_at'].isoformat() if task.get('updated_at') else None,
                "due_date": task.get('due_date').isoformat() if task.get('due_date') else None,
                "priority": task.get('priority'),
                "tags": task.get('tags')
            })
        else:
            return web.json_response({"error": "Task not found"}, status=404)

    except Exception as e:
        logger.error(f"❌ Error in complete_task: {e}")
        return web.json_response({"error": str(e)}, status=500)


# Delete task endpoint
async def delete_task_handler(request):
    """Handle delete_task requests - deletes from database directly"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        task_id = data.get('task_id')

        if not user_id or not task_id:
            return web.json_response({"error": "user_id and task_id are required"}, status=400)

        # Delete task
        query = """
            DELETE FROM task
            WHERE id = $1 AND user_id = $2
            RETURNING id
        """

        rows = await execute_query(query, int(task_id), int(user_id))

        if rows:
            logger.info(f"✅ Task {task_id} deleted")
            return web.json_response({"success": True})
        else:
            return web.json_response({"error": "Task not found"}, status=404)

    except Exception as e:
        logger.error(f"❌ Error in delete_task: {e}")
        return web.json_response({"error": str(e)}, status=500)


# Update task endpoint
async def update_task_handler(request):
    """Handle update_task requests - updates database directly"""
    try:
        data = await request.json()
        user_id = data.get('user_id')
        task_id = data.get('task_id')

        if not user_id or not task_id:
            return web.json_response({"error": "user_id and task_id are required"}, status=400)

        # Build dynamic UPDATE query based on provided fields
        update_fields = []
        update_values = []
        param_count = 2  # Start at $2 because $1 is task_id and $2 will be user_id

        # We'll use a different approach - build a parameterized query
        # First, collect all the fields that need to be updated
        field_updates = []
        query_params = []

        if data.get('title'):
            field_updates.append("title = $" + str(len(query_params) + 1))
            query_params.append(data['title'])

        if data.get('description') is not None:
            field_updates.append("description = $" + str(len(query_params) + 1))
            query_params.append(data['description'])

        if data.get('completed') is not None:
            field_updates.append("completed = $" + str(len(query_params) + 1))
            query_params.append(data['completed'])

        if data.get('due_date'):
            try:
                due_date = datetime.fromisoformat(data['due_date'].replace('Z', '+00:00'))
                field_updates.append("due_date = $" + str(len(query_params) + 1))
                query_params.append(due_date)
            except ValueError:
                pass  # Skip invalid due_date

        if data.get('priority'):
            field_updates.append("priority = $" + str(len(query_params) + 1))
            query_params.append(data['priority'])

        if data.get('tags'):
            import json
            tags_json = json.dumps(data['tags'])
            field_updates.append("tags = $" + str(len(query_params) + 1))
            query_params.append(tags_json)

        if not field_updates:
            return web.json_response({"error": "No valid fields to update"}, status=400)

        # Add updated_at
        field_updates.append("updated_at = NOW()")

        # Build the query
        query = f"""
            UPDATE task
            SET {', '.join(field_updates)}
            WHERE id = ${len(query_params) + 1} AND user_id = ${len(query_params) + 2}
            RETURNING id, user_id, title, description, completed, created_at, updated_at, due_date, priority, tags
        """

        # Add task_id and user_id to params
        query_params.append(int(task_id))
        query_params.append(int(user_id))

        rows = await execute_query(query, *query_params)

        if rows:
            task = rows[0]
            logger.info(f"✅ Task {task_id} updated")
            return web.json_response({
                "id": task['id'],
                "user_id": task['user_id'],
                "title": task['title'],
                "description": task.get('description'),
                "completed": task['completed'],
                "created_at": task['created_at'].isoformat() if task.get('created_at') else None,
                "updated_at": task['updated_at'].isoformat() if task.get('updated_at') else None,
                "due_date": task.get('due_date').isoformat() if task.get('due_date') else None,
                "priority": task.get('priority'),
                "tags": task.get('tags')
            })
        else:
            return web.json_response({"error": "Task not found"}, status=404)

    except Exception as e:
        logger.error(f"❌ Error in update_task: {e}")
        return web.json_response({"error": str(e)}, status=500)


async def init_app():
    """Initialize the aiohttp application"""
    app = web.Application()

    # Add routes
    app.router.add_get('/health', health_handler)
    app.router.add_post('/list_tasks', list_tasks_handler)
    app.router.add_post('/add_task', add_task_handler)
    app.router.add_post('/complete_task', complete_task_handler)
    app.router.add_post('/delete_task', delete_task_handler)
    app.router.add_post('/update_task', update_task_handler)

    # Initialize database pool on startup
    app.on_startup.append(lambda app: init_db_pool())
    app.on_cleanup.append(lambda app: close_db_pool())

    return app


if __name__ == '__main__':
    port = int(os.getenv('PORT', 8002))
    logger.info(f"🚀 Starting MCP Server on port {port}")
    logger.info(f"🔗 Backend API: {BACKEND_API_URL}")
    logger.info(f"💾 Database: {DATABASE_URL[:30]}..." if DATABASE_URL else "❌ No DATABASE_URL set")

    web.run_app(init_app(), host='0.0.0.0', port=port)
