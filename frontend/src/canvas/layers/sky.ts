import type { SceneContext } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, lerpColor, seededRandom, oscillate, withAlpha } from '../utils';

interface SkyGradient {
  top: string;
  mid: string;
  bottom: string;
}

const SKY_COLORS: Record<string, SkyGradient> = {
  dawn:  { top: P.skyDawnTop,  mid: P.skyDawnMid,  bottom: P.skyDawnBottom },
  day:   { top: P.skyDayTop,   mid: P.skyDayMid,   bottom: P.skyDayBottom },
  dusk:  { top: P.skyDuskTop,  mid: P.skyDuskMid,  bottom: P.skyDuskBottom },
  night: { top: P.skyNightTop, mid: P.skyNightMid, bottom: P.skyNightBottom },
};

/** Draw stepped gradient sky background */
export function drawSky(ctx: CanvasRenderingContext2D, sc: SceneContext, groundY = 35): void {
  const grad = SKY_COLORS[sc.time];
  const bandH = 3;

  for (let y = 0; y < groundY; y += bandH) {
    const t = y / groundY;
    const color = t < 0.5
      ? lerpColor(grad.top, grad.mid, t * 2)
      : lerpColor(grad.mid, grad.bottom, (t - 0.5) * 2);
    fillRect(ctx, 0, y, sc.width, bandH, color);
  }
}

/** Draw twinkling stars (night / dusk / dawn only) */
export function drawStars(ctx: CanvasRenderingContext2D, sc: SceneContext, groundY = 35): void {
  if (sc.time === 'day') return;

  const alpha = sc.time === 'night' ? 0.9 : 0.4;
  const count = sc.time === 'night' ? 30 : 12;
  const rng = seededRandom(42);

  for (let i = 0; i < count; i++) {
    const sx = Math.floor(rng() * sc.width);
    const sy = Math.floor(rng() * (groundY - 4));
    const twinkle = oscillate(sc.elapsed, 1.5 + rng() * 3, i * 0.7);
    const a = alpha * (0.3 + twinkle * 0.7);
    setPixel(ctx, sx, sy, withAlpha(P.brightWhite, a));
  }
}

/** Draw sun or moon */
export function drawCelestial(ctx: CanvasRenderingContext2D, sc: SceneContext): void {
  const cx = Math.floor(sc.width * 0.75);

  if (sc.time === 'day' || sc.time === 'dawn') {
    // Sun
    const cy = sc.time === 'dawn' ? 18 : 8;
    const color = sc.time === 'dawn' ? P.brightYellow : P.gold;
    fillRect(ctx, cx - 1, cy - 1, 3, 3, color);
    // Rays
    if (sc.time === 'day') {
      const show = Math.floor(sc.elapsed * 2) % 2 === 0;
      if (show) {
        setPixel(ctx, cx, cy - 2, withAlpha(color, 0.6));
        setPixel(ctx, cx, cy + 2, withAlpha(color, 0.6));
        setPixel(ctx, cx - 2, cy, withAlpha(color, 0.6));
        setPixel(ctx, cx + 2, cy, withAlpha(color, 0.6));
      }
    }
  } else if (sc.time === 'night' || sc.time === 'dusk') {
    // Moon
    const cy = sc.time === 'night' ? 6 : 14;
    fillRect(ctx, cx - 1, cy - 1, 3, 3, P.brightWhite);
    // Crescent shadow
    setPixel(ctx, cx + 1, cy - 1, P.skyNightTop);
    setPixel(ctx, cx + 1, cy, P.skyNightMid);
  }
}

/** Draw drifting clouds */
export function drawClouds(
  ctx: CanvasRenderingContext2D, sc: SceneContext,
  count = 3, groundY = 35,
): void {
  if (sc.weather === 'clear' && sc.time === 'night') return;

  const cloudCount = sc.weather === 'cloudy' ? count + 3 : count;
  const rng = seededRandom(77);

  for (let i = 0; i < cloudCount; i++) {
    const baseX = rng() * sc.width;
    const y = 4 + Math.floor(rng() * (groundY * 0.4));
    const speed = 2 + rng() * 4;
    const w = 5 + Math.floor(rng() * 8);

    const x = ((baseX + sc.elapsed * speed) % (sc.width + w * 2)) - w;

    const alpha = sc.weather === 'fog' ? 0.5 : 0.25;
    const color = sc.time === 'night'
      ? withAlpha(P.brightBlack, alpha)
      : withAlpha(P.white, alpha);

    // Cloud blob: 2-3 px tall, w wide
    fillRect(ctx, Math.floor(x), y, w, 2, color);
    fillRect(ctx, Math.floor(x) + 1, y - 1, w - 2, 1, color);
  }
}

/** Draw fog overlay */
export function drawFog(ctx: CanvasRenderingContext2D, sc: SceneContext): void {
  if (sc.weather !== 'fog') return;
  const alpha = 0.15 + oscillate(sc.elapsed, 6) * 0.1;
  fillRect(ctx, 0, 0, sc.width, sc.height, withAlpha(P.white, alpha));
}
