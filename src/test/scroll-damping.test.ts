import { expect, it } from 'vitest';
import { WHEEL_FACTOR, wheelPixels } from '@/lib/scroll-damping';

it('scales wheel travel and converts line and page deltas first', () => {
  expect(wheelPixels(100, 0, 800)).toBe(100 * WHEEL_FACTOR);
  expect(wheelPixels(3, 1, 800)).toBe(48 * WHEEL_FACTOR);
  expect(wheelPixels(1, 2, 800)).toBe(800 * WHEEL_FACTOR);
});
