from datetime import date, datetime, time as time_type
from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.models.reservation import Reservation, ReservationStatus
from app.models.restaurant import Restaurant, RestaurantTable, TableStatus
from app.repositories.reservation_repo import ReservationRepository
from app.repositories.restaurant_repo import RestaurantRepository
from app.schemas.reservation import ReservationCreate, ReservationUpdate


def _parse_hhmm(s: str) -> time_type:
    h, m = s.split(":")
    return time_type(int(h), int(m))


class ReservationService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = ReservationRepository(db)
        self.restaurant_repo = RestaurantRepository(db)

    def _check_open(self, restaurant: Restaurant, t: time_type) -> bool:
        return _parse_hhmm(restaurant.opening_time) <= t <= _parse_hhmm(restaurant.closing_time)

    def check_availability(self, restaurant_id: int, d: date, t: time_type, party_size: int) -> dict:
        restaurant = self.restaurant_repo.get(restaurant_id)
        if not restaurant:
            raise HTTPException(404, "Restaurant not found")
        if not self._check_open(restaurant, t):
            return {"available": False, "reason": "Outside opening hours"}

        tables = self.restaurant_repo.get_tables(restaurant_id)
        suitable = [tb for tb in tables if tb.capacity >= party_size and tb.status != TableStatus.OUT_OF_SERVICE]
        if not suitable:
            return {"available": False, "reason": "No table large enough"}

        free = []
        for tb in suitable:
            if not self.repo.has_conflict(restaurant_id, d, t, tb.id):
                free.append(tb)
        if not free:
            return {"available": False, "reason": "All suitable tables are booked at that time"}

        best = min(free, key=lambda x: x.capacity)
        return {
            "available": True,
            "table_id": best.id,
            "table_number": best.table_number,
            "capacity": best.capacity,
        }

    def create(self, user_id: int, data: ReservationCreate) -> Reservation:
        avail = self.check_availability(data.restaurant_id, data.reservation_date, data.reservation_time, data.party_size)
        if not avail["available"]:
            raise HTTPException(400, avail["reason"])
        reservation = Reservation(
            user_id=user_id,
            restaurant_id=data.restaurant_id,
            table_id=avail["table_id"],
            reservation_date=data.reservation_date,
            reservation_time=data.reservation_time,
            party_size=data.party_size,
            status=ReservationStatus.CONFIRMED,
            special_request=data.special_request,
        )
        self.repo.add(reservation)
        self.db.commit()
        self.db.refresh(reservation)
        return reservation

    def list_for_user(self, user_id: int) -> list[Reservation]:
        return self.repo.list_for_user(user_id)

    def get_owned(self, user_id: int, reservation_id: int) -> Reservation:
        r = self.repo.get(reservation_id)
        if not r or r.user_id != user_id:
            raise HTTPException(404, "Reservation not found")
        return r

    def update(self, user_id: int, reservation_id: int, data: ReservationUpdate) -> Reservation:
        r = self.get_owned(user_id, reservation_id)
        for field, val in data.model_dump(exclude_none=True).items():
            setattr(r, field, val)
        self.db.commit()
        self.db.refresh(r)
        return r

    def cancel(self, user_id: int, reservation_id: int) -> Reservation:
        r = self.get_owned(user_id, reservation_id)
        r.status = ReservationStatus.CANCELLED
        self.db.commit()
        self.db.refresh(r)
        return r