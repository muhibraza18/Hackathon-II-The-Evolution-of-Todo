from typing import List, Optional
from enum import Enum
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.models import Task


class PriorityLevel(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class PriorityService:
    """Service for handling task priority logic."""

    VALID_PRIORITIES = ["low", "medium", "high", "urgent"]
    PRIORITY_SORT_ORDER = {
        "low": 0,
        "medium": 1,
        "high": 2,
        "urgent": 3
    }

    @staticmethod
    def validate_priority(priority: Optional[str]) -> bool:
        """
        Validate that a priority is one of the allowed values.

        Args:
            priority: The priority to validate

        Returns:
            True if valid, False otherwise
        """
        if priority is None:
            return True

        return priority.lower() in PriorityService.VALID_PRIORITIES

    @staticmethod
    def get_priority_sort_value(priority: Optional[str]) -> int:
        """
        Get the sort value for a priority level.

        Args:
            priority: The priority level

        Returns:
            Integer value for sorting (lower = lower priority)
        """
        if priority is None:
            return -1  # Default to lowest priority

        priority_lower = priority.lower()
        return PriorityService.PRIORITY_SORT_ORDER.get(priority_lower, -1)

    @staticmethod
    def is_high_priority(priority: Optional[str]) -> bool:
        """
        Check if a priority is considered high priority (high or urgent).

        Args:
            priority: The priority to check

        Returns:
            True if high priority, False otherwise
        """
        if priority is None:
            return False

        priority_lower = priority.lower()
        return priority_lower in ["high", "urgent"]

    @staticmethod
    def is_urgent(priority: Optional[str]) -> bool:
        """
        Check if a priority is urgent.

        Args:
            priority: The priority to check

        Returns:
            True if urgent, False otherwise
        """
        if priority is None:
            return False

        return priority.lower() == "urgent"

    @staticmethod
    async def filter_tasks_by_priority(tasks: List[Task], priority: str) -> List[Task]:
        """
        Filter a list of tasks by priority.

        Args:
            tasks: List of tasks to filter
            priority: Priority level to filter by

        Returns:
            List of tasks with the specified priority
        """
        if not PriorityService.validate_priority(priority):
            raise ValueError(f"Invalid priority: {priority}")

        return [task for task in tasks if task.priority and task.priority.lower() == priority.lower()]

    @staticmethod
    async def sort_tasks_by_priority(tasks: List[Task], ascending: bool = False) -> List[Task]:
        """
        Sort a list of tasks by priority.

        Args:
            tasks: List of tasks to sort
            ascending: Sort in ascending order (low to high) if True, descending (high to low) if False

        Returns:
            Sorted list of tasks
        """
        def sort_key(task):
            return PriorityService.get_priority_sort_value(task.priority)

        return sorted(tasks, key=sort_key, reverse=not ascending)

    @staticmethod
    async def get_priority_counts(tasks: List[Task]) -> dict:
        """
        Count tasks by priority level.

        Args:
            tasks: List of tasks to count

        Returns:
            Dictionary with counts for each priority level
        """
        counts = {priority: 0 for priority in PriorityService.VALID_PRIORITIES}

        for task in tasks:
            if task.priority and PriorityService.validate_priority(task.priority):
                priority_lower = task.priority.lower()
                counts[priority_lower] += 1

        return counts

    @staticmethod
    async def get_high_priority_tasks(tasks: List[Task]) -> List[Task]:
        """
        Get all high priority tasks (high or urgent).

        Args:
            tasks: List of tasks to filter

        Returns:
            List of high priority tasks
        """
        high_priority_tasks = []
        for task in tasks:
            if PriorityService.is_high_priority(task.priority):
                high_priority_tasks.append(task)
        return high_priority_tasks

    @staticmethod
    def get_priority_color(priority: Optional[str]) -> str:
        """
        Get a color representation for a priority level.

        Args:
            priority: The priority level

        Returns:
            Color string (e.g., hex code)
        """
        if priority is None:
            return "#CCCCCC"  # Gray for no priority

        priority_lower = priority.lower()
        color_map = {
            "low": "#4CAF50",     # Green
            "medium": "#FFC107",  # Amber
            "high": "#F44336",    # Red
            "urgent": "#D32F2F"   # Darker red
        }

        return color_map.get(priority_lower, "#CCCCCC")

    @staticmethod
    def get_priority_emoji(priority: Optional[str]) -> str:
        """
        Get an emoji representation for a priority level.

        Args:
            priority: The priority level

        Returns:
            Emoji string
        """
        if priority is None:
            return "➖"  # Neutral

        priority_lower = priority.lower()
        emoji_map = {
            "low": "🟢",     # Low
            "medium": "🟡",  # Medium
            "high": "🔴",    # High
            "urgent": "🚨"   # Urgent
        }

        return emoji_map.get(priority_lower, "➖")