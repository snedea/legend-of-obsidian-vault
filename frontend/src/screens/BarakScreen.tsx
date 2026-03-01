import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';

export function BarakScreen() {
  const nav = useNavigate();
  const { notify } = useGame();

  const doAction = async (fn: () => Promise<{ message: string }>) => {
    try {
      const r = await fn();
      notify(r.message);
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Error');
    }
  };

  useKeyboard({
    R: () => doAction(api.barakRead),
    S: () => doAction(api.barakStudy),
    T: () => doAction(api.barakTalk),
    Q: () => nav('/places'),
    ESCAPE: () => nav('/places'),
  }, [nav]);

  return (
    <Terminal title="BARAK'S HOUSE" subtitle="Ancient Warrior">
      <Separator />
      <div className="narrative">
        Barak's house is filled with dusty scrolls and ancient weapons.
        The old warrior sits by the fire.
      </div>
      <Separator />
      <MenuOption shortcut="R" label="Read ancient texts" onClick={() => doAction(api.barakRead)} />
      <MenuOption shortcut="S" label="Study combat techniques" onClick={() => doAction(api.barakStudy)} />
      <MenuOption shortcut="T" label="Talk to Barak" onClick={() => doAction(api.barakTalk)} />
      <MenuOption shortcut="Q" label="Leave" onClick={() => nav('/places')} />
    </Terminal>
  );
}
