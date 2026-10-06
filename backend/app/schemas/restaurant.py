from pydantic import BaseModel


class RestaurantBase(BaseModel):
    name: str
    description: str | None = None
    address: str
    city: str
    cuisine: str
    price_range: str = "MEDIUM"
    avg_price: int = 3000
    rating: float = 4.0
    phone: str | None = None
    opening_time: str = "09:00"
    closing_time: str = "22:00"
    image_url: str | None = None


class RestaurantOut(RestaurantBase):
    id: int
    class Config:
        from_attributes = True


class RestaurantListResponse(BaseModel):
    items: list[RestaurantOut]
    total: int