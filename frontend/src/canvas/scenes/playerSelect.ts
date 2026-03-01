import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, oscillate, withAlpha, seededRandom } from '../utils';
import { drawTorch } from '../layers/terrain';
import { drawVaultWords } from '../layers/vaultText';

export const playerSelectScene: SceneDefinition = {
  id: 'playerSelect',
  render(ctx, sc) {
    // Scroll room
    fillRect(ctx, 0, 0, sc.width, sc.height, '#0e0c14');

    // Wooden shelves
    for (let row = 0; row < 4; row++) {
      const sy = 5 + row * 9;
      fillRect(ctx, 5, sy, sc.width - 10, 2, P.groundLight);

      // Scrolls on shelves
      const rng = seededRandom(210 + row);
      for (let i = 0; i < 6; i++) {
        const sx = 10 + i * 30 + Math.floor(rng() * 10);
        fillRect(ctx, sx, sy - 3, 2, 3, P.brightWhite);
        setPixel(ctx, sx, sy - 4, P.gold); // seal
      }
    }

    // Floor
    fillRect(ctx, 0, 38, sc.width, sc.height - 38, P.groundDark);

    // Candle-lit atmosphere
    drawTorch(ctx, 3, 15, sc);
    drawTorch(ctx, sc.width - 5, 15, sc);
    drawTorch(ctx, Math.floor(sc.width / 2), 3, sc);

    // Warm glow
    const glow = 0.03 + oscillate(sc.elapsed, 4) * 0.02;
    fillRect(ctx, 0, 0, sc.width, sc.height, withAlpha(P.brightYellow, glow));

    drawVaultWords(ctx, sc);
  },
};
