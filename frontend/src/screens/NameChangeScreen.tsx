import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function NameChangeScreen() {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();
  const [newName, setNewName] = useState('');

  const submit = async () => {
    if (!newName.trim()) {
      notify('Name cannot be empty!');
      return;
    }
    try {
      const result = await api.changeName(newName.trim());
      notify(result.message);
      await refreshPlayer();
      nav('/town/inn/bar');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Name change failed');
    }
  };

  useKeyboard({
    ESCAPE: () => nav('/town/inn/bar'),
  }, [nav]);

  return (
    <Terminal title="NAME CHANGE" subtitle="New Identity">
      <SceneCanvas scene="nameChange" />
      <Separator />
      <div className="c-cyan" style={{ padding: '8px 0' }}>
        Enter your new name:
      </div>
      <div style={{ padding: '8px 0' }}>
        <input
          type="text"
          value={newName}
          onChange={(e) => setNewName(e.target.value)}
          onKeyDown={(e) => { if (e.key === 'Enter') submit(); }}
          autoFocus
          maxLength={20}
          style={{ width: '200px' }}
        />
      </div>
      <Separator />
      <MenuOption shortcut="ENTER" label="Confirm" onClick={submit} />
      <MenuOption shortcut="ESC" label="Cancel" onClick={() => nav('/town/inn/bar')} />
    </Terminal>
  );
}
