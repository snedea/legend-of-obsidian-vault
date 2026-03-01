// 3x5 pixel bitmap font for vault text rendering
// Each char is a 3-wide x 5-tall bitmap stored as 5 rows of 3 bits
const GLYPHS: Record<string, number[]> = {
  A: [0b010, 0b101, 0b111, 0b101, 0b101],
  B: [0b110, 0b101, 0b110, 0b101, 0b110],
  C: [0b011, 0b100, 0b100, 0b100, 0b011],
  D: [0b110, 0b101, 0b101, 0b101, 0b110],
  E: [0b111, 0b100, 0b110, 0b100, 0b111],
  F: [0b111, 0b100, 0b110, 0b100, 0b100],
  G: [0b011, 0b100, 0b101, 0b101, 0b011],
  H: [0b101, 0b101, 0b111, 0b101, 0b101],
  I: [0b111, 0b010, 0b010, 0b010, 0b111],
  J: [0b001, 0b001, 0b001, 0b101, 0b010],
  K: [0b101, 0b110, 0b100, 0b110, 0b101],
  L: [0b100, 0b100, 0b100, 0b100, 0b111],
  M: [0b101, 0b111, 0b111, 0b101, 0b101],
  N: [0b101, 0b111, 0b111, 0b111, 0b101],
  O: [0b010, 0b101, 0b101, 0b101, 0b010],
  P: [0b110, 0b101, 0b110, 0b100, 0b100],
  Q: [0b010, 0b101, 0b101, 0b110, 0b011],
  R: [0b110, 0b101, 0b110, 0b110, 0b101],
  S: [0b011, 0b100, 0b010, 0b001, 0b110],
  T: [0b111, 0b010, 0b010, 0b010, 0b010],
  U: [0b101, 0b101, 0b101, 0b101, 0b010],
  V: [0b101, 0b101, 0b101, 0b010, 0b010],
  W: [0b101, 0b101, 0b111, 0b111, 0b101],
  X: [0b101, 0b101, 0b010, 0b101, 0b101],
  Y: [0b101, 0b101, 0b010, 0b010, 0b010],
  Z: [0b111, 0b001, 0b010, 0b100, 0b111],
  '0': [0b010, 0b101, 0b101, 0b101, 0b010],
  '1': [0b010, 0b110, 0b010, 0b010, 0b111],
  '2': [0b110, 0b001, 0b010, 0b100, 0b111],
  '3': [0b110, 0b001, 0b010, 0b001, 0b110],
  '4': [0b101, 0b101, 0b111, 0b001, 0b001],
  '5': [0b111, 0b100, 0b110, 0b001, 0b110],
  '6': [0b011, 0b100, 0b111, 0b101, 0b010],
  '7': [0b111, 0b001, 0b010, 0b010, 0b010],
  '8': [0b010, 0b101, 0b010, 0b101, 0b010],
  '9': [0b010, 0b101, 0b111, 0b001, 0b110],
  ' ': [0b000, 0b000, 0b000, 0b000, 0b000],
  '-': [0b000, 0b000, 0b111, 0b000, 0b000],
  '.': [0b000, 0b000, 0b000, 0b000, 0b010],
  "'": [0b010, 0b010, 0b000, 0b000, 0b000],
};

const CHAR_W = 3;
const CHAR_H = 5;
const SPACING = 1;

/** Measure the width in logical pixels of a text string */
export function measureText(text: string): number {
  return text.length * (CHAR_W + SPACING) - SPACING;
}

/** Draw text at (x, y) in logical pixels using the 3x5 bitmap font */
export function drawText(
  ctx: CanvasRenderingContext2D,
  text: string,
  x: number, y: number,
  color: string,
): void {
  ctx.fillStyle = color;
  const upper = text.toUpperCase();
  let cx = x;
  for (let i = 0; i < upper.length; i++) {
    const glyph = GLYPHS[upper[i]];
    if (glyph) {
      for (let row = 0; row < CHAR_H; row++) {
        for (let col = 0; col < CHAR_W; col++) {
          if (glyph[row] & (1 << (CHAR_W - 1 - col))) {
            ctx.fillRect(cx + col, y + row, 1, 1);
          }
        }
      }
    }
    cx += CHAR_W + SPACING;
  }
}
