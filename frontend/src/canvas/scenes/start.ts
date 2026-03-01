import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { drawSky, drawStars, drawClouds } from '../layers/sky';
import { drawGround, drawMountains } from '../layers/terrain';
import { drawVaultWords } from '../layers/vaultText';
import { fillRect, setPixel, oscillate, withAlpha } from '../utils';

export const startScene: SceneDefinition = {
  id: 'start',
  render(ctx, sc) {
    const gY = 34;

    // Dramatic sky -- always dusk
    drawSky(ctx, { ...sc, time: 'dusk' }, gY);
    drawStars(ctx, { ...sc, time: 'dusk' }, gY);
    drawClouds(ctx, sc, 4, gY);

    drawMountains(ctx, sc, gY, 4);

    // Castle silhouette
    const cx = Math.floor(sc.width / 2);
    // Main keep
    fillRect(ctx, cx - 12, gY - 18, 24, 18, P.black);
    // Towers
    fillRect(ctx, cx - 16, gY - 22, 6, 22, P.black);
    fillRect(ctx, cx + 10, gY - 22, 6, 22, P.black);
    // Tower tops
    fillRect(ctx, cx - 17, gY - 24, 8, 2, P.black);
    fillRect(ctx, cx + 9, gY - 24, 8, 2, P.black);
    // Crenellations
    for (let i = 0; i < 4; i++) {
      setPixel(ctx, cx - 16 + i * 2, gY - 25, P.black);
      setPixel(ctx, cx + 10 + i * 2, gY - 25, P.black);
    }
    // Gate
    fillRect(ctx, cx - 3, gY - 6, 6, 6, '#1a0a1a');
    // Windows
    const glow = oscillate(sc.elapsed, 3);
    setPixel(ctx, cx - 6, gY - 12, withAlpha(P.brightYellow, glow));
    setPixel(ctx, cx + 5, gY - 12, withAlpha(P.brightYellow, glow));
    setPixel(ctx, cx - 14, gY - 16, withAlpha(P.brightYellow, glow * 0.7));
    setPixel(ctx, cx + 13, gY - 16, withAlpha(P.brightYellow, glow * 0.7));

    // Banners on towers
    const sway = Math.round(oscillate(sc.elapsed, 3) - 0.5);
    fillRect(ctx, cx - 13 + sway, gY - 20, 2, 5, P.red);
    fillRect(ctx, cx + 12 + sway, gY - 20, 2, 5, P.red);

    drawGround(ctx, sc, gY, P.groundDark);

    drawVaultWords(ctx, sc);
  },
};
