import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, seededRandom } from '../utils';
import { drawVaultWords } from '../layers/vaultText';

export const settingsScene: SceneDefinition = {
  id: 'settings',
  render(ctx, sc) {
    // Workshop / mechanical room
    fillRect(ctx, 0, 0, sc.width, sc.height, '#0e0c10');

    // Metal plate walls
    const rng = seededRandom(290);
    for (let y = 0; y < sc.height; y += 4) {
      for (let x = 0; x < sc.width; x += 8) {
        fillRect(ctx, x, y, 7, 3, rng() > 0.5 ? '#1a1820' : '#14121a');
        // Rivets
        setPixel(ctx, x, y, P.brightBlack);
        setPixel(ctx, x + 6, y, P.brightBlack);
      }
    }

    // Gear 1 (large)
    const g1x = Math.floor(sc.width * 0.35);
    const g1y = 20;
    const g1r = 10;
    const g1angle = sc.elapsed * 0.5;
    for (let i = 0; i < 8; i++) {
      const a = g1angle + (i / 8) * Math.PI * 2;
      // Teeth
      for (let d = g1r - 2; d <= g1r; d++) {
        const px = g1x + Math.floor(Math.cos(a) * d);
        const py = g1y + Math.floor(Math.sin(a) * d);
        setPixel(ctx, px, py, P.stoneLight);
      }
    }
    // Hub
    fillRect(ctx, g1x - 2, g1y - 2, 4, 4, P.stoneMid);
    setPixel(ctx, g1x, g1y, P.brightBlack);

    // Gear 2 (medium, meshed)
    const g2x = Math.floor(sc.width * 0.55);
    const g2y = 18;
    const g2r = 7;
    const g2angle = -sc.elapsed * 0.7;
    for (let i = 0; i < 6; i++) {
      const a = g2angle + (i / 6) * Math.PI * 2;
      for (let d = g2r - 2; d <= g2r; d++) {
        const px = g2x + Math.floor(Math.cos(a) * d);
        const py = g2y + Math.floor(Math.sin(a) * d);
        setPixel(ctx, px, py, P.stoneLight);
      }
    }
    fillRect(ctx, g2x - 1, g2y - 1, 3, 3, P.stoneMid);

    // Gear 3 (small)
    const g3x = Math.floor(sc.width * 0.7);
    const g3y = 25;
    const g3r = 5;
    const g3angle = sc.elapsed * 1.0;
    for (let i = 0; i < 5; i++) {
      const a = g3angle + (i / 5) * Math.PI * 2;
      for (let d = g3r - 1; d <= g3r; d++) {
        const px = g3x + Math.floor(Math.cos(a) * d);
        const py = g3y + Math.floor(Math.sin(a) * d);
        setPixel(ctx, px, py, P.stoneLight);
      }
    }
    fillRect(ctx, g3x - 1, g3y - 1, 2, 2, P.stoneMid);

    // Levers / switches
    for (let i = 0; i < 3; i++) {
      const lx = 15 + i * 25;
      fillRect(ctx, lx, 35, 1, 6, P.stoneMid);
      const up = (i + Math.floor(sc.elapsed)) % 3 === 0;
      fillRect(ctx, lx - 1, up ? 33 : 38, 3, 2, P.brightBlack);
    }

    drawVaultWords(ctx, sc);
  },
};
