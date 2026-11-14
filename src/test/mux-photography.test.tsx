import { cleanup,render,screen } from '@testing-library/react';
import { afterEach,describe,expect,it,vi } from 'vitest';
import JourneyDock from '@/components/journey/JourneyDock';
const status=vi.hoisted(()=>({state:'ready'}));
vi.mock('@/components/journey/journey-context',()=>({useJourney:()=>({selected:0,componentFocus:false,state:status.state})}));
afterEach(cleanup);
describe('consistent front-sided transparent MU-X presentation',()=>{
 it.each(['ready','fallback'])('renders all three locations without 3D infrastructure when GPU state is %s',state=>{
  status.state=state;const {container}=render(<><JourneyDock mode="services" label="OVERVIEW"/><JourneyDock mode="process" label="PROCESS"/><JourneyDock mode="completion" label="REQUEST"/></>);
  const images=screen.getAllByAltText('Isuzu MU-X — front three-quarter view');expect(images).toHaveLength(3);
  expect(container.querySelector('[data-scene-dock],canvas,svg,[role=status]')).toBeNull();expect(container.textContent).not.toMatch(/360°|DRAG TO ROTATE/);
  for(const image of images){expect(image).toHaveAttribute('src',expect.stringContaining('mux-red-toli-front-3q-640.webp'));expect(image).toHaveAttribute('srcset',expect.stringContaining('1100w'));expect(image).toHaveAttribute('loading','lazy');expect(image).toHaveAttribute('decoding','async');}
  expect(container.querySelectorAll('.mux-photography img')).toHaveLength(3);
  expect(new Set(images.map(i=>i.getAttribute('src'))).size).toBe(1);
 });
});
