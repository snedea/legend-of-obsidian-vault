import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, withAlpha, seededRandom } from '../utils';
import { drawTorch } from '../layers/terrain';
import { drawFireflies } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';

export const violetScene: SceneDefinition = {
  id: 'violet',
  render(ctx, sc) {
    // Rose garden at dusk
    fillRect(ctx, 0, 0, sc.width, sc.height, '#14081a');

    // Night sky gradient
    for (let y = 0; y < 20; y++) {
      const t = y / 20;
      const alpha = t * 0.3;
      fillRect(ctx, 0, y, sc.width, 1, withAlpha(P.brightMagenta, alpha * 0.1));
    }

    // Ground
    fillRect(ctx, 0, 30, sc.width, sc.height - 30, '#1a101a');

    // Rose bushes
    const rng = seededRandom(240);
    for (let i = 0; i < 10; i++) {
      const rx = Math.floor(rng() * sc.width);
      const ry = 28 + Math.floor(rng() * 8);
      // Leaves
      fillRect(ctx, rx - 1, ry, 3, 2, P.treeDark);
      // Roses
      setPixel(ctx, rx, ry - 1, P.brightRed);
      if (rng() > 0.5) setPixel(ctx, rx + 1, ry - 1, P.red);
    }

    // Trellis arch
    const cx = Math.floor(sc.width / 2);
    for (let y = 15; y < 35; y++) {
      setPixel(ctx, cx - 15, y, P.groundLight);
      setPixel(ctx, cx + 15, y, P.groundLight);
    }
    for (let x = cx - 15; x <= cx + 15; x++) {
      const archY = 15 + Math.floor(Math.pow((x - cx) / 15, 2) * 5);
      setPixel(ctx, x, archY, P.groundLight);
    }
    // Climbing roses on trellis
    for (let i = 0; i < 6; i++) {
      const rx = cx - 14 + Math.floor(rng() * 28);
      const ry = 16 + Math.floor(rng() * 15);
      setPixel(ctx, rx, ry, P.brightRed);
    }

    // Candles
    drawTorch(ctx, cx - 20, 28, sc);
    drawTorch(ctx, cx + 20, 28, sc);

    drawFireflies(ctx, sc, 5, 640);

    drawVaultWords(ctx, sc);
  },
};
