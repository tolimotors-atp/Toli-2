import { expect, it } from 'vitest';
import { sharedCarTop } from '@/lib/shared-vehicle';

it('scrolls in, holds, then leaves with the journey section', () => {
  expect(sharedCarTop(900, 400, 800, 64, 3000)).toBe(900);  // still below the hold line: moves with the page
  expect(sharedCarTop(-300, 400, 800, 64, 3000)).toBe(200); // held mid-screen
  expect(sharedCarTop(-300, 400, 800, 64, 500)).toBe(76);   // journey ending: pushed up with it
});
