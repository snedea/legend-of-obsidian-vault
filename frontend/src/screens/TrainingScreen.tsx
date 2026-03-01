import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function TrainingScreen() {
  const nav = useNavigate();
  const { notify, setCombat } = useGame();
  const [training, setTraining] = useState<api.TrainingStatus | null>(null);

  const load = useCallback(async () => {
    setTraining(await api.getTraining());
  }, []);

  useEffect(() => { load(); }, [load]);

  const challenge = async (level: number) => {
    try {
      const state = await api.startMasterFight(level);
      setCombat(state);
      nav('/combat');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Challenge failed');
    }
  };

  useKeyboard({
    C: () => {
      if (training?.can_challenge_current) {
        challenge(training.current_level);
      }
    },
    Q: () => nav('/town'),
    ESCAPE: () => nav('/town'),
  }, [training, nav]);

  if (!training) return <Terminal title="TURGON'S TRAINING"><div className="c-muted">Loading...</div></Terminal>;

  return (
    <Terminal title="TURGON'S TRAINING" subtitle={`Level ${training.current_level}`}>
      <SceneCanvas scene="training" />
      <Separator />
      <div className="c-cyan">Your current level: {training.current_level}</div>
      <Separator />
      <div style={{ padding: '4px 0' }}>
        {training.masters.map((m) => (
          <div key={m.level} style={{ padding: '2px 0' }}>
            <span className={m.level === training.current_level ? 'c-yellow bold' : 'c-muted'}>
              Level {m.level}: {m.name}
            </span>
            {m.can_challenge && (
              <span className="c-green"> [READY TO CHALLENGE]</span>
            )}
            {m.level === training.current_level && !m.can_challenge && (
              <span className="c-muted"> (Need {m.exp_needed.toLocaleString()} exp, have {m.current_exp.toLocaleString()})</span>
            )}
          </div>
        ))}
      </div>
      <Separator />
      {training.can_challenge_current && (
        <MenuOption shortcut="C" label="Challenge your master!" onClick={() => challenge(training.current_level)} />
      )}
      <MenuOption shortcut="Q" label="Return to town" onClick={() => nav('/town')} />
    </Terminal>
  );
}
