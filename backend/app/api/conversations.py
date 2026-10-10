from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.chat import ConversationOut, MessageOut
from app.services.chat_service import ChatService


router = APIRouter(prefix="/api/conversations", tags=["conversations"])


@router.get("", response_model=list[ConversationOut])
def list_mine(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ChatService(db).list_for_user(user.id)


@router.get("/{cid}", response_model=ConversationOut)
def get_one(cid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ChatService(db).get_owned(user.id, cid)


@router.get("/{cid}/messages", response_model=list[MessageOut])
def messages(cid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ChatService(db).messages(user.id, cid)