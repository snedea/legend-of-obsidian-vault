import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { StatusBar } from '../components/StatusBar';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';


export function ForestScreen() {
  const nav = useNavigate();
  const { player, setCombat, notify } = useGame();

  const enterCombat = async () => {
    if (!player || player.forest_fights <= 0) {
      notify('No forest fights remaining!');
      return;
    }
    try {
      notify('Something stirs in the forest...');
      const state = await api.enterForest();
      setCombat(state);
      nav('/combat');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Error entering combat');
    }
  };

  useKeyboard({
    L: enterCombat,
    E: enterCombat,
    H: () => nav('/town/healer'),
    R: () => nav('/town'),
    Q: () => nav('/town'),
    C: () => nav('/places/cavern'),
  }, [player, nav]);

  if (!player) {
    nav('/');
    return null;
  }

  return (
    <Terminal title="MYSTICAL FOREST" subtitle="Where Knowledge Awaits">
      <div className="c-cyan" style={{ textAlign: 'center', fontWeight: 'bold' }}>
        THE MYSTICAL FOREST OF KNOWLEDGE
      </div>
      <SceneCanvas scene="forest" />
      <Separator char="=" />

      <div style={{ padding: '8px 0' }}>
        <div className="narrative">
          The murky forest stands before you - a giant maw of gloomy darkness ever beckoning.
        </div>
      </div>

      <div style={{ padding: '4px 0' }}>
        <MenuOption shortcut="L" label="Look for something to kill" onClick={enterCombat} />
        <MenuOption shortcut="H" label="Healer's hut" onClick={() => nav('/town/healer')} />
        <MenuOption shortcut="R" label="Return to town" onClick={() => nav('/town')} />
      </div>

      <Separator />
      <StatusBar />
    </Terminal>
  );
}
