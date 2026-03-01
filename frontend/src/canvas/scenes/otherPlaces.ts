import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { drawSky, drawStars, drawCelestial, drawClouds, drawFog } from '../layers/sky';
import { drawGround, drawPath, drawTreeLine, drawMountains } from '../layers/terrain';
import { drawRain, drawSnow } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';
import { fillRect } from '../utils';

export const otherPlacesScene: SceneDefinition = {
  id: 'otherPlaces',
  render(ctx, sc) {
    const gY = 34;
    drawSky(ctx, sc, gY);
    drawStars(ctx, sc, gY);
    drawCelestial(ctx, sc);
    drawClouds(ctx, sc, 3, gY);

    drawMountains(ctx, sc, gY, 3);

    // Trees in distance
    drawTreeLine(ctx, sc, gY, 6, 6, 12, P.treeDark, 320);

    drawGround(ctx, sc, gY);

    // Crossroads
    drawPath(ctx, sc, gY + 2, 3);
    // Vertical path
    const cx = Math.floor(sc.width / 2);
    fillRect(ctx, cx - 2, gY + 2, 4, sc.height - gY - 2, P.stoneMid);

    // Signpost
    fillRect(ctx, cx, gY - 8, 1, 8, P.groundLight);
    // Signs pointing different directions
    fillRect(ctx, cx + 1, gY - 7, 8, 2, P.groundMid);
    fillRect(ctx, cx - 9, gY - 4, 8, 2, P.groundMid);
    fillRect(ctx, cx + 1, gY - 1, 6, 2, P.groundMid);

    drawRain(ctx, sc);
    drawSnow(ctx, sc);
    drawFog(ctx, sc);
    drawVaultWords(ctx, sc);
  },
};
