import type { SceneContext } from '../types';
import { drawText, measureText } from '../bitmapFont';
import { withAlpha } from '../utils';
import { P } from '../palette';

interface FloatingWord {
  text: string;
  x: number;
  y: number;
  vx: number;
  alpha: number;
  fadeDir: 'in' | 'hold' | 'out';
  life: number;
}

const MAX_VISIBLE = 2;
const SPAWN_MIN = 8;  // seconds between spawns
const SPAWN_MAX = 15;

let words: FloatingWord[] = [];
let nextSpawn = SPAWN_MIN;
let lastSpawnTime = 0;

export function resetVaultText(): void {
  words = [];
  nextSpawn = SPAWN_MIN;
  lastSpawnTime = 0;
}

export function drawVaultWords(ctx: CanvasRenderingContext2D, sc: SceneContext): void {
  if (sc.vaultWords.length === 0) return;

  // Spawn logic
  if (words.length < MAX_VISIBLE && sc.elapsed - lastSpawnTime > nextSpawn) {
    const text = sc.vaultWords[Math.floor(Math.random() * sc.vaultWords.length)];
    // Truncate long titles
    const display = text.length > 20 ? text.slice(0, 18) + '..' : text;
    words.push({
      text: display,
      x: sc.width + 2,
      y: 5 + Math.floor(Math.random() * 15),
      vx: -(3 + Math.random() * 4),
      alpha: 0,
      fadeDir: 'in',
      life: 8 + Math.random() * 4,
    });
    lastSpawnTime = sc.elapsed;
    nextSpawn = SPAWN_MIN + Math.random() * (SPAWN_MAX - SPAWN_MIN);
  }

  const dt = 1 / 15; // approx

  for (let i = words.length - 1; i >= 0; i--) {
    const w = words[i];
    w.x += w.vx * dt;
    w.life -= dt;

    // Fade stages
    if (w.fadeDir === 'in') {
      w.alpha = Math.min(1, w.alpha + dt * 1.5);
      if (w.alpha >= 0.8) w.fadeDir = 'hold';
    } else if (w.fadeDir === 'hold' && w.life < 2) {
      w.fadeDir = 'out';
    } else if (w.fadeDir === 'out') {
      w.alpha = Math.max(0, w.alpha - dt * 1.5);
    }

    // Remove dead words
    const tw = measureText(w.text);
    if (w.life <= 0 || w.alpha <= 0 || w.x + tw < -2) {
      words.splice(i, 1);
      continue;
    }

    // Draw with glow effect
    const color = withAlpha(P.brightMagenta, w.alpha * 0.5);
    drawText(ctx, w.text, Math.floor(w.x), Math.floor(w.y), color);
  }
}
