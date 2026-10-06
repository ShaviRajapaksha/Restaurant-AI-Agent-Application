from datetime import date, time
from pydantic import BaseModel
from app.models.reservation import ReservationStatus


class ReservationCreate(BaseModel):
    restaurant_id: int
    reservation_date: date
    reservation_time: time
    party_size: int
    special_request: str | None = None


class ReservationUpdate(BaseModel):
    reservation_date: date | None = None
    reservation_time: time | None = None
    party_size: int | None = None
    status: ReservationStatus | None = None
    special_request: str | None = None


class ReservationOut(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    table_id: int | None
    reservation_date: date
    reservation_time: time
    party_size: int
    status: ReservationStatus
    special_request: str | None
    class Config:
        from_attributes = True