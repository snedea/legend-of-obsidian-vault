import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useKeyboard } from '../hooks/useKeyboard';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function InnScreen() {
  const nav = useNavigate();

  useKeyboard({
    B: () => nav('/town/inn/bar'),
    V: () => nav('/town/inn/violet'),
    Q: () => nav('/town'),
    ESCAPE: () => nav('/town'),
  }, [nav]);

  return (
    <Terminal title="THE INN" subtitle="Rest Your Weary Bones">
      <SceneCanvas scene="inn" />
      <Separator />
      <div className="c-muted" style={{ padding: '8px 0' }}>
        The innkeeper greets you warmly.
        "Rest well, traveler. Tomorrow brings new adventures."
      </div>
      <Separator />
      <MenuOption shortcut="B" label="Enter the bar room" onClick={() => nav('/town/inn/bar')} />
      <MenuOption shortcut="V" label="Visit Violet's room" onClick={() => nav('/town/inn/violet')} />
      <Separator />
      <MenuOption shortcut="Q" label="Return to town" onClick={() => nav('/town')} />
    </Terminal>
  );
}
