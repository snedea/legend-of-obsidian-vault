import { useEffect, useState, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { Terminal } from '../components/Terminal';
import { MenuOption } from '../components/MenuOption';
import { Separator } from '../components/Separator';
import { useGame } from '../context/GameContext';
import { useKeyboard } from '../hooks/useKeyboard';
import * as api from '../services/api';

export function BankScreen() {
  const nav = useNavigate();
  const { notify, refreshPlayer } = useGame();
  const [bank, setBank] = useState<api.BankInfo | null>(null);
  const [mode, setMode] = useState<'menu' | 'deposit' | 'withdraw'>('menu');
  const [amount, setAmount] = useState('');

  const load = useCallback(async () => {
    const b = await api.getBank();
    setBank(b);
  }, []);

  useEffect(() => { load(); }, [load]);

  const doTransaction = async (all = false) => {
    if (!bank) return;
    const val = all
      ? (mode === 'deposit' ? bank.gold : bank.bank_gold)
      : parseInt(amount, 10);
    if (!val || val <= 0) return;

    try {
      const r = mode === 'deposit'
        ? await api.bankDeposit(val)
        : await api.bankWithdraw(val);
      notify(r.message);
      setBank({ ...bank, gold: r.gold, bank_gold: r.bank_gold });
      await refreshPlayer();
      setMode('menu');
      setAmount('');
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Transaction failed');
    }
  };

  const doRob = async () => {
    try {
      const r = await api.bankRob();
      notify(r.message);
      if (bank) setBank({ ...bank, gold: r.gold, bank_gold: r.bank_gold, can_rob: false });
      await refreshPlayer();
    } catch (e) {
      notify(e instanceof Error ? e.message : 'Robbery failed');
    }
  };

  useKeyboard(
    mode === 'menu'
      ? {
          D: () => setMode('deposit'),
          W: () => setMode('withdraw'),
          R: () => bank?.can_rob ? doRob() : undefined,
          Q: () => nav('/town'),
          ESCAPE: () => nav('/town'),
        }
      : {
          A: () => doTransaction(true),
          Q: () => { setMode('menu'); setAmount(''); },
          ESCAPE: () => { setMode('menu'); setAmount(''); },
        },
    [mode, bank, amount],
  );

  if (!bank) return <Terminal title="YE OLD BANK"><div className="c-muted">Loading...</div></Terminal>;

  return (
    <Terminal title="YE OLD BANK" subtitle="Safe Storage Since 1337">
      <Separator />
      <div className="c-white">Gold on hand: <span className="c-gold">{bank.gold.toLocaleString()}</span></div>
      <div className="c-white">Gold in bank: <span className="c-gold">{bank.bank_gold.toLocaleString()}</span></div>
      <Separator />

      {mode === 'menu' ? (
        <div style={{ padding: '4px 0' }}>
          <MenuOption shortcut="D" label="Deposit gold" onClick={() => setMode('deposit')} disabled={bank.gold <= 0} />
          <MenuOption shortcut="W" label="Withdraw gold" onClick={() => setMode('withdraw')} disabled={bank.bank_gold <= 0} />
          {bank.can_rob && <MenuOption shortcut="R" label="Rob the bank!" onClick={doRob} />}
          <MenuOption shortcut="Q" label="Return to town" onClick={() => nav('/town')} />
        </div>
      ) : (
        <div style={{ padding: '4px 0' }}>
          <div className="c-cyan">{mode === 'deposit' ? 'How much to deposit?' : 'How much to withdraw?'}</div>
          <div style={{ marginTop: 4 }}>
            <input
              type="number"
              value={amount}
              onChange={(e) => setAmount(e.target.value)}
              onKeyDown={(e) => { if (e.key === 'Enter') doTransaction(); }}
              autoFocus
              min={1}
              max={mode === 'deposit' ? bank.gold : bank.bank_gold}
              style={{ width: '200px' }}
            />
          </div>
          <MenuOption shortcut="A" label="All" onClick={() => doTransaction(true)} />
          <MenuOption shortcut="Q" label="Cancel" onClick={() => { setMode('menu'); setAmount(''); }} />
        </div>
      )}
    </Terminal>
  );
}
