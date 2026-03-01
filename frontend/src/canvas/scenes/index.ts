import type { SceneId, SceneDefinition } from '../types';

import { townScene } from './town';
import { forestScene } from './forest';
import { combatScene } from './combat';
import { bankScene } from './bank';
import { healerScene } from './healer';
import { innScene } from './inn';
import { barRoomScene } from './barRoom';
import { cavernScene } from './cavern';
import { fairyScene } from './fairy';
import { gatewayScene } from './gateway';
import { werewolfScene } from './werewolf';
import { weaponShopScene } from './weaponShop';
import { armorShopScene } from './armorShop';
import { trainingScene } from './training';
import { warriorsScene } from './warriors';
import { newsScene } from './news';
import { startScene } from './start';
import { charCreateScene } from './charCreate';
import { playerSelectScene } from './playerSelect';
import { statsScene } from './stats';
import { otherPlacesScene } from './otherPlaces';
import { xenonScene } from './xenon';
import { violetScene } from './violet';
import { bribeScene } from './bribe';
import { gemsScene } from './gems';
import { nameChangeScene } from './nameChange';
import { vaultScene } from './vault';
import { settingsScene } from './settings';

const registry: Record<SceneId, SceneDefinition> = {
  town: townScene,
  forest: forestScene,
  combat: combatScene,
  bank: bankScene,
  healer: healerScene,
  inn: innScene,
  barRoom: barRoomScene,
  cavern: cavernScene,
  fairy: fairyScene,
  gateway: gatewayScene,
  werewolf: werewolfScene,
  weaponShop: weaponShopScene,
  armorShop: armorShopScene,
  training: trainingScene,
  warriors: warriorsScene,
  news: newsScene,
  start: startScene,
  charCreate: charCreateScene,
  playerSelect: playerSelectScene,
  stats: statsScene,
  otherPlaces: otherPlacesScene,
  xenon: xenonScene,
  violet: violetScene,
  bribe: bribeScene,
  gems: gemsScene,
  nameChange: nameChangeScene,
  vault: vaultScene,
  settings: settingsScene,
};

export function getScene(id: SceneId): SceneDefinition | undefined {
  return registry[id];
}
