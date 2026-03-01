import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, oscillate, withAlpha } from '../utils';
import { drawTorch } from '../layers/terrain';
import { ParticleSystem, emitSparks } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';

const forgeSparks = new ParticleSystem();

export const charCreateScene: SceneDefinition = {
  id: 'charCreate',
  render(ctx, sc) {
    // Dark forge interior
    fillRect(ctx, 0, 0, sc.width, sc.height, '#100808');

    // Stone floor
    fillRect(ctx, 0, 30, sc.width, sc.height - 30, P.stoneDark);

    // Central forge / anvil
    const cx = Math.floor(sc.width / 2);
    // Forge basin
    fillRect(ctx, cx - 8, 20, 16, 12, P.stoneMid);
    fillRect(ctx, cx - 6, 22, 12, 6, P.black);

    // Molten glow
    const glow = oscillate(sc.elapsed, 1.5);
    fillRect(ctx, cx - 5, 24, 10, 3, withAlpha(P.brightRed, 0.3 + glow * 0.2));
    fillRect(ctx, cx - 3, 25, 6, 1, withAlpha(P.brightYellow, 0.4 + glow * 0.3));

    // Anvil
    fillRect(ctx, cx + 20, 30, 8, 2, P.stoneLight);
    fillRect(ctx, cx + 22, 32, 4, 4, P.stoneMid);

    // Sparks
    emitSparks(forgeSparks, cx, 23, sc);
    forgeSparks.update(ctx, 1 / 15);

    // Weapon molds on walls
    for (let i = 0; i < 4; i++) {
      const mx = 10 + i * 45;
      fillRect(ctx, mx, 10, 1, 8, P.brightBlack);
    }

    // Ambient forge glow
    fillRect(ctx, cx - 15, 18, 30, 16, withAlpha(P.brightRed, 0.03 + glow * 0.02));

    drawTorch(ctx, 5, 8, sc);
    drawTorch(ctx, sc.width - 8, 8, sc);

    drawVaultWords(ctx, sc);
  },
};
