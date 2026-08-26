import {useEffect, useState} from 'react'

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
}

function App() {
  const [game, setGame] = useState<GameState | null>(null)

  useEffect(() => {
    fetch('http://localhost:8000/api/game')
      .then((response) => response.json())
      .then((data) => setGame(data))
      .catch((error) => console.error('Error fetching game state:', error))
  }, [])
  
  if (!game) {
    return <p>Loading game state...</p>
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
    </main>
  )
}

export default App