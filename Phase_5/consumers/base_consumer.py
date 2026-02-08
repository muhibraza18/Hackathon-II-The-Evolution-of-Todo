"""
Base consumer module using Dapr for pub/sub.
"""
import logging
import os
from typing import Dict, Any
from datetime import datetime

logger = logging.getLogger(__name__)

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_GRPC_PORT = os.getenv("DAPR_GRPC_PORT", "50001")
DAPR_HOST = os.getenv("DAPR_HOST", "localhost")


class BaseConsumer:
    """Base class for Dapr-based consumers."""

    def __init__(self, app_id: str):
        self.app_id = app_id
        self.dapr_url = f"http://{DAPR_HOST}:{DAPR_HTTP_PORT}/v1.0"

    async def log_event(self, event_type: str, event_data: Dict[str, Any], action: str):
        """Log an event with structured logging."""
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "app_id": self.app_id,
            "event_type": event_type,
            "action": action,
            "data": event_data
        }
        logger.info(f"Event logged: {log_entry}")
        return log_entry


def get_consumer_name() -> str:
    """Get the consumer name from environment or default."""
    return os.getenv("CONSUMER_NAME", "consumer")
