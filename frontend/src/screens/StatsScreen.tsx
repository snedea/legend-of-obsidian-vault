import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { HpBar } from '../components/HpBar';
import { Separator } from '../components/Separator';
import { MenuOption } from '../components/MenuOption';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import { SceneCanvas } from '../canvas/SceneCanvas';

const CLASS_NAMES: Record<string, string> = {
  K: 'Death Knight',
  P: 'Mystical',
  D: 'Thieving',
};

export function StatsScreen() {
  const nav = useNavigate();
  const { player } = useGame();

  useKeyboard({ Q: () => nav(-1 as never), ESCAPE: () => nav(-1 as never) }, [nav]);

  if (!player) return null;

  return (
    <Terminal title="CHARACTER STATS" subtitle={player.name}>
      <SceneCanvas scene="stats" />
      <Separator />
      <div className="two-columns" style={{ padding: '4px 0' }}>
        <div>
          <div><span className="c-muted">Name:</span> <span className="c-white bold">{player.name}</span></div>
          <div><span className="c-muted">Gender:</span> {player.gender === 'M' ? 'Male' : 'Female'}</div>
          <div><span className="c-muted">Class:</span> <span className="c-cyan">{CLASS_NAMES[player.class_type] ?? player.class_type}</span></div>
          <div><span className="c-muted">Level:</span> <span className="c-yellow">{player.level}</span></div>
          <div><span className="c-muted">Experience:</span> {player.experience.toLocaleString()}</div>
          <div><HpBar current={player.hitpoints} max={player.max_hitpoints} label="HP:" /></div>
        </div>
        <div>
          <div><span className="c-muted">Attack:</span> <span className="c-red">{player.attack_power}</span></div>
          <div><span className="c-muted">Defense:</span> <span className="c-blue">{player.defense_power}</span></div>
          <div><span className="c-muted">Gold:</span> <span className="c-gold">{player.gold.toLocaleString()}</span></div>
          <div><span className="c-muted">Bank:</span> <span className="c-gold">{player.bank_gold.toLocaleString()}</span></div>
          <div><span className="c-muted">Gems:</span> {player.gems}</div>
          <div><span className="c-muted">Charm:</span> {player.charm}</div>
        </div>
      </div>
      <Separator />
      <div className="two-columns" style={{ padding: '4px 0' }}>
        <div>
          <div><span className="c-muted">Weapon:</span> <span className="c-white">{player.weapon}</span></div>
          <div><span className="c-muted">Armor:</span> <span className="c-white">{player.armor}</span></div>
          <div><span className="c-muted">Horse:</span> {player.horse ? player.horse_name || 'Yes' : 'None'}</div>
        </div>
        <div>
          <div><span className="c-muted">Forest Fights:</span> {player.forest_fights}</div>
          <div><span className="c-muted">Total Kills:</span> {player.total_kills}</div>
          <div><span className="c-muted">Dragon Kills:</span> {player.dragon_kills}</div>
        </div>
      </div>
      <Separator />
      <div style={{ padding: '4px 0' }}>
        <div><span className="c-muted">Fairy Lore:</span> {player.fairy_lore ? <span className="c-green">Learned</span> : 'Not learned'}</div>
        <div><span className="c-muted">Werewolf:</span> {player.is_werewolf ? <span className="c-magenta">Cursed</span> : 'Normal'}</div>
        <div><span className="c-muted">Spirit:</span> {player.spirit_level}</div>
        <div><span className="c-muted">Days Played:</span> {player.days_played}</div>
      </div>
      <Separator />
      <MenuOption shortcut="Q" label="Return" onClick={() => nav(-1 as never)} />
    </Terminal>
  );
}
