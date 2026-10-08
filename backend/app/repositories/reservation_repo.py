from datetime import date, time
from sqlalchemy import select, and_
from sqlalchemy.orm import Session
from app.models.reservation import Reservation, ReservationStatus
from app.repositories.base import BaseRepository


class ReservationRepository(BaseRepository[Reservation]):
    model = Reservation

    def list_for_user(self, user_id: int) -> list[Reservation]:
        return list(self.db.scalars(
            select(Reservation).where(Reservation.user_id == user_id).order_by(Reservation.id.desc())
        ))

    def has_conflict(self, restaurant_id: int, d: date, t: time, table_id: int | None = None) -> bool:
        stmt = select(Reservation).where(
            and_(
                Reservation.restaurant_id == restaurant_id,
                Reservation.reservation_date == d,
                Reservation.reservation_time == t,
                Reservation.status.in_([ReservationStatus.PENDING, ReservationStatus.CONFIRMED]),
            )
        )
        if table_id is not None:
            stmt = stmt.where(Reservation.table_id == table_id)
        return self.db.scalar(stmt) is not None