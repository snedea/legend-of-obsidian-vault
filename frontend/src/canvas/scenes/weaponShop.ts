import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, oscillate, withAlpha, seededRandom } from '../utils';
import { drawTorch } from '../layers/terrain';
import { ParticleSystem, emitSparks } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';

const sparks = new ParticleSystem();

export const weaponShopScene: SceneDefinition = {
  id: 'weaponShop',
  render(ctx, sc) {
    // Smithy interior
    fillRect(ctx, 0, 0, sc.width, sc.height, '#1a1010');

    // Stone walls
    const rng = seededRandom(170);
    for (let y = 0; y < sc.height; y += 3) {
      for (let x = 0; x < sc.width; x += 5) {
        fillRect(ctx, x, y, 4, 2, rng() > 0.5 ? '#2a1818' : '#1a1010');
      }
    }

    // Forge at right
    const fx = sc.width - 40;
    fillRect(ctx, fx, 20, 25, 18, P.stoneMid);
    fillRect(ctx, fx + 2, 22, 21, 10, P.black);
    // Fire in forge
    const fireGlow = oscillate(sc.elapsed, 0.4);
    for (let r = 0; r < 5; r++) {
      const w = 5 - r;
      const color = r < 2 ? P.brightYellow : (r < 4 ? P.brightRed : P.red);
      fillRect(ctx, fx + 12 - Math.floor(w / 2), 32 - r - 1, w, 1, color);
    }
    // Forge glow
    fillRect(ctx, fx - 5, 18, 35, 22, withAlpha(P.brightRed, 0.05 + fireGlow * 0.05));

    // Anvil
    fillRect(ctx, fx - 20, 34, 8, 2, P.stoneLight);
    fillRect(ctx, fx - 18, 36, 4, 4, P.stoneMid);

    // Weapon rack on left wall
    for (let i = 0; i < 5; i++) {
      const wy = 10 + i * 6;
      fillRect(ctx, 10, wy, 1, 5, P.brightWhite); // sword blade
      setPixel(ctx, 10, wy + 5, P.gold); // hilt
    }

    // Sparks from hammering
    if (sc.frame % 30 < 5) {
      emitSparks(sparks, fx - 16, 33, sc);
    }
    sparks.update(ctx, 1 / 15);

    drawTorch(ctx, 5, 12, sc);
    drawTorch(ctx, Math.floor(sc.width / 2), 12, sc);

    drawVaultWords(ctx, sc);
  },
};
