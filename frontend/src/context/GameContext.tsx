import { createContext, useContext, useState, useCallback, type ReactNode } from 'react';
import type { Character, CombatState } from '../services/api';
import * as api from '../services/api';

interface GameContextValue {
  player: Character | null;
  combat: CombatState | null;
  notification: string | null;
  refreshPlayer: () => Promise<void>;
  setPlayer: (p: Character | null) => void;
  setCombat: (c: CombatState | null) => void;
  notify: (msg: string) => void;
}

const GameContext = createContext<GameContextValue | null>(null);

export function GameProvider({ children }: { children: ReactNode }) {
  const [player, setPlayer] = useState<Character | null>(null);
  const [combat, setCombat] = useState<CombatState | null>(null);
  const [notification, setNotification] = useState<string | null>(null);

  const refreshPlayer = useCallback(async () => {
    try {
      const p = await api.getCurrentCharacter();
      setPlayer(p);
    } catch {
      // No player selected
    }
  }, []);

  const notify = useCallback((msg: string) => {
    setNotification(msg);
    setTimeout(() => setNotification(null), 3000);
  }, []);

  return (
    <GameContext.Provider
      value={{ player, combat, notification, refreshPlayer, setPlayer, setCombat, notify }}
    >
      {children}
    </GameContext.Provider>
  );
}

export function useGame(): GameContextValue {
  const ctx = useContext(GameContext);
  if (!ctx) throw new Error('useGame must be within GameProvider');
  return ctx;
}
