/** Viewport top of the shared car: scrolls in with Services, holds mid-screen, leaves with the end of Journey. */
export function sharedCarTop(natural: number, height: number, viewportHeight: number, navHeight: number, journeyBottom: number) {
  const hold = Math.max(navHeight + 16, (viewportHeight - height) / 2);
  return Math.min(Math.max(hold, natural), journeyBottom - height - 24);
}
