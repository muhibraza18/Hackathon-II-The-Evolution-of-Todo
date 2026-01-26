"""
Skill: Message Persister
Purpose: Save user and assistant messages to database
Reusable: Yes - used after every chat interaction
"""

from sqlmodel import Session
from models import Message, Conversation
from datetime import datetime

class MessagePersister:
    """Handles saving messages to database"""
    
    @staticmethod
    def save_user_message(
        session: Session,
        user_id: str,
        conversation_id: int,
        content: str
    ) -> Message:
        """Save user message to database"""
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role="user",
            content=content,
            created_at=datetime.utcnow()
        )
        session.add(message)
        session.commit()
        return message
    
    @staticmethod
    def save_assistant_message(
        session: Session,
        user_id: str,
        conversation_id: int,
        content: str
    ) -> Message:
        """Save assistant message to database"""
        message = Message(
            user_id=user_id,
            conversation_id=conversation_id,
            role="assistant",
            content=content,
            created_at=datetime.utcnow()
        )
        session.add(message)
        session.commit()
        return message