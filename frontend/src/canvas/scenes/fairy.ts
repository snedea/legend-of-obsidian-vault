import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { drawSky, drawStars, drawClouds } from '../layers/sky';
import { drawGround, drawTree } from '../layers/terrain';
import { drawFireflies } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';
import { setPixel, seededRandom, oscillate, withAlpha } from '../utils';

export const fairyScene: SceneDefinition = {
  id: 'fairy',
  render(ctx, sc) {
    const gY = 33;

    // Enchanted sky -- always dusk-like
    drawSky(ctx, { ...sc, time: 'dusk' }, gY);
    drawStars(ctx, { ...sc, time: 'dusk' }, gY);
    drawClouds(ctx, sc, 2, gY);

    // Enchanted trees
    drawTree(ctx, 10, gY + 2, 18, sc, P.treeLight);
    drawTree(ctx, 40, gY + 2, 14, sc, P.treeMid);
    drawTree(ctx, sc.width - 45, gY + 2, 16, sc, P.treeLight);
    drawTree(ctx, sc.width - 12, gY + 2, 20, sc, P.treeMid);

    // Magical glade ground
    drawGround(ctx, sc, gY + 2, '#1a2a1a');

    // Flowers
    const rng = seededRandom(140);
    const flowerColors = [P.brightMagenta, P.brightRed, P.brightYellow, P.brightCyan];
    for (let i = 0; i < 20; i++) {
      const fx = Math.floor(rng() * sc.width);
      const fy = gY + 3 + Math.floor(rng() * 8);
      setPixel(ctx, fx, fy, flowerColors[Math.floor(rng() * flowerColors.length)]);
    }

    // Sparkles floating upward
    for (let i = 0; i < 10; i++) {
      const sx = Math.floor(60 + Math.sin(sc.elapsed * 0.5 + i * 2.5) * 50);
      const sy = Math.floor(gY - 5 + Math.cos(sc.elapsed * 0.4 + i * 1.8) * 10);
      const alpha = oscillate(sc.elapsed, 1.5, i * 0.8);
      setPixel(ctx, sx, sy, withAlpha(P.brightMagenta, alpha * 0.7));
    }

    // Fairy ring -- circle of mushrooms
    const cx = Math.floor(sc.width / 2);
    for (let a = 0; a < 8; a++) {
      const angle = (a / 8) * Math.PI * 2;
      const mx = cx + Math.floor(Math.cos(angle) * 15);
      const my = gY + 4 + Math.floor(Math.sin(angle) * 4);
      setPixel(ctx, mx, my, P.brightRed);
      setPixel(ctx, mx, my - 1, P.brightWhite);
    }

    // Lots of fireflies
    drawFireflies(ctx, sc, 12, 620);

    drawVaultWords(ctx, sc);
  },
};
