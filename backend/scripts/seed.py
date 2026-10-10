"""Seed the database with realistic Colombo-based restaurant data."""
from datetime import date, time, timedelta
from sqlalchemy import select

from app.core.database import SessionLocal
from app.models.user import User, UserRole
from app.models.restaurant import Restaurant, RestaurantTable, TableStatus
from app.models.menu import MenuCategory, MenuItem
from app.core.security import hash_password


RESTAURANTS = [
    {
        "name": "Italian Garden",
        "cuisine": "Italian",
        "city": "Colombo",
        "address": "42 Galle Road, Colombo 03",
        "avg_price": 4500,
        "rating": 4.6,
        "opening_time": "11:00",
        "closing_time": "23:00",
        "description": "Authentic Italian trattoria with wood-fired pizza.",
        "menu": {
            "Starters": [("Bruschetta", 850), ("Caprese Salad", 1200)],
            "Pasta": [("Spaghetti Carbonara", 2100), ("Chicken Pasta", 2000), ("Penne Arrabbiata", 1800)],
            "Pizza": [("Margherita", 1900), ("Pepperoni", 2300)],
            "Desserts": [("Tiramisu", 900)],
            "Drinks": [("Coke", 400), ("Sparkling Water", 350)],
        },
    },
    {
        "name": "Golden Dragon",
        "cuisine": "Chinese",
        "city": "Colombo",
        "address": "88 Duplication Road, Colombo 04",
        "avg_price": 3800, "rating": 4.3,
        "opening_time": "11:30", "closing_time": "22:30",
        "description": "Classic Chinese restaurant with Szechuan specials.",
        "menu": {
            "Starters": [("Spring Rolls", 700), ("Hot & Sour Soup", 650)],
            "Mains": [("Kung Pao Chicken", 1900), ("Sweet & Sour Pork", 2000), ("Fried Rice", 1200)],
            "Drinks": [("Jasmine Tea", 350), ("Coke", 400)],
        },
    },
    {
        "name": "Sakura Sushi",
        "cuisine": "Japanese",
        "city": "Colombo",
        "address": "12 Marine Drive, Colombo 03",
        "avg_price": 6500, "rating": 4.8,
        "opening_time": "12:00", "closing_time": "23:00",
        "description": "Fresh sushi and sashimi crafted by Japanese chefs.",
        "menu": {
            "Sushi": [("Salmon Nigiri", 1500), ("Tuna Roll", 2200), ("California Roll", 1800)],
            "Hot Dishes": [("Chicken Teriyaki", 2400), ("Miso Soup", 600)],
            "Drinks": [("Green Tea", 300), ("Sake", 1800)],
        },
    },
    {
        "name": "Spice of India",
        "cuisine": "Indian",
        "city": "Colombo",
        "address": "35 Park Street, Colombo 02",
        "avg_price": 2800, "rating": 4.4,
        "opening_time": "10:30", "closing_time": "22:00",
        "description": "North and South Indian favourites.",
        "menu": {
            "Starters": [("Samosa", 500), ("Chicken Tikka", 1500)],
            "Curries": [("Butter Chicken", 1800), ("Paneer Masala", 1600)],
            "Breads": [("Naan", 300), ("Roti", 250)],
            "Drinks": [("Mango Lassi", 600)],
        },
    },
    {
        "name": "Ceylon Curry House",
        "cuisine": "Sri Lankan",
        "city": "Colombo",
        "address": "7 Hospital Street, Colombo 01",
        "avg_price": 1500, "rating": 4.5,
        "opening_time": "07:00", "closing_time": "22:00",
        "description": "Traditional rice and curry, hoppers, and kottu.",
        "menu": {
            "Rice & Curry": [("Chicken Curry", 800), ("Fish Curry", 900), ("Veg Curry", 600)],
            "Short Eats": [("Egg Hopper", 150), ("Plain Hopper", 80)],
            "Kottu": [("Chicken Kottu", 900), ("Cheese Kottu", 1100)],
            "Drinks": [("King Coconut", 200), ("Tea", 100)],
        },
    },
    {
        "name": "Taco Loco",
        "cuisine": "Mexican",
        "city": "Colombo",
        "address": "23 Independence Ave, Colombo 07",
        "avg_price": 3500, "rating": 4.2,
        "opening_time": "12:00", "closing_time": "23:00",
        "description": "Vibrant Mexican street food.",
        "menu": {
            "Tacos": [("Beef Taco", 900), ("Chicken Taco", 850), ("Veg Taco", 700)],
            "Burritos": [("Chicken Burrito", 1600), ("Bean Burrito", 1300)],
            "Drinks": [("Margarita", 1900), ("Horchata", 600)],
        },
    },
    {
        "name": "Bangkok Street",
        "cuisine": "Thai",
        "city": "Colombo",
        "address": "5 Flower Road, Colombo 07",
        "avg_price": 3200, "rating": 4.4,
        "opening_time": "11:00", "closing_time": "22:30",
        "description": "Thai street food classics.",
        "menu": {
            "Starters": [("Chicken Satay", 900), ("Tom Yum Soup", 1100)],
            "Mains": [("Pad Thai", 1600), ("Green Curry", 1800)],
            "Drinks": [("Thai Iced Tea", 500)],
        },
    },
    {
        "name": "Burger Republic",
        "cuisine": "American",
        "city": "Colombo",
        "address": "19 Union Place, Colombo 02",
        "avg_price": 2500, "rating": 4.1,
        "opening_time": "11:00", "closing_time": "23:30",
        "description": "Gourmet burgers and fries.",
        "menu": {
            "Burgers": [("Classic Cheeseburger", 1500), ("Bacon Burger", 1800), ("Veggie Burger", 1300)],
            "Sides": [("Fries", 500), ("Onion Rings", 600)],
            "Drinks": [("Milkshake", 800), ("Coke", 400)],
        },
    },
    {
        "name": "La Piazza",
        "cuisine": "Italian",
        "city": "Colombo",
        "address": "68 Rosmead Place, Colombo 07",
        "avg_price": 7000, "rating": 4.7,
        "opening_time": "18:00", "closing_time": "23:30",
        "description": "Fine dining Italian.",
        "menu": {
            "Antipasti": [("Prosciutto Plate", 2200), ("Burrata", 2600)],
            "Pasta": [("Truffle Tagliatelle", 3800), ("Seafood Linguine", 4200)],
            "Mains": [("Osso Buco", 5500)],
            "Desserts": [("Panna Cotta", 1200)],
            "Drinks": [("Red Wine", 2500)],
        },
    },
    {
        "name": "Nihon Ramen",
        "cuisine": "Japanese",
        "city": "Colombo",
        "address": "3 Bagatale Road, Colombo 03",
        "avg_price": 2200, "rating": 4.5,
        "opening_time": "11:00", "closing_time": "22:00",
        "description": "Ramen bar with tonkotsu and miso broths.",
        "menu": {
            "Ramen": [("Tonkotsu Ramen", 1600), ("Miso Ramen", 1500), ("Veg Ramen", 1300)],
            "Sides": [("Gyoza", 800)],
            "Drinks": [("Green Tea", 300)],
        },
    },
    {
        "name": "Delhi Darbar",
        "cuisine": "Indian",
        "city": "Colombo",
        "address": "12 Bambalapitiya, Colombo 04",
        "avg_price": 2400, "rating": 4.3,
        "opening_time": "11:00", "closing_time": "23:00",
        "description": "Mughlai and tandoori cuisine.",
        "menu": {
            "Tandoor": [("Tandoori Chicken", 2200), ("Seekh Kebab", 1800)],
            "Curries": [("Rogan Josh", 1900), ("Dal Makhani", 1400)],
            "Breads": [("Garlic Naan", 400)],
        },
    },
    {
        "name": "Colombo Cafe",
        "cuisine": "Sri Lankan",
        "city": "Colombo",
        "address": "1 Fort, Colombo 01",
        "avg_price": 1200, "rating": 4.0,
        "opening_time": "07:30", "closing_time": "21:00",
        "description": "Casual cafe with local favourites.",
        "menu": {
            "Breakfast": [("String Hoppers", 400), ("Milk Rice", 300)],
            "Lunch": [("Rice & Curry", 700), ("Lamprais", 1200)],
            "Drinks": [("Iced Coffee", 500)],
        },
    },
]


TABLES = [
    ("T1", 2), ("T2", 2), ("T3", 4), ("T4", 4), ("T5", 6), ("T6", 8),
]


def seed():
    db = SessionLocal()
    try:
        # Users
        if not db.scalar(select(User).where(User.email == "demo@example.com")):
            db.add(User(
                name="Demo User", email="demo@example.com",
                password_hash=hash_password("demo1234"),
                role=UserRole.CUSTOMER,
            ))
        if not db.scalar(select(User).where(User.email == "admin@example.com")):
            db.add(User(
                name="Admin", email="admin@example.com",
                password_hash=hash_password("admin1234"),
                role=UserRole.ADMIN,
            ))
        db.commit()

        # Restaurants
        for rdata in RESTAURANTS:
            existing = db.scalar(select(Restaurant).where(Restaurant.name == rdata["name"]))
            if existing:
                continue
            r = Restaurant(
                name=rdata["name"], description=rdata["description"],
                address=rdata["address"], city=rdata["city"],
                cuisine=rdata["cuisine"], avg_price=rdata["avg_price"],
                rating=rdata["rating"], opening_time=rdata["opening_time"],
                closing_time=rdata["closing_time"],
                phone="+94 11 234 5678",
            )
            db.add(r)
            db.flush()

            for tname, cap in TABLES:
                db.add(RestaurantTable(
                    restaurant_id=r.id, table_number=tname, capacity=cap,
                    status=TableStatus.AVAILABLE,
                ))

            for cat_name, items in rdata["menu"].items():
                cat = MenuCategory(restaurant_id=r.id, name=cat_name)
                db.add(cat)
                db.flush()
                for item_name, price in items:
                    db.add(MenuItem(
                        category_id=cat.id, name=item_name,
                        description=f"{item_name} — house favourite",
                        price=price, available=True,
                    ))
        db.commit()
        print("Seed complete.")
    finally:
        db.close()


if __name__ == "__main__":
    seed()