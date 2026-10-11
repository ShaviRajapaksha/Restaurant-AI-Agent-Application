from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import json
import asyncio

from app.core.database import get_db, SessionLocal
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService
from app.agent.agent import AgentRuntime


router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("/chat")
async def chat(
    data: ChatRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """Streams agent events as Server-Sent Events (SSE)."""
    chat_svc = ChatService(db)
    conv = chat_svc.get_or_create(
        user.id, data.conversation_id, title=data.message[:60] or "New conversation"
    )

    # ---- Snapshot primitives BEFORE the request-scoped session closes ----
    user_id = user.id
    conversation_id = conv.id
    user_message = data.message

    async def event_stream():
        # Fresh session for the lifetime of the stream
        session = SessionLocal()
        try:
            yield f"data: {json.dumps({'type': 'meta', 'data': {'conversation_id': conversation_id}})}\n\n"

            runtime = AgentRuntime(session, user_id, conversation_id)
            agen = runtime.run(user_message)
            try:
                async for evt in agen:
                    yield f"data: {json.dumps(evt, default=str)}\n\n"
            finally:
                await agen.aclose()
        finally:
            session.close()

    return StreamingResponse(event_stream(), media_type="text/event-stream")