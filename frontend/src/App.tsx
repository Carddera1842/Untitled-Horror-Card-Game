import {useEffect, useState} from 'react'
import GameCard from './components/GameCard'

interface GameState {
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
  card: {
    name: string
    damage: number
    cost: number
  }
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
  
  if (!game) {
    return <p>Loading game state...</p>
  }

  const playCard = () => {
    fetch('http://localhost:8000/api/game/play-card', {
      method: 'POST'
      })
      .then((response) => response.json())
      .then((data) => {
        setGame(data.game)
        setMessage(data.message)
      })
      .catch((error) => console.error('Error playing card:', error))

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

        <GameCard
          name={game.card.name}
          damage={game.card.damage}
          cost={game.card.cost}
          onPlay={playCard}
        />
    </main>
  )
}

export default App