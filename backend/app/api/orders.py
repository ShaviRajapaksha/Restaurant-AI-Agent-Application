from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.order import OrderCreate, OrderOut
from app.services.order_service import OrderService


router = APIRouter(prefix="/api/orders", tags=["orders"])


@router.get("", response_model=list[OrderOut])
def list_mine(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return OrderService(db).list_for_user(user.id)


@router.post("", response_model=OrderOut, status_code=201)
def create(data: OrderCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return OrderService(db).create(user.id, data)


@router.get("/{oid}", response_model=OrderOut)
def get_one(oid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return OrderService(db).get_owned(user.id, oid)