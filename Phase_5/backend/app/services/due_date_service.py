from datetime import datetime, timedelta, timezone
from typing import Optional
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.models import Task


class DueDateService:
    """Service for handling due date validation and logic."""

    @staticmethod
    def validate_due_date(due_date: Optional[datetime]) -> bool:
        """
        Validate that a due date is in the future if provided.

        Args:
            due_date: The due date to validate

        Returns:
            True if valid, False otherwise
        """
        if due_date is None:
            # None is valid (no due date set)
            return True

        # Check that due date is in the future
        # Handle both timezone-aware and naive datetimes
        now = datetime.now(timezone.utc)
        if due_date.tzinfo is None:
            # If due_date is naive, treat it as UTC
            due_date_utc = due_date.replace(tzinfo=timezone.utc)
        else:
            # Convert to UTC if timezone-aware
            due_date_utc = due_date.astimezone(timezone.utc)

        return due_date_utc > now

    @staticmethod
    def validate_due_date_range(start_date: Optional[datetime], end_date: Optional[datetime]) -> bool:
        """
        Validate that the due date range is valid (start is before end).

        Args:
            start_date: The start date
            end_date: The end date

        Returns:
            True if valid, False otherwise
        """
        if start_date is None or end_date is None:
            # If either date is None, the range check is valid
            return True

        return start_date <= end_date

    @staticmethod
    def is_overdue(due_date: Optional[datetime]) -> bool:
        """
        Check if a due date has passed.

        Args:
            due_date: The due date to check

        Returns:
            True if overdue, False otherwise
        """
        if due_date is None:
            # Tasks without due dates are not overdue
            return False

        # Handle both timezone-aware and naive datetimes
        now = datetime.now(timezone.utc)
        if due_date.tzinfo is None:
            due_date_utc = due_date.replace(tzinfo=timezone.utc)
        else:
            due_date_utc = due_date.astimezone(timezone.utc)

        return now > due_date_utc

    @staticmethod
    def is_due_soon(due_date: Optional[datetime], hours_ahead: int = 24) -> bool:
        """
        Check if a due date is coming up soon.

        Args:
            due_date: The due date to check
            hours_ahead: Number of hours ahead to consider "soon"

        Returns:
            True if due soon, False otherwise
        """
        if due_date is None:
            # Tasks without due dates are not due soon
            return False

        # Handle both timezone-aware and naive datetimes
        now = datetime.now(timezone.utc)
        if due_date.tzinfo is None:
            due_date_utc = due_date.replace(tzinfo=timezone.utc)
        else:
            due_date_utc = due_date.astimezone(timezone.utc)

        time_until_due = due_date_utc - now
        return timedelta(0) <= time_until_due <= timedelta(hours=hours_ahead)

    @staticmethod
    def format_due_date(due_date: Optional[datetime], include_time: bool = True) -> str:
        """
        Format a due date for display.

        Args:
            due_date: The due date to format
            include_time: Whether to include time in the format

        Returns:
            Formatted date string
        """
        if due_date is None:
            return ""

        if include_time:
            return due_date.strftime("%Y-%m-%d %H:%M")
        else:
            return due_date.strftime("%Y-%m-%d")

    @staticmethod
    async def get_tasks_due_soon(db_session: AsyncSession, user_id: str, hours_ahead: int = 24) -> list:
        """
        Get tasks that are due soon for a user.

        Args:
            db_session: Database session
            user_id: User ID to filter tasks
            hours_ahead: Number of hours ahead to consider "soon"

        Returns:
            List of tasks due soon
        """
        from app import crud

        all_tasks = await crud.get_tasks(db_session, user_id)
        due_soon_tasks = []

        for task in all_tasks:
            if DueDateService.is_due_soon(task.due_date, hours_ahead):
                due_soon_tasks.append(task)

        return due_soon_tasks

    @staticmethod
    async def get_overdue_tasks(db_session: AsyncSession, user_id: str) -> list:
        """
        Get overdue tasks for a user.

        Args:
            db_session: Database session
            user_id: User ID to filter tasks

        Returns:
            List of overdue tasks
        """
        from app import crud

        all_tasks = await crud.get_tasks(db_session, user_id)
        overdue_tasks = []

        for task in all_tasks:
            if DueDateService.is_overdue(task.due_date):
                overdue_tasks.append(task)

        return overdue_tasks