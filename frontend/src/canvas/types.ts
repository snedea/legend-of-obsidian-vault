export type SceneId =
  | 'town' | 'forest' | 'combat' | 'bank' | 'healer'
  | 'inn' | 'barRoom' | 'cavern' | 'fairy' | 'gateway'
  | 'werewolf' | 'weaponShop' | 'armorShop' | 'training'
  | 'warriors' | 'news' | 'start' | 'charCreate'
  | 'playerSelect' | 'stats' | 'otherPlaces' | 'xenon'
  | 'violet' | 'bribe' | 'gems' | 'nameChange'
  | 'vault' | 'settings';

export type TimeOfDay = 'dawn' | 'day' | 'dusk' | 'night';
export type Weather = 'clear' | 'rain' | 'snow' | 'fog' | 'cloudy';

export interface SceneContext {
  time: TimeOfDay;
  weather: Weather;
  frame: number;
  elapsed: number; // seconds since scene started
  width: number;   // logical pixels
  height: number;  // logical pixels
  vaultWords: string[];
}

export interface SceneDefinition {
  id: SceneId;
  render: (ctx: CanvasRenderingContext2D, scene: SceneContext) => void;
}
