from sqlmodel import Session
from typing import List
from ..database.models import Message


def create_user_message(user_id: str, conversation_id: int, content: str, db: Session) -> Message:
    """
    Create a new user message in the database.

    Args:
        user_id: The ID of the user
        conversation_id: The ID of the conversation
        content: The content of the message
        db: Database session

    Returns:
        The created message object
    """
    user_message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="user",
        content=content
    )
    db.add(user_message)
    db.commit()
    db.refresh(user_message)
    return user_message


def create_assistant_message(user_id: str, conversation_id: int, content: str, db: Session) -> Message:
    """
    Create a new assistant message in the database.

    Args:
        user_id: The ID of the user
        conversation_id: The ID of the conversation
        content: The content of the message
        db: Database session

    Returns:
        The created message object
    """
    assistant_message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="assistant",
        content=content
    )
    db.add(assistant_message)
    db.commit()
    db.refresh(assistant_message)
    return assistant_message


def create_tool_message(user_id: str, conversation_id: int, content: str, db: Session) -> Message:
    """
    Create a new tool message in the database.

    Args:
        user_id: The ID of the user
        conversation_id: The ID of the conversation
        content: The content of the message
        db: Database session

    Returns:
        The created message object
    """
    tool_message = Message(
        user_id=user_id,
        conversation_id=conversation_id,
        role="tool",
        content=content
    )
    db.add(tool_message)
    db.commit()
    db.refresh(tool_message)
    return tool_message


def get_messages_for_conversation(conversation_id: int, db: Session) -> List[Message]:
    """
    Get all messages for a specific conversation.

    Args:
        conversation_id: The ID of the conversation
        db: Database session

    Returns:
        List of messages in the conversation
    """
    from sqlmodel import select

    query = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at)
    result = db.exec(query)
    messages = result.all()
    return messages


def get_latest_messages(conversation_id: int, limit: int, db: Session) -> List[Message]:
    """
    Get the latest messages for a specific conversation.

    Args:
        conversation_id: The ID of the conversation
        limit: Number of messages to return
        db: Database session

    Returns:
        List of the latest messages in the conversation
    """
    from sqlmodel import select

    query = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at.desc()).limit(limit)
    result = db.exec(query)
    messages = result.all()

    # Return in chronological order (reverse the list)
    return list(reversed(messages))