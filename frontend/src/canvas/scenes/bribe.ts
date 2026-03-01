import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, oscillate, withAlpha, seededRandom } from '../utils';
import { drawVaultWords } from '../layers/vaultText';

export const bribeScene: SceneDefinition = {
  id: 'bribe',
  render(ctx, sc) {
    // Dark alley
    fillRect(ctx, 0, 0, sc.width, sc.height, '#080610');

    // Night sky sliver at top
    fillRect(ctx, Math.floor(sc.width * 0.3), 0, Math.floor(sc.width * 0.4), 8, P.skyNightMid);

    // Tall building walls on sides
    fillRect(ctx, 0, 0, Math.floor(sc.width * 0.3), sc.height, P.stoneDark);
    fillRect(ctx, Math.floor(sc.width * 0.7), 0, Math.floor(sc.width * 0.3), sc.height, P.stoneDark);

    // Moon through gap
    const mx = Math.floor(sc.width * 0.5);
    fillRect(ctx, mx - 1, 2, 3, 3, P.brightWhite);

    // Moonlight beam
    const beamA = 0.03 + oscillate(sc.elapsed, 5) * 0.02;
    for (let y = 5; y < sc.height; y++) {
      const w = 2 + Math.floor((y / sc.height) * 10);
      fillRect(ctx, mx - Math.floor(w / 2), y, w, 1, withAlpha(P.brightWhite, beamA));
    }

    // Shadows / figure silhouette
    const figX = Math.floor(sc.width * 0.35);
    fillRect(ctx, figX, 25, 3, 12, P.black);
    fillRect(ctx, figX, 23, 3, 3, P.black);

    // Cobblestone ground
    fillRect(ctx, Math.floor(sc.width * 0.3), 38, Math.floor(sc.width * 0.4), sc.height - 38, P.stoneDark);
    const rng = seededRandom(250);
    for (let i = 0; i < 10; i++) {
      const px = Math.floor(sc.width * 0.3) + Math.floor(rng() * sc.width * 0.4);
      const py = 38 + Math.floor(rng() * 5);
      setPixel(ctx, px, py, P.stoneMid);
    }

    drawVaultWords(ctx, sc);
  },
};
