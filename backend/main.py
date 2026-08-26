from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from card import Card
from enemy import Enemy
from player import Player

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
handgun = Card("Handgun", 8, 5)

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
        "card": {
            "name": handgun.name,
            "damage": handgun.damage,
            "cost": handgun.cost
        }
    }

@app.get("/api/game")
def  get_game():
    return get_game_state()

@app.post("/api/game/play-card")
def play_card():
    if player.energy >= handgun.cost:
        player.energy -= handgun.cost
        infected.health -= handgun.damage

        return {
            "success": True,
            "message": f"You played {handgun.name}!",
            "game": get_game_state()
        }
    else:
        return {
            "success": False,
            "message": "Not enough energy to play the card.",
            "game": get_game_state()
        }

