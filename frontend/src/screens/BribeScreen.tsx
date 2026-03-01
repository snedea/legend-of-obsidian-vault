import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';

export function BribeScreen() {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();
  const [bribe, setBribe] = useState<api.BribeStatus | null>(null);

  const load = useCallback(async () => {
    setBribe(await api.getBribeStatus());
  }, []);

  useEffect(() => { load(); }, [load]);

  const kill = async (targetName: string) => {
    try {
      const result = await api.bribeKill(targetName);
      notify(result.message);
      if (result.exp_gained > 0) {
        notify(`You gain ${result.exp_gained} experience and ${result.gold_gained} gold!`);
      }
      await refreshPlayer();
      nav('/town/inn/bar');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Bribe failed');
    }
  };

  const keyMap: Record<string, () => void> = {
    Q: () => nav('/town/inn/bar'),
    ESCAPE: () => nav('/town/inn/bar'),
  };
  if (bribe) {
    bribe.targets.forEach((t, i) => {
      keyMap[String(i + 1)] = () => kill(t.name);
    });
  }

  useKeyboard(keyMap, [bribe, nav]);

  if (!bribe) return <Terminal title="SLEEPING TARGETS"><div className="c-muted">Loading...</div></Terminal>;

  return (
    <Terminal title="SLEEPING TARGETS" subtitle="Dark Dealings">
      <Separator />
      <div className="c-red">Bribe cost: {bribe.cost.toLocaleString()} gold</div>
      <div className="c-muted">Your gold: {bribe.gold.toLocaleString()}</div>
      <Separator />
      {bribe.targets.length === 0 ? (
        <div className="c-muted" style={{ padding: '8px 0' }}>
          No one is sleeping at the inn tonight.
        </div>
      ) : (
        <div style={{ padding: '4px 0' }}>
          <div className="c-yellow">Choose your target:</div>
          {bribe.targets.map((t, i) => (
            <MenuOption
              key={t.name}
              shortcut={String(i + 1)}
              label={`${t.name} - Level ${t.level}`}
              onClick={() => kill(t.name)}
            />
          ))}
        </div>
      )}
      <Separator />
      <MenuOption shortcut="Q" label="Cancel" onClick={() => nav('/town/inn/bar')} />
    </Terminal>
  );
}
