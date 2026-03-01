import { useGame } from '../context/GameContext';

export function StatusBar() {
  const { player } = useGame();
  if (!player) return null;

  return (
    <div className="status-bar">
      <span>
        <span className="stat-label">HP:</span>{' '}
        <span className="stat-value">{player.hitpoints}/{player.max_hitpoints}</span>
      </span>
      <span>
        <span className="stat-label">Lvl:</span>{' '}
        <span className="stat-value">{player.level}</span>
      </span>
      <span>
        <span className="stat-label">Gold:</span>{' '}
        <span className="stat-gold">{player.gold.toLocaleString()}</span>
      </span>
      <span>
        <span className="stat-label">Gems:</span>{' '}
        <span className="stat-value">{player.gems}</span>
      </span>
      <span>
        <span className="stat-label">Fights:</span>{' '}
        <span className="stat-value">{player.forest_fights}</span>
      </span>
    </div>
  );
}
