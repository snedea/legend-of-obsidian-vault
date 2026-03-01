import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function XenonScreen() {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();
  const [status, setStatus] = useState<api.XenonStatus | null>(null);

  const load = useCallback(async () => {
    setStatus(await api.getXenonStatus());
  }, []);

  useEffect(() => { load(); }, [load]);

  const doAction = async (action: string, amount?: number) => {
    try {
      const r = await api.xenonTransaction(action, amount);
      notify(r.message);
      setStatus({ stored_gold: r.stored_gold, stored_gems: r.stored_gems,
        gold: r.gold, gems: r.gems, has_horse: status?.has_horse ?? false,
        horse_name: status?.horse_name ?? '', children: status?.children ?? 0 });
      await refreshPlayer();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Error');
    }
  };

  useKeyboard({
    '1': () => status && doAction('store_gold', status.gold),
    '2': () => status && doAction('retrieve_gold', status.stored_gold),
    '3': () => status && doAction('store_gems', status.gems),
    '4': () => status && doAction('retrieve_gems', status.stored_gems),
    Q: () => nav('/places'),
    ESCAPE: () => nav('/places'),
  }, [status, nav]);

  if (!status) return <Terminal title="XENON'S STORAGE"><div className="c-muted">Loading...</div></Terminal>;

  return (
    <Terminal title="XENON'S STORAGE" subtitle="Safe Keeping">
      <SceneCanvas scene="xenon" />
      <Separator />
      <div className="two-columns">
        <div>
          <div className="c-muted">On Hand:</div>
          <div>Gold: <span className="c-gold">{status.gold.toLocaleString()}</span></div>
          <div>Gems: {status.gems}</div>
        </div>
        <div>
          <div className="c-muted">In Storage:</div>
          <div>Gold: <span className="c-gold">{status.stored_gold.toLocaleString()}</span></div>
          <div>Gems: {status.stored_gems}</div>
        </div>
      </div>
      <Separator />
      <MenuOption shortcut="1" label="Store all gold" onClick={() => doAction('store_gold', status.gold)} />
      <MenuOption shortcut="2" label="Retrieve all gold" onClick={() => doAction('retrieve_gold', status.stored_gold)} />
      <MenuOption shortcut="3" label="Store all gems" onClick={() => doAction('store_gems', status.gems)} />
      <MenuOption shortcut="4" label="Retrieve all gems" onClick={() => doAction('retrieve_gems', status.stored_gems)} />
      <Separator />
      <MenuOption shortcut="Q" label="Leave" onClick={() => nav('/places')} />
    </Terminal>
  );
}
