import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function VaultScreen() {
  const nav = useNavigate();
  const { notify } = useGame();
  const [status, setStatus] = useState<api.VaultStatus | null>(null);
  const [inputMode, setInputMode] = useState(false);
  const [path, setPath] = useState('');

  const load = useCallback(async () => {
    setStatus(await api.getVaultStatus());
  }, []);

  useEffect(() => { load(); }, [load]);

  const autoDetect = async () => {
    try {
      const s = await api.autoDetectVault();
      setStatus(s);
      notify(s.connected ? `Vault found: ${s.path} (${s.note_count} notes)` : 'No vault detected');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Detection failed');
    }
  };

  const setVaultPath = async () => {
    if (!path.trim()) return;
    try {
      const s = await api.setVaultPath(path.trim());
      setStatus(s);
      setInputMode(false);
      notify(`Vault set: ${s.note_count} notes found`);
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Invalid path');
    }
  };

  useKeyboard(
    inputMode
      ? { ESCAPE: () => setInputMode(false) }
      : {
          A: autoDetect,
          S: () => setInputMode(true),
          Q: () => nav(-1 as never),
          ESCAPE: () => nav(-1 as never),
        },
    [inputMode, path, nav],
  );

  return (
    <Terminal title="VAULT SETTINGS" subtitle="Obsidian Integration">
      <SceneCanvas scene="vault" />
      <Separator />
      {status && (
        <div style={{ padding: '4px 0' }}>
          <div>Status: {status.connected ? <span className="c-green">Connected</span> : <span className="c-red">Not connected</span>}</div>
          {status.path && <div className="c-muted">Path: {status.path}</div>}
          {status.connected && <div>Notes: {status.note_count}</div>}
        </div>
      )}
      <Separator />

      {inputMode ? (
        <div style={{ padding: '4px 0' }}>
          <div className="c-cyan">Enter vault path:</div>
          <input
            type="text"
            value={path}
            onChange={(e) => setPath(e.target.value)}
            onKeyDown={(e) => { if (e.key === 'Enter') setVaultPath(); }}
            autoFocus
            style={{ width: '100%' }}
          />
          <div className="c-muted">Press Enter to set, ESC to cancel</div>
        </div>
      ) : (
        <>
          <MenuOption shortcut="A" label="Auto-detect vault" onClick={autoDetect} />
          <MenuOption shortcut="S" label="Set vault path manually" onClick={() => setInputMode(true)} />
          <MenuOption shortcut="Q" label="Return" onClick={() => nav(-1 as never)} />
        </>
      )}
    </Terminal>
  );
}
