from pydantic import BaseModel


class MenuItemOut(BaseModel):
    id: int
    name: str
    description: str | None
    price: int
    available: bool
    image_url: str | None
    category_id: int
    class Config:
        from_attributes = True


class MenuCategoryOut(BaseModel):
    id: int
    name: str
    items: list[MenuItemOut]
    class Config:
        from_attributes = True