import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';

interface ShopProps {
  type: 'weapons' | 'armor';
}

export function ShopScreen({ type }: ShopProps) {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();
  const [shop, setShop] = useState<api.ShopList | null>(null);

  const load = useCallback(async () => {
    setShop(type === 'weapons' ? await api.listWeapons() : await api.listArmor());
  }, [type]);

  useEffect(() => { load(); }, [load]);

  const buy = async (index: number) => {
    try {
      const r = type === 'weapons' ? await api.buyWeapon(index) : await api.buyArmor(index);
      notify(r.message);
      await refreshPlayer();
      await load();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Purchase failed');
    }
  };

  useKeyboard({
    Q: () => nav('/town'),
    ESCAPE: () => nav('/town'),
  }, [nav]);

  const title = type === 'weapons' ? "KING ARTHUR'S WEAPONS" : "ABDUL'S ARMOUR";

  if (!shop) return <Terminal title={title}><div className="c-muted">Loading...</div></Terminal>;

  return (
    <Terminal title={title} subtitle={`Gold: ${shop.current_gold.toLocaleString()}`}>
      <Separator />
      <div style={{ padding: '4px 0' }}>
        {shop.items.filter((_, i) => i <= shop.current_item_index + 1).map((item) => (
          <div key={item.index} className="shop-item">
            <span>
              {item.owned && <span className="c-green">* </span>}
              <span className={item.owned ? 'c-green' : 'c-white'}>{item.name}</span>
              <span className="c-muted"> (ATK: {item.stat_value})</span>
            </span>
            <span>
              {item.owned ? (
                <span className="c-green">EQUIPPED</span>
              ) : (
                <button
                  className="menu-option"
                  style={{ width: 'auto', display: 'inline' }}
                  onClick={() => buy(item.index)}
                  disabled={!item.can_buy}
                >
                  <span className="price">{item.price.toLocaleString()} gold</span>
                </button>
              )}
            </span>
          </div>
        ))}
      </div>
      <Separator />
      <button className="menu-option" onClick={() => nav('/town')}>
        <span className="shortcut">(Q)</span> Return to town
      </button>
    </Terminal>
  );
}

export function WeaponsScreen() {
  return <ShopScreen type="weapons" />;
}

export function ArmorScreen() {
  return <ShopScreen type="armor" />;
}
