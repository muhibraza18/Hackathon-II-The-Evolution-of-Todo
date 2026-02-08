"""
Notification Consumer Service
Subscribes to task events via Dapr pub/sub and handles reminder notifications.
"""
import logging
import os
import asyncio
import aiohttp
from datetime import datetime, timezone
from typing import Dict, Any
from fastapi import FastAPI, Request
import asyncpg

from .base_consumer import BaseConsumer

logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Consumer Service")
consumer = BaseConsumer("notification-consumer")

# Database connection pool
db_pool = None

# Track reminded tasks to avoid duplicate notifications
reminded_tasks = set()

# Background scheduler task
scheduler_task = None

# Dapr sidecar URL
DAPR_HTTP_URL = "http://localhost:3500"


async def get_db_connection():
    """Get database connection from environment variable."""
    global db_pool
    if db_pool is None:
        db_url = os.getenv("DATABASE_URL")
        if not db_url:
            logger.error("DATABASE_URL environment variable not set")
            return None
        db_pool = await asyncpg.create_pool(db_url, min_size=1, max_size=5)
    return db_pool


async def publish_reminder_event(task_data: Dict[str, Any]):
    """Publish reminder event via Dapr pub/sub using HTTP."""
    try:
        event = {
            "data": task_data,
            "datacontenttype": "application/json",
            "pubsubname": "task-pubsub",
            "topic": "due_date.reminder",
            "type": "com.dapr.event.sent"
        }

        async with aiohttp.ClientSession() as session:
            url = f"{DAPR_HTTP_URL}/v1.0/publish/task-pubsub/due_date.reminder"
            async with session.post(url, json=event, timeout=aiohttp.ClientTimeout(total=10)) as response:
                if response.status in (200, 204):  # 200 or 204 are both success
                    logger.info(f"✅ Published due_date.reminder event for task {task_data.get('task_id')}")
                else:
                    text = await response.text()
                    logger.error(f"Failed to publish reminder event: {response.status} - {text}")
    except Exception as e:
        logger.error(f"Exception publishing reminder event: {e}")


async def check_due_tasks():
    """Background task to check for due tasks and trigger reminders."""
    global reminded_tasks
    iteration = 0

    while True:
        iteration += 1
        try:
            logger.info(f"🔄 Scheduler iteration #{iteration} started at {datetime.utcnow().isoformat()}")
            pool = await get_db_connection()
            if not pool:
                logger.error("Cannot check due tasks - no database connection")
                await asyncio.sleep(60)
                continue

            async with pool.acquire() as conn:
                # Get current time in UTC as naive datetime (database stores naive datetimes)
                now_utc = datetime.utcnow()

                # Query for tasks with due dates that have passed but haven't been reminded
                query = """
                    SELECT id, title, user_id, due_date, description
                    FROM task
                    WHERE due_date IS NOT NULL
                    AND due_date <= $1
                    AND completed = false
                    ORDER BY due_date ASC
                """

                rows = await conn.fetch(query, now_utc)
                logger.info(f"📊 Found {len(rows)} due tasks (current UTC: {now_utc.isoformat()})")
                for row in rows:
                    logger.info(f"  - Due task: {row['title']} (due: {row['due_date']}, task_id: {row['id']})")

                for row in rows:
                    task_id = str(row['id'])

                    # Check if we already reminded this task
                    if task_id in reminded_tasks:
                        continue

                    # Trigger reminder notification
                    logger.info(f"🔔🔔🔔 REMINDER TRIGGERED 🔔🔔🔔")
                    logger.info(f"📋 Task: {row['title']}")
                    logger.info(f"⏰ Due Date: {row['due_date']}")
                    logger.info(f"👤 User ID: {row['user_id']}")
                    logger.info(f"📝 Description: {row['description'] or 'No description'}")
                    logger.info(f"🆔 Task ID: {task_id}")
                    logger.info(f"⏰ Current Time: {now_utc.isoformat()}")
                    print("")  # Empty line for visibility
                    print(f"*** REMINDER: Task '{row['title']}' is DUE! ***")
                    print(f"*** Due Date was: {row['due_date']} ***")
                    print("")

                    # Mark as reminded
                    reminded_tasks.add(task_id)

                    # Publish reminder event via Dapr
                    reminder_event = {
                        "task_id": task_id,
                        "title": row['title'],
                        "user_id": str(row['user_id']),
                        "due_date": row['due_date'].isoformat() if row['due_date'] else None,
                        "description": row['description'],
                        "timestamp": now_utc.isoformat()
                    }
                    await publish_reminder_event(reminder_event)

            # Sleep for 30 seconds before next check
            logger.info(f"😴 Scheduler iteration #{iteration} completed, sleeping for 30 seconds...")
            await asyncio.sleep(30)
            logger.info(f"⏰ Scheduler iteration #{iteration} woke up from sleep")

        except Exception as e:
            logger.error(f"❌ Error in check_due_tasks iteration #{iteration}: {e}")
            import traceback
            logger.error(f"Traceback: {traceback.format_exc()}")
            await asyncio.sleep(60)


@app.on_event("startup")
async def startup_event():
    """Start background scheduler on startup."""
    global scheduler_task
    logger.info("🚀 Starting reminder scheduler...")
    scheduler_task = asyncio.create_task(check_due_tasks())
    logger.info("✅ Reminder scheduler started - will check for due tasks every 30 seconds")


@app.on_event("shutdown")
async def shutdown_event():
    """Clean up on shutdown."""
    global scheduler_task, db_pool
    if scheduler_task:
        scheduler_task.cancel()
        logger.info("⏹️  Reminder scheduler stopped")
    if db_pool:
        await db_pool.close()
        logger.info("🔒 Database connection pool closed")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "notification-consumer",
        "scheduler_running": scheduler_task is not None and not scheduler_task.done(),
        "reminded_tasks_count": len(reminded_tasks),
        "timestamp": consumer.log_event("health.check", {}, "health_check")
    }


@app.post("/notification/subscription")
async def task_subscription(request: Request):
    """
    Dapr subscription endpoint for processing task events.
    This endpoint is called by Dapr when task-related events are published.
    """
    try:
        event_data = await request.json()
        logger.info(f"Received event via Dapr: {event_data}")

        # Extract event data
        event_type = event_data.get("type", "")
        data = event_data.get("data", {})

        # Process the event based on type
        if "task.created" in event_type:
            result = await handle_task_created(data)
        elif "due_date.reminder" in event_type:
            result = await handle_due_date_reminder(data)
        else:
            result = {"action": "ignored"}

        # Log the processing
        consumer.log_event(event_type, data, result.get("action", "processed"))

        return {"status": "success", **result}

    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {"status": "error", "message": str(e)}


async def handle_task_created(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle task created events - schedule reminders if due date exists."""
    task_id = data.get("task_id")
    due_date = data.get("due_date")

    if due_date:
        logger.info(f"Task {task_id} has due date: {due_date}")
        return {
            "action": "scheduled_reminder",
            "task_id": task_id,
            "due_date": due_date,
            "message": "Reminder scheduled via Dapr Jobs API (not implemented)"
        }
    else:
        return {
            "action": "no_reminder",
            "task_id": task_id,
            "message": "Task has no due date"
        }


async def handle_due_date_reminder(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle due date reminder events from Dapr Jobs API."""
    task_id = data.get("task_id")
    logger.info(f"🔔 REMINDER FIRED for task {task_id}")
    return {
        "action": "sent_notification",
        "task_id": task_id,
        "message": "Reminder notification sent"
    }


# Dapr subscription configuration
@app.get("/dapr/subscribe")
async def subscribe():
    """Return subscription information for Dapr."""
    return [
        {
            "pubsubname": "task-pubsub",
            "topic": "task.created",
            "route": "/notification/subscription",
            "metadata": {"rawPayload": "false"}
        },
        {
            "pubsubname": "task-pubsub",
            "topic": "due_date.reminder",
            "route": "/notification/subscription",
            "metadata": {"rawPayload": "false"}
        }
    ]


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8002"))
    uvicorn.run(app, host="0.0.0.0", port=port)
