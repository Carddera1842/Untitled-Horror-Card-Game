from fastapi import FastAPI

app = FastAPI()

@app.get("/api/game")
def  get_game():
    return {
        "player": {
            "name": "Survivor",
            "health": 100,
            "energy": 50
        },
        "enemy": {
            "name": "Infected",
            "health": 100,
            "attack": 6
        }
    }

