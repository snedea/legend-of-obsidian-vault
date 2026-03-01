import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { StatusBar } from '../components/StatusBar';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';

export function TownSquare() {
  const nav = useNavigate();
  const { player } = useGame();

  useKeyboard({
    F: () => nav('/forest'),
    K: () => nav('/town/weapons'),
    A: () => nav('/town/armor'),
    H: () => nav('/town/healer'),
    V: () => nav('/town/stats'),
    I: () => nav('/town/inn'),
    T: () => nav('/town/training'),
    Y: () => nav('/town/bank'),
    L: () => nav('/town/warriors'),
    D: () => nav('/town/news'),
    O: () => nav('/places'),
    G: () => nav('/settings'),
    Q: () => nav('/'),
  }, [nav]);

  if (!player) {
    nav('/');
    return null;
  }

  return (
    <Terminal title="TOWN SQUARE" subtitle={`Day ${player.days_played}`}>
      <pre className="ascii-art c-cyan">{`
       ╔═══════════════════════════════════════╗
       ║         THE TOWN OF LORDIA            ║
       ║    Where Heroes Gather and Plan       ║
       ╚═══════════════════════════════════════╝
`}</pre>
      <Separator />
      <div className="menu-columns" style={{ padding: '4px 0' }}>
        <div>
          <MenuOption shortcut="F" label="Forest" onClick={() => nav('/forest')} />
          <MenuOption shortcut="K" label="King Arthur's Weapons" onClick={() => nav('/town/weapons')} />
          <MenuOption shortcut="A" label="Abdul's Armour" onClick={() => nav('/town/armor')} />
          <MenuOption shortcut="H" label="Healer's Hut" onClick={() => nav('/town/healer')} />
          <MenuOption shortcut="V" label="View Stats" onClick={() => nav('/town/stats')} />
          <MenuOption shortcut="I" label="Inn" onClick={() => nav('/town/inn')} />
        </div>
        <div>
          <MenuOption shortcut="T" label="Turgon's Training" onClick={() => nav('/town/training')} />
          <MenuOption shortcut="Y" label="Ye Old Bank" onClick={() => nav('/town/bank')} />
          <MenuOption shortcut="L" label="List Warriors" onClick={() => nav('/town/warriors')} />
          <MenuOption shortcut="D" label="Daily News" onClick={() => nav('/town/news')} />
        </div>
        <div>
          <MenuOption shortcut="O" label="Other Places" onClick={() => nav('/places')} />
          <MenuOption shortcut="G" label="Game Settings" onClick={() => nav('/settings')} />
          <MenuOption shortcut="Q" label="Quit to Fields" onClick={() => nav('/')} />
        </div>
      </div>
      <Separator />
      <StatusBar />
    </Terminal>
  );
}
