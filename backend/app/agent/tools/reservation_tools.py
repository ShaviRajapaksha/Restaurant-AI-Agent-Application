from datetime import date as date_cls, time as time_cls
from app.agent.tools.registry import Tool, registry
from app.services.reservation_service import ReservationService
from app.schemas.reservation import ReservationCreate


def _check_availability(db, *, restaurant_id: int, date: str, time: str, party_size: int):
    svc = ReservationService(db)
    d = date_cls.fromisoformat(date)
    t = time_cls.fromisoformat(time)
    return svc.check_availability(restaurant_id, d, t, party_size)


def _check_restaurant_hours(db, *, restaurant_id: int):
    svc = ReservationService(db)
    r = svc.restaurant_repo.get(restaurant_id)
    if not r:
        return {"error": "Restaurant not found"}
    return {"opening_time": r.opening_time, "closing_time": r.closing_time}


def _create_reservation(db, *, user_id: int, restaurant_id: int, date: str, time: str, party_size: int, special_request: str | None = None):
    svc = ReservationService(db)
    data = ReservationCreate(
        restaurant_id=restaurant_id,
        reservation_date=date_cls.fromisoformat(date),
        reservation_time=time_cls.fromisoformat(time),
        party_size=party_size,
        special_request=special_request,
    )
    r = svc.create(user_id, data)
    return {
        "reservation_id": r.id,
        "restaurant_id": r.restaurant_id,
        "date": r.reservation_date.isoformat(),
        "time": r.reservation_time.isoformat(),
        "party_size": r.party_size,
        "status": r.status.value,
    }


def _get_reservation(db, *, user_id: int, reservation_id: int):
    svc = ReservationService(db)
    r = svc.get_owned(user_id, reservation_id)
    return {
        "reservation_id": r.id,
        "restaurant_id": r.restaurant_id,
        "date": r.reservation_date.isoformat(),
        "time": r.reservation_time.isoformat(),
        "party_size": r.party_size,
        "status": r.status.value,
    }


def _cancel_reservation(db, *, user_id: int, reservation_id: int):
    svc = ReservationService(db)
    r = svc.cancel(user_id, reservation_id)
    return {"reservation_id": r.id, "status": r.status.value}


def register_reservation_tools():
    registry.register(Tool(
        name="check_table_availability",
        description="Check whether a restaurant can seat a party at a given date/time. Date = YYYY-MM-DD, time = HH:MM.",
        parameters={
            "type": "object",
            "required": ["restaurant_id", "date", "time", "party_size"],
            "properties": {
                "restaurant_id": {"type": "integer"},
                "date": {"type": "string"},
                "time": {"type": "string"},
                "party_size": {"type": "integer"},
            },
        },
        handler=_check_availability,
    ))

    registry.register(Tool(
        name="check_restaurant_hours",
        description="Get the opening and closing times of a restaurant.",
        parameters={
            "type": "object",
            "required": ["restaurant_id"],
            "properties": {"restaurant_id": {"type": "integer"}},
        },
        handler=_check_restaurant_hours,
    ))

    registry.register(Tool(
        name="create_reservation",
        description="Create a restaurant reservation. Only call AFTER user confirmation.",
        parameters={
            "type": "object",
            "required": ["restaurant_id", "date", "time", "party_size"],
            "properties": {
                "restaurant_id": {"type": "integer"},
                "date": {"type": "string", "description": "YYYY-MM-DD"},
                "time": {"type": "string", "description": "HH:MM"},
                "party_size": {"type": "integer"},
                "special_request": {"type": "string"},
            },
        },
        handler=_create_reservation,
        requires_confirmation=True,
    ))

    registry.register(Tool(
        name="get_reservation",
        description="Get details of one of the current user's reservations by ID.",
        parameters={"type": "object", "required": ["reservation_id"],
                    "properties": {"reservation_id": {"type": "integer"}}},
        handler=_get_reservation,
    ))

    registry.register(Tool(
        name="cancel_reservation",
        description="Cancel a reservation owned by the user. Only call AFTER explicit user confirmation.",
        parameters={"type": "object", "required": ["reservation_id"],
                    "properties": {"reservation_id": {"type": "integer"}}},
        handler=_cancel_reservation,
        requires_confirmation=True,
    ))