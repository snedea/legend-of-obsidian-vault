import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useKeyboard } from '../hooks/useKeyboard';
import { useGame } from '../context/GameContext';
import * as api from '../services/api';

const DIFFICULTY_MODES = [
  { key: '1', value: 'age_based', label: 'Age-Based - Older notes = Harder' },
  { key: '2', value: 'random', label: 'Random - Chaos mode' },
  { key: '3', value: 'player_level', label: 'Player Level - Balanced' },
  { key: '4', value: 'content', label: 'Content Complexity' },
  { key: '5', value: 'ai', label: 'AI-Determined - Mixed factors' },
];

const PROVIDERS = [
  { key: '6', value: 'tinyllama', label: 'TinyLlama (Local)' },
  { key: '7', value: 'claude_cli', label: 'Claude CLI' },
  { key: '8', value: 'claude_api', label: 'Claude API' },
];

export function SettingsScreen() {
  const nav = useNavigate();
  const { notify } = useGame();
  const [settings, setSettings] = useState<api.Settings | null>(null);
  const [aiStatus, setAiStatus] = useState<api.AIStatus | null>(null);

  const load = useCallback(async () => {
    const [s, ai] = await Promise.all([api.getSettings(), api.getAIStatus()]);
    setSettings(s);
    setAiStatus(ai);
  }, []);

  useEffect(() => { load(); }, [load]);

  const update = async (updates: Partial<api.Settings>) => {
    try {
      const s = await api.updateSettings(updates);
      setSettings(s);
      notify('Settings updated');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Update failed');
    }
  };

  const keyMap: Record<string, () => void> = {
    Q: () => nav(-1 as never),
    ESCAPE: () => nav(-1 as never),
    V: () => nav('/settings/vault'),
  };
  DIFFICULTY_MODES.forEach(({ key, value }) => {
    keyMap[key] = () => update({ difficulty_mode: value });
  });
  PROVIDERS.forEach(({ key, value }) => {
    keyMap[key] = () => update({ ai_provider: value });
  });

  useKeyboard(keyMap, [settings, nav]);

  if (!settings) return <Terminal title="SETTINGS"><div className="c-muted">Loading...</div></Terminal>;

  return (
    <Terminal title="GAME SETTINGS" subtitle="Configure Your Adventure">
      <Separator />
      <div className="c-cyan bold">ENEMY DIFFICULTY</div>
      {DIFFICULTY_MODES.map((m) => (
        <MenuOption
          key={m.value}
          shortcut={m.key}
          label={`${m.label}${settings.difficulty_mode === m.value ? ' *' : ''}`}
          onClick={() => update({ difficulty_mode: m.value })}
        />
      ))}
      <Separator />
      <div className="c-cyan bold">AI PROVIDER</div>
      <div className="c-muted">
        Current: {aiStatus?.provider ?? '...'} ({aiStatus?.available ? 'available' : aiStatus?.status ?? '...'})
      </div>
      {PROVIDERS.map((p) => (
        <MenuOption
          key={p.value}
          shortcut={p.key}
          label={`${p.label}${settings.ai_provider === p.value ? ' *' : ''}`}
          onClick={() => update({ ai_provider: p.value })}
        />
      ))}
      <Separator />
      <MenuOption shortcut="V" label="Vault Settings" onClick={() => nav('/settings/vault')} />
      <MenuOption shortcut="Q" label="Return" onClick={() => nav(-1 as never)} />
    </Terminal>
  );
}
