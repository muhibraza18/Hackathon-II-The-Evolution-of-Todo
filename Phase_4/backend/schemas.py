from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List
from enum import Enum


class RoleEnum(str, Enum):
    user = "user"
    assistant = "assistant"


class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    completed: bool = False


class TaskCreate(TaskBase):
    user_id: str


class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    completed: Optional[bool] = None


class TaskResponse(TaskBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class ConversationBase(BaseModel):
    pass


class ConversationCreate(ConversationBase):
    user_id: str


class ConversationResponse(ConversationBase):
    id: int
    user_id: str
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MessageBase(BaseModel):
    conversation_id: int
    role: RoleEnum
    content: str


class MessageCreate(MessageBase):
    user_id: str


class MessageUpdate(BaseModel):
    content: Optional[str] = None


class MessageResponse(MessageBase):
    id: int
    user_id: str
    created_at: datetime

    class Config:
        from_attributes = True


class ConversationWithMessages(ConversationResponse):
    messages: List[MessageResponse] = []