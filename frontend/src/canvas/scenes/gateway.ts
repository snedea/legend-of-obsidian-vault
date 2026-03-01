import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, oscillate, withAlpha } from '../utils';
import { drawSky, drawStars } from '../layers/sky';
import { drawGround } from '../layers/terrain';
import { ParticleSystem } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';

const energy = new ParticleSystem();

export const gatewayScene: SceneDefinition = {
  id: 'gateway',
  render(ctx, sc) {
    const gY = 36;
    drawSky(ctx, { ...sc, time: 'night' }, gY);
    drawStars(ctx, { ...sc, time: 'night' }, gY);
    drawGround(ctx, sc, gY, P.stoneDark);

    // Portal frame -- stone pillars
    const cx = Math.floor(sc.width / 2);
    fillRect(ctx, cx - 16, gY - 24, 3, 24, P.stoneMid);
    fillRect(ctx, cx + 13, gY - 24, 3, 24, P.stoneMid);
    fillRect(ctx, cx - 16, gY - 26, 32, 3, P.stoneLight);

    // Swirling portal interior
    for (let y = gY - 23; y < gY; y++) {
      for (let x = cx - 13; x < cx + 13; x++) {
        const dx = x - cx;
        const dy = y - (gY - 12);
        const dist = Math.sqrt(dx * dx + dy * dy);
        const angle = Math.atan2(dy, dx) + sc.elapsed * 1.5;
        const swirl = Math.sin(angle * 3 + dist * 0.3);
        const alpha = 0.3 + swirl * 0.3;
        const color = swirl > 0 ? P.brightBlue : P.brightMagenta;
        setPixel(ctx, x, y, withAlpha(color, Math.max(0, alpha)));
      }
    }

    // Portal center glow
    const glowA = 0.2 + oscillate(sc.elapsed, 2) * 0.15;
    fillRect(ctx, cx - 3, gY - 14, 6, 6, withAlpha(P.brightWhite, glowA));

    // Energy particles
    if (sc.frame % 3 === 0) {
      const angle = Math.random() * Math.PI * 2;
      const r = 8 + Math.random() * 5;
      const px = cx + Math.cos(angle) * r;
      const py = gY - 12 + Math.sin(angle) * r * 0.6;
      energy.spawn(px, py, -Math.cos(angle) * 6, -Math.sin(angle) * 4, 0.8, P.brightCyan);
    }
    energy.update(ctx, 1 / 15);

    // Runes on pillars
    for (let i = 0; i < 4; i++) {
      const ry = gY - 22 + i * 5;
      const glow = oscillate(sc.elapsed, 1.5, i);
      setPixel(ctx, cx - 15, ry, withAlpha(P.brightCyan, glow));
      setPixel(ctx, cx + 14, ry, withAlpha(P.brightCyan, glow));
    }

    drawVaultWords(ctx, sc);
  },
};
