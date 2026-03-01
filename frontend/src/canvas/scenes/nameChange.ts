import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, oscillate, withAlpha } from '../utils';
import { drawVaultWords } from '../layers/vaultText';

export const nameChangeScene: SceneDefinition = {
  id: 'nameChange',
  render(ctx, sc) {
    // Mystical chamber
    fillRect(ctx, 0, 0, sc.width, sc.height, '#0c0a18');

    // Floor
    fillRect(ctx, 0, 34, sc.width, sc.height - 34, P.stoneDark);

    // Floating scroll in center
    const cx = Math.floor(sc.width / 2);
    const hover = Math.sin(sc.elapsed * 1.5) * 2;
    const sy = Math.floor(18 + hover);

    // Scroll
    fillRect(ctx, cx - 10, sy, 20, 12, P.brightWhite);
    fillRect(ctx, cx - 11, sy, 2, 12, '#d0c080');
    fillRect(ctx, cx + 9, sy, 2, 12, '#d0c080');

    // Text lines on scroll
    for (let i = 0; i < 4; i++) {
      fillRect(ctx, cx - 7, sy + 2 + i * 2, 14, 1, P.brightBlack);
    }

    // Glowing runes around scroll
    for (let i = 0; i < 8; i++) {
      const angle = (i / 8) * Math.PI * 2 + sc.elapsed * 0.5;
      const rx = cx + Math.floor(Math.cos(angle) * 20);
      const ry = 24 + Math.floor(Math.sin(angle) * 10);
      const glow = oscillate(sc.elapsed, 1.2, i * 0.9);
      setPixel(ctx, rx, ry, withAlpha(P.brightCyan, glow * 0.7));
    }

    // Magical glow beneath scroll
    fillRect(ctx, cx - 12, sy + 13, 24, 2, withAlpha(P.brightMagenta, 0.1 + oscillate(sc.elapsed, 2) * 0.1));

    drawVaultWords(ctx, sc);
  },
};
