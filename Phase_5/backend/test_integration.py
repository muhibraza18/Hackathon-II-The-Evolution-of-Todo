"""
Integration test for the Todo AI Chatbot database schema.
Tests all components working together.
"""
import pytest
import asyncio
from sqlmodel import SQLModel
from sqlmodel.ext.asyncio.session import AsyncSession
from sqlalchemy.ext.asyncio import create_async_engine
from datetime import datetime
from models import Task, Conversation, Message
from crud import (
    create_task, get_tasks, update_task, delete_task,
    create_conversation, get_conversations, delete_conversation,
    create_message, get_messages_by_conversation
)


@pytest.mark.asyncio
async def test_full_integration():
    """
    Test all components working together in a realistic scenario.
    """
    # Create an in-memory SQLite database for testing
    engine = create_async_engine("sqlite+aiosqlite:///:memory:")

    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    async with AsyncSession(engine) as session:
        # Test user ID
        user_id = "integration_test_user"

        # 1. Create a task
        task = await create_task(session, user_id, "Integration Test Task", "This is an integration test")
        assert task is not None
        assert task.title == "Integration Test Task"
        assert task.user_id == user_id
        print("✓ Task creation successful")

        # 2. Verify task retrieval
        user_tasks = await get_tasks(session, user_id)
        assert len(user_tasks) == 1
        assert user_tasks[0].id == task.id
        print("✓ Task retrieval successful")

        # 3. Create a conversation
        conversation = await create_conversation(session, user_id)
        assert conversation is not None
        assert conversation.user_id == user_id
        print("✓ Conversation creation successful")

        # 4. Create messages in the conversation
        message1 = await create_message(session, user_id, conversation.id, "user", "Hello, I created a task.")
        message2 = await create_message(session, user_id, conversation.id, "assistant", "Great! Which task did you create?")
        message3 = await create_message(session, user_id, conversation.id, "user", "I created 'Integration Test Task'.")

        assert message1 is not None
        assert message2 is not None
        assert message3 is not None
        print("✓ Message creation successful")

        # 5. Verify messages are associated with the conversation
        conv_messages = await get_messages_by_conversation(session, conversation.id, user_id)
        assert len(conv_messages) == 3
        assert conv_messages[0].content == "Hello, I created a task."
        assert conv_messages[1].content == "Great! Which task did you create?"
        assert conv_messages[2].content == "I created 'Integration Test Task'."
        print("✓ Message-conversation association successful")

        # 6. Update the task
        updated_task = await update_task(session, task.id, user_id, completed=True)
        assert updated_task is not None
        assert updated_task.completed is True
        print("✓ Task update successful")

        # 7. Test user isolation by creating another user's data
        other_user_id = "other_integration_user"

        # Create a task for the other user
        other_task = await create_task(session, other_user_id, "Other User Task", "This belongs to other user")

        # Verify that the first user can't see the other user's task
        first_user_tasks = await get_tasks(session, user_id)
        other_user_tasks = await get_tasks(session, other_user_id)

        assert len(first_user_tasks) == 1  # Still just the original task
        assert len(other_user_tasks) == 1  # Just the other user's task
        print("✓ User isolation successful")

        # 8. Test cascade delete by deleting the conversation
        delete_result = await delete_conversation(session, conversation.id, user_id)
        assert delete_result is True

        # Verify the conversation is gone
        all_conversations = await get_conversations(session, user_id)
        assert len(all_conversations) == 0

        # Verify messages are also gone due to cascade delete
        remaining_messages = await get_messages_by_conversation(session, conversation.id, user_id)
        assert len(remaining_messages) == 0
        print("✓ Cascade delete successful")

        # 9. Clean up by deleting the task
        delete_task_result = await delete_task(session, task.id, user_id)
        assert delete_task_result is True
        print("✓ Cleanup successful")

        print("✓ All integration tests passed!")


if __name__ == "__main__":
    # Run the integration test
    asyncio.run(test_full_integration())
    print("\n✓ Integration test suite completed successfully!")