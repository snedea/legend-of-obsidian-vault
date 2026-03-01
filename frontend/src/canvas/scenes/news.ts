import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { drawSky, drawStars, drawCelestial, drawClouds, drawFog } from '../layers/sky';
import { drawGround, drawPath, drawBuilding } from '../layers/terrain';
import { drawRain, drawSnow } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';
import { fillRect, setPixel } from '../utils';

export const newsScene: SceneDefinition = {
  id: 'news',
  render(ctx, sc) {
    const gY = 35;
    drawSky(ctx, sc, gY);
    drawStars(ctx, sc, gY);
    drawCelestial(ctx, sc);
    drawClouds(ctx, sc, 2, gY);

    drawGround(ctx, sc, gY);
    drawPath(ctx, sc, gY + 2, 3);

    // Town podium
    const cx = Math.floor(sc.width / 2);
    fillRect(ctx, cx - 10, gY - 4, 20, 4, P.stoneMid);
    fillRect(ctx, cx - 8, gY - 6, 16, 2, P.stoneLight);

    // Lectern
    fillRect(ctx, cx - 2, gY - 10, 4, 4, P.groundLight);
    fillRect(ctx, cx - 3, gY - 11, 6, 2, P.groundMid);

    // Scroll on lectern
    fillRect(ctx, cx - 1, gY - 13, 3, 3, P.brightWhite);
    setPixel(ctx, cx, gY - 12, P.black);

    // Surrounding buildings
    drawBuilding(ctx, 10, gY, 10, 8, P.stoneDark, P.red);
    drawBuilding(ctx, sc.width - 22, gY, 12, 9, P.stoneDark, P.yellow);

    drawRain(ctx, sc);
    drawSnow(ctx, sc);
    drawFog(ctx, sc);
    drawVaultWords(ctx, sc);
  },
};
