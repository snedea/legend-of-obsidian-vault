import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { drawSky, drawStars, drawClouds } from '../layers/sky';
import { drawGround, drawTreeLine } from '../layers/terrain';
import { drawVaultWords } from '../layers/vaultText';
import { fillRect, setPixel, oscillate, withAlpha, seededRandom } from '../utils';

export const werewolfScene: SceneDefinition = {
  id: 'werewolf',
  render(ctx, sc) {
    const gY = 34;

    // Always night
    drawSky(ctx, { ...sc, time: 'night' }, gY);
    drawStars(ctx, { ...sc, time: 'night' }, gY);
    drawClouds(ctx, { ...sc, time: 'night' }, 3, gY);

    // Full moon
    const mx = Math.floor(sc.width * 0.7);
    fillRect(ctx, mx - 2, 4, 5, 5, P.brightWhite);
    fillRect(ctx, mx - 1, 3, 3, 1, P.brightWhite);
    fillRect(ctx, mx - 1, 9, 3, 1, P.brightWhite);

    // Dark trees
    drawTreeLine(ctx, sc, gY, 10, 8, 16, P.treeDark, 310);

    drawGround(ctx, sc, gY, P.groundDark);

    // Den / cave entrance
    const cx = Math.floor(sc.width / 2);
    fillRect(ctx, cx - 12, gY - 8, 24, 8, P.stoneDark);
    fillRect(ctx, cx - 8, gY - 5, 16, 5, P.black);

    // Glowing eyes in the dark
    const blink = oscillate(sc.elapsed, 3, 0);
    if (blink > 0.1) {
      setPixel(ctx, cx - 3, gY - 3, P.brightYellow);
      setPixel(ctx, cx + 2, gY - 3, P.brightYellow);
    }

    // Mist along ground
    const rng = seededRandom(160);
    for (let i = 0; i < 12; i++) {
      const fogX = Math.floor(rng() * sc.width);
      const fogY = gY + Math.floor(rng() * 3);
      const w = 4 + Math.floor(rng() * 8);
      const drift = (sc.elapsed * 2 + fogX) % (sc.width + 20);
      const alpha = 0.1 + oscillate(sc.elapsed, 4, i * 0.5) * 0.1;
      fillRect(ctx, Math.floor(drift) - 10, fogY, w, 1, withAlpha(P.white, alpha));
    }

    drawVaultWords(ctx, sc);
  },
};
