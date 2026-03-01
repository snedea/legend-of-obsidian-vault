import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function GatewayScreen() {
  const nav = useNavigate();
  const { player, notify, refreshPlayer } = useGame();

  const doPortal = async (fn: () => Promise<api.GatewayResult>) => {
    try {
      const r = await fn();
      notify(r.message);
      await refreshPlayer();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Error');
    }
  };

  useKeyboard({
    Z: () => doPortal(api.gatewayZycho),
    D: () => doPortal(api.gatewayDeath),
    R: () => doPortal(api.gatewayRandom),
    Q: () => nav('/places'),
    ESCAPE: () => nav('/places'),
  }, [nav]);

  const gems = player?.gems ?? 0;

  return (
    <Terminal title="GATEWAY PORTAL" subtitle="Between Worlds">
      <SceneCanvas scene="gateway" />
      <Separator />
      <div className="narrative">
        A shimmering portal pulses with otherworldly energy.
        Each journey costs 1 gem.
      </div>
      <div className="c-cyan">Gems: {gems}</div>
      <Separator />
      <MenuOption shortcut="Z" label="Zycho Zircus" onClick={() => doPortal(api.gatewayZycho)} disabled={gems < 1} />
      <MenuOption shortcut="D" label="Death's Mansion" onClick={() => doPortal(api.gatewayDeath)} disabled={gems < 1} />
      <MenuOption shortcut="R" label="Random Portal" onClick={() => doPortal(api.gatewayRandom)} disabled={gems < 1} />
      <Separator />
      <MenuOption shortcut="Q" label="Return" onClick={() => nav('/places')} />
    </Terminal>
  );
}
