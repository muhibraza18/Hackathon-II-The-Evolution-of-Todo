"""
Skill: Conversation Manager
Purpose: Create and retrieve conversations
Reusable: Yes - used by chat endpoint
"""

from sqlmodel import Session, select
from models import Conversation
from datetime import datetime
from typing import Optional

class ConversationManager:
    """Manages conversation creation and retrieval"""
    
    @staticmethod
    def get_or_create_conversation(
        session: Session,
        user_id: str,
        conversation_id: Optional[int] = None
    ) -> Conversation:
        """
        Gets existing conversation or creates new one
        """
        if conversation_id:
            # Fetch existing
            conv = session.get(Conversation, conversation_id)
            if conv and conv.user_id == user_id:
                return conv
        
        # Create new conversation
        new_conv = Conversation(
            user_id=user_id,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        session.add(new_conv)
        session.commit()
        session.refresh(new_conv)
        return new_conv