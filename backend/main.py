from fastapi import FastAPI
from pydantic import BaseModel

from card import Card
from enemy import Enemy
from player import Player

class PlayCardRequest(BaseModel):
    card_index: int

app = FastAPI()

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
def  get_game():
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
        return {
            "success": False,
            "message": "Not enough energy to play the card.",
            "game": get_game_state()
        }

@app.post("/api/game/end-turn")
def end_turn():
    player.energy = 5
    player.health -= infected.attack

    return {
        "message": f"{infected.name} attacked you for {infected.attack} damage!",
        "game": get_game_state()
    }