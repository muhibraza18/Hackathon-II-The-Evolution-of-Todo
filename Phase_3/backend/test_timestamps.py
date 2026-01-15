"""
Test script for timestamp auto-population functionality.
"""
import pytest
import asyncio
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from datetime import datetime
from models import Task, Conversation, Message
from crud import create_task, create_conversation, create_message


@pytest.mark.asyncio
async def test_task_timestamps():
    """
    Test that Task model timestamps are auto-populated.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Record time before creating task
        before_time = datetime.utcnow()

        # Create a task
        task = await create_task(session, "user123", "Test Task", "Test description")

        # Record time after creating task
        after_time = datetime.utcnow()

        # Verify timestamps were auto-populated
        assert task.created_at is not None
        assert task.updated_at is not None

        # Verify timestamps are within reasonable range
        assert before_time <= task.created_at <= after_time
        assert before_time <= task.updated_at <= after_time

        print("✓ Task timestamp auto-population test passed")


@pytest.mark.asyncio
async def test_conversation_timestamps():
    """
    Test that Conversation model timestamps are auto-populated.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Record time before creating conversation
        before_time = datetime.utcnow()

        # Create a conversation
        conversation = await create_conversation(session, "user123")

        # Record time after creating conversation
        after_time = datetime.utcnow()

        # Verify timestamps were auto-populated
        assert conversation.created_at is not None
        assert conversation.updated_at is not None

        # Verify timestamps are within reasonable range
        assert before_time <= conversation.created_at <= after_time
        assert before_time <= conversation.updated_at <= after_time

        print("✓ Conversation timestamp auto-population test passed")


@pytest.mark.asyncio
async def test_message_timestamps():
    """
    Test that Message model timestamps are auto-populated.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Create a conversation first
        conversation = await create_conversation(session, "user123")

        # Record time before creating message
        before_time = datetime.utcnow()

        # Create a message
        message = await create_message(session, "user123", conversation.id, "user", "Test message")

        # Record time after creating message
        after_time = datetime.utcnow()

        # Verify timestamp was auto-populated
        assert message.created_at is not None

        # Verify timestamp is within reasonable range
        assert before_time <= message.created_at <= after_time

        print("✓ Message timestamp auto-population test passed")


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_task_timestamps())
    asyncio.run(test_conversation_timestamps())
    asyncio.run(test_message_timestamps())
    print("\n✓ All timestamp tests passed!")