from fastapi import FastAPI
<<<<<<< HEAD
from fastapi.middleware.cors import CORSMiddleware
=======
from pydantic import BaseModel
>>>>>>> main

from card import Card
from enemy import Enemy
from player import Player

class PlayCardRequest(BaseModel):
    card_index: int

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

player = Player("Survivor", 100, 5)
infected = Enemy("Infected", 100, 6)
hand = [
    Card("Handgun", 8, 2),
    Card("Combat Knife", 4, 1),
    Card("Shotgun", 15, 3)
]

def get_game_state():
    return {
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
def get_game():
    return get_game_state()

@app.post("/api/game/play-card")
def play_card(request: PlayCardRequest):
    card = hand[request.card_index]

    if player.energy >= card.cost:
        player.energy -= card.cost
        infected.health -= card.damage

        return {
            "success": True,
            "message": f"You played {card.name}!",
            "game": get_game_state()
        }
    else:
        "success": False,
        "message": "Not enough energy to play the card.",
        "game": get_game_state()

