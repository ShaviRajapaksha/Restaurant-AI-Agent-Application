from sqlalchemy.orm import Session
from fastapi import HTTPException

from app.repositories.restaurant_repo import RestaurantRepository
from app.models.restaurant import Restaurant


class RestaurantService:
    def __init__(self, db: Session):
        self.repo = RestaurantRepository(db)

    def search(self, **kwargs) -> list[Restaurant]:
        return self.repo.search(**kwargs)

    def get(self, rid: int) -> Restaurant:
        r = self.repo.get_with_menu(rid)
        if not r:
            raise HTTPException(status_code=404, detail="Restaurant not found")
        return r