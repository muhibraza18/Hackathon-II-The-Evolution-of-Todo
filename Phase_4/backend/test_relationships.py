"""
Test script for foreign key relationships and cascade delete functionality.
"""
import pytest
import asyncio
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from database import get_db_session
from models import Conversation, Message
from crud import (
    create_conversation,
    create_message,
    get_messages_by_conversation,
    get_conversation_by_id,
    delete_conversation,
    get_message_by_id
)


@pytest.mark.asyncio
async def test_foreign_key_relationships():
    """
    Test that foreign key relationships are properly enforced.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Create a conversation
        conversation = await create_conversation(session, "user123")
        conversation_id = conversation.id
        assert conversation_id is not None

        # Create a message associated with the conversation
        message = await create_message(session, "user123", conversation_id, "user", "Test message")
        assert message.conversation_id == conversation_id

        # Verify the message is associated with the conversation
        messages = await get_messages_by_conversation(session, conversation_id, "user123")
        assert len(messages) == 1
        assert messages[0].id == message.id
        assert messages[0].content == "Test message"

        print("✓ Foreign key relationships test passed")


@pytest.mark.asyncio
async def test_cascade_delete():
    """
    Test that deleting a conversation also deletes all associated messages.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Create a conversation
        conversation = await create_conversation(session, "user123")
        conversation_id = conversation.id
        assert conversation_id is not None

        # Create multiple messages in the conversation
        message1 = await create_message(session, "user123", conversation_id, "user", "First message")
        message2 = await create_message(session, "user123", conversation_id, "assistant", "Second message")
        message3 = await create_message(session, "user123", conversation_id, "user", "Third message")

        # Verify all messages exist
        messages_before = await get_messages_by_conversation(session, conversation_id, "user123")
        assert len(messages_before) == 3

        # Delete the conversation (which should trigger cascade delete for messages)
        delete_result = await delete_conversation(session, conversation_id, "user123")
        assert delete_result is True

        # Verify the conversation is deleted
        deleted_conversation = await get_conversation_by_id(session, conversation_id, "user123")
        assert deleted_conversation is None

        # Verify all associated messages are also deleted
        messages_after = await get_messages_by_conversation(session, conversation_id, "user123")
        assert len(messages_after) == 0

        # Verify individual messages can't be retrieved
        retrieved_msg1 = await get_message_by_id(session, message1.id, "user123")
        assert retrieved_msg1 is None
        retrieved_msg2 = await get_message_by_id(session, message2.id, "user123")
        assert retrieved_msg2 is None
        retrieved_msg3 = await get_message_by_id(session, message3.id, "user123")
        assert retrieved_msg3 is None

        print("✓ Cascade delete test passed")


@pytest.mark.asyncio
async def test_user_isolation():
    """
    Test that users can only access their own data.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Create conversations for different users
        user1_conversation = await create_conversation(session, "user1")
        user2_conversation = await create_conversation(session, "user2")

        # Create messages in each user's conversation
        await create_message(session, "user1", user1_conversation.id, "user", "User1 message")
        await create_message(session, "user2", user2_conversation.id, "user", "User2 message")

        # Verify user1 can only access their own conversation
        user1_conversations = await get_conversations(session, "user1")
        user2_conversations = await get_conversations(session, "user2")
        assert len(user1_conversations) == 1
        assert len(user2_conversations) == 1
        assert user1_conversations[0].id == user1_conversation.id
        assert user2_conversations[0].id == user2_conversation.id

        # Verify user1 can only access their own messages
        user1_messages = await get_messages_by_conversation(session, user1_conversation.id, "user1")
        user2_messages = await get_messages_by_conversation(session, user2_conversation.id, "user2")
        assert len(user1_messages) == 1
        assert len(user2_messages) == 1
        assert user1_messages[0].content == "User1 message"
        assert user2_messages[0].content == "User2 message"

        print("✓ User isolation test passed")




if __name__ == "__main__":
    # Run tests
    asyncio.run(test_foreign_key_relationships())
    asyncio.run(test_cascade_delete())
    asyncio.run(test_user_isolation())
    print("\n✓ All relationship tests passed!")