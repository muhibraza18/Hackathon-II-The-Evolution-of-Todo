"""
Recurring Task Consumer Service
Subscribes to task events via Dapr pub/sub and handles recurring task logic.
"""
import logging
import os
from typing import Dict, Any
from fastapi import FastAPI, Request

from .base_consumer import BaseConsumer

logger = logging.getLogger(__name__)

app = FastAPI(title="Recurring Task Consumer Service")
consumer = BaseConsumer("recurring-task-consumer")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "recurring-task-consumer",
        "timestamp": consumer.log_event("health.check", {}, "health_check")
    }


@app.post("/recurring-task/subscription")
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
        topic = event_data.get("topic", "todo-events")

        # Process the event based on type
        if "task.created" in event_type:
            result = await handle_task_created(data)
        elif "task.completed" in event_type:
            result = await handle_task_completed(data)
        else:
            result = {"action": "ignored", "reason": "unhandled_event_type"}

        # Log the processing
        consumer.log_event(event_type, data, result.get("action", "processed"))

        return {"status": "success", **result}

    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {"status": "error", "message": str(e)}


async def handle_task_created(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle task created events."""
    task_id = data.get("task_id")
    recurrence_rule = data.get("recurrence_rule")

    if recurrence_rule:
        logger.info(f"Task {task_id} has recurrence rule: {recurrence_rule}")
        return {
            "action": "checked_recurrence",
            "task_id": task_id,
            "recurrence_rule": recurrence_rule,
            "message": "Task has recurrence - will create next instance on completion"
        }
    else:
        return {
            "action": "no_recurrence",
            "task_id": task_id,
            "message": "Task has no recurrence rule"
        }


async def handle_task_completed(data: Dict[str, Any]) -> Dict[str, Any]:
    """Handle task completed events."""
    task_id = data.get("task_id")
    recurrence_rule = data.get("recurrence_rule")

    if recurrence_rule:
        logger.info(f"Creating next instance for recurring task {task_id}")
        return {
            "action": "would_create_next_instance",
            "parent_task_id": task_id,
            "recurrence_rule": recurrence_rule,
            "message": "Next instance would be created (database operation not implemented)"
        }
    else:
        return {
            "action": "completed",
            "task_id": task_id,
            "message": "Task completed (no recurrence)"
        }


# Dapr subscription configuration
@app.get("/dapr/subscribe")
async def subscribe():
    """Return subscription information for Dapr."""
    return [
        {
            "pubsubname": "task-pubsub",
            "topic": "task-created",
            "route": "/recurring-task/subscription",
            "metadata": {"rawPayload": "false"}
        },
        {
            "pubsubname": "task-pubsub",
            "topic": "task-completed",
            "route": "/recurring-task/subscription",
            "metadata": {"rawPayload": "false"}
        }
    ]


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8001"))
    uvicorn.run(app, host="0.0.0.0", port=port)
