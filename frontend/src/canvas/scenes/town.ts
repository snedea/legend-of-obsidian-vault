import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { drawSky, drawStars, drawCelestial, drawClouds, drawFog } from '../layers/sky';
import { drawGround, drawBuilding, drawPath, drawTorch } from '../layers/terrain';
import { drawRain, drawSnow, ParticleSystem, emitSmoke } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';
import { fillRect } from '../utils';

const smoke = new ParticleSystem();

export const townScene: SceneDefinition = {
  id: 'town',
  render(ctx, sc) {
    const gY = 35;

    drawSky(ctx, sc, gY);
    drawStars(ctx, sc, gY);
    drawCelestial(ctx, sc);
    drawClouds(ctx, sc, 3, gY);

    // Buildings
    drawBuilding(ctx, 30, gY, 12, 10, P.stoneDark, P.red);
    drawBuilding(ctx, 55, gY, 10, 8, P.stoneMid, P.brightRed);
    drawBuilding(ctx, 80, gY, 14, 12, P.stoneDark, P.yellow);
    drawBuilding(ctx, 110, gY, 9, 7, P.stoneMid, P.red);
    drawBuilding(ctx, 140, gY, 11, 9, P.stoneDark, P.brightRed);
    drawBuilding(ctx, 168, gY, 13, 11, P.stoneMid, P.yellow);

    // Chimney smoke
    emitSmoke(smoke, 36, gY - 14, sc);
    emitSmoke(smoke, 87, gY - 16, sc);

    // Ground + path
    drawGround(ctx, sc, gY);
    drawPath(ctx, sc, gY + 2, 4);

    // Torches
    drawTorch(ctx, 48, gY - 3, sc);
    drawTorch(ctx, 100, gY - 3, sc);
    drawTorch(ctx, 155, gY - 3, sc);

    // Sign
    fillRect(ctx, 125, gY - 5, 1, 5, P.groundLight);
    fillRect(ctx, 122, gY - 6, 7, 3, P.yellow);

    smoke.update(ctx, 1 / 15);

    drawRain(ctx, sc);
    drawSnow(ctx, sc);
    drawFog(ctx, sc);
    drawVaultWords(ctx, sc);
  },
};
