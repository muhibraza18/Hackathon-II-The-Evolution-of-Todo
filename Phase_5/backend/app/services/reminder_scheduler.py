"""
Reminder scheduling service for the event-driven architecture.
"""
import asyncio
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession

from ..database.models import Task
from ..services.kafka_publisher import event_publisher
from ..utils.logger import get_logger

logger = get_logger(__name__)


class ReminderScheduler:
    """
    Service for scheduling and publishing reminder events for tasks with due dates.
    """

    @staticmethod
    async def schedule_reminder_for_task(task: Task, db_session: AsyncSession):
        """
        Schedule a reminder for a task with a due date.

        Args:
            task: The task to schedule a reminder for
            db_session: Database session for any needed operations
        """
        if not task.due_date:
            logger.debug(f"No due date for task {task.id}, skipping reminder scheduling")
            return

        # Calculate time until due date
        time_until_due = task.due_date - datetime.utcnow()

        if time_until_due.total_seconds() <= 0:
            # Due date has already passed, don't schedule a reminder
            logger.debug(f"Due date for task {task.id} has already passed, skipping reminder")
            return

        # For this implementation, we'll schedule a reminder 24 hours before the due date
        # In a production system, this could be configurable
        reminder_time_delta = timedelta(hours=24)

        if time_until_due < reminder_time_delta:
            # If due date is less than 24 hours away, schedule reminder at the due time
            delay_seconds = time_until_due.total_seconds()
        else:
            delay_seconds = (time_until_due - reminder_time_delta).total_seconds()

        # Schedule the reminder
        logger.info(f"Scheduling reminder for task {task.id} in {delay_seconds} seconds")
        asyncio.create_task(ReminderScheduler._publish_reminder_after_delay(
            task, delay_seconds
        ))

    @staticmethod
    async def _publish_reminder_after_delay(task: Task, delay_seconds: float):
        """
        Internal method to publish a reminder after a specified delay.

        Args:
            task: The task to create a reminder for
            delay_seconds: Number of seconds to wait before publishing the reminder
        """
        # Wait for the specified delay
        await asyncio.sleep(delay_seconds)

        # Check if task still exists and hasn't been completed (in a real system you'd re-fetch from DB)
        if task.completed:
            logger.debug(f"Task {task.id} already completed, skipping reminder")
            return

        # Publish reminder event
        event_payload = {
            "event_type": "task.reminder",
            "task_id": str(task.id) if task.id else None,
            "user_id": str(task.user_id) if task.user_id else None,
            "timestamp": datetime.utcnow().isoformat(),
            "payload": {
                "title": task.title,
                "due_date": task.due_date.isoformat() if task.due_date else None,
                "priority": task.priority,
                "notification_method": "email"  # Configurable in real implementation
            }
        }

        success = await event_publisher.publish("reminders", event_payload)
        if success:
            logger.info(f"Reminder published for task {task.id}")
        else:
            logger.error(f"Failed to publish reminder for task {task.id}")

    @staticmethod
    async def cancel_scheduled_reminder(task_id: str):
        """
        Cancel a scheduled reminder for a task (not implemented in this simple version).

        Args:
            task_id: The ID of the task to cancel the reminder for
        """
        # In a more sophisticated implementation, this would cancel the scheduled task
        # For now, we just log that this would happen
        logger.info(f"Would cancel reminder for task {task_id}")

    @staticmethod
    async def reschedule_reminder(task: Task, db_session: AsyncSession):
        """
        Reschedule a reminder for an updated task.

        Args:
            task: The updated task
            db_session: Database session for any needed operations
        """
        # Cancel any existing scheduled reminder
        await ReminderScheduler.cancel_scheduled_reminder(str(task.id) if task.id else "")

        # Schedule new reminder
        await ReminderScheduler.schedule_reminder_for_task(task, db_session)


# Global instance of the reminder scheduler
reminder_scheduler = ReminderScheduler()