/** Fill a rectangle at logical pixel coordinates */
export function fillRect(
  ctx: CanvasRenderingContext2D,
  x: number, y: number, w: number, h: number,
  color: string,
): void {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, w, h);
}

/** Set a single logical pixel */
export function setPixel(
  ctx: CanvasRenderingContext2D,
  x: number, y: number,
  color: string,
): void {
  ctx.fillStyle = color;
  ctx.fillRect(x, y, 1, 1);
}

/** Seeded pseudo-random number generator (mulberry32) */
export function seededRandom(seed: number): () => number {
  let s = seed | 0;
  return () => {
    s = (s + 0x6d2b79f5) | 0;
    let t = Math.imul(s ^ (s >>> 15), 1 | s);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Parse hex color to [r, g, b] */
function hexToRgb(hex: string): [number, number, number] {
  const n = parseInt(hex.slice(1), 16);
  return [(n >> 16) & 0xff, (n >> 8) & 0xff, n & 0xff];
}

/** Linearly interpolate between two hex colors, t in [0, 1] */
export function lerpColor(a: string, b: string, t: number): string {
  const [ar, ag, ab] = hexToRgb(a);
  const [br, bg, bb] = hexToRgb(b);
  const clamp = (v: number) => Math.max(0, Math.min(255, Math.round(v)));
  const r = clamp(ar + (br - ar) * t);
  const g = clamp(ag + (bg - ag) * t);
  const bl = clamp(ab + (bb - ab) * t);
  return `rgb(${r},${g},${bl})`;
}

/** Oscillate between 0 and 1 using a sine wave */
export function oscillate(elapsed: number, period: number, phase = 0): number {
  return (Math.sin((elapsed / period) * Math.PI * 2 + phase) + 1) / 2;
}

/** Return rgba string with alpha */
export function withAlpha(hex: string, alpha: number): string {
  const [r, g, b] = hexToRgb(hex);
  return `rgba(${r},${g},${b},${alpha})`;
}

/** Hash a string to a number (for seeding) */
export function hashStr(s: string): number {
  let h = 0;
  for (let i = 0; i < s.length; i++) {
    h = ((h << 5) - h + s.charCodeAt(i)) | 0;
  }
  return h;
}
