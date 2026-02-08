import json
from typing import List, Optional, Dict, Any
from sqlmodel.ext.asyncio.session import AsyncSession
from app.database.models import Task


class TagService:
    """Service for handling task tags logic."""

    MAX_TAGS_PER_TASK = 10
    MAX_TAG_LENGTH = 50

    @staticmethod
    def validate_tags(tags: Optional[str]) -> bool:
        """
        Validate that a tags JSON string is properly formatted.

        Args:
            tags: JSON string representing a list of tags

        Returns:
            True if valid, False otherwise
        """
        if tags is None:
            return True

        try:
            parsed_tags = json.loads(tags)
        except (json.JSONDecodeError, TypeError):
            return False

        if not isinstance(parsed_tags, list):
            return False

        if len(parsed_tags) > TagService.MAX_TAGS_PER_TASK:
            return False

        for tag in parsed_tags:
            if not isinstance(tag, str):
                return False
            if len(tag) > TagService.MAX_TAG_LENGTH:
                return False
            if not TagService.is_valid_tag_format(tag):
                return False

        return True

    @staticmethod
    def is_valid_tag_format(tag: str) -> bool:
        """
        Validate that a tag string has valid format (no special characters that could be harmful).

        Args:
            tag: The tag string to validate

        Returns:
            True if valid format, False otherwise
        """
        # Basic validation: only alphanumeric, spaces, hyphens, underscores
        import re
        pattern = r'^[a-zA-Z0-9\s\-_]+$'
        return bool(re.match(pattern, tag.strip()))

    @staticmethod
    def parse_tags(tags: Optional[str]) -> List[str]:
        """
        Parse a JSON string into a list of tags.

        Args:
            tags: JSON string representing a list of tags

        Returns:
            List of tags, or empty list if invalid
        """
        if tags is None:
            return []

        try:
            parsed_tags = json.loads(tags)
            if isinstance(parsed_tags, list):
                return [tag.strip() for tag in parsed_tags if isinstance(tag, str)]
        except (json.JSONDecodeError, TypeError):
            pass

        return []

    @staticmethod
    def serialize_tags(tags: List[str]) -> str:
        """
        Serialize a list of tags into a JSON string.

        Args:
            tags: List of tag strings

        Returns:
            JSON string representation of the tags
        """
        # Clean and validate tags before serializing
        clean_tags = []
        for tag in tags:
            if isinstance(tag, str) and TagService.is_valid_tag_format(tag):
                clean_tag = tag.strip()
                if clean_tag and len(clean_tag) <= TagService.MAX_TAG_LENGTH:
                    clean_tags.append(clean_tag)

        # Limit to max number of tags
        clean_tags = clean_tags[:TagService.MAX_TAGS_PER_TASK]

        return json.dumps(clean_tags)

    @staticmethod
    async def filter_tasks_by_tag(tasks: List[Task], tag: str) -> List[Task]:
        """
        Filter a list of tasks by a specific tag.

        Args:
            tasks: List of tasks to filter
            tag: Tag to filter by

        Returns:
            List of tasks containing the specified tag
        """
        filtered_tasks = []
        for task in tasks:
            task_tags = TagService.parse_tags(task.tags)
            if tag.lower() in [t.lower() for t in task_tags]:
                filtered_tasks.append(task)
        return filtered_tasks

    @staticmethod
    async def filter_tasks_by_tags(tasks: List[Task], tags: List[str]) -> List[Task]:
        """
        Filter a list of tasks by multiple tags (tasks must have at least one of the tags).

        Args:
            tasks: List of tasks to filter
            tags: List of tags to filter by

        Returns:
            List of tasks containing at least one of the specified tags
        """
        filtered_tasks = []
        tag_set = {tag.lower() for tag in tags}

        for task in tasks:
            task_tags = TagService.parse_tags(task.tags)
            task_tag_set = {t.lower() for t in task_tags}

            if tag_set.intersection(task_tag_set):
                filtered_tasks.append(task)

        return filtered_tasks

    @staticmethod
    async def get_all_unique_tags(tasks: List[Task]) -> List[str]:
        """
        Get all unique tags from a list of tasks.

        Args:
            tasks: List of tasks to extract tags from

        Returns:
            List of unique tags
        """
        all_tags = set()
        for task in tasks:
            task_tags = TagService.parse_tags(task.tags)
            for tag in task_tags:
                all_tags.add(tag.lower())
        return sorted(list(all_tags))

    @staticmethod
    async def add_tag_to_task(task: Task, tag: str) -> Task:
        """
        Add a tag to a task.

        Args:
            task: The task to add the tag to
            tag: The tag to add

        Returns:
            Updated task with the new tag
        """
        if not TagService.is_valid_tag_format(tag):
            raise ValueError(f"Invalid tag format: {tag}")

        current_tags = TagService.parse_tags(task.tags)
        tag_lower = tag.lower()

        # Check if tag already exists (case-insensitive)
        if tag_lower not in [t.lower() for t in current_tags]:
            if len(current_tags) >= TagService.MAX_TAGS_PER_TASK:
                raise ValueError(f"Maximum number of tags ({TagService.MAX_TAGS_PER_TASK}) reached")

            current_tags.append(tag)
            task.tags = TagService.serialize_tags(current_tags)

        return task

    @staticmethod
    async def remove_tag_from_task(task: Task, tag: str) -> Task:
        """
        Remove a tag from a task.

        Args:
            task: The task to remove the tag from
            tag: The tag to remove

        Returns:
            Updated task without the specified tag
        """
        current_tags = TagService.parse_tags(task.tags)
        tag_lower = tag.lower()

        # Remove tag (case-insensitive)
        updated_tags = [t for t in current_tags if t.lower() != tag_lower]
        task.tags = TagService.serialize_tags(updated_tags)

        return task

    @staticmethod
    async def get_tasks_by_tag_counts(tasks: List[Task]) -> Dict[str, int]:
        """
        Get a count of how many times each tag appears in a list of tasks.

        Args:
            tasks: List of tasks to analyze

        Returns:
            Dictionary mapping tags to their counts
        """
        tag_counts = {}
        for task in tasks:
            task_tags = TagService.parse_tags(task.tags)
            for tag in task_tags:
                tag_lower = tag.lower()
                tag_counts[tag_lower] = tag_counts.get(tag_lower, 0) + 1

        return tag_counts

    @staticmethod
    def normalize_tag(tag: str) -> str:
        """
        Normalize a tag string (trim whitespace, convert to lowercase).

        Args:
            tag: The tag to normalize

        Returns:
            Normalized tag string
        """
        return tag.strip().lower()