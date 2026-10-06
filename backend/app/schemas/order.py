from pydantic import BaseModel
from app.models.order import OrderStatus


class OrderItemIn(BaseModel):
    menu_item_id: int
    quantity: int = 1


class OrderCreate(BaseModel):
    restaurant_id: int
    items: list[OrderItemIn]


class OrderItemOut(BaseModel):
    id: int
    menu_item_id: int
    name_snapshot: str
    unit_price: int
    quantity: int
    class Config:
        from_attributes = True


class OrderOut(BaseModel):
    id: int
    user_id: int
    restaurant_id: int
    status: OrderStatus
    total_amount: int
    items: list[OrderItemOut]
    class Config:
        from_attributes = True