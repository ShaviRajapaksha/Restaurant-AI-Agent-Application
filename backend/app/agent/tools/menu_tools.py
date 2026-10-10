from app.agent.tools.registry import Tool, registry
from app.services.restaurant_service import RestaurantService


def _get_restaurant_menu(db, *, restaurant_id: int):
    svc = RestaurantService(db)
    r = svc.get(restaurant_id)
    return {
        "restaurant_id": r.id,
        "restaurant_name": r.name,
        "categories": [
            {
                "id": c.id,
                "name": c.name,
                "items": [
                    {
                        "id": i.id,
                        "name": i.name,
                        "description": i.description,
                        "price": i.price,
                        "available": i.available,
                    }
                    for i in c.items if i.available
                ],
            }
            for c in r.menu_categories
        ],
    }


def _search_menu_items(db, *, restaurant_id: int, query: str):
    svc = RestaurantService(db)
    r = svc.get(restaurant_id)
    q = query.lower()
    hits = []
    for c in r.menu_categories:
        for i in c.items:
            if q in i.name.lower() or (i.description and q in i.description.lower()):
                hits.append({"id": i.id, "name": i.name, "price": i.price, "category": c.name})
    return {"restaurant_id": r.id, "matches": hits}


def register_menu_tools():
    registry.register(Tool(
        name="get_restaurant_menu",
        description="Return the full menu (categories and available items) for a restaurant.",
        parameters={
            "type": "object",
            "required": ["restaurant_id"],
            "properties": {"restaurant_id": {"type": "integer"}},
        },
        handler=_get_restaurant_menu,
    ))

    registry.register(Tool(
        name="search_menu_items",
        description="Search menu items of a restaurant by name/description keyword.",
        parameters={
            "type": "object",
            "required": ["restaurant_id", "query"],
            "properties": {
                "restaurant_id": {"type": "integer"},
                "query": {"type": "string"},
            },
        },
        handler=_search_menu_items,
    ))