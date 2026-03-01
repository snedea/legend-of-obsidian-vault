import { listNotes } from '../services/api';

let cachedWords: string[] = [];
let fetched = false;

export async function fetchVaultWords(): Promise<string[]> {
  if (fetched) return cachedWords;
  try {
    const data = await listNotes(100, 0);
    cachedWords = data.notes
      .map((n) => n.title)
      .filter((t) => t.length > 2 && t.length < 30);
    fetched = true;
  } catch {
    // Vault may not be connected -- that's fine
    cachedWords = [];
  }
  return cachedWords;
}

export function getVaultWords(): string[] {
  return cachedWords;
}
