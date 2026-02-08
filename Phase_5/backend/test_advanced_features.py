"""
Test script to validate the advanced todo features implementation.
This script tests the core functionality added for the advanced todo features.
"""
import asyncio
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.orm import sessionmaker
from datetime import datetime, timedelta
import json

from app.database.models import Task, User
import crud
from app.services.priority_service import PriorityService
from app.services.tag_service import TagService
from app.services.due_date_service import DueDateService
from app.services.recurring_task_service import RecurringTaskService


def test_task_model_extensions():
    """Test that the Task model has been properly extended."""
    print("Testing Task model extensions...")

    # Check that new fields exist
    assert hasattr(Task, 'due_date'), "Task model should have due_date field"
    assert hasattr(Task, 'priority'), "Task model should have priority field"
    assert hasattr(Task, 'tags'), "Task model should have tags field"
    assert hasattr(Task, 'recurring_config'), "Task model should have recurring_config field"
    assert hasattr(Task, 'next_occurrence_id'), "Task model should have next_occurrence_id field"
    assert hasattr(Task, 'parent_task_id'), "Task model should have parent_task_id field"
    assert hasattr(Task, 'original_task_id'), "Task model should have original_task_id field"

    print("✓ Task model extensions validated")


def test_priority_service():
    """Test the priority service functionality."""
    print("Testing Priority Service...")

    # Test priority validation
    assert PriorityService.validate_priority("high"), "High priority should be valid"
    assert PriorityService.validate_priority("urgent"), "Urgent priority should be valid"
    assert PriorityService.validate_priority("low"), "Low priority should be valid"
    assert PriorityService.validate_priority("medium"), "Medium priority should be valid"
    assert not PriorityService.validate_priority("invalid"), "Invalid priority should not be valid"

    # Test priority sorting
    assert PriorityService.get_priority_sort_value("low") == 0, "Low should have sort value 0"
    assert PriorityService.get_priority_sort_value("medium") == 1, "Medium should have sort value 1"
    assert PriorityService.get_priority_sort_value("high") == 2, "High should have sort value 2"
    assert PriorityService.get_priority_sort_value("urgent") == 3, "Urgent should have sort value 3"

    print("✓ Priority Service validated")


def test_tag_service():
    """Test the tag service functionality."""
    print("Testing Tag Service...")

    # Test tag validation
    assert TagService.validate_tags(json.dumps(["work", "important"])), "Valid tags should pass validation"
    assert not TagService.validate_tags(json.dumps([""])), "Empty tags should fail validation"

    # Test tag parsing and serialization
    tags_list = ["work", "personal", "urgent"]
    serialized = TagService.serialize_tags(tags_list)
    parsed = TagService.parse_tags(serialized)
    assert parsed == tags_list, "Parse and serialize should be symmetric"

    print("✓ Tag Service validated")


def test_due_date_service():
    """Test the due date service functionality."""
    print("Testing Due Date Service...")

    # Test future date validation
    future_date = datetime.utcnow() + timedelta(days=1)
    past_date = datetime.utcnow() - timedelta(days=1)

    assert DueDateService.validate_due_date(future_date), "Future date should be valid"
    assert not DueDateService.validate_due_date(past_date), "Past date should not be valid"
    assert DueDateService.validate_due_date(None), "None should be valid"

    print("✓ Due Date Service validated")


def test_recurring_task_service():
    """Test the recurring task service functionality."""
    print("Testing Recurring Task Service...")

    # Test configuration validation
    valid_config = {
        "type": "daily",
        "interval": 1,
        "end_condition": {"type": "never"}
    }

    invalid_config = {
        "type": "invalid_type",
        "interval": 1
    }

    async def test_validation():
        result = await RecurringTaskService.validate_recurring_config(valid_config)
        assert result, "Valid config should pass validation"

        result = await RecurringTaskService.validate_recurring_config(invalid_config)
        assert not result, "Invalid config should fail validation"

    asyncio.run(test_validation())

    print("✓ Recurring Task Service validated")


if __name__ == "__main__":
    print("Starting validation of Advanced Todo Features implementation...\n")

    test_task_model_extensions()
    test_priority_service()
    test_tag_service()
    test_due_date_service()
    test_recurring_task_service()

    print("\n✅ All validation tests passed! Advanced Todo Features implementation is working correctly.")