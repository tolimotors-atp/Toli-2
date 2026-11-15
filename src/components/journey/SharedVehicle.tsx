import { useEffect, useRef, useState } from 'react';
import MuxPhotography from './MuxPhotography';
import { useJourney } from './journey-context';
import { sharedCarTop } from '@/lib/shared-vehicle';
import './shared-vehicle.css';

/** One car for Services and Journey on wide screens: it holds still while their content scrolls, then leaves with Journey. */
export default function SharedVehicle() {
  const { selected, componentFocus } = useJourney();
  const box = useRef<HTMLDivElement>(null);
  const [on, setOn] = useState(false);
  useEffect(() => {
    const stack = box.current?.parentElement;
    const wide = matchMedia('(min-width:1100px)');
    if (!stack) return;
    let frame = 0;
    const place = () => {
      frame = 0;
      const el = box.current, dock = document.querySelector<HTMLElement>('#services .journey-dock'), journey = document.getElementById('process');
      const active = wide.matches && !!dock && !!journey;
      setOn(prev => (prev === active ? prev : active));
      if (!active || !el) { stack.dataset.sharedCar = 'off'; return; }
      const d = dock.getBoundingClientRect();
      const nav = document.querySelector('.experience-navigation')?.getBoundingClientRect().height ?? 64;
      const jr = journey.getBoundingClientRect();
      const top = sharedCarTop(d.top, d.height, innerHeight, nav, jr.bottom);
      stack.style.setProperty('--car-right', `${d.right - jr.left}px`);
      el.style.width = `${d.width}px`;
      el.style.height = `${d.height}px`;
      el.style.transform = `translate3d(${d.left}px,${top}px,0)`;
      // While the car still travels with the page the in-section photo is used, so nothing trails the scroll.
      stack.dataset.sharedCar = Math.abs(top - d.top) < 0.5 ? 'ready' : 'on';
    };
    const schedule = () => { if (!frame) frame = requestAnimationFrame(place); };
    const mutation = new MutationObserver(schedule);
    mutation.observe(stack, { childList: true, subtree: true });
    addEventListener('scroll', place, { passive: true });
    addEventListener('resize', place);
    schedule();
    return () => {
      cancelAnimationFrame(frame); mutation.disconnect();
      removeEventListener('scroll', place); removeEventListener('resize', place);
      delete stack.dataset.sharedCar;
    };
  }, []);
  return <div ref={box} className="shared-vehicle" aria-hidden="true">{on && <MuxPhotography highlight={componentFocus ? (selected === 1 ? 'wheel' : selected === 2 ? 'battery' : undefined) : undefined} />}</div>;
}
