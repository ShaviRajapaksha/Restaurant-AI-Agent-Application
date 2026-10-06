import enum
from datetime import date as date_type, time as time_type
from sqlalchemy import Date, Enum, ForeignKey, Integer, String, Time, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.base import TimestampMixin


class ReservationStatus(str, enum.Enum):
    PENDING = "PENDING"
    CONFIRMED = "CONFIRMED"
    CANCELLED = "CANCELLED"
    COMPLETED = "COMPLETED"


class Reservation(Base, TimestampMixin):
    __tablename__ = "reservations"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id", ondelete="CASCADE"))
    table_id: Mapped[int | None] = mapped_column(ForeignKey("restaurant_tables.id", ondelete="SET NULL"))
    reservation_date: Mapped[date_type] = mapped_column(Date, nullable=False)
    reservation_time: Mapped[time_type] = mapped_column(Time, nullable=False)
    party_size: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[ReservationStatus] = mapped_column(
        Enum(ReservationStatus), default=ReservationStatus.PENDING
    )
    special_request: Mapped[str | None] = mapped_column(Text)

    user = relationship("User", back_populates="reservations")
    restaurant = relationship("Restaurant", back_populates="reservations")
    table = relationship("RestaurantTable")