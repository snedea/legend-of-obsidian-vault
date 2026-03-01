import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function DailyNewsScreen() {
  const nav = useNavigate();
  const [news, setNews] = useState('');

  useEffect(() => {
    api.getDailyNews().then((r) => setNews(r.message));
  }, []);

  useKeyboard({ Q: () => nav('/town'), ESCAPE: () => nav('/town') }, [nav]);

  return (
    <Terminal title="DAILY NEWS" subtitle="Town Crier">
      <SceneCanvas scene="news" />
      <Separator />
      <div className="c-white" style={{ padding: '8px 0' }}>
        {news || 'Loading...'}
      </div>
      <Separator />
      <MenuOption shortcut="Q" label="Return to town" onClick={() => nav('/town')} />
    </Terminal>
  );
}
