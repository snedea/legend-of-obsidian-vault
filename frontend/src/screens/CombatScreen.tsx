import { useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { HpBar } from '../components/HpBar';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';
import type { Rewards } from '../services/api';

export function CombatScreen() {
  const nav = useNavigate();
  const { combat, setCombat, notify, refreshPlayer } = useGame();
  const [log, setLog] = useState<string[]>(combat?.log ?? []);
  const [enemyHp, setEnemyHp] = useState(combat?.enemy.hitpoints ?? 0);
  const [playerHp, setPlayerHp] = useState(combat?.player.hitpoints ?? 0);
  const [combatOver, setCombatOver] = useState(false);
  const [showQuiz, setShowQuiz] = useState(false);
  const [quiz, setQuiz] = useState<api.QuizQuestion | null>(null);

  const appendLog = (msg: string) => setLog((prev) => [...prev, msg]);

  const handleResult = useCallback(async (
    pMsg: string, eMsg: string, eHp: number, pHp: number,
    over: boolean, victory: boolean, rewards: Rewards | null,
  ) => {
    appendLog(pMsg);
    if (eMsg) appendLog(eMsg);
    setEnemyHp(eHp);
    setPlayerHp(pHp);
    if (over) {
      setCombatOver(true);
      if (victory && rewards) {
        appendLog(`Victory! +${rewards.experience} exp, +${rewards.gold} gold`);
        if (rewards.level_up) appendLog('LEVEL UP!');
        if (rewards.can_train) appendLog('You have enough experience to train!');
      } else if (!victory) {
        appendLog('You have been defeated!');
      }
      await refreshPlayer();
      setTimeout(() => {
        setCombat(null);
        nav(victory ? '/forest' : '/town');
      }, 2500);
    }
  }, [refreshPlayer, setCombat, nav]);

  const doAttack = useCallback(async () => {
    if (combatOver) return;
    try {
      const r = await api.combatAttack();
      await handleResult(r.player_message, r.enemy_message, r.enemy_hp, r.player_hp,
        r.combat_over, r.victory, r.rewards);
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Attack failed');
    }
  }, [combatOver, handleResult, notify]);

  const doSkill = useCallback(async () => {
    if (combatOver) return;
    try {
      const r = await api.combatSkill();
      await handleResult(r.player_message, r.enemy_message, r.enemy_hp, r.player_hp,
        r.combat_over, r.victory, r.rewards);
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Skill failed');
    }
  }, [combatOver, handleResult, notify]);

  const doHeal = useCallback(async () => {
    if (combatOver) return;
    try {
      const r = await api.combatHeal();
      appendLog(r.message);
      if (r.enemy_message) appendLog(r.enemy_message);
      setEnemyHp(r.enemy_hp);
      setPlayerHp(r.player_hp);
      if (r.combat_over) {
        setCombatOver(true);
        appendLog('You have been defeated!');
        await refreshPlayer();
        setTimeout(() => { setCombat(null); nav('/town'); }, 2500);
      }
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Heal failed');
    }
  }, [combatOver, refreshPlayer, setCombat, nav, notify]);

  const doRun = useCallback(async () => {
    try {
      const r = await api.combatRun();
      appendLog(r.message);
      setCombatOver(true);
      await refreshPlayer();
      setTimeout(() => { setCombat(null); nav('/forest'); }, 1000);
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Flee failed');
    }
  }, [refreshPlayer, setCombat, nav, notify]);

  const startQuiz = useCallback(async () => {
    if (combatOver) return;
    try {
      const q = await api.quizStart();
      setQuiz(q);
      setShowQuiz(true);
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Quiz failed');
    }
  }, [combatOver, notify]);

  const answerQuiz = useCallback(async (index: number) => {
    if (!quiz) return;
    try {
      const r = await api.quizAnswer(index);
      setShowQuiz(false);
      setQuiz(null);
      appendLog(r.message);
      if (r.enemy_message) appendLog(r.enemy_message);
      setEnemyHp(r.enemy_hp);
      setPlayerHp(r.player_hp);
      if (r.combat_over) {
        setCombatOver(true);
        if (r.victory) {
          appendLog(`Victory! +${r.rewards?.experience ?? 0} exp, +${r.rewards?.gold ?? 0} gold`);
        } else {
          appendLog('You have been defeated!');
        }
        await refreshPlayer();
        setTimeout(() => { setCombat(null); nav(r.victory ? '/forest' : '/town'); }, 2500);
      }
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Answer failed');
    }
  }, [quiz, refreshPlayer, setCombat, nav, notify]);

  useKeyboard(
    showQuiz
      ? {
          '1': () => answerQuiz(0),
          '2': () => answerQuiz(1),
          '3': () => answerQuiz(2),
          ESCAPE: () => { setShowQuiz(false); setQuiz(null); },
        }
      : {
          A: doAttack,
          K: startQuiz,
          S: doSkill,
          H: doHeal,
          R: doRun,
        },
    [showQuiz, combatOver, quiz],
  );

  if (!combat) {
    nav('/forest');
    return null;
  }

  const enemy = combat.enemy;
  const enemyMax = enemy.max_hitpoints;
  const playerMax = combat.player.max_hitpoints;

  return (
    <Terminal title="MYSTICAL ENCOUNTER" subtitle="Battle for Knowledge">
      {/* Narrative */}
      {enemy.encounter_narrative && (
        <div className="narrative" style={{ maxHeight: '120px', overflow: 'hidden' }}>
          {enemy.encounter_narrative}
        </div>
      )}

      <Separator />

      {/* Enemy Status */}
      <div className="combat-section">
        <div className="combat-label">ENEMY STATUS</div>
        <div>Name: <span className="c-white bold">{enemy.name}</span></div>
        <div><HpBar current={enemyHp} max={enemyMax} label="HP:" /></div>
        <div className="c-muted">
          Level: {enemy.level}  ATK: {enemy.attack}  Weapon: {enemy.weapon}  Armor: {enemy.armor}
        </div>
      </div>

      <Separator char="-" />

      {/* Player Status */}
      <div className="combat-section">
        <div className="combat-label">PLAYER STATUS</div>
        <div>Name: <span className="c-white bold">{combat.player.name}</span></div>
        <div><HpBar current={playerHp} max={playerMax} label="HP:" /></div>
        <div className="c-muted">
          Level: {combat.player.level}  ATK: {combat.player.attack_power}  DEF: {combat.player.defense_power}  Gold: {combat.player.gold}
        </div>
      </div>

      <Separator />

      {/* Quiz overlay */}
      {showQuiz && quiz && (
        <div style={{ padding: '8px', border: '1px solid var(--accent)' }}>
          <div className="c-cyan bold">KNOWLEDGE QUIZ</div>
          <div className="c-white" style={{ margin: '4px 0' }}>{quiz.question}</div>
          {quiz.options.map((opt, i) => (
            <MenuOption
              key={i}
              shortcut={String(i + 1)}
              label={opt}
              onClick={() => answerQuiz(i)}
            />
          ))}
          <div className="c-muted">ESC to cancel</div>
        </div>
      )}

      {/* Combat commands */}
      {!showQuiz && !combatOver && (
        <div style={{ padding: '4px 0' }}>
          <div className="c-cyan bold">BATTLE COMMANDS</div>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            <MenuOption shortcut="A" label="Attack" onClick={doAttack} />
            <MenuOption shortcut="K" label="Knowledge Quiz" onClick={startQuiz} />
            <MenuOption shortcut="S" label="Skill" onClick={doSkill} />
            {combat.player.fairy_lore && (
              <MenuOption shortcut="H" label="Heal" onClick={doHeal} />
            )}
            <MenuOption shortcut="R" label="Run Away" onClick={doRun} />
          </div>
        </div>
      )}

      {/* Combat log */}
      <div
        style={{
          marginTop: 8,
          maxHeight: '120px',
          overflowY: 'auto',
          borderTop: '1px solid var(--muted)',
          paddingTop: 4,
        }}
      >
        {log.slice(-8).map((entry, i) => (
          <div key={i} className={entry.includes('MISS') || entry.includes('defeated') ? 'c-red' : entry.includes('Victory') || entry.includes('CRITICAL') ? 'c-green' : 'c-white'}>
            {entry}
          </div>
        ))}
      </div>
    </Terminal>
  );
}
