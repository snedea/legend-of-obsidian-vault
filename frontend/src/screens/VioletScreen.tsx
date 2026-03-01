import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import { SceneCanvas } from '../canvas/SceneCanvas';

export function VioletScreen() {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();
  const [violet, setViolet] = useState<api.VioletStatus | null>(null);
  const [married, setMarried] = useState(false);

  const load = useCallback(async () => {
    setViolet(await api.getVioletStatus());
  }, []);

  useEffect(() => { load(); }, [load]);

  const flirt = async (charmLevel: number) => {
    try {
      const result = await api.violetFlirt(charmLevel);
      notify(result.message);
      if (result.exp_gained > 0) {
        notify(`You gain ${result.exp_gained} experience!`);
      }
      if (result.special === 'marry') {
        setMarried(true);
      }
      await refreshPlayer();
      if (result.special !== 'marry') {
        await load();
      }
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Error');
    }
  };

  const keyMap: Record<string, () => void> = {
    Q: () => nav('/town/inn/bar'),
    ESCAPE: () => nav('/town/inn/bar'),
  };
  if (violet && !violet.violet_married && !married) {
    violet.options.forEach((opt, i) => {
      const key = String(i + 1);
      keyMap[key] = () => flirt(opt.charm_level);
    });
  }

  useKeyboard(keyMap, [violet, married, nav]);

  if (!violet) return <Terminal title="VIOLET'S ROOM"><div className="c-muted">Loading...</div></Terminal>;

  if (married) {
    return (
      <Terminal title="WEDDING CELEBRATION" subtitle="Congratulations!">
        <Separator char="=" />
        <div style={{ padding: '16px 0', textAlign: 'center' }}>
          <div className="c-yellow bold">Congratulations!</div>
          <div className="c-white" style={{ padding: '8px 0' }}>
            You and Violet are now married!
          </div>
          <div className="c-white">The entire inn celebrates your union!</div>
          <div className="c-cyan" style={{ padding: '8px 0' }}>
            Violet whispers: "I'll always be here for you, my love."
          </div>
          <Separator />
          <div className="c-green">Marriage Benefits:</div>
          <div className="c-white">- Free room at the inn</div>
          <div className="c-white">- Violet's loving support</div>
          <div className="c-white">- Increased charm and confidence</div>
        </div>
        <Separator />
        <MenuOption shortcut="Q" label="Return to inn" onClick={() => nav('/town/inn/bar')} />
      </Terminal>
    );
  }

  if (violet.violet_married) {
    return (
      <Terminal title="VIOLET'S ROOM" subtitle="Love Lost">
        <Separator />
        <div style={{ padding: '8px 0' }}>
          <div className="c-muted">You enter Violet's room, but instead of the lovely</div>
          <div className="c-muted">Violet, you find Grizelda, the Inn's cleaning woman!</div>
          <div className="c-yellow" style={{ padding: '8px 0' }}>
            "Violet? She married {violet.violet_husband} and moved away."
          </div>
          <div className="c-muted">"Now get out of here before I call the guards!"</div>
        </div>
        <Separator />
        <MenuOption shortcut="Q" label="Leave quickly" onClick={() => nav('/town/inn/bar')} />
      </Terminal>
    );
  }

  if (violet.options.length === 0) {
    return (
      <Terminal title="VIOLET'S ROOM" subtitle="Romance & Charm">
        <Separator />
        <div className="c-cyan">Your charm: {violet.charm}</div>
        <Separator />
        <div style={{ padding: '8px 0' }}>
          <div className="c-muted">Violet looks at you with mild interest, but</div>
          <div className="c-muted">you lack the charm to do anything...</div>
        </div>
        <Separator />
        <MenuOption shortcut="Q" label="Leave disappointed" onClick={() => nav('/town/inn/bar')} />
      </Terminal>
    );
  }

  return (
    <Terminal title="VIOLET'S ROOM" subtitle="Romance & Charm">
      <SceneCanvas scene="violet" />
      <Separator />
      <div style={{ padding: '8px 0' }}>
        <div className="c-magenta">You enter Violet's room. The beautiful barmaid</div>
        <div className="c-magenta">looks up at you with sparkling eyes...</div>
      </div>
      <div className="c-cyan">Your charm: {violet.charm}</div>
      <Separator />
      <div className="c-yellow">What would you like to do?</div>
      <div style={{ padding: '4px 0' }}>
        {violet.options.map((opt, i) => (
          <MenuOption
            key={opt.charm_level}
            shortcut={String(i + 1)}
            label={`${opt.action} (Charm: ${opt.charm_level})`}
            onClick={() => flirt(opt.charm_level)}
          />
        ))}
      </div>
      <Separator />
      <MenuOption shortcut="Q" label="Leave gracefully" onClick={() => nav('/town/inn/bar')} />
    </Terminal>
  );
}
