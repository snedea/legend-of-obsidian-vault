import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, seededRandom } from '../utils';
import { drawTorch } from '../layers/terrain';
import { drawVaultWords } from '../layers/vaultText';
import { ParticleSystem } from '../layers/particles';

const sparkles = new ParticleSystem();

export const bankScene: SceneDefinition = {
  id: 'bank',
  render(ctx, sc) {
    // Dark vault interior
    fillRect(ctx, 0, 0, sc.width, sc.height, P.black);

    // Stone walls
    const rng = seededRandom(100);
    for (let y = 0; y < sc.height; y += 3) {
      for (let x = 0; x < sc.width; x += 5) {
        const off = (y / 3) % 2 === 0 ? 0 : 2;
        fillRect(ctx, x + off, y, 4, 2, rng() > 0.5 ? P.stoneDark : P.stoneMid);
      }
    }

    // Vault door arch
    const cx = Math.floor(sc.width / 2);
    fillRect(ctx, cx - 15, 5, 30, sc.height - 5, P.stoneDark);
    fillRect(ctx, cx - 13, 8, 26, sc.height - 8, P.black);
    // Door
    fillRect(ctx, cx - 10, 12, 20, sc.height - 12, P.brightBlack);
    // Door handle
    setPixel(ctx, cx + 6, 28, P.gold);

    // Gold piles
    const goldY = sc.height - 8;
    for (let i = 0; i < 5; i++) {
      const gx = cx - 8 + i * 4;
      for (let r = 0; r < 3; r++) {
        fillRect(ctx, gx - r, goldY + r, r * 2 + 2, 1, r === 0 ? P.brightYellow : P.gold);
      }
    }

    // Gold sparkles
    if (sc.frame % 5 === 0) {
      const sx = cx - 8 + Math.random() * 20;
      sparkles.spawn(sx, goldY - 1, (Math.random() - 0.5) * 2, -2 - Math.random() * 3, 0.8, P.brightYellow);
    }
    sparkles.update(ctx, 1 / 15);

    // Torches
    drawTorch(ctx, cx - 18, 15, sc);
    drawTorch(ctx, cx + 18, 15, sc);

    drawVaultWords(ctx, sc);
  },
};
