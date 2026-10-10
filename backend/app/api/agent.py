from fastapi import APIRouter, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.ext.asyncio import AsyncSession
import json

from app.core.database import get_async_db
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
    db: AsyncSession = Depends(get_async_db),
):
    # Capture plain values NOW, while the request-scoped objects are still valid.
    user_id: int = user.id
    user_name: str = user.name

    # Create/fetch the conversation with the request-scoped async session.
    chat_svc = ChatService(db)
    conv = await chat_svc.get_or_create_async(
        user_id=user_id,
        conversation_id=data.conversation_id,
        title=data.message[:60] or "New conversation",
    )
    conversation_id: int = conv.id

    async def event_stream():
        # Send conversation id immediately
        yield f"data: {json.dumps({'type': 'meta', 'data': {'conversation_id': conversation_id}})}\n\n"

        # Fresh async session for the streaming lifetime
        from app.core.database import AsyncSessionLocal
        async with AsyncSessionLocal() as session:
            runtime = AgentRuntime(session, user_id, conversation_id)
            try:
                async for evt in runtime.run(data.message):
                    yield f"data: {json.dumps(evt, default=str)}\n\n"
            except Exception as exc:  # noqa: BLE001
                err = {"type": "error", "data": {"message": str(exc)}}
                yield f"data: {json.dumps(err)}\n\n"

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",  # disable proxy buffering (nginx)
            "Connection": "keep-alive",
        },
    )