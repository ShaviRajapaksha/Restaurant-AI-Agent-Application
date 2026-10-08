from sqlalchemy import select
from sqlalchemy.orm import selectinload
from app.models.order import Order
from app.repositories.base import BaseRepository


class OrderRepository(BaseRepository[Order]):
    model = Order

    def list_for_user(self, user_id: int) -> list[Order]:
        return list(self.db.scalars(
            select(Order).where(Order.user_id == user_id)
            .options(selectinload(Order.items))
            .order_by(Order.id.desc())
        ))

    def get_with_items(self, order_id: int) -> Order | None:
        return self.db.scalar(
            select(Order).where(Order.id == order_id).options(selectinload(Order.items))
        )