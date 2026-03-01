import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function HealerScreen() {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();
  const [info, setInfo] = useState<api.HealerInfo | null>(null);

  const load = useCallback(async () => {
    setInfo(await api.getHealer());
  }, []);

  useEffect(() => { load(); }, [load]);

  const heal = async (type: string, amount?: number) => {
    try {
      const r = await api.healerHeal(type, amount);
      notify(r.message);
      await refreshPlayer();
      await load();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Heal failed');
    }
  };

  useKeyboard({
    F: () => heal('full'),
    P: () => info ? heal('partial', info.hp_missing) : undefined,
    Q: () => nav(-1 as never),
    ESCAPE: () => nav(-1 as never),
  }, [info]);

  if (!info) return <Terminal title="HEALER'S HUT"><div className="c-muted">Loading...</div></Terminal>;

  return (
    <Terminal title="HEALER'S HUT" subtitle="Rest and Recovery">
      <SceneCanvas scene="healer" />
      <Separator />
      <div className="c-white">HP: {info.current_hp} / {info.max_hp} ({info.hp_missing} missing)</div>
      <div className="c-white">Gold: <span className="c-gold">{info.current_gold.toLocaleString()}</span></div>
      <Separator />
      <MenuOption
        shortcut="F"
        label={`Full Heal (${info.full_heal_cost} gold)`}
        onClick={() => heal('full')}
        disabled={info.hp_missing === 0 || info.current_gold < info.full_heal_cost}
      />
      <MenuOption
        shortcut="P"
        label={`Partial Heal (1 gold per HP, ${info.hp_missing} HP needed)`}
        onClick={() => heal('partial', info.hp_missing)}
        disabled={info.hp_missing === 0 || info.current_gold <= 0}
      />
      <MenuOption shortcut="Q" label="Return" onClick={() => nav(-1 as never)} />
    </Terminal>
  );
}
