from app.agent.tools.registry import Tool, registry
from app.services.restaurant_service import RestaurantService


def _search_restaurants(db, *, query=None, cuisine=None, city=None, max_price=None, min_rating=None, sort="rating_desc", limit=10):
    svc = RestaurantService(db)
    results = svc.search(
        query=query, cuisine=cuisine, city=city,
        max_price=max_price, min_rating=min_rating, sort=sort, limit=limit,
    )
    return {
        "count": len(results),
        "restaurants": [
            {
                "id": r.id,
                "name": r.name,
                "cuisine": r.cuisine,
                "city": r.city,
                "address": r.address,
                "rating": r.rating,
                "avg_price": r.avg_price,
                "price_range": r.price_range,
                "opening_time": r.opening_time,
                "closing_time": r.closing_time,
            }
            for r in results
        ],
    }


def _get_restaurant_details(db, *, restaurant_id: int):
    svc = RestaurantService(db)
    r = svc.get(restaurant_id)
    return {
        "id": r.id,
        "name": r.name,
        "description": r.description,
        "cuisine": r.cuisine,
        "address": r.address,
        "city": r.city,
        "rating": r.rating,
        "avg_price": r.avg_price,
        "opening_time": r.opening_time,
        "closing_time": r.closing_time,
        "phone": r.phone,
    }


def register_restaurant_tools():
    registry.register(Tool(
        name="search_restaurants",
        description="Search restaurants by cuisine, city, budget, rating, or free-text query.",
        parameters={
            "type": "object",
            "properties": {
                "query": {"type": "string"},
                "cuisine": {"type": "string"},
                "city": {"type": "string"},
                "max_price": {"type": "integer", "description": "Maximum average price per person (LKR)"},
                "min_rating": {"type": "number"},
                "sort": {"type": "string", "enum": ["rating_desc", "price_asc", "price_desc"]},
                "limit": {"type": "integer", "default": 10},
            },
        },
        handler=_search_restaurants,
    ))

    registry.register(Tool(
        name="get_restaurant_details",
        description="Get full details of a specific restaurant by its ID.",
        parameters={
            "type": "object",
            "required": ["restaurant_id"],
            "properties": {"restaurant_id": {"type": "integer"}},
        },
        handler=_get_restaurant_details,
    ))