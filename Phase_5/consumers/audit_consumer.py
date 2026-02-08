"""
Audit Consumer Service
Subscribes to all task events via Dapr pub/sub and logs them for audit purposes.
"""
import logging
import os
from typing import Dict, Any
from fastapi import FastAPI, Request

from .base_consumer import BaseConsumer

logger = logging.getLogger(__name__)

app = FastAPI(title="Audit Consumer Service")
consumer = BaseConsumer("audit-consumer")


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {
        "status": "healthy",
        "service": "audit-consumer",
        "timestamp": consumer.log_event("health.check", {}, "health_check")
    }


@app.post("/audit/subscription")
async def task_subscription(request: Request):
    """
    Dapr subscription endpoint for processing all task events for audit purposes.
    This endpoint is called by Dapr when any task-related event is published.
    """
    try:
        event_data = await request.json()
        logger.info(f"Received event for audit via Dapr: {event_data}")

        # Extract event data
        event_type = event_data.get("type", "")
        data = event_data.get("data", {})
        topic = event_data.get("topic", "todo-events")

        # Log all events for audit
        audit_log = {
            "action": "logged",
            "table": "audit_log",
            "event_type": event_type,
            "data": data,
            "timestamp": consumer.log_event(event_type, data, "audit_log")
        }

        logger.info(f"Audit log entry created: {audit_log}")

        return {"status": "success", **audit_log}

    except Exception as e:
        logger.error(f"Error processing audit event: {e}")
        return {"status": "error", "message": str(e)}


# Dapr subscription configuration
@app.get("/dapr/subscribe")
async def subscribe():
    """Return subscription information for Dapr."""
    return [
        {
            "pubsubname": "kafka-pubsub",
            "topic": "todo-events",
            "route": "/audit/subscription",
            "metadata": {"rawPayload": "false"}
        }
    ]


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", "8003"))
    uvicorn.run(app, host="0.0.0.0", port=port)
