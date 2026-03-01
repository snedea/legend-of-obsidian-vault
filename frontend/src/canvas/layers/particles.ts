import type { SceneContext } from '../types';
import { P } from '../palette';
import { setPixel, withAlpha, seededRandom } from '../utils';

interface Particle {
  x: number;
  y: number;
  vx: number;
  vy: number;
  life: number;
  maxLife: number;
  color: string;
}

export class ParticleSystem {
  private particles: Particle[] = [];

  constructor() {}

  /** Spawn a single particle */
  spawn(
    x: number, y: number,
    vx: number, vy: number,
    life: number, color: string,
  ): void {
    if (this.particles.length > 200) return;
    this.particles.push({ x, y, vx, vy, life, maxLife: life, color });
  }

  /** Update and draw all particles */
  update(ctx: CanvasRenderingContext2D, dt: number): void {
    for (let i = this.particles.length - 1; i >= 0; i--) {
      const p = this.particles[i];
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.life -= dt;

      if (p.life <= 0) {
        this.particles.splice(i, 1);
        continue;
      }

      const alpha = Math.min(1, p.life / p.maxLife);
      setPixel(ctx, Math.floor(p.x), Math.floor(p.y), withAlpha(p.color, alpha));
    }
  }

  get count(): number {
    return this.particles.length;
  }
}

/** Draw weather-based rain streaks */
export function drawRain(ctx: CanvasRenderingContext2D, sc: SceneContext): void {
  if (sc.weather !== 'rain') return;

  const rng = seededRandom(sc.frame * 3);
  const count = 25;
  for (let i = 0; i < count; i++) {
    const x = Math.floor(rng() * sc.width);
    const y = Math.floor(rng() * sc.height);
    setPixel(ctx, x, y, withAlpha(P.brightCyan, 0.4));
    if (y + 1 < sc.height) {
      setPixel(ctx, x, y + 1, withAlpha(P.brightCyan, 0.2));
    }
  }
}

/** Draw weather-based snow */
export function drawSnow(ctx: CanvasRenderingContext2D, sc: SceneContext): void {
  if (sc.weather !== 'snow') return;

  const rng = seededRandom(1000);
  const count = 20;
  for (let i = 0; i < count; i++) {
    const baseX = rng() * sc.width;
    const baseY = rng() * sc.height;
    const drift = Math.sin(sc.elapsed * 0.5 + i * 2) * 3;
    const fall = (sc.elapsed * (2 + rng() * 3) + baseY) % sc.height;
    const x = Math.floor((baseX + drift) % sc.width);
    const y = Math.floor(fall);
    setPixel(ctx, x, y, withAlpha(P.brightWhite, 0.7));
  }
}

/** Draw fireflies (warm, gentle floating lights) */
export function drawFireflies(ctx: CanvasRenderingContext2D, sc: SceneContext, count = 5, seed = 600): void {
  const rng = seededRandom(seed);
  for (let i = 0; i < count; i++) {
    const baseX = rng() * sc.width;
    const baseY = 20 + rng() * (sc.height - 25);
    const x = Math.floor(baseX + Math.sin(sc.elapsed * 0.8 + i * 3) * 8);
    const y = Math.floor(baseY + Math.cos(sc.elapsed * 0.6 + i * 2) * 4);
    const alpha = 0.3 + Math.sin(sc.elapsed * 2 + i * 5) * 0.3;
    if (x >= 0 && x < sc.width && y >= 0 && y < sc.height) {
      setPixel(ctx, x, y, withAlpha(P.brightYellow, Math.max(0, alpha)));
    }
  }
}

/** Draw smoke rising from a point */
export function emitSmoke(ps: ParticleSystem, x: number, y: number, sc: SceneContext): void {
  if (sc.frame % 4 !== 0) return;
  ps.spawn(x, y, (Math.random() - 0.5) * 2, -3 - Math.random() * 2, 2 + Math.random(), P.brightBlack);
}

/** Draw forge sparks */
export function emitSparks(ps: ParticleSystem, x: number, y: number, sc: SceneContext): void {
  if (sc.frame % 3 !== 0) return;
  const angle = Math.random() * Math.PI;
  const speed = 4 + Math.random() * 6;
  ps.spawn(x, y, Math.cos(angle) * speed, -Math.sin(angle) * speed, 0.5 + Math.random() * 0.5, P.brightYellow);
}

/** Draw dripping water drops */
export function emitDrips(ps: ParticleSystem, x: number, y: number, sc: SceneContext): void {
  if (sc.frame % 20 !== 0) return;
  ps.spawn(x, y, 0, 6 + Math.random() * 4, 1, P.brightCyan);
}
