import { useEffect } from 'react';

type KeyMap = Record<string, () => void>;

/**
 * Maps keypresses to handler functions.
 * Keys should be uppercase letters or special key names.
 */
export function useKeyboard(keyMap: KeyMap, deps: unknown[] = []) {
  useEffect(() => {
    function handler(e: KeyboardEvent) {
      // Don't capture keys when typing in an input
      if (
        e.target instanceof HTMLInputElement ||
        e.target instanceof HTMLTextAreaElement
      ) {
        return;
      }

      const key = e.key.toUpperCase();
      const fn = keyMap[key];
      if (fn) {
        e.preventDefault();
        fn();
      }
    }

    window.addEventListener('keydown', handler);
    return () => window.removeEventListener('keydown', handler);
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, deps);
}
