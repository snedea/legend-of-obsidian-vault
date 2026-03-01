import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function CavernScreen() {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();

  const doAction = async (action: 'explore' | 'search') => {
    try {
      const r = action === 'explore' ? await api.cavernExplore() : await api.cavernSearch();
      notify(r.message);
      await refreshPlayer();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Error');
    }
  };

  useKeyboard({
    E: () => doAction('explore'),
    S: () => doAction('search'),
    Q: () => nav('/places'),
    ESCAPE: () => nav('/places'),
  }, [nav]);

  return (
    <Terminal title="THE CAVERN" subtitle="Dark and Mysterious">
      <SceneCanvas scene="cavern" />
      <Separator />
      <div className="narrative">
        The cavern entrance yawns before you, darkness swirling within.
        Strange sounds echo from the depths.
      </div>
      <Separator />
      <MenuOption shortcut="E" label="Explore the cavern" onClick={() => doAction('explore')} />
      <MenuOption shortcut="S" label="Search for treasures" onClick={() => doAction('search')} />
      <MenuOption shortcut="Q" label="Return" onClick={() => nav('/places')} />
    </Terminal>
  );
}
