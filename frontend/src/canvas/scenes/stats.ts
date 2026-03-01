import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, oscillate, withAlpha, seededRandom } from '../utils';
import { drawVaultWords } from '../layers/vaultText';

export const statsScene: SceneDefinition = {
  id: 'stats',
  render(ctx, sc) {
    // Mystical chamber
    fillRect(ctx, 0, 0, sc.width, sc.height, '#0a0814');

    // Floor
    fillRect(ctx, 0, 35, sc.width, sc.height - 35, P.stoneDark);

    // Crystal ball on pedestal
    const cx = Math.floor(sc.width / 2);
    // Pedestal
    fillRect(ctx, cx - 4, 30, 8, 5, P.stoneMid);
    fillRect(ctx, cx - 5, 29, 10, 2, P.stoneLight);

    // Crystal ball
    fillRect(ctx, cx - 3, 22, 6, 6, withAlpha(P.brightCyan, 0.6));
    fillRect(ctx, cx - 2, 21, 4, 1, withAlpha(P.brightCyan, 0.4));
    fillRect(ctx, cx - 2, 28, 4, 1, withAlpha(P.brightCyan, 0.4));

    // Swirling glow inside
    const phase = sc.elapsed * 2;
    for (let i = 0; i < 5; i++) {
      const px = cx + Math.round(Math.cos(phase + i * 1.2) * 2);
      const py = 25 + Math.round(Math.sin(phase + i * 1.2) * 2);
      setPixel(ctx, px, py, withAlpha(P.brightMagenta, 0.7));
    }

    // Mystical glow
    const glowA = 0.05 + oscillate(sc.elapsed, 3) * 0.05;
    fillRect(ctx, cx - 10, 18, 20, 16, withAlpha(P.brightCyan, glowA));

    // Magical symbols on floor
    const rng = seededRandom(220);
    for (let i = 0; i < 8; i++) {
      const sx = 20 + Math.floor(rng() * (sc.width - 40));
      const sy = 36 + Math.floor(rng() * 6);
      const glow2 = oscillate(sc.elapsed, 2 + rng(), i);
      setPixel(ctx, sx, sy, withAlpha(P.brightMagenta, glow2 * 0.4));
    }

    drawVaultWords(ctx, sc);
  },
};
