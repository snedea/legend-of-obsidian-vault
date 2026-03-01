import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, oscillate, withAlpha } from '../utils';
import { ParticleSystem } from '../layers/particles';
import { drawVaultWords } from '../layers/vaultText';

const energyPs = new ParticleSystem();

export const vaultScene: SceneDefinition = {
  id: 'vault',
  render(ctx, sc) {
    // Deep purple void
    fillRect(ctx, 0, 0, sc.width, sc.height, '#08041a');

    // Floor
    fillRect(ctx, 0, 36, sc.width, sc.height - 36, P.stoneDark);

    // Central obsidian crystal
    const cx = Math.floor(sc.width / 2);
    const crystalH = 16;
    const crystalBase = 30;

    // Crystal shape -- diamond
    for (let r = 0; r < crystalH; r++) {
      const t = r / crystalH;
      const w = t < 0.5 ? Math.floor(t * 2 * 8) + 1 : Math.floor((1 - t) * 2 * 8) + 1;
      const color = withAlpha(P.brightMagenta, 0.4 + t * 0.3);
      fillRect(ctx, cx - Math.floor(w / 2), crystalBase - crystalH + r, w, 1, color);
    }

    // Inner glow
    const glow = oscillate(sc.elapsed, 2);
    fillRect(ctx, cx - 2, crystalBase - 10, 4, 4, withAlpha(P.brightWhite, glow * 0.4));

    // Purple energy rays
    for (let i = 0; i < 6; i++) {
      const angle = (i / 6) * Math.PI * 2 + sc.elapsed * 0.3;
      const len = 12 + oscillate(sc.elapsed, 1.5, i) * 5;
      for (let d = 3; d < len; d++) {
        const px = cx + Math.floor(Math.cos(angle) * d);
        const py = crystalBase - 8 + Math.floor(Math.sin(angle) * d * 0.6);
        const alpha = 0.3 * (1 - d / len);
        if (px >= 0 && px < sc.width && py >= 0 && py < sc.height) {
          setPixel(ctx, px, py, withAlpha(P.brightMagenta, alpha));
        }
      }
    }

    // Energy particles orbiting
    if (sc.frame % 3 === 0) {
      const angle = Math.random() * Math.PI * 2;
      const r = 10 + Math.random() * 8;
      energyPs.spawn(
        cx + Math.cos(angle) * r, crystalBase - 8 + Math.sin(angle) * r * 0.5,
        -Math.cos(angle) * 4, -Math.sin(angle) * 3,
        1, P.brightMagenta,
      );
    }
    energyPs.update(ctx, 1 / 15);

    // Rune circle on floor
    for (let i = 0; i < 12; i++) {
      const angle = (i / 12) * Math.PI * 2;
      const rx = cx + Math.floor(Math.cos(angle) * 25);
      const ry = 38 + Math.floor(Math.sin(angle) * 3);
      const runeGlow = oscillate(sc.elapsed, 1, i * 0.5);
      setPixel(ctx, rx, ry, withAlpha(P.brightMagenta, runeGlow * 0.5));
    }

    drawVaultWords(ctx, sc);
  },
};
