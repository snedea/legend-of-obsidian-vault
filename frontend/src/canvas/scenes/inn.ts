import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, oscillate, seededRandom, withAlpha } from '../utils';
import { drawTorch } from '../layers/terrain';
import { drawVaultWords } from '../layers/vaultText';
import { ParticleSystem, emitSmoke } from '../layers/particles';

const smoke = new ParticleSystem();

export const innScene: SceneDefinition = {
  id: 'inn',
  render(ctx, sc) {
    // Warm interior
    fillRect(ctx, 0, 0, sc.width, sc.height, '#1a1410');

    // Wooden walls
    const rng = seededRandom(110);
    for (let y = 0; y < 25; y += 2) {
      fillRect(ctx, 0, y, sc.width, 1, rng() > 0.5 ? '#2a1a10' : '#1a1008');
    }

    // Floor
    fillRect(ctx, 0, 25, sc.width, sc.height - 25, '#1a1008');
    for (let x = 0; x < sc.width; x += 6) {
      fillRect(ctx, x, 25, 1, sc.height - 25, '#0a0804');
    }

    // Fireplace
    const fx = 20;
    fillRect(ctx, fx, 15, 16, 15, P.stoneDark);
    fillRect(ctx, fx + 2, 18, 12, 12, P.black);
    // Fire
    const fireH = 4 + Math.floor(oscillate(sc.elapsed, 0.5) * 3);
    for (let r = 0; r < fireH; r++) {
      const w = fireH - r;
      const color = r < 2 ? P.brightYellow : P.brightRed;
      fillRect(ctx, fx + 8 - Math.floor(w / 2), 30 - r - 1, w, 1, color);
    }

    // Firelight glow
    const glowA = 0.05 + oscillate(sc.elapsed, 0.5) * 0.05;
    fillRect(ctx, 0, 15, 50, 25, withAlpha(P.brightYellow, glowA));

    // Candles on tables
    drawTorch(ctx, 80, 28, sc);
    drawTorch(ctx, 130, 28, sc);
    drawTorch(ctx, 180, 28, sc);

    // Tables
    fillRect(ctx, 75, 32, 14, 2, P.groundLight);
    fillRect(ctx, 125, 32, 14, 2, P.groundLight);

    // Bed area
    fillRect(ctx, sc.width - 30, 26, 16, 8, P.blue);
    fillRect(ctx, sc.width - 30, 24, 16, 2, P.white);

    emitSmoke(smoke, fx + 8, 15, sc);
    smoke.update(ctx, 1 / 15);

    drawVaultWords(ctx, sc);
  },
};
