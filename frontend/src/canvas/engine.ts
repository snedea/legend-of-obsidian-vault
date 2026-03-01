import type { SceneContext, SceneDefinition } from './types';
import { getSessionEnvironment } from './environment';

const TARGET_FPS = 15;
const FRAME_MS = 1000 / TARGET_FPS;

export class SceneEngine {
  private ctx: CanvasRenderingContext2D;
  private scene: SceneDefinition;
  private animId = 0;
  private frame = 0;
  private startTime = 0;
  private lastFrame = 0;
  private vaultWords: string[] = [];
  private logicalW: number;
  private logicalH: number;

  constructor(
    canvas: HTMLCanvasElement,
    scene: SceneDefinition,
    scale: number,
  ) {
    this.scene = scene;
    const ctx = canvas.getContext('2d');
    if (!ctx) throw new Error('Canvas 2d context unavailable');
    this.ctx = ctx;

    // Set logical dimensions based on actual canvas size / scale
    this.logicalW = Math.floor(canvas.width / scale);
    this.logicalH = Math.floor(canvas.height / scale);

    // Scale the context so we draw in logical pixels
    ctx.setTransform(scale, 0, 0, scale, 0, 0);
    ctx.imageSmoothingEnabled = false;
  }

  setVaultWords(words: string[]): void {
    this.vaultWords = words;
  }

  start(): void {
    this.startTime = performance.now();
    this.lastFrame = this.startTime;
    this.tick(this.startTime);
  }

  stop(): void {
    if (this.animId) {
      cancelAnimationFrame(this.animId);
      this.animId = 0;
    }
  }

  private tick = (now: number): void => {
    this.animId = requestAnimationFrame(this.tick);

    // Frame limit to TARGET_FPS
    if (now - this.lastFrame < FRAME_MS) return;
    this.lastFrame = now;
    this.frame++;

    const env = getSessionEnvironment();
    const sceneCtx: SceneContext = {
      time: env.time,
      weather: env.weather,
      frame: this.frame,
      elapsed: (now - this.startTime) / 1000,
      width: this.logicalW,
      height: this.logicalH,
      vaultWords: this.vaultWords,
    };

    this.scene.render(this.ctx, sceneCtx);
  };
}
