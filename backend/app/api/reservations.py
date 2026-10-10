from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.api.deps import get_current_user
from app.models.user import User
from app.schemas.reservation import ReservationCreate, ReservationUpdate, ReservationOut
from app.services.reservation_service import ReservationService


router = APIRouter(prefix="/api/reservations", tags=["reservations"])


@router.get("", response_model=list[ReservationOut])
def list_mine(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ReservationService(db).list_for_user(user.id)


@router.post("", response_model=ReservationOut, status_code=201)
def create(data: ReservationCreate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ReservationService(db).create(user.id, data)


@router.get("/{rid}", response_model=ReservationOut)
def get_one(rid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ReservationService(db).get_owned(user.id, rid)


@router.patch("/{rid}", response_model=ReservationOut)
def update(rid: int, data: ReservationUpdate, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ReservationService(db).update(user.id, rid, data)


@router.delete("/{rid}", response_model=ReservationOut)
def cancel(rid: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    return ReservationService(db).cancel(user.id, rid)