from sqlalchemy import select
from app.models.chat import Conversation, Message, ToolCall
from app.repositories.base import BaseRepository


class ConversationRepository(BaseRepository[Conversation]):
    model = Conversation

    def list_for_user(self, user_id: int) -> list[Conversation]:
        return list(self.db.scalars(
            select(Conversation).where(Conversation.user_id == user_id).order_by(Conversation.id.desc())
        ))

    def get_messages(self, conversation_id: int) -> list[Message]:
        return list(self.db.scalars(
            select(Message).where(Message.conversation_id == conversation_id).order_by(Message.id.asc())
        ))

    def add_message(self, conversation_id: int, role, content: str, payload: dict | None = None) -> Message:
        msg = Message(conversation_id=conversation_id, role=role, content=content, payload=payload)
        self.db.add(msg)
        self.db.flush()
        return msg

    def log_tool(self, conversation_id: int, name: str, args: dict, result: dict | None, error: str | None = None) -> ToolCall:
        tc = ToolCall(conversation_id=conversation_id, name=name, arguments=args, result=result, error=error)
        self.db.add(tc)
        self.db.flush()
        return tc