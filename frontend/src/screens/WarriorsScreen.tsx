import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { Separator } from '../components/Separator';
import { MenuOption } from '../components/MenuOption';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

const CLASS_SHORT: Record<string, string> = { K: 'DK', P: 'MY', D: 'TH' };

export function WarriorsScreen() {
  const nav = useNavigate();
  const [warriors, setWarriors] = useState<api.Warrior[]>([]);

  useEffect(() => {
    api.listWarriors().then((r) => setWarriors(r.warriors));
  }, []);

  useKeyboard({ Q: () => nav('/town'), ESCAPE: () => nav('/town') }, [nav]);

  return (
    <Terminal title="WARRIORS LIST" subtitle="Heroes of the Realm">
      <SceneCanvas scene="warriors" />
      <Separator />
      <div style={{ padding: '4px 0' }}>
        <div className="c-cyan" style={{ display: 'flex', gap: '8px' }}>
          <span style={{ width: '20px' }}>#</span>
          <span style={{ width: '150px' }}>Name</span>
          <span style={{ width: '40px' }}>Lvl</span>
          <span style={{ width: '40px' }}>Cls</span>
          <span style={{ width: '100px' }}>Weapon</span>
          <span style={{ width: '60px' }}>Kills</span>
        </div>
        {warriors.map((w, i) => (
          <div key={w.name} style={{ display: 'flex', gap: '8px' }} className={w.alive ? 'c-white' : 'c-muted'}>
            <span style={{ width: '20px' }}>{i + 1}</span>
            <span style={{ width: '150px' }}>{w.name}{w.alive ? '' : ' [DEAD]'}</span>
            <span style={{ width: '40px' }}>{w.level}</span>
            <span style={{ width: '40px' }}>{CLASS_SHORT[w.class_type] ?? w.class_type}</span>
            <span style={{ width: '100px' }}>{w.weapon}</span>
            <span style={{ width: '60px' }}>{w.total_kills}</span>
          </div>
        ))}
        {warriors.length === 0 && <div className="c-muted">No warriors yet.</div>}
      </div>
      <Separator />
      <MenuOption shortcut="Q" label="Return to town" onClick={() => nav('/town')} />
    </Terminal>
  );
}
