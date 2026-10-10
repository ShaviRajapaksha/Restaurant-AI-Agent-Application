from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.models.order import Order, OrderItem, OrderStatus
from app.models.menu import MenuItem
from app.repositories.order_repo import OrderRepository
from app.repositories.restaurant_repo import RestaurantRepository
from app.schemas.order import OrderCreate


class OrderService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = OrderRepository(db)
        self.restaurant_repo = RestaurantRepository(db)

    def create(self, user_id: int, data: OrderCreate) -> Order:
        restaurant = self.restaurant_repo.get(data.restaurant_id)
        if not restaurant:
            raise HTTPException(404, "Restaurant not found")

        order = Order(user_id=user_id, restaurant_id=data.restaurant_id, status=OrderStatus.PENDING, total_amount=0)
        self.repo.add(order)

        total = 0
        for item_in in data.items:
            mi = self.db.get(MenuItem, item_in.menu_item_id)
            if not mi or not mi.available:
                raise HTTPException(400, f"Menu item {item_in.menu_item_id} unavailable")
            if mi.category.restaurant_id != data.restaurant_id:
                raise HTTPException(400, "Menu item does not belong to restaurant")
            oi = OrderItem(
                order_id=order.id,
                menu_item_id=mi.id,
                name_snapshot=mi.name,
                unit_price=mi.price,
                quantity=item_in.quantity,
            )
            self.db.add(oi)
            total += mi.price * item_in.quantity

        order.total_amount = total
        order.status = OrderStatus.CONFIRMED
        self.db.commit()
        self.db.refresh(order)
        return order

    def list_for_user(self, user_id: int) -> list[Order]:
        return self.repo.list_for_user(user_id)

    def get_owned(self, user_id: int, order_id: int) -> Order:
        o = self.repo.get_with_items(order_id)
        if not o or o.user_id != user_id:
            raise HTTPException(404, "Order not found")
        return o