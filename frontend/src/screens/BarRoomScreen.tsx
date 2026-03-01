import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';

export function BarRoomScreen() {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();
  const [inn, setInn] = useState<api.InnStatus | null>(null);

  const load = useCallback(async () => {
    setInn(await api.getInnStatus());
  }, []);

  useEffect(() => { load(); }, [load]);

  const rentRoom = async () => {
    try {
      const result = await api.rentRoom();
      notify(result.message);
      if (result.success) {
        await refreshPlayer();
        await load();
      }
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Error renting room');
    }
  };

  useKeyboard({
    G: () => inn?.can_access_bar && inn.gems >= 2 && nav('/town/inn/gems'),
    R: () => inn?.can_access_bar && rentRoom(),
    B: () => inn?.can_access_bar && nav('/town/inn/bribe'),
    N: () => inn?.can_access_bar && nav('/town/inn/name-change'),
    V: () => nav('/town/inn/violet'),
    Q: () => nav('/town/inn'),
    ESCAPE: () => nav('/town/inn'),
  }, [inn, nav]);

  if (!inn) return <Terminal title="THE BAR ROOM"><div className="c-muted">Loading...</div></Terminal>;

  if (!inn.can_access_bar) {
    return (
      <Terminal title="THE BAR ROOM" subtitle="Drinks & Deals">
        <Separator />
        <div style={{ padding: '8px 0' }}>
          <div className="c-muted">The bartender glances at you dismissively.</div>
          <div className="c-muted">"Get out of here, kid. Come back when you've</div>
          <div className="c-muted">proven yourself in the forest."</div>
        </div>
        <Separator />
        <MenuOption shortcut="Q" label="Return to inn" onClick={() => nav('/town/inn')} />
      </Terminal>
    );
  }

  return (
    <Terminal title="THE BAR ROOM" subtitle="Drinks & Deals">
      <Separator />
      <div style={{ padding: '8px 0' }}>
        <div className="c-yellow">The gruff bartender eyes you carefully.</div>
        <div className="c-yellow">"What'll it be, warrior?"</div>
      </div>
      <Separator />
      <MenuOption shortcut="G" label={`Gems for stats (2 gems) [Have: ${inn.gems}]`} onClick={() => nav('/town/inn/gems')} />
      <MenuOption shortcut="R" label={`Room for the night (${inn.room_cost} gold)${inn.inn_room ? ' [RENTED]' : ''}`} onClick={rentRoom} />
      <MenuOption shortcut="B" label={`Bribe me to kill sleeping players (${inn.bribe_cost} gold)`} onClick={() => nav('/town/inn/bribe')} />
      <MenuOption shortcut="N" label="Name change" onClick={() => nav('/town/inn/name-change')} />
      <MenuOption shortcut="V" label="Visit Violet's room" onClick={() => nav('/town/inn/violet')} />
      <Separator />
      <MenuOption shortcut="Q" label="Return to inn" onClick={() => nav('/town/inn')} />
    </Terminal>
  );
}
