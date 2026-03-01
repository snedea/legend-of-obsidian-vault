import { useEffect, useRef } from 'react';
import type { SceneId } from './types';
import { SceneEngine } from './engine';
import { getScene } from './scenes';
import { fetchVaultWords, getVaultWords } from './vaultWords';
import { resetVaultText } from './layers/vaultText';

const PIXEL_SCALE = 4;
const CANVAS_HEIGHT = 180; // physical pixels

interface Props {
  scene: SceneId;
}

export function SceneCanvas({ scene }: Props) {
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const engineRef = useRef<SceneEngine | null>(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const sceneDef = getScene(scene);
    if (!sceneDef) return;

    // Size canvas to container width
    const parent = canvas.parentElement;
    const w = parent ? parent.clientWidth : 844;
    canvas.width = w;
    canvas.height = CANVAS_HEIGHT;

    resetVaultText();

    const engine = new SceneEngine(canvas, sceneDef, PIXEL_SCALE);
    engineRef.current = engine;

    // Fetch vault words in background
    fetchVaultWords().then((words) => {
      engine.setVaultWords(words);
    });

    // Also set any already-cached words immediately
    engine.setVaultWords(getVaultWords());

    engine.start();

    return () => {
      engine.stop();
      engineRef.current = null;
    };
  }, [scene]);

  return (
    <canvas
      ref={canvasRef}
      style={{
        width: '100%',
        height: `${CANVAS_HEIGHT}px`,
        imageRendering: 'pixelated',
        display: 'block',
      }}
    />
  );
}
