import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { drawSky, drawStars, drawClouds } from '../layers/sky';
import { drawGround, drawMountains } from '../layers/terrain';
import { drawRain, ParticleSystem } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';
import { fillRect, setPixel, withAlpha } from '../utils';

const sparks = new ParticleSystem();

export const combatScene: SceneDefinition = {
  id: 'combat',
  render(ctx, sc) {
    const gY = 34;

    // Stormy sky -- override to dark
    drawSky(ctx, { ...sc, time: 'night' }, gY);
    drawStars(ctx, { ...sc, time: 'night' }, gY);
    drawClouds(ctx, { ...sc, weather: 'cloudy' }, 5, gY);

    // Lightning flash
    if (sc.frame % 90 === 0 || sc.frame % 90 === 1) {
      fillRect(ctx, 0, 0, sc.width, gY, withAlpha(P.brightWhite, 0.3));
    }

    drawMountains(ctx, sc, gY, 2);
    drawGround(ctx, sc, gY, P.groundDark);

    // Crossed swords silhouette in center
    const cx = Math.floor(sc.width / 2);
    const cy = gY - 10;
    // Left sword
    for (let i = 0; i < 8; i++) {
      setPixel(ctx, cx - 4 + i, cy - 4 + i, P.brightWhite);
    }
    // Right sword
    for (let i = 0; i < 8; i++) {
      setPixel(ctx, cx + 4 - i, cy - 4 + i, P.brightWhite);
    }
    // Hilts
    fillRect(ctx, cx - 6, cy - 1, 3, 1, P.gold);
    fillRect(ctx, cx + 4, cy - 1, 3, 1, P.gold);

    // Clash sparks
    if (sc.frame % 10 < 3) {
      const angle = Math.random() * Math.PI * 2;
      const speed = 5 + Math.random() * 8;
      sparks.spawn(cx, cy, Math.cos(angle) * speed, Math.sin(angle) * speed, 0.4, P.brightYellow);
    }
    sparks.update(ctx, 1 / 15);

    drawRain(ctx, { ...sc, weather: 'rain' });
    drawVaultWords(ctx, sc);
  },
};
