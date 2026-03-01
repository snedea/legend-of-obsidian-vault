import type { TimeOfDay, Weather } from './types';

const TIMES: TimeOfDay[] = ['dawn', 'day', 'dusk', 'night'];
const WEATHERS: Weather[] = ['clear', 'clear', 'clear', 'rain', 'snow', 'fog', 'cloudy'];

function pick<T>(arr: T[]): T {
  return arr[Math.floor(Math.random() * arr.length)];
}

export function getSessionEnvironment(): { time: TimeOfDay; weather: Weather } {
  const stored = sessionStorage.getItem('lov-env');
  if (stored) {
    try {
      const parsed = JSON.parse(stored);
      if (parsed.time && parsed.weather) return parsed;
    } catch { /* regenerate */ }
  }
  const env = { time: pick(TIMES), weather: pick(WEATHERS) };
  sessionStorage.setItem('lov-env', JSON.stringify(env));
  return env;
}
