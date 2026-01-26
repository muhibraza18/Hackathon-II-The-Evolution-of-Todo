"""
Test script for Conversation model creation and basic operations.
"""
import pytest
import asyncio
from sqlmodel import SQLModel, create_engine
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from database import get_db_session
from models import Conversation
from crud import create_conversation, get_conversations, get_conversation_by_id, delete_conversation


@pytest.mark.asyncio
async def test_conversation_creation():
    """
    Test basic Conversation model creation.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Create a conversation
        conversation = await create_conversation(session, "user123")

        # Verify the conversation was created with correct properties
        assert conversation.user_id == "user123"
        assert conversation.id is not None
        assert conversation.created_at is not None

        print("✓ Conversation creation test passed")


@pytest.mark.asyncio
async def test_conversation_crud_operations():
    """
    Test CRUD operations for Conversation model.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Create a conversation
        conversation = await create_conversation(session, "user123")
        original_conv_id = conversation.id

        # Verify creation
        assert conversation.user_id == "user123"
        assert conversation.id is not None

        # Get the conversation by ID
        retrieved_conv = await get_conversation_by_id(session, original_conv_id, "user123")
        assert retrieved_conv is not None
        assert retrieved_conv.user_id == "user123"

        # Get all conversations for user
        conversations = await get_conversations(session, "user123")
        assert len(conversations) == 1
        assert conversations[0].id == original_conv_id

        # Delete the conversation
        delete_result = await delete_conversation(session, original_conv_id, "user123")
        assert delete_result is True

        # Verify deletion
        deleted_conv = await get_conversation_by_id(session, original_conv_id, "user123")
        assert deleted_conv is None

        print("✓ Conversation CRUD operations test passed")


if __name__ == "__main__":
    # Run tests
    asyncio.run(test_conversation_creation())
    asyncio.run(test_conversation_crud_operations())
    print("\n✓ All Conversation model tests passed!")