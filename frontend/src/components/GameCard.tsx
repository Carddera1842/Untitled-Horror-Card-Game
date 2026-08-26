interface GameCardProps {
  name: string
  damage: number
  cost: number
  onPlay: () => void
}

function GameCard({ name, damage, cost, onPlay }: GameCardProps) {
  return (
    <div className="game-card">
      <h3>{name}</h3>

      <div className="card-body">
        <p>Damage: {damage}</p>
      </div>
        
      <div className="card-cost">
        <p>Cost: {cost}</p>
      </div>
      
      <button onClick={onPlay}>Play Card</button>
    </div>
  )
}

export default GameCard