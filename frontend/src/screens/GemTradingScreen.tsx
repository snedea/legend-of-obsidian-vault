import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';

export function GemTradingScreen() {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();
  const [gems, setGems] = useState(0);

  const load = useCallback(async () => {
    const inn = await api.getInnStatus();
    setGems(inn.gems);
  }, []);

  useEffect(() => { load(); }, [load]);

  const trade = async (stat: string) => {
    try {
      const result = await api.gemTrade(stat);
      notify(result.message);
      if (result.success) {
        setGems(result.gems);
        await refreshPlayer();
        nav('/town/inn/bar');
      }
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Trade failed');
    }
  };

  useKeyboard({
    D: () => trade('defense'),
    S: () => trade('strength'),
    H: () => trade('hitpoints'),
    Q: () => nav('/town/inn/bar'),
    ESCAPE: () => nav('/town/inn/bar'),
  }, [nav]);

  return (
    <Terminal title="GEM TRADING" subtitle="Power Exchange">
      <Separator />
      <div className="c-cyan" style={{ padding: '8px 0' }}>
        You have {gems} gems. Trade 2 gems for 1 stat point:
      </div>
      <Separator />
      <MenuOption shortcut="D" label="Defense (Vitality)" onClick={() => trade('defense')} />
      <MenuOption shortcut="S" label="Strength" onClick={() => trade('strength')} />
      <MenuOption shortcut="H" label="Hit Points" onClick={() => trade('hitpoints')} />
      <Separator />
      <MenuOption shortcut="Q" label="Cancel" onClick={() => nav('/town/inn/bar')} />
    </Terminal>
  );
}
