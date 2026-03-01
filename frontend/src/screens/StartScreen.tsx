import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useKeyboard } from '../hooks/useKeyboard';

const TITLE_ART = `
    ██╗     ███████╗ ██████╗ ███████╗███╗   ██╗██████╗
    ██║     ██╔════╝██╔════╝ ██╔════╝████╗  ██║██╔══██╗
    ██║     █████╗  ██║  ███╗█████╗  ██╔██╗ ██║██║  ██║
    ██║     ██╔══╝  ██║   ██║██╔══╝  ██║╚██╗██║██║  ██║
    ███████╗███████╗╚██████╔╝███████╗██║ ╚████║██████╔╝
    ╚══════╝╚══════╝ ╚═════╝ ╚══════╝╚═╝  ╚═══╝╚═════╝

           OF THE OBSIDIAN VAULT

        A LORD-Inspired Knowledge RPG
`;

export function StartScreen() {
  const nav = useNavigate();

  useKeyboard({
    N: () => nav('/create'),
    E: () => nav('/select'),
    V: () => nav('/settings/vault'),
    B: () => nav('/settings'),
    Q: () => window.close(),
  }, [nav]);

  return (
    <Terminal title="LEGEND OF THE OBSIDIAN VAULT" subtitle="v0.0.5">
      <pre className="ascii-art c-cyan" style={{ textAlign: 'center' }}>{TITLE_ART}</pre>
      <Separator />
      <div style={{ padding: '8px 0' }}>
        <MenuOption shortcut="N" label="Start New Game" onClick={() => nav('/create')} />
        <MenuOption shortcut="E" label="Enter Existing Game" onClick={() => nav('/select')} />
        <MenuOption shortcut="V" label="Vault Settings" onClick={() => nav('/settings/vault')} />
        <MenuOption shortcut="B" label="AI Settings" onClick={() => nav('/settings')} />
        <MenuOption shortcut="Q" label="Quit" onClick={() => window.close()} />
      </div>
      <Separator />
      <div className="c-muted" style={{ textAlign: 'center', padding: '8px' }}>
        Transform your Obsidian notes into epic battles!
      </div>
    </Terminal>
  );
}
