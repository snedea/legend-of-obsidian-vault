import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';

type Step = 'name' | 'gender' | 'class';

export function CharacterCreation() {
  const nav = useNavigate();
  const { setPlayer, notify } = useGame();
  const [step, setStep] = useState<Step>('name');
  const [name, setName] = useState('');
  const [gender, setGender] = useState('');

  const handleCreate = async (classType: string) => {
    try {
      const player = await api.createCharacter(name, gender, classType);
      setPlayer(player);
      notify(`${player.name} enters the realm!`);
      nav('/town');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Creation failed');
    }
  };

  useKeyboard(
    step === 'gender'
      ? {
          M: () => { setGender('M'); setStep('class'); },
          F: () => { setGender('F'); setStep('class'); },
          ESCAPE: () => setStep('name'),
        }
      : step === 'class'
        ? {
            K: () => handleCreate('K'),
            P: () => handleCreate('P'),
            D: () => handleCreate('D'),
            ESCAPE: () => setStep('gender'),
          }
        : { ESCAPE: () => nav('/') },
    [step, name, gender, nav],
  );

  return (
    <Terminal title="CHARACTER CREATION" subtitle="Forge Your Legend">
      <pre className="ascii-art c-yellow">{`
     ╔══════════════════════════════╗
     ║   CREATE YOUR CHARACTER      ║
     ╚══════════════════════════════╝
`}</pre>
      <Separator />

      {step === 'name' && (
        <div style={{ padding: '8px 0' }}>
          <div className="c-cyan">What is your name, warrior?</div>
          <div style={{ marginTop: 8 }}>
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === 'Enter' && name.trim()) setStep('gender');
              }}
              placeholder="Enter your name..."
              autoFocus
              maxLength={20}
              style={{ width: '300px' }}
            />
          </div>
          <div className="c-muted" style={{ marginTop: 4 }}>Press Enter to continue</div>
        </div>
      )}

      {step === 'gender' && (
        <div style={{ padding: '8px 0' }}>
          <div className="c-cyan">Choose your gender, {name}:</div>
          <div style={{ marginTop: 8 }}>
            <MenuOption shortcut="M" label="Male" onClick={() => { setGender('M'); setStep('class'); }} />
            <MenuOption shortcut="F" label="Female" onClick={() => { setGender('F'); setStep('class'); }} />
          </div>
        </div>
      )}

      {step === 'class' && (
        <div style={{ padding: '8px 0' }}>
          <div className="c-cyan">Choose your class, {name}:</div>
          <div style={{ marginTop: 8 }}>
            <MenuOption shortcut="K" label="Death Knight - Powerful melee attacks" onClick={() => handleCreate('K')} />
            <MenuOption shortcut="P" label="Mystical - Arcane spell power" onClick={() => handleCreate('P')} />
            <MenuOption shortcut="D" label="Thieving - Cunning and stealth" onClick={() => handleCreate('D')} />
          </div>
        </div>
      )}

      <Separator />
      <div className="c-muted">ESC to go back</div>
    </Terminal>
  );
}
