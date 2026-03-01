import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, seededRandom, oscillate, withAlpha } from '../utils';
import { ParticleSystem, emitDrips } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';

const drips = new ParticleSystem();

export const cavernScene: SceneDefinition = {
  id: 'cavern',
  render(ctx, sc) {
    // Dark cave
    fillRect(ctx, 0, 0, sc.width, sc.height, P.black);

    // Rocky ceiling
    const rng = seededRandom(130);
    for (let x = 0; x < sc.width; x += 2) {
      const h = 3 + Math.floor(rng() * 5);
      fillRect(ctx, x, 0, 2, h, rng() > 0.5 ? P.stoneDark : P.stoneMid);
    }

    // Cave mouth silhouette
    const cx = Math.floor(sc.width / 2);
    for (let y = 0; y < 30; y++) {
      const t = y / 30;
      const w = Math.floor(20 + t * 15);
      fillRect(ctx, cx - w, y, w * 2, 1, P.stoneDark);
    }
    // Inner glow
    for (let y = 5; y < 28; y++) {
      const t = y / 28;
      const w = Math.floor(15 + t * 10);
      fillRect(ctx, cx - w, y, w * 2, 1, '#0c0a18');
    }

    // Crystals
    const crystalColors = [P.brightMagenta, P.brightCyan, P.brightBlue, P.brightRed];
    for (let i = 0; i < 8; i++) {
      const crx = 20 + Math.floor(rng() * (sc.width - 40));
      const cry = 10 + Math.floor(rng() * 20);
      const color = crystalColors[Math.floor(rng() * crystalColors.length)];
      const glow = oscillate(sc.elapsed, 2 + rng() * 3, i * 1.3);
      fillRect(ctx, crx, cry - 2, 1, 3, color);
      setPixel(ctx, crx - 1, cry, withAlpha(color, glow * 0.5));
      setPixel(ctx, crx + 1, cry, withAlpha(color, glow * 0.5));
    }

    // Stalactites
    for (let i = 0; i < 6; i++) {
      const sx = 15 + Math.floor(rng() * (sc.width - 30));
      const sh = 3 + Math.floor(rng() * 4);
      for (let r = 0; r < sh; r++) {
        setPixel(ctx, sx, r, P.stoneLight);
      }
    }

    // Floor
    fillRect(ctx, 0, 38, sc.width, sc.height - 38, P.stoneDark);

    // Dripping water
    emitDrips(drips, cx - 10, 8, sc);
    emitDrips(drips, cx + 15, 6, sc);
    drips.update(ctx, 1 / 15);

    drawVaultWords(ctx, sc);
  },
};
