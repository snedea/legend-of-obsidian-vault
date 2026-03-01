import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import type { Character } from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function PlayerSelect() {
  const nav = useNavigate();
  const { setPlayer, notify } = useGame();
  const [players, setPlayers] = useState<Character[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.listCharacters().then((res) => {
      setPlayers(res.characters);
      setLoading(false);
    }).catch(() => setLoading(false));
  }, []);

  const select = async (name: string) => {
    try {
      const p = await api.selectCharacter(name);
      setPlayer(p);
      notify(`Welcome back, ${p.name}!`);
      nav('/town');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Selection failed');
    }
  };

  // Number keys 1-9 select characters
  const keyMap: Record<string, () => void> = {
    ESCAPE: () => nav('/'),
  };
  players.slice(0, 9).forEach((p, i) => {
    keyMap[String(i + 1)] = () => select(p.name);
  });

  useKeyboard(keyMap, [players, nav]);

  return (
    <Terminal title="SELECT CHARACTER" subtitle="Choose Your Hero">
      <SceneCanvas scene="playerSelect" />
      <Separator />
      {loading ? (
        <div className="c-muted">Loading characters...</div>
      ) : players.length === 0 ? (
        <div className="c-muted">No characters found. Create one first!</div>
      ) : (
        <div style={{ padding: '8px 0' }}>
          {players.map((p, i) => (
            <button
              key={p.name}
              className="menu-option"
              onClick={() => select(p.name)}
            >
              <span className="c-gold">({i + 1})</span>{' '}
              <span className="c-white bold">{p.name}</span>{' '}
              <span className="c-muted">
                Level {p.level} {p.class_type === 'K' ? 'Death Knight' : p.class_type === 'P' ? 'Mystical' : 'Thieving'}
                {' '}{p.alive ? '' : '[DEAD]'}
              </span>
            </button>
          ))}
        </div>
      )}
      <Separator />
      <div className="c-muted">ESC to go back</div>
    </Terminal>
  );
}
