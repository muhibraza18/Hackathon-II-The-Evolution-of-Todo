"""
Test script for Message model creation and relationships.
"""
import pytest
import asyncio
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from database import get_db_session
from models import Message
from crud import create_message, get_messages_by_conversation, get_message_by_id, create_conversation


@pytest.mark.asyncio
async def test_message_creation():
    """
    Test basic Message model creation.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # First create a conversation
        conversation = await create_conversation(session, "user123")
        conversation_id = conversation.id

        # Create a message
        message = await create_message(session, "user123", conversation_id, "user", "Hello, world!")

        # Verify the message was created with correct properties
        assert message.user_id == "user123"
        assert message.conversation_id == conversation_id
        assert message.role == "user"
        assert message.content == "Hello, world!"
        assert message.id is not None
        assert message.created_at is not None

        print("✓ Message creation test passed")


@pytest.mark.asyncio
async def test_message_relationships():
    """
    Test Message model relationships with Conversation.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Create a conversation
        conversation = await create_conversation(session, "user123")
        conversation_id = conversation.id

        # Create multiple messages in the conversation
        message1 = await create_message(session, "user123", conversation_id, "user", "First message")
        message2 = await create_message(session, "user123", conversation_id, "assistant", "Second message")
        message3 = await create_message(session, "user123", conversation_id, "user", "Third message")

        # Verify all messages were created
        assert message1.id is not None
        assert message2.id is not None
        assert message3.id is not None

        # Get all messages in the conversation
        messages = await get_messages_by_conversation(session, conversation_id, "user123")
        assert len(messages) == 3
        assert messages[0].content == "First message"
        assert messages[1].content == "Second message"
        assert messages[2].content == "Third message"

        # Verify message roles are correct
        assert messages[0].role == "user"
        assert messages[1].role == "assistant"
        assert messages[2].role == "user"

        print("✓ Message relationships test passed")


@pytest.mark.asyncio
async def test_message_validation():
    """
    Test Message model validation rules.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # First create a conversation
        conversation = await create_conversation(session, "user123")
        conversation_id = conversation.id

        # Test creating a message with valid role
        valid_message = await create_message(session, "user123", conversation_id, "user", "Valid message")
        assert valid_message.role in ["user", "assistant"]

        # Test creating a message with the other valid role
        valid_message2 = await create_message(session, "user123", conversation_id, "assistant", "Assistant message")
        assert valid_message2.role in ["user", "assistant"]

        print("✓ Message validation test passed")


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_message_creation())
    asyncio.run(test_message_relationships())
    asyncio.run(test_message_validation())
    print("\n✓ All Message model tests passed!")