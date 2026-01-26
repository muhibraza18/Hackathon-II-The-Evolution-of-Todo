from sqlmodel import Session, select
from typing import Optional
from ..database.models import Conversation


def get_or_create_conversation(user_id: str, conversation_id: Optional[int], db: Session) -> Conversation:
    """
    Get an existing conversation or create a new one if conversation_id is None.

    Args:
        user_id: The ID of the user
        conversation_id: The ID of the conversation (None to create new)
        db: Database session

    Returns:
        The conversation object
    """
    if conversation_id is None:
        # Create a new conversation
        conversation = Conversation(user_id=user_id)
        db.add(conversation)
        db.commit()
        db.refresh(conversation)
        return conversation
    else:
        # Get existing conversation
        conversation_query = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        conversation_result = db.exec(conversation_query)
        conversation = conversation_result.first()

        if not conversation:
            raise ValueError(f"Conversation {conversation_id} not found or doesn't belong to user {user_id}")

        return conversation


def get_conversation_history(conversation_id: int, db: Session):
    """
    Get the conversation history for a given conversation ID.

    Args:
        conversation_id: The ID of the conversation
        db: Database session

    Returns:
        List of messages in the conversation
    """
    from ..database.models import Message

    # Get all messages in the conversation, ordered by creation time
    history_query = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.created_at)
    history_result = db.exec(history_query)
    messages = history_result.all()

    return messages