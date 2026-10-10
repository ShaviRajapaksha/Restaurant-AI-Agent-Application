from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.schemas.restaurant import RestaurantOut, RestaurantListResponse
from app.schemas.menu import MenuCategoryOut
from app.services.restaurant_service import RestaurantService


router = APIRouter(prefix="/api/restaurants", tags=["restaurants"])


@router.get("", response_model=RestaurantListResponse)
def list_restaurants(
    q: str | None = None,
    cuisine: str | None = None,
    city: str | None = None,
    max_price: int | None = None,
    min_rating: float | None = None,
    sort: str = "rating_desc",
    limit: int = Query(20, le=100),
    db: Session = Depends(get_db),
):
    items = RestaurantService(db).search(
        query=q, cuisine=cuisine, city=city, max_price=max_price,
        min_rating=min_rating, sort=sort, limit=limit,
    )
    return {"items": [RestaurantOut.model_validate(r) for r in items], "total": len(items)}


@router.get("/{rid}", response_model=RestaurantOut)
def get_restaurant(rid: int, db: Session = Depends(get_db)):
    return RestaurantService(db).get(rid)


@router.get("/{rid}/menu", response_model=list[MenuCategoryOut])
def get_menu(rid: int, db: Session = Depends(get_db)):
    r = RestaurantService(db).get(rid)
    return [MenuCategoryOut.model_validate(c) for c in r.menu_categories]