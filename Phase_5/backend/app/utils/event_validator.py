"""
Event validation utilities for the event-driven architecture.
"""
from typing import Dict, Any, Optional
from datetime import datetime
from .logger import get_logger

logger = get_logger(__name__)


class EventValidator:
    """
    Utility class for validating event payloads and structures.
    """

    @staticmethod
    def validate_base_event(event_data: Dict[str, Any]) -> bool:
        """
        Validate the base structure of an event.

        Args:
            event_data: The event data to validate

        Returns:
            True if valid, False otherwise
        """
        required_fields = ['event_type', 'timestamp']

        for field in required_fields:
            if field not in event_data:
                logger.error(f"Missing required field '{field}' in event: {event_data}")
                return False

        # Validate timestamp format
        if not EventValidator._validate_timestamp(event_data['timestamp']):
            logger.error(f"Invalid timestamp format in event: {event_data}")
            return False

        # Validate event_type is a string
        if not isinstance(event_data['event_type'], str):
            logger.error(f"Event type must be a string in event: {event_data}")
            return False

        # Validate payload is a dictionary if present
        if 'payload' in event_data and not isinstance(event_data['payload'], dict):
            logger.error(f"Payload must be a dictionary in event: {event_data}")
            return False

        return True

    @staticmethod
    def validate_task_created_event(event_data: Dict[str, Any]) -> bool:
        """
        Validate a task created event.

        Args:
            event_data: The task created event data to validate

        Returns:
            True if valid, False otherwise
        """
        if not EventValidator.validate_base_event(event_data):
            return False

        if event_data['event_type'] != 'task.created':
            logger.error(f"Invalid event type for task created event: {event_data['event_type']}")
            return False

        # Validate required payload fields
        payload = event_data.get('payload', {})
        required_payload_fields = ['title']

        for field in required_payload_fields:
            if field not in payload:
                logger.error(f"Missing required payload field '{field}' in task created event: {event_data}")
                return False

        return True

    @staticmethod
    def validate_task_updated_event(event_data: Dict[str, Any]) -> bool:
        """
        Validate a task updated event.

        Args:
            event_data: The task updated event data to validate

        Returns:
            True if valid, False otherwise
        """
        if not EventValidator.validate_base_event(event_data):
            return False

        if event_data['event_type'] != 'task.updated':
            logger.error(f"Invalid event type for task updated event: {event_data['event_type']}")
            return False

        # For update events, we just need to ensure the payload is a dictionary
        payload = event_data.get('payload', {})
        if not isinstance(payload, dict):
            logger.error(f"Payload must be a dictionary in task updated event: {event_data}")
            return False

        return True

    @staticmethod
    def validate_task_completed_event(event_data: Dict[str, Any]) -> bool:
        """
        Validate a task completed event.

        Args:
            event_data: The task completed event data to validate

        Returns:
            True if valid, False otherwise
        """
        if not EventValidator.validate_base_event(event_data):
            return False

        if event_data['event_type'] != 'task.completed':
            logger.error(f"Invalid event type for task completed event: {event_data['event_type']}")
            return False

        # Validate required payload fields
        payload = event_data.get('payload', {})
        required_payload_fields = ['title']

        for field in required_payload_fields:
            if field not in payload:
                logger.error(f"Missing required payload field '{field}' in task completed event: {event_data}")
                return False

        return True

    @staticmethod
    def validate_reminder_event(event_data: Dict[str, Any]) -> bool:
        """
        Validate a reminder event.

        Args:
            event_data: The reminder event data to validate

        Returns:
            True if valid, False otherwise
        """
        if not EventValidator.validate_base_event(event_data):
            return False

        if event_data['event_type'] != 'task.reminder':
            logger.error(f"Invalid event type for reminder event: {event_data['event_type']}")
            return False

        # Validate required payload fields
        payload = event_data.get('payload', {})
        required_payload_fields = ['title', 'due_date', 'priority']

        for field in required_payload_fields:
            if field not in payload:
                logger.error(f"Missing required payload field '{field}' in reminder event: {event_data}")
                return False

        return True

    @staticmethod
    def _validate_timestamp(timestamp_value: Any) -> bool:
        """
        Validate that a timestamp value is in the correct format.

        Args:
            timestamp_value: The timestamp value to validate

        Returns:
            True if valid, False otherwise
        """
        if isinstance(timestamp_value, str):
            try:
                # Try to parse the string as ISO format
                datetime.fromisoformat(timestamp_value.replace('Z', '+00:00'))
                return True
            except ValueError:
                return False
        elif isinstance(timestamp_value, datetime):
            return True
        else:
            return False

    @staticmethod
    def validate_event_by_type(event_data: Dict[str, Any]) -> bool:
        """
        Validate an event based on its type.

        Args:
            event_data: The event data to validate

        Returns:
            True if valid, False otherwise
        """
        event_type = event_data.get('event_type')

        if event_type == 'task.created':
            return EventValidator.validate_task_created_event(event_data)
        elif event_type == 'task.updated':
            return EventValidator.validate_task_updated_event(event_data)
        elif event_type == 'task.completed':
            return EventValidator.validate_task_completed_event(event_data)
        elif event_type == 'task.reminder':
            return EventValidator.validate_reminder_event(event_data)
        else:
            # For other event types, just validate the base structure
            return EventValidator.validate_base_event(event_data)