import random
from datetime import datetime, timedelta
from uuid import uuid4
from app import SessionLocal, engine, Base, User, Place, Review

# 1. RESET THE DATABASE (Optional: Comment out if you want to keep existing data)
print("⚡ DROPPING OLD TABLES...")
Base.metadata.drop_all(bind=engine)
print("⚡ CREATING NEW TABLES...")
Base.metadata.create_all(bind=engine)

db = SessionLocal()

# 2. CREATE USERS
print("⚡ SEEDING USERS...")
admins = [
    User(id=str(uuid4()), email="admin@critique.com", name="System Admin", role="admin", password="admin", university="Tech U"),
    User(id=str(uuid4()), email="gordon@critique.com", name="Gordon R.", role="admin", password="lambsauce", university="Culinary Academy"),
]

students = [
    User(id=str(uuid4()), email=f"student{i}@uni.edu", name=n, role="student", password="123", university="State College")
    for i, n in enumerate(["Alice Eater", "Bob Burger", "Charlie Chew", "Diana Drink", "Evan Eats"])
]

all_users = admins + students
db.add_all(all_users)
db.commit()

# 3. CREATE PLACES (With Real Images)
print("⚡ SEEDING PLACES...")
places_data = [
    {
        "name": "The Midnight Oil",
        "type": "Cafe",
        "address": "Library Basement, Room 101",
        "photo": "https://images.unsplash.com/photo-1554118811-1e0d58224f24?q=80&w=2047&auto=format&fit=crop",
        "tags": "coffee, study, quiet, late-night, wifi",
        "description": "The only place open during finals week. Espresso is strong, lighting is dim."
    },
    {
        "name": "Burger Barn",
        "type": "Fast Food",
        "address": "Student Center, Food Court",
        "photo": "https://images.unsplash.com/photo-1568901346375-23c9450c58cd?q=80&w=1899&auto=format&fit=crop",
        "tags": "burgers, cheap, greasy, fast, lunch",
        "description": "Greasy perfection. The fries are soggy but in a good way."
    },
    {
        "name": "Green Roots",
        "type": "Restaurant",
        "address": "North Campus, near Gym",
        "photo": "https://images.unsplash.com/photo-1512621776951-a57141f2eefd?q=80&w=2070&auto=format&fit=crop",
        "tags": "vegan, healthy, salad, expensive, organic",
        "description": "Actually good salad bowls. Your wallet will weep, but your body will thank you."
    },
    {
        "name": "Taco Tuesday Truck",
        "type": "Food Truck",
        "address": "Parking Lot B",
        "photo": "https://images.unsplash.com/photo-1565299585323-38d6b0865b47?q=80&w=1980&auto=format&fit=crop",
        "tags": "tacos, mexican, spicy, outdoor, cash-only",
        "description": "Only here on Tuesdays and Thursdays. The carnitas are legendary."
    },
    {
        "name": "Sugar Rush",
        "type": "Desserts",
        "address": "Main Street",
        "photo": "https://images.unsplash.com/photo-1551024601-bec78aea704b?q=80&w=1964&auto=format&fit=crop",
        "tags": "donuts, sweet, dessert, bakery, breakfast",
        "description": "Gourmet donuts. Try the maple bacon glaze."
    },
    {
        "name": "Pasta Palace",
        "type": "Restaurant",
        "address": "Downtown",
        "photo": "https://images.unsplash.com/photo-1473093295043-cdd812d0e601?q=80&w=2070&auto=format&fit=crop",
        "tags": "italian, pasta, dinner, date-night, wine",
        "description": "Good for dates. Portions are huge."
    },
    {
        "name": "Brew & Bites",
        "type": "Beverages",
        "address": "Engineering Block",
        "photo": "https://images.unsplash.com/photo-1497935586351-b67a49e012bf?q=80&w=2071&auto=format&fit=crop",
        "tags": "coffee, tea, snacks, grab-and-go",
        "description": "Quick caffeine fix between lectures."
    },
    {
        "name": "The Spicy Spoon",
        "type": "Restaurant",
        "address": "West Wing",
        "photo": "https://images.unsplash.com/photo-1585937421612-70a008356f36?q=80&w=2070&auto=format&fit=crop",
        "tags": "curry, spicy, indian, hot, buffet",
        "description": "Authentic spice levels. Not for the faint of heart."
    }
]

places_objs = []
for p in places_data:
    new_p = Place(
        name=p["name"],
        type=p["type"],
        address=p["address"],
        photo=p["photo"],
        tags=p["tags"],
        description=p["description"],
        creator_id=admins[0].id
    )
    db.add(new_p)
    places_objs.append(new_p)
db.commit()

# 4. CREATE REVIEWS
print("⚡ SEEDING REVIEWS...")
comments = [
    "Absolutely amazing!", "Terrible service.", "It was okay, nothing special.",
    "Best food on campus.", "Too expensive for what you get.", "Will come back again!",
    "The wifi was broken.", "Delicious!", "Gross.", "Highly recommend the special."
]

for _ in range(30):
    u = random.choice(all_users)
    p = random.choice(places_objs)
    r = Review(
        place_id=p.id,
        user_id=u.id,
        rating=random.randint(1, 5),
        text=random.choice(comments) if random.random() > 0.2 else "", # 20% chance of no text (Star only)
        created_at=int((datetime.utcnow() - timedelta(days=random.randint(0, 10))).timestamp() * 1000)
    )
    db.add(r)
    # Update user stats
    u.total_reviews = (u.total_reviews or 0) + 1

db.commit()
print("⚡ DONE. DATABASE SEEDED.")
print(" -> Admin Login: admin@critique.com / admin")