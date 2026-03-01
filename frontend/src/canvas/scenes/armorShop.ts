import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, seededRandom } from '../utils';
import { drawTorch } from '../layers/terrain';
import { ParticleSystem, emitSparks } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';

const sparks = new ParticleSystem();

export const armorShopScene: SceneDefinition = {
  id: 'armorShop',
  render(ctx, sc) {
    // Workshop interior
    fillRect(ctx, 0, 0, sc.width, sc.height, '#12100e');

    // Stone floor
    const rng = seededRandom(180);
    for (let y = 28; y < sc.height; y += 2) {
      for (let x = 0; x < sc.width; x += 4) {
        fillRect(ctx, x, y, 3, 1, rng() > 0.5 ? P.stoneDark : '#1a1818');
      }
    }

    // Armor stands
    for (let i = 0; i < 4; i++) {
      const ax = 20 + i * 40;
      // Stand pole
      fillRect(ctx, ax, 15, 1, 20, P.stoneLight);
      fillRect(ctx, ax - 2, 35, 5, 1, P.stoneMid);
      // Armor silhouette (chest piece)
      fillRect(ctx, ax - 3, 16, 7, 8, P.brightBlack);
      fillRect(ctx, ax - 2, 17, 5, 6, P.stoneMid);
      // Helmet
      fillRect(ctx, ax - 1, 14, 3, 2, P.stoneLight);
    }

    // Anvil + hammering
    const anvX = sc.width - 35;
    fillRect(ctx, anvX, 32, 10, 2, P.stoneLight);
    fillRect(ctx, anvX + 2, 34, 6, 4, P.stoneMid);

    // Sparks from hammering
    if (sc.frame % 25 < 4) {
      emitSparks(sparks, anvX + 5, 31, sc);
    }
    sparks.update(ctx, 1 / 15);

    drawTorch(ctx, 8, 10, sc);
    drawTorch(ctx, sc.width - 12, 10, sc);

    drawVaultWords(ctx, sc);
  },
};
