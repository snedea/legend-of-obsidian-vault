import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useKeyboard } from '../hooks/useKeyboard';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function OtherPlaces() {
  const nav = useNavigate();

  useKeyboard({
    C: () => nav('/places/cavern'),
    F: () => nav('/places/fairy'),
    B: () => nav('/places/barak'),
    X: () => nav('/places/xenon'),
    W: () => nav('/places/werewolf'),
    G: () => nav('/places/gateway'),
    Q: () => nav('/town'),
    ESCAPE: () => nav('/town'),
  }, [nav]);

  return (
    <Terminal title="OTHER PLACES" subtitle="Explore the Realm">
      <SceneCanvas scene="otherPlaces" />
      <Separator />
      <div style={{ padding: '4px 0' }}>
        <MenuOption shortcut="C" label="Cavern" onClick={() => nav('/places/cavern')} />
        <MenuOption shortcut="F" label="Fairy Garden" onClick={() => nav('/places/fairy')} />
        <MenuOption shortcut="B" label="Barak's House" onClick={() => nav('/places/barak')} />
        <MenuOption shortcut="X" label="Xenon's Storage" onClick={() => nav('/places/xenon')} />
        <MenuOption shortcut="W" label="WereWolf Den" onClick={() => nav('/places/werewolf')} />
        <MenuOption shortcut="G" label="Gateway Portal" onClick={() => nav('/places/gateway')} />
      </div>
      <Separator />
      <MenuOption shortcut="Q" label="Return to town" onClick={() => nav('/town')} />
    </Terminal>
  );
}
