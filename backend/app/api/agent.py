from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from fastapi.responses import StreamingResponse
import json

from app.core.database import get_db, SessionLocal
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.chat import ChatRequest
from app.services.chat_service import ChatService
from app.agent.agent import AgentRuntime


router = APIRouter(prefix="/api/agent", tags=["agent"])


@router.post("/chat")
async def chat(data: ChatRequest, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Streams agent events as Server-Sent Events (SSE)."""
    chat_svc = ChatService(db)
    conv = chat_svc.get_or_create(user.id, data.conversation_id, title=data.message[:60] or "New conversation")

    # We need a fresh session inside the generator because FastAPI will close the dep one
    def event_stream():
        session = SessionLocal()
        try:
            runtime = AgentRuntime(session, user.id, conv.id)
            # Send conversation_id first
            yield f"data: {json.dumps({'type': 'meta', 'data': {'conversation_id': conv.id}})}\n\n"

            import asyncio
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            try:
                agen = runtime.run(data.message)
                while True:
                    try:
                        evt = loop.run_until_complete(agen.__anext__())
                    except StopAsyncIteration:
                        break
                    yield f"data: {json.dumps(evt, default=str)}\n\n"
                # close gen
                try:
                    loop.run_until_complete(agen.aclose())
                except Exception:
                    pass
            finally:
                loop.close()
        finally:
            session.close()

    return StreamingResponse(event_stream(), media_type="text/event-stream")