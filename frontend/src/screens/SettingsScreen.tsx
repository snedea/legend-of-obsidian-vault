import { useEffect, useState, useCallback, useRef } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useKeyboard } from '../hooks/useKeyboard';
import { useGame } from '../context/GameContext';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

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
  { key: '9', value: 'ollama', label: 'Ollama (Remote GPU)' },
];

interface CrtSettings {
  scanlines: boolean;
  glow: boolean;
  flicker: boolean;
  vignette: boolean;
}

function loadCrtSettings(): CrtSettings {
  const stored = localStorage.getItem('lov-crt-settings');
  if (stored) {
    try { return JSON.parse(stored); } catch { /* fall through */ }
  }
  return { scanlines: true, glow: true, flicker: true, vignette: true };
}

function saveCrtSettings(s: CrtSettings) {
  localStorage.setItem('lov-crt-settings', JSON.stringify(s));
  applyCrtSettings(s);
}

function applyCrtSettings(s: CrtSettings) {
  const html = document.documentElement;
  html.setAttribute('data-crt-scanlines', s.scanlines ? 'on' : 'off');
  html.setAttribute('data-crt-glow', s.glow ? 'on' : 'off');
  html.setAttribute('data-crt-flicker', s.flicker ? 'on' : 'off');
  html.setAttribute('data-crt-vignette', s.vignette ? 'on' : 'off');
}

// Apply CRT settings on module load so they persist across navigations
applyCrtSettings(loadCrtSettings());

export function SettingsScreen() {
  const nav = useNavigate();
  const { notify } = useGame();
  const [settings, setSettings] = useState<api.Settings | null>(null);
  const [aiStatus, setAiStatus] = useState<api.AIStatus | null>(null);
  const [crt, setCrt] = useState<CrtSettings>(loadCrtSettings);
  const [ollamaHost, setOllamaHost] = useState('');
  const [ollamaModel, setOllamaModel] = useState('');
  const hostRef = useRef<HTMLInputElement>(null);
  const modelRef = useRef<HTMLInputElement>(null);

  const load = useCallback(async () => {
    const [s, ai] = await Promise.all([api.getSettings(), api.getAIStatus()]);
    setSettings(s);
    setAiStatus(ai);
  }, []);

  useEffect(() => {
    load().then(() => {});
  }, [load]);

  // Sync local Ollama fields when settings load
  useEffect(() => {
    if (settings) {
      setOllamaHost(settings.ollama_host);
      setOllamaModel(settings.ollama_model);
    }
  }, [settings]);

  const update = async (updates: Partial<api.Settings>) => {
    try {
      const s = await api.updateSettings(updates);
      setSettings(s);
      notify('Settings updated');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Update failed');
    }
  };

  const toggleCrt = (key: keyof CrtSettings) => {
    const next = { ...crt, [key]: !crt[key] };
    setCrt(next);
    saveCrtSettings(next);
    notify(`${key} ${next[key] ? 'enabled' : 'disabled'}`);
  };

  const keyMap: Record<string, () => void> = {
    Q: () => nav(-1 as never),
    ESCAPE: () => nav(-1 as never),
    V: () => nav('/settings/vault'),
    S: () => toggleCrt('scanlines'),
    G: () => toggleCrt('glow'),
    K: () => toggleCrt('flicker'),
    I: () => toggleCrt('vignette'),
  };
  DIFFICULTY_MODES.forEach(({ key, value }) => {
    keyMap[key] = () => update({ difficulty_mode: value });
  });
  PROVIDERS.forEach(({ key, value }) => {
    keyMap[key] = () => update({ ai_provider: value });
  });

  useKeyboard(keyMap, [settings, crt, nav]);

  if (!settings) return <Terminal title="SETTINGS"><div className="c-muted">Loading...</div></Terminal>;

  return (
    <Terminal title="GAME SETTINGS" subtitle="Configure Your Adventure">
      <SceneCanvas scene="settings" />
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
      {settings.ai_provider === 'ollama' && (
        <div style={{ marginTop: 4, marginLeft: 16 }}>
          <div className="c-muted" style={{ marginBottom: 4 }}>
            <label>Host: </label>
            <input
              ref={hostRef}
              type="text"
              value={ollamaHost}
              onChange={(e) => setOllamaHost(e.target.value)}
              onBlur={() => { if (ollamaHost !== settings.ollama_host) update({ ollama_host: ollamaHost }); }}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.currentTarget.blur(); } }}
              style={{ width: 260 }}
            />
          </div>
          <div className="c-muted">
            <label>Model: </label>
            <input
              ref={modelRef}
              type="text"
              value={ollamaModel}
              onChange={(e) => setOllamaModel(e.target.value)}
              onBlur={() => { if (ollamaModel !== settings.ollama_model) update({ ollama_model: ollamaModel }); }}
              onKeyDown={(e) => { if (e.key === 'Enter') { e.currentTarget.blur(); } }}
              style={{ width: 200 }}
            />
          </div>
        </div>
      )}
      <Separator />
      <div className="c-cyan bold">CRT DISPLAY EFFECTS</div>
      <MenuOption shortcut="S" label={`Scanlines [${crt.scanlines ? 'ON' : 'OFF'}]`} onClick={() => toggleCrt('scanlines')} />
      <MenuOption shortcut="G" label={`Phosphor Glow [${crt.glow ? 'ON' : 'OFF'}]`} onClick={() => toggleCrt('glow')} />
      <MenuOption shortcut="K" label={`Screen Flicker [${crt.flicker ? 'ON' : 'OFF'}]`} onClick={() => toggleCrt('flicker')} />
      <MenuOption shortcut="I" label={`Vignette [${crt.vignette ? 'ON' : 'OFF'}]`} onClick={() => toggleCrt('vignette')} />
      <Separator />
      <MenuOption shortcut="V" label="Vault Settings" onClick={() => nav('/settings/vault')} />
      <MenuOption shortcut="Q" label="Return" onClick={() => nav(-1 as never)} />
    </Terminal>
  );
}
