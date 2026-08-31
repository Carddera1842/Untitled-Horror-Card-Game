import {useEffect, useState} from 'react'
import GameCard from './components/GameCard'

interface GameState {
  status: "playing" | "won" | "lost"
  encounter: {
    number: number
    total: number
    type: string
  }
  player: {
    name: string
    health: number
    energy: number
  }
  enemy: {
    name: string
    health: number
    attack: number
  }
  hand: {
    name: string
    damage: number
    cost: number
  }[]
}

function App() {
  const [game, setGame] = useState<GameState | null>(null)
  const [message, setMessage] = useState("")

  useEffect(() => {
    fetch('http://localhost:8000/api/game')
      .then((response) => response.json())
      .then((data) => setGame(data))
      .catch((error) => console.error('Error fetching game state:', error))
  }, [])

  const playCard = (cardIndex: number) => {
    fetch('http://localhost:8000/api/game/play-card', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ card_index: cardIndex }),
      })
      .then((response) => response.json())
      .then((data) => {
        setGame(data.game)
        setMessage(data.message)
      })
      .catch((error) => console.error('Error playing card:', error))

  }

  const endTurn = () => {
    fetch('http://localhost:8000/api/game/end-turn', {
      method: 'POST',
    })
      .then((response) => response.json())
      .then((data) => {
        setGame(data.game)
        setMessage(data.message)
      })
      .catch((error) => console.error('Error ending turn:', error))
  }

  if (!game) {
    return <p>Loading game state...</p>
  }

  const nextEncounter = () => {
    fetch('http://localhost:8000/api/game/next-encounter', {
      method: 'POST',
    })
      .then((response) => response.json())
      .then((data) => {
        if (data.game) {
          setGame(data.game)
        }
        setMessage(data.message)
      })
      .catch((error) =>
        console.error("Error starting next encounter:", error)
    )
  }

  return (
    <main>
      <h1>Untitled Horror Card Game</h1>

      <section>
        <h2>{game.player.name}</h2>
        <p>Health: {game.player.health}</p>
        <p>Energy: {game.player.energy}</p>
      </section>

      <section>
        <h2>{game.enemy.name}</h2>
        <p>Health: {game.enemy.health}</p>
        <p>Attack: {game.enemy.attack}</p>
      </section>

      {message && <p>{message}</p>}

      {game.status === "won" && (
        <section>
          <h2>Victory! You defeated {game.enemy.name}!</h2>

          <button onClick={nextEncounter}>
            Next Encounter
          </button>
        </section>
        )}
      {game.status === "lost" && (<h2>Game Over! {game.enemy.name} has defeated you!</h2>)}

      <div className="hand">
        {game.hand.map((card, index) => (
          <GameCard
            key={index}
            name={card.name}
            damage={card.damage}
            cost={card.cost}
            canPlay={
              game.status === "playing" && game.player.energy >= card.cost
            }
            onPlay={() => playCard(index)}
          />
        ))}
      </div>

      <button 
        onClick={endTurn}
        disabled={game.status !== "playing"}
      >
        End Turn
      </button>

      <h2>
        Encounter {game.encounter.number} of {game.encounter.total}
      </h2>

      <p>
        type: {game.encounter.type}
      </p>
    </main>
  )
}

export default App