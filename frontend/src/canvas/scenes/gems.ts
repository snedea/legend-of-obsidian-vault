import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, oscillate, withAlpha, seededRandom } from '../utils';
import { drawTorch } from '../layers/terrain';
import { ParticleSystem } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';

const sparkles = new ParticleSystem();

export const gemsScene: SceneDefinition = {
  id: 'gems',
  render(ctx, sc) {
    // Crystal cavern
    fillRect(ctx, 0, 0, sc.width, sc.height, '#0a0814');

    // Rocky walls
    const rng = seededRandom(260);
    for (let y = 0; y < sc.height; y += 3) {
      for (let x = 0; x < sc.width; x += 5) {
        fillRect(ctx, x, y, 4, 2, rng() > 0.5 ? '#1a1428' : '#0e0a18');
      }
    }

    // Crystal formations
    const gemColors = [P.brightRed, P.brightGreen, P.brightBlue, P.brightMagenta, P.brightCyan, P.brightYellow];
    for (let i = 0; i < 12; i++) {
      const gx = 10 + Math.floor(rng() * (sc.width - 20));
      const gy = 5 + Math.floor(rng() * 30);
      const color = gemColors[Math.floor(rng() * gemColors.length)];
      const h = 2 + Math.floor(rng() * 4);

      // Diamond/crystal shape
      for (let r = 0; r < h; r++) {
        const w = r < h / 2 ? r + 1 : h - r;
        fillRect(ctx, gx - Math.floor(w / 2), gy + r, w, 1, color);
      }

      // Glow
      const glow = oscillate(sc.elapsed, 1.5 + rng() * 2, i * 0.7);
      setPixel(ctx, gx, gy, withAlpha(P.brightWhite, glow * 0.6));
    }

    // Sparkle particles
    if (sc.frame % 4 === 0) {
      const sx = 10 + Math.random() * (sc.width - 20);
      const sy = 5 + Math.random() * 30;
      sparkles.spawn(sx, sy, (Math.random() - 0.5) * 3, -1 - Math.random() * 2, 0.6,
        gemColors[Math.floor(Math.random() * gemColors.length)]);
    }
    sparkles.update(ctx, 1 / 15);

    drawTorch(ctx, 3, 15, sc);
    drawTorch(ctx, sc.width - 5, 15, sc);

    drawVaultWords(ctx, sc);
  },
};
