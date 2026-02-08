"""
Test script for Task model creation and basic operations.
"""
import pytest
import asyncio
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from database import get_db_session
from models import Task
from crud import create_task, get_tasks, get_task_by_id, update_task, delete_task


@pytest.mark.asyncio
async def test_task_creation():
    """
    Test basic Task model creation.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Create a task
        task = await create_task(session, "user123", "Test Task", "This is a test task")

        # Verify the task was created with correct properties
        assert task.title == "Test Task"
        assert task.description == "This is a test task"
        assert task.user_id == "user123"
        assert task.completed is False
        assert task.id is not None

        print("✓ Task creation test passed")


@pytest.mark.asyncio
async def test_task_crud_operations():
    """
    Test all CRUD operations for Task model.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Create a task
        task = await create_task(session, "user123", "Initial Task", "Initial description")
        original_task_id = task.id

        # Verify creation
        assert task.title == "Initial Task"
        assert task.description == "Initial description"

        # Get the task by ID
        retrieved_task = await get_task_by_id(session, original_task_id, "user123")
        assert retrieved_task is not None
        assert retrieved_task.title == "Initial Task"

        # Get all tasks for user
        tasks = await get_tasks(session, "user123")
        assert len(tasks) == 1
        assert tasks[0].id == original_task_id

        # Update the task
        updated_task = await update_task(session, original_task_id, "user123",
                                       title="Updated Task", completed=True)
        assert updated_task is not None
        assert updated_task.title == "Updated Task"
        assert updated_task.completed is True

        # Delete the task
        delete_result = await delete_task(session, original_task_id, "user123")
        assert delete_result is True

        # Verify deletion
        deleted_task = await get_task_by_id(session, original_task_id, "user123")
        assert deleted_task is None

        print("✓ Task CRUD operations test passed")


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_task_creation())
    asyncio.run(test_task_crud_operations())
    print("\n✓ All Task model tests passed!")