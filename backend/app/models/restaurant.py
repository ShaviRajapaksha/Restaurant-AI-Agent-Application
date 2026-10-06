from sqlalchemy import Float, ForeignKey, Integer, String, Text, Time, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
import enum

from app.core.database import Base
from app.models.base import TimestampMixin

class TableStatus(str, enum.Enum):
    AVAILABLE = "AVAILABLE"
    RESERVED = "RESERVED"
    OCCUPIED = "OCCUPIED"
    OUT_OF_SERVICE = "OUT_OF_SERVICE"

class Restaurant(Base, TimestampMixin):
    __tablename__ = "restaurants"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(200), nullable=False, index=True)
    description: Mapped[str | None] = mapped_column(Text)
    address: Mapped[str] = mapped_column(String(300), nullable=False)
    city: Mapped[str] = mapped_column(String(100), nullable=False, index=True)
    latitude: Mapped[float | None] = mapped_column(Float)
    longitude: Mapped[float | None] = mapped_column(Float)
    cuisine: Mapped[str] = mapped_column(String(80), nullable=False, index=True)
    price_range: Mapped[str] = mapped_column(String(20), default="MEDIUM")  # LOW, MEDIUM, HIGH
    avg_price: Mapped[int] = mapped_column(Integer, default=3000)
    rating: Mapped[float] = mapped_column(Float, default=4.0)
    phone: Mapped[str | None] = mapped_column(String(40))
    opening_time: Mapped[str] = mapped_column(String(10), default="09:00")
    closing_time: Mapped[str] = mapped_column(String(10), default="22:00")
    image_url: Mapped[str | None] = mapped_column(String(400))

    tables = relationship("RestaurantTable", back_populates="restaurant", cascade="all, delete-orphan")
    menu_categories = relationship("MenuCategory", back_populates="restaurant", cascade="all, delete-orphan")
    reservations = relationship("Reservation", back_populates="restaurant")
    orders = relationship("Order", back_populates="restaurant")

class RestaurantTable(Base):
    __tablename__ = "restaurant_tables"

    id: Mapped[int] = mapped_column(primary_key=True)
    restaurant_id: Mapped[int] = mapped_column(ForeignKey("restaurants.id", ondelete="CASCADE"))
    table_number: Mapped[str] = mapped_column(String(20), nullable=False)
    capacity: Mapped[int] = mapped_column(Integer, nullable=False)
    status: Mapped[TableStatus] = mapped_column(Enum(TableStatus), default=TableStatus.AVAILABLE)

    restaurant = relationship("Restaurant", back_populates="tables")













