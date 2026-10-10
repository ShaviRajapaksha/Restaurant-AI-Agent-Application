from app.agent.tools.registry import Tool, registry
from app.services.reservation_service import ReservationService
from app.services.order_service import OrderService
from app.repositories.user_repo import UserRepository


def _get_current_user(db, *, user_id: int):
    u = UserRepository(db).get(user_id)
    if not u:
        return {"error": "user not found"}
    return {"id": u.id, "name": u.name, "email": u.email, "role": u.role.value}


def _get_user_reservations(db, *, user_id: int):
    svc = ReservationService(db)
    return {
        "reservations": [
            {
                "id": r.id, "restaurant_id": r.restaurant_id,
                "date": r.reservation_date.isoformat(),
                "time": r.reservation_time.isoformat(),
                "party_size": r.party_size, "status": r.status.value,
            }
            for r in svc.list_for_user(user_id)
        ]
    }


def _get_user_orders(db, *, user_id: int):
    svc = OrderService(db)
    return {
        "orders": [
            {"id": o.id, "restaurant_id": o.restaurant_id, "status": o.status.value, "total": o.total_amount}
            for o in svc.list_for_user(user_id)
        ]
    }


def register_user_tools():
    registry.register(Tool(
        name="get_current_user",
        description="Return the current authenticated user's profile.",
        parameters={"type": "object", "properties": {}},
        handler=_get_current_user,
    ))
    registry.register(Tool(
        name="get_user_reservations",
        description="List all reservations belonging to the current user.",
        parameters={"type": "object", "properties": {}},
        handler=_get_user_reservations,
    ))
    registry.register(Tool(
        name="get_user_orders",
        description="List all orders belonging to the current user.",
        parameters={"type": "object", "properties": {}},
        handler=_get_user_orders,
    ))