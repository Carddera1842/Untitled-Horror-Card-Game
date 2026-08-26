from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

