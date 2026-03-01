import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { drawSky, drawStars, drawCelestial, drawClouds, drawFog } from '../layers/sky';
import { drawGround, drawTree } from '../layers/terrain';
import { drawRain, drawSnow } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';
import { fillRect, setPixel, seededRandom, oscillate, withAlpha } from '../utils';

export const healerScene: SceneDefinition = {
  id: 'healer',
  render(ctx, sc) {
    const gY = 34;

    drawSky(ctx, sc, gY);
    drawStars(ctx, sc, gY);
    drawCelestial(ctx, sc);
    drawClouds(ctx, sc, 2, gY);

    drawGround(ctx, sc, gY, '#1a2a1a');

    // Small hut
    const hx = Math.floor(sc.width / 2) - 10;
    fillRect(ctx, hx, gY - 8, 20, 8, P.groundLight);
    // Thatched roof
    for (let r = 0; r < 4; r++) {
      fillRect(ctx, hx - 2 + r, gY - 12 + r, 24 - r * 2, 1, P.treeMid);
    }
    // Door
    fillRect(ctx, hx + 9, gY - 4, 3, 4, P.groundDark);

    // Herb garden
    const rng = seededRandom(700);
    for (let i = 0; i < 12; i++) {
      const px = 20 + Math.floor(rng() * (sc.width - 40));
      const py = gY + 2 + Math.floor(rng() * 6);
      const color = [P.brightGreen, P.green, P.brightYellow][Math.floor(rng() * 3)];
      setPixel(ctx, px, py, color);
      if (rng() > 0.5) setPixel(ctx, px, py - 1, color);
    }

    // Healing glow around hut
    const glowAlpha = 0.1 + oscillate(sc.elapsed, 3) * 0.1;
    fillRect(ctx, hx - 4, gY - 14, 28, 16, withAlpha(P.brightGreen, glowAlpha));

    // Butterflies
    for (let i = 0; i < 3; i++) {
      const bx = Math.floor(40 + Math.sin(sc.elapsed * 0.7 + i * 4) * 30 + i * 40);
      const by = Math.floor(gY - 5 + Math.cos(sc.elapsed * 0.9 + i * 3) * 5);
      const wing = oscillate(sc.elapsed, 0.25, i) > 0.5;
      setPixel(ctx, bx, by, P.brightMagenta);
      setPixel(ctx, bx - 1, by + (wing ? -1 : 0), P.brightMagenta);
      setPixel(ctx, bx + 1, by + (wing ? -1 : 0), P.brightMagenta);
    }

    drawTree(ctx, 10, gY + 2, 14, sc, P.treeMid);
    drawTree(ctx, sc.width - 15, gY + 2, 12, sc, P.treeMid);

    drawRain(ctx, sc);
    drawSnow(ctx, sc);
    drawFog(ctx, sc);
    drawVaultWords(ctx, sc);
  },
};
