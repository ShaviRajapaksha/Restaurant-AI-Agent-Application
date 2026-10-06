from datetime import datetime
from pydantic import BaseModel
from app.models.chat import MessageRole


class ChatRequest(BaseModel):
    conversation_id: int | None = None
    message: str


class AgentEvent(BaseModel):
    type: str  # "status", "message", "cards", "error"
    data: dict


class MessageOut(BaseModel):
    id: int
    role: MessageRole
    content: str
    payload: dict | None
    created_at: datetime
    class Config:
        from_attributes = True


class ConversationOut(BaseModel):
    id: int
    title: str
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True


class ChatResponse(BaseModel):
    conversation_id: int
    reply: str
    payload: dict | None = None
    events: list[AgentEvent] = []