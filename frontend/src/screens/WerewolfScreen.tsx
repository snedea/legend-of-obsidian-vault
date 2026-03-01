import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';

export function WerewolfScreen() {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();
  const [status, setStatus] = useState<api.WerewolfStatus | null>(null);

  const load = useCallback(async () => {
    setStatus(await api.getWerewolfStatus());
  }, []);

  useEffect(() => { load(); }, [load]);

  const doAction = async (fn: () => Promise<api.WerewolfResult>) => {
    try {
      const r = await fn();
      notify(r.message);
      await refreshPlayer();
      await load();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Error');
    }
  };

  useKeyboard(
    status?.is_werewolf
      ? {
          P: () => doAction(api.werewolfPractice),
          M: () => doAction(api.werewolfMeditate),
          H: () => doAction(api.werewolfHowl),
          Q: () => nav('/places'),
          ESCAPE: () => nav('/places'),
        }
      : {
          A: () => doAction(api.werewolfAccept),
          Q: () => nav('/places'),
          ESCAPE: () => nav('/places'),
        },
    [status, nav],
  );

  if (!status) return <Terminal title="WEREWOLF DEN"><div className="c-muted">Loading...</div></Terminal>;

  return (
    <Terminal title="WEREWOLF DEN" subtitle="The Pack Awaits">
      <Separator />
      <div className="narrative">
        {status.is_werewolf
          ? 'The pack greets you with low growls of recognition.'
          : 'A dark cave entrance. Yellow eyes watch from the shadows.'}
      </div>
      <Separator />
      {status.is_werewolf ? (
        <>
          <div className="c-magenta">Transformations: {status.transformations}</div>
          <MenuOption shortcut="P" label="Practice transformation" onClick={() => doAction(api.werewolfPractice)} />
          <MenuOption shortcut="M" label="Meditate with pack" onClick={() => doAction(api.werewolfMeditate)} />
          <MenuOption shortcut="H" label="Howl at the moon" onClick={() => doAction(api.werewolfHowl)} />
        </>
      ) : (
        <MenuOption
          shortcut="A"
          label="Accept the werewolf curse (5000 gold)"
          onClick={() => doAction(api.werewolfAccept)}
          disabled={status.gold < 5000}
        />
      )}
      <Separator />
      <MenuOption shortcut="Q" label="Return" onClick={() => nav('/places')} />
    </Terminal>
  );
}
