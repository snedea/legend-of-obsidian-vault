import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, oscillate, withAlpha, seededRandom } from '../utils';
import { drawTorch } from '../layers/terrain';
import { drawVaultWords } from '../layers/vaultText';

export const xenonScene: SceneDefinition = {
  id: 'xenon',
  render(ctx, sc) {
    // Storage room
    fillRect(ctx, 0, 0, sc.width, sc.height, '#100e0a');

    // Stone walls
    const rng = seededRandom(230);
    for (let y = 0; y < 28; y += 3) {
      for (let x = 0; x < sc.width; x += 5) {
        fillRect(ctx, x, y, 4, 2, rng() > 0.5 ? P.stoneDark : '#1a1410');
      }
    }

    // Floor
    fillRect(ctx, 0, 28, sc.width, sc.height - 28, P.groundDark);

    // Treasure chests
    for (let i = 0; i < 3; i++) {
      const tx = 25 + i * 55;
      fillRect(ctx, tx, 26, 10, 6, P.groundMid);
      fillRect(ctx, tx, 25, 10, 2, P.groundLight);
      // Latch
      setPixel(ctx, tx + 5, 26, P.gold);
      // Gold glow
      const glow = oscillate(sc.elapsed, 2, i * 1.5);
      fillRect(ctx, tx + 1, 28, 8, 2, withAlpha(P.brightYellow, glow * 0.15));
    }

    // Bags of coins
    for (let i = 0; i < 4; i++) {
      const bx = 15 + i * 45;
      fillRect(ctx, bx, 33, 4, 4, P.yellow);
      setPixel(ctx, bx + 2, 32, P.yellow);
    }

    // Scattered coins
    for (let i = 0; i < 8; i++) {
      const cx = Math.floor(rng() * sc.width);
      const cy = 30 + Math.floor(rng() * 10);
      setPixel(ctx, cx, cy, P.gold);
    }

    drawTorch(ctx, 5, 10, sc);
    drawTorch(ctx, sc.width - 8, 10, sc);

    drawVaultWords(ctx, sc);
  },
};
