from fastapi import FastAPI
from pydantic import BaseModel

from card import Card
from enemy import Enemy
from player import Player
from database import Base, engine, SessionLocal
from models import CardModel

Base.metadata.create_all(bind=engine)

class PlayCardRequest(BaseModel):
    card_index: int

app = FastAPI()

player = Player("Survivor", 100, 5)
infected = Enemy("Infected", 100, 6)

def load_cards():
    db = SessionLocal()

    try:
        card_records = db.query(CardModel).all()

        return [
            Card(
                card.name,
                card.damage,
                card.cost
            )
            for card in card_records
        ]
    finally:
        db.close()

hand = load_cards()

def get_game_status():
    if infected.health <= 0:
        return "You win!"
    if player.health <= 0:
        return "You lose!"
    return "Game in progress."

def get_game_state():
    return {
        "status": get_game_status(),
        "player": {
            "name": player.name,
            "health": player.health,
            "energy": player.energy
        },
        "enemy": {
            "name": infected.name,
            "health": infected.health,
            "attack": infected.attack
        },
        "hand": [{
            "name": card.name,
            "damage": card.damage,
            "cost": card.cost
        }
        for card in hand
        ]
    }

@app.get("/api/game")
def  get_game():
    return get_game_state()

@app.post("/api/game/play-card")
def play_card(request: PlayCardRequest):
    if get_game_status() != "Game in progress.":
        return {
            "success": False,
            "message": "The game is over. Please start a new game.",
            "game": get_game_state()
        }

    card = hand[request.card_index]

    if player.energy >= card.cost:
        player.energy -= card.cost
        infected.health -= card.damage

        if player.health <= 0:
            return {
                "success": True,
                "message": f"You played {card.name} and lost the game!",
                "game": get_game_state()
            }

        return {
            "success": True,
            "message": f"You played {card.name}!",
            "game": get_game_state()
        }
    else:
        return {
            "success": False,
            "message": "Not enough energy to play the card.",
            "game": get_game_state()
        }

@app.post("/api/game/end-turn")
def end_turn():
    if get_game_status() != "Game in progress.":
        return {
            "message": "The game is over. Please start a new game.",
            "game": get_game_state()
        }

    player.health -= infected.attack

    if player.health <= 0:
        return {
            "message": f"{infected.name} attacked you for {infected.attack} damage! You lost the game!",
            "game": get_game_state()
        }

    player.energy = 5
    

    return {
        "message": f"{infected.name} attacked you for {infected.attack} damage!",
        "game": get_game_state()
    }

