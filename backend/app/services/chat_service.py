from sqlalchemy.orm import Session
from app.models.chat import Conversation
from app.repositories.chat_repo import ConversationRepository
from fastapi import HTTPException


class ChatService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ConversationRepository(db)

    def get_or_create(self, user_id: int, conversation_id: int | None, title: str) -> Conversation:
        if conversation_id:
            c = self.repo.get(conversation_id)
            if not c or c.user_id != user_id:
                raise HTTPException(404, "Conversation not found")
            return c
        c = Conversation(user_id=user_id, title=title[:200], agent_state={})
        self.repo.add(c)
        self.db.commit()
        self.db.refresh(c)
        return c

    def list_for_user(self, user_id: int) -> list[Conversation]:
        return self.repo.list_for_user(user_id)

    def get_owned(self, user_id: int, cid: int) -> Conversation:
        c = self.repo.get(cid)
        if not c or c.user_id != user_id:
            raise HTTPException(404, "Conversation not found")
        return c

    def messages(self, user_id: int, cid: int):
        self.get_owned(user_id, cid)
        return self.repo.get_messages(cid)

    def save_state(self, conversation: Conversation, state: dict) -> None:
        conversation.agent_state = state
        self.db.commit()