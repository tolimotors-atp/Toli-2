/** Mouse wheel and trackpad travel this fraction of the native distance. Lower is slower. */
export const WHEEL_FACTOR = 0.5;

/** Pixels for one wheel event: line and page deltas are converted first. */
export function wheelPixels(deltaY: number, deltaMode: number, viewportHeight: number) {
  const px = deltaMode === 1 ? deltaY * 16 : deltaMode === 2 ? deltaY * viewportHeight : deltaY;
  return px * WHEEL_FACTOR;
}

function insideScroller(node: EventTarget | null) {
  for (let el = node instanceof HTMLElement ? node : null; el && el !== document.body; el = el.parentElement) {
    const { overflowY } = getComputedStyle(el);
    if ((overflowY === 'auto' || overflowY === 'scroll') && el.scrollHeight > el.clientHeight + 1) return true;
  }
  return false;
}

/** Eased, slower page scroll for wheels and trackpads. shortcut: touch scrolling stays native, a site cannot rescale it without hijacking touch. */
export function installScrollDamping() {
  if (typeof window === 'undefined' || window.matchMedia?.('(prefers-reduced-motion: reduce)').matches) return () => {};
  let target = scrollY, expected = scrollY, frame = 0, animating = false;
  // Hands the page back to the browser: used when the user grabs the scrollbar, presses a key or touches.
  const stop = () => { cancelAnimationFrame(frame); frame = 0; animating = false; target = scrollY; };
  const step = () => {
    const distance = target - scrollY;
    if (Math.abs(distance) < 1) { scrollTo({ top: target, behavior: 'instant' }); animating = false; frame = 0; return; }
    scrollTo({ top: scrollY + distance * 0.2, behavior: 'instant' });
    expected = scrollY;
    frame = requestAnimationFrame(step);
  };
  const wheel = (e: WheelEvent) => {
    if (e.ctrlKey || e.defaultPrevented || Math.abs(e.deltaX) > Math.abs(e.deltaY)) return;
    if (document.querySelector('[role=dialog][aria-modal=true]') || insideScroller(e.target)) return;
    e.preventDefault();
    if (!animating) target = scrollY;
    const max = document.documentElement.scrollHeight - innerHeight;
    target = Math.min(max, Math.max(0, target + wheelPixels(e.deltaY, e.deltaMode, innerHeight)));
    animating = true;
    expected = scrollY;
    if (!frame) frame = requestAnimationFrame(step);
  };
  // A scroll we did not cause (scrollbar drag, menu jump) ends the easing and resets the target.
  const sync = () => {
    if (!animating) target = scrollY;
    else if (Math.abs(scrollY - expected) > 2) stop();
  };
  addEventListener('wheel', wheel, { passive: false });
  addEventListener('scroll', sync, { passive: true });
  addEventListener('pointerdown', stop, { passive: true });
  addEventListener('keydown', stop);
  addEventListener('touchstart', stop, { passive: true });
  return () => {
    removeEventListener('wheel', wheel); removeEventListener('scroll', sync);
    removeEventListener('pointerdown', stop); removeEventListener('keydown', stop); removeEventListener('touchstart', stop);
    cancelAnimationFrame(frame);
  };
}
