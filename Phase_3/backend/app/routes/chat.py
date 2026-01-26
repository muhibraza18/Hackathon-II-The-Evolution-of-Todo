from fastapi import APIRouter, Depends, HTTPException, Request
from typing import Optional, List, Dict, Any  # Any is already imported
from sqlmodel import Session, select
from pydantic import BaseModel
from ..database.connection import get_db_session
from ..services.agent import process_chat_request
from ..database.models import Conversation, Message

router = APIRouter()


class ChatRequest(BaseModel):
    """Request model for chat endpoint"""
    conversation_id: Optional[int] = None
    message: str


class ToolCall(BaseModel):
    """Model for representing a tool call"""
    name: str
    arguments: Dict[str, Any]
    result: Any  # ✅ Accept any type - dict, list, etc.


class ChatResponse(BaseModel):
    """Response model for chat endpoint"""
    conversation_id: int
    response: str
    tool_calls: List[ToolCall]


@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(
    request: Request,
    chat_request: ChatRequest,
    db: Session = Depends(get_db_session)
):
    """
    Main chat endpoint that processes user messages and returns AI responses
    with any tool calls executed. User ID is extracted from the authenticated session.
    """
    # Extract user_id from the request state (set by auth middleware)
    user_id = getattr(request.state, 'user_id', None)

    if not user_id:
        print("❌ No user_id in request.state - authentication failed")
        raise HTTPException(
            status_code=401, 
            detail="User not authenticated. Please login again."
        )

    print(f"✅ Chat request from user_id: {user_id}")
    print(f"📝 Message: {chat_request.message[:50]}...")

    try:
        # Process the chat request using the agent service
        result = await process_chat_request(
            user_id=user_id,
            conversation_id=chat_request.conversation_id,
            message=chat_request.message,
            db=db
        )

        print(f"✅ Response generated for conversation {result['conversation_id']}")

        return ChatResponse(
            conversation_id=result["conversation_id"],
            response=result["response"],
            tool_calls=result["tool_calls"]
        )
    except ValueError as e:
        print(f"❌ Validation error: {e}")
        # Handle validation errors
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        print(f"❌ Internal error: {e}")
        # Handle other errors
        raise HTTPException(status_code=500, detail=f"Internal server error: {str(e)}")