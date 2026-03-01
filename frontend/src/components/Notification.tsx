import { useGame } from '../context/GameContext';

export function Notification() {
  const { notification } = useGame();
  if (!notification) return null;
  return <div className="notification">{notification}</div>;
}
