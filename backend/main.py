from fastapi import FastAPI
from pydantic import BaseModel

from card import Card
from enemy import Enemy
from player import Player
from database import Base, engine, SessionLocal
from models import CardModel, EnemyModel

Base.metadata.create_all(bind=engine)

class PlayCardRequest(BaseModel):
    card_index: int

app = FastAPI()

player = Player("Survivor", 100, 5)

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

def load_enemies_by_type(enemy_type):
    db = SessionLocal()

    try:
        enemy_records = db.query(EnemyModel).filter(EnemyModel.enemy_type == enemy_type).all()

        return [
            Enemy(
                enemy.name,
                enemy.health,
                enemy.attack
            )
            for enemy in enemy_records
        ]
    finally:
        db.close()

regular_enemies = load_enemies_by_type("regular")
elite_enemies = load_enemies_by_type("elite")
boss_enemies = load_enemies_by_type("boss")

encounter_types = [
    "regular",
    "regular",
    "elite",
    "regular",
    "elite",
    "boss"
]

current_encounter = 0

def get_enemy_for_encounter():
    encounter_type = encounter_types[current_encounter]

    if encounter_type == "regular":
        source_enemy = regular_enemies[0]
    elif encounter_type == "elite":
        source_enemy = elite_enemies[0]
    else:
        source_enemy = boss_enemies[0]

    return Enemy(
        source_enemy.name,
        source_enemy.health,
        source_enemy.attack
    )

current_enemy = get_enemy_for_encounter()

def get_game_status():
    if current_enemy.health <= 0:
        return "won"
    if player.health <= 0:
        return "lost"
    return "playing"

def get_game_state():
    return {
        "status": get_game_status(),
        "encounter": {
            "number": current_encounter + 1,
            "total": len(encounter_types),
            "type": encounter_types[current_encounter]
        },
        "player": {
            "name": player.name,
            "health": player.health,
            "energy": player.energy
        },
        "enemy": {
            "name": current_enemy.name,
            "health": current_enemy.health,
            "attack": current_enemy.attack
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
    if get_game_status() != "playing":
        return {
            "success": False,
            "message": "The game is over. Please start a new game.",
            "game": get_game_state()
        }

    card = hand[request.card_index]

    if player.energy >= card.cost:
        player.energy -= card.cost
        current_enemy.health -= card.damage

        if current_enemy.health <= 0:
            return {
                "success": True,
                "message": f"You played {card.name} and won the battle!",
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
    if get_game_status() != "playing":
        return {
            "message": "The game is over. Please start a new game.",
            "game": get_game_state()
        }

    player.health -= current_enemy.attack

    if player.health <= 0:
        return {
            "message": f"{current_enemy.name} attacked you for {current_enemy.attack} damage! You lost the battle!",
            "game": get_game_state()
        }

    player.energy = 5
    

    return {
        "message": f"{current_enemy.name} attacked you for {current_enemy.attack} damage!",
        "game": get_game_state()
    }

@app.post("/api/game/next-encounter")
def next_encounter():
    global current_encounter, current_enemy

    if get_game_status() != "won":
        return {
            "success": False,
            "message": "You must defeat the current enemy first.",
            "game": get_game_state()
        }

    current_encounter += 1

    if current_encounter >= len(encounter_types):
        return {
            "success": True,
            "message": "You completed the run!",
            "game": get_game_state()
        }

    current_enemy = get_enemy_for_encounter()
    player.energy = 5

    return {
        "success": True,
        "message": f"Next encounter: {current_enemy.name}",
        "game": get_game_state()
    }