import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { drawSky, drawStars, drawCelestial, drawClouds, drawFog } from '../layers/sky';
import { drawGround, drawTreeLine, drawTree } from '../layers/terrain';
import { drawRain, drawSnow, drawFireflies } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';
import { fillRect, seededRandom, setPixel, oscillate } from '../utils';

export const forestScene: SceneDefinition = {
  id: 'forest',
  render(ctx, sc) {
    const gY = 34;

    drawSky(ctx, sc, gY);
    drawStars(ctx, sc, gY);
    drawCelestial(ctx, sc);
    drawClouds(ctx, sc, 2, gY);

    // Back layer -- dark distant trees
    drawTreeLine(ctx, sc, gY, 12, 8, 16, P.treeDark, 301);

    // Mid layer -- medium trees
    drawTreeLine(ctx, sc, gY + 2, 8, 10, 18, P.treeMid, 302);

    // Ground -- dark forest floor
    drawGround(ctx, sc, gY + 2, P.groundDark);

    // Undergrowth -- small bushes
    const rng = seededRandom(350);
    for (let i = 0; i < 15; i++) {
      const bx = Math.floor(rng() * sc.width);
      const by = gY + 3 + Math.floor(rng() * 5);
      fillRect(ctx, bx, by, 2 + Math.floor(rng() * 3), 1, P.treeDark);
    }

    // Foreground -- a couple big trees
    drawTree(ctx, 15, gY + 4, 20, sc, P.treeLight);
    drawTree(ctx, sc.width - 20, gY + 4, 22, sc, P.treeLight);

    // Birds -- small V shapes flying
    const rng2 = seededRandom(360);
    for (let i = 0; i < 3; i++) {
      const bx = Math.floor((rng2() * sc.width + sc.elapsed * (5 + i * 2)) % (sc.width + 20)) - 10;
      const by = 5 + Math.floor(rng2() * 12);
      const flap = oscillate(sc.elapsed, 0.4, i * 2) > 0.5;
      setPixel(ctx, bx, by, P.brightBlack);
      setPixel(ctx, bx - 1, by + (flap ? -1 : 0), P.brightBlack);
      setPixel(ctx, bx + 1, by + (flap ? -1 : 0), P.brightBlack);
    }

    // Fireflies at night/dusk
    if (sc.time === 'night' || sc.time === 'dusk') {
      drawFireflies(ctx, sc, 8, 610);
    }

    drawRain(ctx, sc);
    drawSnow(ctx, sc);
    drawFog(ctx, sc);
    drawVaultWords(ctx, sc);
  },
};
