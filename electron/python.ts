import { spawn, type ChildProcess } from 'child_process';
import path from 'path';
import { app } from 'electron';
import http from 'http';

let backendProcess: ChildProcess | null = null;

const BACKEND_PORT = 8742;

function getProjectRoot(): string {
  if (app.isPackaged) {
    // Production: game files are in extraResources/game/
    return path.join(process.resourcesPath, 'game');
  }
  // Development: project root is two levels up from electron/dist/
  return path.resolve(__dirname, '..', '..');
}

/** Check if backend is already running (e.g. started by npm run dev) */
function isBackendRunning(): Promise<boolean> {
  return new Promise((resolve) => {
    const req = http.get(`http://127.0.0.1:${BACKEND_PORT}/api/health`, (res) => {
      resolve(res.statusCode === 200);
    });
    req.on('error', () => resolve(false));
    req.setTimeout(500, () => { req.destroy(); resolve(false); });
  });
}

export async function startBackend(): Promise<number> {
  // Fix #5: Don't start a second backend if one is already running
  if (await isBackendRunning()) {
    console.log('[backend] Already running on port', BACKEND_PORT);
    return BACKEND_PORT;
  }

  return new Promise((resolve, reject) => {
    const projectRoot = getProjectRoot();

    // Both dev and prod use python3 + uvicorn with the bundled .py files.
    // No PyInstaller binary is needed.
    backendProcess = spawn('python3', [
      '-m', 'uvicorn', 'backend.main:app',
      '--host', '127.0.0.1',
      '--port', String(BACKEND_PORT),
    ], {
      cwd: projectRoot,
      stdio: ['ignore', 'pipe', 'pipe'],
    });

    let resolved = false;

    backendProcess.stdout?.on('data', (data: Buffer) => {
      console.log(`[backend] ${data.toString().trim()}`);
    });

    backendProcess.stderr?.on('data', (data: Buffer) => {
      const msg = data.toString().trim();
      console.log(`[backend] ${msg}`);
      if (!resolved && (msg.includes('Application startup complete') || msg.includes('Uvicorn running'))) {
        resolved = true;
        resolve(BACKEND_PORT);
      }
    });

    backendProcess.on('error', (err) => {
      console.error('Failed to start backend:', err);
      if (!resolved) { resolved = true; reject(err); }
    });

    backendProcess.on('exit', (code) => {
      console.log(`Backend exited with code ${code}`);
      backendProcess = null;
    });

    // Fallback: poll health endpoint
    let attempts = 0;
    const maxAttempts = 30; // 15 seconds
    const pollInterval = setInterval(() => {
      attempts++;
      if (resolved) { clearInterval(pollInterval); return; }
      if (attempts > maxAttempts) {
        clearInterval(pollInterval);
        if (!resolved) { resolved = true; reject(new Error('Backend did not start in time')); }
        return;
      }

      const req = http.get(`http://127.0.0.1:${BACKEND_PORT}/api/health`, (res) => {
        if (res.statusCode === 200 && !resolved) {
          clearInterval(pollInterval);
          resolved = true;
          resolve(BACKEND_PORT);
        }
      });
      req.on('error', () => { /* not ready */ });
      req.end();
    }, 500);
  });
}

export function stopBackend(): void {
  if (backendProcess) {
    console.log('Stopping backend...');
    backendProcess.kill('SIGTERM');
    setTimeout(() => {
      if (backendProcess) {
        backendProcess.kill('SIGKILL');
        backendProcess = null;
      }
    }, 3000);
  }
}

export function getBackendPort(): number {
  return BACKEND_PORT;
}
