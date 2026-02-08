"""
Skill: Conversation History Builder
Purpose: Fetch and format conversation history for AI agent
Reusable: Yes - used by chat endpoint
"""

from typing import List, Dict
from sqlmodel import Session, select
from models import Message

class ConversationBuilder:
    """Builds conversation history from database"""
    
    @staticmethod
    def build_history(
        session: Session, 
        conversation_id: int, 
        user_id: str
    ) -> List[Dict[str, str]]:
        """
        Fetches messages and formats for OpenAI agent
        Returns: [{"role": "user", "content": "..."}, ...]
        """
        messages = session.exec(
            select(Message)
            .where(Message.conversation_id == conversation_id)
            .where(Message.user_id == user_id)
            .order_by(Message.created_at)
        ).all()
        
        return [
            {"role": msg.role, "content": msg.content}
            for msg in messages
        ]