import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, oscillate, seededRandom, withAlpha } from '../utils';
import { drawVaultWords } from '../layers/vaultText';

export const barRoomScene: SceneDefinition = {
  id: 'barRoom',
  render(ctx, sc) {
    // Warm tavern interior
    fillRect(ctx, 0, 0, sc.width, sc.height, '#1a1210');

    // Wooden paneling
    for (let x = 0; x < sc.width; x += 4) {
      fillRect(ctx, x, 0, 3, 24, x % 8 < 4 ? '#2a1a10' : '#221810');
    }

    // Floor
    fillRect(ctx, 0, 24, sc.width, sc.height - 24, '#1a1008');

    // Bar counter
    fillRect(ctx, 20, 20, sc.width - 40, 3, P.groundLight);
    fillRect(ctx, 20, 23, sc.width - 40, 1, '#2a1a10');

    // Bottles on shelf
    const rng = seededRandom(120);
    for (let i = 0; i < 10; i++) {
      const bx = 30 + i * 15;
      const color = [P.red, P.green, P.brightBlue, P.brightYellow][Math.floor(rng() * 4)];
      fillRect(ctx, bx, 12, 2, 6, color);
      setPixel(ctx, bx, 11, P.brightWhite); // cork
    }

    // Hanging lanterns
    for (let i = 0; i < 4; i++) {
      const lx = 40 + i * 40;
      fillRect(ctx, lx, 2, 1, 4, P.brightBlack);
      const glow = oscillate(sc.elapsed, 2, i * 1.5);
      setPixel(ctx, lx, 6, glow > 0.3 ? P.brightYellow : P.yellow);
      if (glow > 0.6) {
        setPixel(ctx, lx - 1, 6, withAlpha(P.brightYellow, 0.3));
        setPixel(ctx, lx + 1, 6, withAlpha(P.brightYellow, 0.3));
      }
    }

    // Mugs on counter
    for (let i = 0; i < 5; i++) {
      const mx = 35 + i * 28;
      fillRect(ctx, mx, 18, 3, 2, P.gold);
    }

    // Stools
    for (let i = 0; i < 6; i++) {
      fillRect(ctx, 30 + i * 25, 25, 3, 4, P.groundLight);
    }

    drawVaultWords(ctx, sc);
  },
};
