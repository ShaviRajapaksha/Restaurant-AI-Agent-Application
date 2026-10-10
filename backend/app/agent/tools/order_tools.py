from app.agent.tools.registry import Tool, registry
from app.services.order_service import OrderService
from app.schemas.order import OrderCreate, OrderItemIn


def _create_order(db, *, user_id: int, restaurant_id: int, items: list[dict]):
    svc = OrderService(db)
    payload = OrderCreate(
        restaurant_id=restaurant_id,
        items=[OrderItemIn(menu_item_id=i["menu_item_id"], quantity=i.get("quantity", 1)) for i in items],
    )
    o = svc.create(user_id, payload)
    return {
        "order_id": o.id,
        "status": o.status.value,
        "total_amount": o.total_amount,
        "items": [
            {"name": it.name_snapshot, "qty": it.quantity, "unit_price": it.unit_price}
            for it in o.items
        ],
    }


def _get_order(db, *, user_id: int, order_id: int):
    svc = OrderService(db)
    o = svc.get_owned(user_id, order_id)
    return {
        "order_id": o.id,
        "status": o.status.value,
        "total_amount": o.total_amount,
        "items": [
            {"name": it.name_snapshot, "qty": it.quantity, "unit_price": it.unit_price}
            for it in o.items
        ],
    }


def _get_order_status(db, *, user_id: int, order_id: int):
    svc = OrderService(db)
    o = svc.get_owned(user_id, order_id)
    return {"order_id": o.id, "status": o.status.value}


def register_order_tools():
    registry.register(Tool(
        name="create_order",
        description="Create a food order for the user. Only call AFTER user confirmation of the item list and total.",
        parameters={
            "type": "object",
            "required": ["restaurant_id", "items"],
            "properties": {
                "restaurant_id": {"type": "integer"},
                "items": {
                    "type": "array",
                    "items": {
                        "type": "object",
                        "required": ["menu_item_id"],
                        "properties": {
                            "menu_item_id": {"type": "integer"},
                            "quantity": {"type": "integer", "default": 1},
                        },
                    },
                },
            },
        },
        handler=_create_order,
        requires_confirmation=True,
    ))

    registry.register(Tool(
        name="get_order",
        description="Get details of one of the current user's orders.",
        parameters={"type": "object", "required": ["order_id"], "properties": {"order_id": {"type": "integer"}}},
        handler=_get_order,
    ))

    registry.register(Tool(
        name="get_order_status",
        description="Get the status of an order.",
        parameters={"type": "object", "required": ["order_id"], "properties": {"order_id": {"type": "integer"}}},
        handler=_get_order_status,
    ))