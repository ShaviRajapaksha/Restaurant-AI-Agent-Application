from sqlalchemy import select, and_, or_
from sqlalchemy.orm import Session, selectinload
from app.models.restaurant import Restaurant, RestaurantTable
from app.models.menu import MenuCategory, MenuItem
from app.repositories.base import BaseRepository


class RestaurantRepository(BaseRepository[Restaurant]):
    model = Restaurant

    def search(
        self,
        query: str | None = None,
        cuisine: str | None = None,
        city: str | None = None,
        max_price: int | None = None,
        min_rating: float | None = None,
        sort: str = "rating_desc",
        limit: int = 20,
    ) -> list[Restaurant]:
        stmt = select(Restaurant)
        conditions = []
        if query:
            like = f"%{query.lower()}%"
            conditions.append(or_(
                Restaurant.name.ilike(like),
                Restaurant.description.ilike(like),
            ))
        if cuisine:
            conditions.append(Restaurant.cuisine.ilike(f"%{cuisine}%"))
        if city:
            conditions.append(Restaurant.city.ilike(f"%{city}%"))
        if max_price:
            conditions.append(Restaurant.avg_price <= max_price)
        if min_rating:
            conditions.append(Restaurant.rating >= min_rating)
        if conditions:
            stmt = stmt.where(and_(*conditions))

        if sort == "rating_desc":
            stmt = stmt.order_by(Restaurant.rating.desc())
        elif sort == "price_asc":
            stmt = stmt.order_by(Restaurant.avg_price.asc())
        elif sort == "price_desc":
            stmt = stmt.order_by(Restaurant.avg_price.desc())
        else:
            stmt = stmt.order_by(Restaurant.id.asc())

        return list(self.db.scalars(stmt.limit(limit)))

    def get_with_menu(self, restaurant_id: int) -> Restaurant | None:
        return self.db.scalar(
            select(Restaurant)
            .where(Restaurant.id == restaurant_id)
            .options(
                selectinload(Restaurant.menu_categories).selectinload(MenuCategory.items),
                selectinload(Restaurant.tables),
            )
        )

    def get_tables(self, restaurant_id: int) -> list[RestaurantTable]:
        return list(self.db.scalars(
            select(RestaurantTable).where(RestaurantTable.restaurant_id == restaurant_id)
        ))