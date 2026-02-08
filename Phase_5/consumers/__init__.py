"""
Consumers package for event-driven architecture with Dapr.
"""
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

__all__ = ['recurring_task_consumer', 'notification_consumer', 'audit_consumer']
