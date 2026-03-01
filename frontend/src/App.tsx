import { useCallback, useEffect, useRef } from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { GameProvider } from './context/GameContext';
import { Notification } from './components/Notification';

import { StartScreen } from './screens/StartScreen';
import { CharacterCreation } from './screens/CharacterCreation';
import { PlayerSelect } from './screens/PlayerSelect';
import { TownSquare } from './screens/TownSquare';
import { ForestScreen } from './screens/ForestScreen';
import { CombatScreen } from './screens/CombatScreen';
import { BankScreen } from './screens/BankScreen';
import { HealerScreen } from './screens/HealerScreen';
import { WeaponsScreen, ArmorScreen } from './screens/WeaponsScreen';
import { TrainingScreen } from './screens/TrainingScreen';
import { StatsScreen } from './screens/StatsScreen';
import { WarriorsScreen } from './screens/WarriorsScreen';
import { InnScreen } from './screens/InnScreen';
import { DailyNewsScreen } from './screens/DailyNewsScreen';
import { OtherPlaces } from './screens/OtherPlaces';
import { CavernScreen } from './screens/CavernScreen';
import { FairyScreen } from './screens/FairyScreen';
import { BarakScreen } from './screens/BarakScreen';
import { XenonScreen } from './screens/XenonScreen';
import { WerewolfScreen } from './screens/WerewolfScreen';
import { GatewayScreen } from './screens/GatewayScreen';
import { BarRoomScreen } from './screens/BarRoomScreen';
import { GemTradingScreen } from './screens/GemTradingScreen';
import { VioletScreen } from './screens/VioletScreen';
import { BribeScreen } from './screens/BribeScreen';
import { NameChangeScreen } from './screens/NameChangeScreen';
import { SettingsScreen } from './screens/SettingsScreen';
import { VaultScreen } from './screens/VaultScreen';

const api = (window as unknown as { electronAPI?: {
  showTrafficLights?: () => void;
  hideTrafficLights?: () => void;
} }).electronAPI;

function TrafficLightZone() {
  const hideTimer = useRef<ReturnType<typeof setTimeout> | null>(null);

  useEffect(() => {
    return () => {
      if (hideTimer.current) {
        clearTimeout(hideTimer.current);
        hideTimer.current = null;
      }
    };
  }, []);

  const handleEnter = useCallback(() => {
    if (hideTimer.current) clearTimeout(hideTimer.current);
    hideTimer.current = null;
    api?.showTrafficLights?.();
  }, []);

  const handleLeave = useCallback(() => {
    hideTimer.current = setTimeout(() => {
      hideTimer.current = null;
      api?.hideTrafficLights?.();
    }, 800);
  }, []);

  return (
    <div
      className="traffic-light-zone"
      onMouseEnter={handleEnter}
      onMouseLeave={handleLeave}
    />
  );
}

export default function App() {
  return (
    <BrowserRouter>
      <GameProvider>
        <div className="drag-region" />
        <TrafficLightZone />
        <div className="crt-overlay" />
        <div className="crt-vignette" />
        <Routes>
          <Route path="/" element={<StartScreen />} />
          <Route path="/create" element={<CharacterCreation />} />
          <Route path="/select" element={<PlayerSelect />} />
          <Route path="/town" element={<TownSquare />} />
          <Route path="/forest" element={<ForestScreen />} />
          <Route path="/combat" element={<CombatScreen />} />
          <Route path="/town/bank" element={<BankScreen />} />
          <Route path="/town/healer" element={<HealerScreen />} />
          <Route path="/town/weapons" element={<WeaponsScreen />} />
          <Route path="/town/armor" element={<ArmorScreen />} />
          <Route path="/town/training" element={<TrainingScreen />} />
          <Route path="/town/stats" element={<StatsScreen />} />
          <Route path="/town/warriors" element={<WarriorsScreen />} />
          <Route path="/town/inn" element={<InnScreen />} />
          <Route path="/town/inn/bar" element={<BarRoomScreen />} />
          <Route path="/town/inn/gems" element={<GemTradingScreen />} />
          <Route path="/town/inn/violet" element={<VioletScreen />} />
          <Route path="/town/inn/bribe" element={<BribeScreen />} />
          <Route path="/town/inn/name-change" element={<NameChangeScreen />} />
          <Route path="/town/news" element={<DailyNewsScreen />} />
          <Route path="/places" element={<OtherPlaces />} />
          <Route path="/places/cavern" element={<CavernScreen />} />
          <Route path="/places/fairy" element={<FairyScreen />} />
          <Route path="/places/barak" element={<BarakScreen />} />
          <Route path="/places/xenon" element={<XenonScreen />} />
          <Route path="/places/werewolf" element={<WerewolfScreen />} />
          <Route path="/places/gateway" element={<GatewayScreen />} />
          <Route path="/settings" element={<SettingsScreen />} />
          <Route path="/settings/vault" element={<VaultScreen />} />
        </Routes>
        <Notification />
      </GameProvider>
    </BrowserRouter>
  );
}
