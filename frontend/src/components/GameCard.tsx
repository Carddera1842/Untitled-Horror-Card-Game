import './GameCard.css'

interface GameCardProps {
  name: string
  damage: number
  cost: number
  canPlay: boolean
  onPlay: () => void
}

function GameCard({ name, damage, cost, canPlay, onPlay }: GameCardProps) {
  return (
    <div className="game-card">
      <h3>{name}</h3>

      <div className="card-body">
        <p>Damage: {damage}</p>
      </div>
        
      <div className="card-cost">
        <p>Cost: {cost}</p>
      </div>
      
      <button 
        onClick={onPlay}
        disabled={!canPlay}
      >
        {canPlay ? 'Play Card' : 'Not Enough Energy'}
      </button>
    </div>
  )
}

export default GameCard