from datetime import datetime, timedelta
from typing import Optional, Dict, Any
import json
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.models import Task
from app import crud
from .event_publisher import publish_task_created_event


class RecurringTaskService:
    """Service for handling recurring task logic."""

    @staticmethod
    async def create_next_occurrence(db_session: AsyncSession, original_task: Task) -> Optional[Task]:
        """
        Create the next occurrence of a recurring task based on the recurring_config.

        Args:
            db_session: Database session
            original_task: The original recurring task

        Returns:
            The newly created task occurrence or None if not recurring
        """
        if not original_task.recurring_config:
            return None

        try:
            config = json.loads(original_task.recurring_config)
        except (json.JSONDecodeError, TypeError):
            return None

        # Determine the next due date based on the recurrence pattern
        next_due_date = RecurringTaskService.calculate_next_due_date(
            original_task.due_date, config
        )

        if not next_due_date:
            return None

        # Create the next occurrence
        next_task = await crud.create_task(
            db_session=db_session,
            user_id=original_task.user_id,
            title=original_task.title,
            description=original_task.description,
            completed=False,
            due_date=next_due_date,
            priority=original_task.priority,
            tags=original_task.tags,
            recurring_config=original_task.recurring_config
        )

        # Update the original task to link to the next occurrence
        original_task.next_occurrence_id = str(next_task.id)
        db_session.add(original_task)
        await db_session.commit()
        await db_session.refresh(original_task)

        # Publish event for the new task
        await publish_task_created_event(next_task)

        return next_task

    @staticmethod
    def calculate_next_due_date(current_due_date: Optional[datetime], config: Dict[str, Any]) -> Optional[datetime]:
        """
        Calculate the next due date based on the recurrence configuration.

        Args:
            current_due_date: The current due date
            config: Recurrence configuration dictionary

        Returns:
            The next due date or None if calculation fails
        """
        if not current_due_date:
            # If no current due date, use current time
            current_due_date = datetime.utcnow()

        recurrence_type = config.get('type')
        interval = config.get('interval', 1)

        if recurrence_type == 'daily':
            next_date = current_due_date + timedelta(days=interval)
        elif recurrence_type == 'weekly':
            next_date = current_due_date + timedelta(weeks=interval)
        elif recurrence_type == 'monthly':
            # Handle month increments carefully to avoid invalid dates
            next_date = RecurringTaskService.add_months(current_due_date, interval)
        else:
            # Invalid recurrence type
            return None

        return next_date

    @staticmethod
    def add_months(date: datetime, months: int) -> datetime:
        """
        Add months to a date, handling month-end edge cases properly.

        Args:
            date: The starting date
            months: Number of months to add

        Returns:
            The resulting date after adding months
        """
        month = date.month - 1 + months
        year = date.year + month // 12
        month = month % 12 + 1
        day = min(date.day, RecurringTaskService.days_in_month(year, month))
        return date.replace(year=year, month=month, day=day)

    @staticmethod
    def days_in_month(year: int, month: int) -> int:
        """
        Calculate the number of days in a given month/year.

        Args:
            year: The year
            month: The month (1-12)

        Returns:
            Number of days in the month
        """
        import calendar
        return calendar.monthrange(year, month)[1]

    @staticmethod
    async def validate_recurring_config(config: Dict[str, Any]) -> bool:
        """
        Validate a recurring task configuration.

        Args:
            config: Recurrence configuration dictionary

        Returns:
            True if valid, False otherwise
        """
        required_keys = {'type', 'interval'}
        if not required_keys.issubset(config.keys()):
            return False

        recurrence_type = config['type']
        interval = config['interval']

        # Validate type
        if recurrence_type not in ['daily', 'weekly', 'monthly']:
            return False

        # Validate interval
        if not isinstance(interval, int) or interval <= 0:
            return False

        # Validate end condition if present
        end_condition = config.get('end_condition')
        if end_condition:
            if not isinstance(end_condition, dict):
                return False

            end_type = end_condition.get('type')
            if end_type not in ['never', 'after_date', 'after_occurrences']:
                return False

            if end_type == 'after_date':
                try:
                    from datetime import datetime
                    datetime.fromisoformat(end_condition['value'].replace('Z', '+00:00'))
                except (TypeError, ValueError):
                    return False
            elif end_type == 'after_occurrences':
                try:
                    count = int(end_condition['value'])
                    if count <= 0:
                        return False
                except (TypeError, ValueError):
                    return False

        return True