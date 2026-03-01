import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';

export function FairyScreen() {
  const nav = useNavigate();
  const { player, notify, refreshPlayer } = useGame();

  const doAction = async (fn: () => Promise<api.IGMResult>) => {
    try {
      const r = await fn();
      notify(r.message);
      await refreshPlayer();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Error');
    }
  };

  useKeyboard({
    L: () => doAction(api.fairyLearn),
    P: () => doAction(api.fairyPractice),
    M: () => doAction(api.fairyMeditate),
    G: () => doAction(api.fairyGather),
    Q: () => nav('/places'),
    ESCAPE: () => nav('/places'),
  }, [nav]);

  return (
    <Terminal title="FAIRY GARDEN" subtitle="Enchanted Glade">
      <Separator />
      <div className="narrative">
        A shimmering glade opens before you. Tiny lights dance among the flowers.
        The fairy queen regards you curiously.
      </div>
      <Separator />
      <MenuOption
        shortcut="L"
        label={player?.fairy_lore ? 'Fairy Lore (already learned)' : 'Learn Fairy Lore (1000 gold)'}
        onClick={() => doAction(api.fairyLearn)}
        disabled={player?.fairy_lore}
      />
      <MenuOption shortcut="P" label="Practice healing" onClick={() => doAction(api.fairyPractice)} />
      <MenuOption shortcut="M" label="Meditate with fairy" onClick={() => doAction(api.fairyMeditate)} />
      <MenuOption shortcut="G" label="Gather herbs" onClick={() => doAction(api.fairyGather)} />
      <MenuOption shortcut="Q" label="Return" onClick={() => nav('/places')} />
    </Terminal>
  );
}
