import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, oscillate } from '../utils';
import { drawTorch } from '../layers/terrain';
import { drawVaultWords } from '../layers/vaultText';

export const warriorsScene: SceneDefinition = {
  id: 'warriors',
  render(ctx, sc) {
    // Grand hall
    fillRect(ctx, 0, 0, sc.width, sc.height, '#100e14');

    // Marble floor
    fillRect(ctx, 0, 32, sc.width, sc.height - 32, P.stoneMid);
    for (let x = 0; x < sc.width; x += 8) {
      fillRect(ctx, x, 32, 1, sc.height - 32, P.stoneDark);
    }

    // Pillars
    for (let i = 0; i < 5; i++) {
      const px = 15 + i * 40;
      fillRect(ctx, px, 5, 3, 27, P.stoneLight);
      fillRect(ctx, px - 1, 5, 5, 2, P.stoneLight);
      fillRect(ctx, px - 1, 30, 5, 2, P.stoneLight);
    }

    // Statues on pedestals
    for (let i = 0; i < 3; i++) {
      const sx = 35 + i * 55;
      // Pedestal
      fillRect(ctx, sx - 2, 29, 5, 3, P.stoneMid);
      // Figure
      fillRect(ctx, sx - 1, 22, 3, 7, P.brightBlack);
      fillRect(ctx, sx, 20, 1, 2, P.brightBlack);
      // Sword
      fillRect(ctx, sx + 2, 23, 1, 4, P.brightWhite);
    }

    // Banners
    const bannerColors = [P.red, P.blue, P.brightRed];
    for (let i = 0; i < 3; i++) {
      const bx = 25 + i * 55;
      const sway = Math.round(oscillate(sc.elapsed, 4, i * 2) * 1 - 0.5);
      fillRect(ctx, bx + sway, 6, 4, 10, bannerColors[i]);
      fillRect(ctx, bx, 5, 6, 1, P.gold);
    }

    // Torches
    drawTorch(ctx, 8, 12, sc);
    drawTorch(ctx, sc.width - 10, 12, sc);

    drawVaultWords(ctx, sc);
  },
};
