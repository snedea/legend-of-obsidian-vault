import type { SceneDefinition } from '../types';
import { P } from '../palette';
import { fillRect, setPixel, seededRandom } from '../utils';
import { drawTorch } from '../layers/terrain';
import { drawVaultWords } from '../layers/vaultText';

export const trainingScene: SceneDefinition = {
  id: 'training',
  render(ctx, sc) {
    // Arena interior
    fillRect(ctx, 0, 0, sc.width, sc.height, '#14100e');

    // Sandy floor
    fillRect(ctx, 0, 28, sc.width, sc.height - 28, P.groundLight);
    const rng = seededRandom(190);
    for (let i = 0; i < 30; i++) {
      setPixel(ctx, Math.floor(rng() * sc.width), 28 + Math.floor(rng() * 12), P.groundMid);
    }

    // Training dummies
    for (let i = 0; i < 3; i++) {
      const dx = 30 + i * 55;
      // Pole
      fillRect(ctx, dx, 18, 1, 16, P.groundLight);
      // Cross bar
      fillRect(ctx, dx - 3, 22, 7, 1, P.groundLight);
      // Head
      fillRect(ctx, dx - 1, 16, 3, 3, P.groundMid);
      // Hit wobble
      if (sc.frame % 45 >= i * 10 && sc.frame % 45 < i * 10 + 5) {
        const wobble = Math.sin(sc.elapsed * 20 + i) > 0 ? 1 : -1;
        setPixel(ctx, dx + wobble, 16, P.groundMid);
      }
    }

    // Stone walls
    for (let y = 0; y < 28; y += 3) {
      for (let x = 0; x < sc.width; x += 6) {
        fillRect(ctx, x, y, 5, 2, rng() > 0.5 ? P.stoneDark : '#1a1818');
      }
    }

    // Torches along walls
    drawTorch(ctx, 10, 10, sc);
    drawTorch(ctx, Math.floor(sc.width * 0.33), 10, sc);
    drawTorch(ctx, Math.floor(sc.width * 0.66), 10, sc);
    drawTorch(ctx, sc.width - 12, 10, sc);

    drawVaultWords(ctx, sc);
  },
};
