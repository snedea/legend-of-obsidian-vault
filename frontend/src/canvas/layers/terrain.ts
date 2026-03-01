import type { SceneContext } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, seededRandom, oscillate, withAlpha } from '../utils';

/** Draw flat ground fill from groundY to bottom */
export function drawGround(
  ctx: CanvasRenderingContext2D, sc: SceneContext,
  groundY: number, color = P.groundMid,
): void {
  fillRect(ctx, 0, groundY, sc.width, sc.height - groundY, color);
  // Slight noise for texture
  const rng = seededRandom(123);
  for (let i = 0; i < 40; i++) {
    const x = Math.floor(rng() * sc.width);
    const y = groundY + Math.floor(rng() * (sc.height - groundY));
    setPixel(ctx, x, y, rng() > 0.5 ? P.groundDark : P.groundLight);
  }
}

/** Draw a simple triangular mountain silhouette */
export function drawMountains(
  ctx: CanvasRenderingContext2D, sc: SceneContext,
  groundY: number, count = 3,
): void {
  const rng = seededRandom(200);
  for (let i = 0; i < count; i++) {
    const cx = Math.floor((sc.width / (count + 1)) * (i + 1) + (rng() - 0.5) * 20);
    const h = 8 + Math.floor(rng() * 10);
    const halfW = 8 + Math.floor(rng() * 12);
    const color = rng() > 0.5 ? P.brightBlack : P.stoneDark;

    for (let row = 0; row < h; row++) {
      const t = row / h;
      const w = Math.floor(halfW * t);
      const y = groundY - h + row;
      fillRect(ctx, cx - w, y, w * 2 + 1, 1, color);
    }
    // Snow cap
    if (h > 10) {
      fillRect(ctx, cx - 1, groundY - h, 3, 2, P.brightWhite);
      setPixel(ctx, cx, groundY - h - 1, P.brightWhite);
    }
  }
}

/** Draw a pixel tree (simple triangle + trunk) */
export function drawTree(
  ctx: CanvasRenderingContext2D,
  x: number, groundY: number,
  height: number, sc: SceneContext,
  color = P.treeMid,
): void {
  const trunkH = Math.max(2, Math.floor(height * 0.25));
  const crownH = height - trunkH;

  // Trunk
  fillRect(ctx, x, groundY - trunkH, 1, trunkH, P.groundLight);

  // Crown -- triangle, sway slightly
  const sway = Math.round(oscillate(sc.elapsed, 3 + (x % 5), x) * 1 - 0.5);
  for (let row = 0; row < crownH; row++) {
    const t = row / crownH;
    const w = Math.max(1, Math.floor(t * (height * 0.5)));
    const cy = groundY - trunkH - crownH + row;
    fillRect(ctx, x - w + sway, cy, w * 2 + 1, 1, color);
  }
}

/** Draw a row of trees at varying heights */
export function drawTreeLine(
  ctx: CanvasRenderingContext2D, sc: SceneContext,
  groundY: number, count = 8, minH = 6, maxH = 14,
  color = P.treeMid, seed = 300,
): void {
  const rng = seededRandom(seed);
  const spacing = Math.floor(sc.width / count);
  for (let i = 0; i < count; i++) {
    const x = Math.floor(i * spacing + rng() * spacing * 0.6);
    const h = minH + Math.floor(rng() * (maxH - minH));
    drawTree(ctx, x, groundY, h, sc, color);
  }
}

/** Draw cobblestone / path pattern */
export function drawPath(
  ctx: CanvasRenderingContext2D, sc: SceneContext,
  y: number, h = 3,
): void {
  fillRect(ctx, 0, y, sc.width, h, P.stoneMid);
  const rng = seededRandom(400);
  for (let i = 0; i < 20; i++) {
    const px = Math.floor(rng() * sc.width);
    const py = y + Math.floor(rng() * h);
    setPixel(ctx, px, py, rng() > 0.5 ? P.stoneDark : P.stoneLight);
  }
}

/** Draw water / river strip */
export function drawWater(
  ctx: CanvasRenderingContext2D, sc: SceneContext,
  y: number, h = 3,
): void {
  fillRect(ctx, 0, y, sc.width, h, P.waterDark);
  // Animated ripples
  const rng = seededRandom(500);
  for (let i = 0; i < 12; i++) {
    const rx = (Math.floor(rng() * sc.width) + Math.floor(sc.elapsed * 3)) % sc.width;
    const ry = y + Math.floor(rng() * h);
    setPixel(ctx, rx, ry, withAlpha(P.waterLight, 0.6));
  }
}

/** Draw a simple building silhouette */
export function drawBuilding(
  ctx: CanvasRenderingContext2D,
  x: number, groundY: number,
  w: number, h: number,
  color = P.stoneDark, roofColor = P.red,
): void {
  // Walls
  fillRect(ctx, x, groundY - h, w, h, color);
  // Roof (triangle)
  for (let row = 0; row < 3; row++) {
    const rw = Math.floor((w / 2) + 1 - row);
    fillRect(ctx, x + Math.floor(w / 2) - rw, groundY - h - 3 + row, rw * 2 + 1, 1, roofColor);
  }
  // Door
  fillRect(ctx, x + Math.floor(w / 2), groundY - 2, 1, 2, P.groundDark);
  // Window
  if (w >= 5) {
    setPixel(ctx, x + 1, groundY - h + 2, P.brightYellow);
    setPixel(ctx, x + w - 2, groundY - h + 2, P.brightYellow);
  }
}

/** Draw a torch / flame at position */
export function drawTorch(
  ctx: CanvasRenderingContext2D,
  x: number, y: number,
  sc: SceneContext,
): void {
  // Stick
  fillRect(ctx, x, y, 1, 3, P.groundLight);
  // Flame (flickers)
  const flicker = oscillate(sc.elapsed, 0.3, x * 7);
  const color = flicker > 0.5 ? P.brightYellow : P.brightRed;
  setPixel(ctx, x, y - 1, color);
  if (flicker > 0.7) setPixel(ctx, x, y - 2, withAlpha(P.brightYellow, 0.5));
}
