from database import SessionLocal
from models import CardModel

db = SessionLocal()

cards = [
    CardModel(
        name="Handgun",
        description="A reliable handgun.",
        damage=8,
        cost=2
    ),
    CardModel(
        name="Combat Knife",
        description="A close-range survival weapon.",
        damage=4,
        cost=1
    ),
    CardModel(
        name="Shotgun",
        description="Powerful, but expensive to use.",
        damage=15,
        cost=3
    )
]

db.add_all(cards)
db.commit()

db.close()

print("Cards added successfully!")