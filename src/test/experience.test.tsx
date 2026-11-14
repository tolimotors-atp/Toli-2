import VehicleStudio from '@/components/VehicleStudio';
import { resetRequestDrafts } from '@/lib/service-request';
import { render, screen, fireEvent, waitFor, cleanup } from '@testing-library/react';
import { beforeEach, afterEach, expect, it, vi } from 'vitest';
import { MemoryRouter, Routes, Route } from 'react-router-dom';
import { JourneyProvider } from '@/components/journey/JourneyProvider';
import Services from '@/components/Services';
import ServiceRequest from '@/pages/ServiceRequest';
import Hero from '@/components/Hero';
import CtaBanner from '@/components/CtaBanner';
import HowItWorks from '@/components/HowItWorks';
import ExperienceNavigation from '@/components/journey/ExperienceNavigation';
import { navigateExperience } from '@/lib/experience-navigation';
const scene=vi.hoisted(()=>({select:vi.fn(),focus:vi.fn(),technical:vi.fn(),present:vi.fn(),dispose:vi.fn(),pause:vi.fn()}));
const loader=vi.hoisted(()=>vi.fn());
vi.mock('@/lib/load-vehicle-scene',()=>({loadVehicleScene:loader}));
let reduced=false,near:IntersectionObserverCallback;
beforeEach(()=>{
 resetRequestDrafts();vi.spyOn(window,'scrollTo').mockImplementation(()=>{});reduced=false;loader.mockReset();Object.values(scene).forEach(fn=>fn.mockReset());
 loader.mockResolvedValue({createVehicleScene:options=>{options.ready();return scene;}});
 vi.stubGlobal('innerWidth',1024);vi.stubGlobal('scrollY',0);
 vi.stubGlobal('matchMedia',(q:string)=>({get matches(){return q.includes('reduce')?reduced:true;},addEventListener:vi.fn(),removeEventListener:vi.fn()}));
 vi.stubGlobal('ResizeObserver',class{observe(){}unobserve(){}disconnect(){}});
 vi.stubGlobal('IntersectionObserver',class{constructor(cb:IntersectionObserverCallback,o?:IntersectionObserverInit){if(o?.rootMargin==='160px')near=cb;}observe(){}unobserve(){}disconnect(){}});
 vi.spyOn(HTMLElement.prototype,'getBoundingClientRect').mockReturnValue({top:100,bottom:600,left:0,right:600,width:600,height:500} as DOMRect);
 Object.defineProperty(HTMLElement.prototype,'scrollIntoView',{configurable:true,value:vi.fn()});
});
afterEach(()=>{cleanup();vi.restoreAllMocks();vi.unstubAllGlobals();delete (HTMLElement.prototype as unknown as {scrollIntoView?:unknown}).scrollIntoView;});
const mount=(children:React.ReactNode)=>render(<MemoryRouter><Routes><Route path="/" element={<JourneyProvider>{children}</JourneyProvider>}/><Route path="/enquire-now" element={<ServiceRequest/>}/></Routes></MemoryRouter>);
const revealService=()=>{if(screen.queryByLabelText('Name *')){fireEvent.change(screen.getByLabelText('Name *'),{target:{value:'QA Example'}});fireEvent.change(screen.getByLabelText('Phone Number *'),{target:{value:'9990000000'}});fireEvent.click(screen.getByRole('button',{name:'CONTINUE'}));fireEvent.click(screen.getByRole('button',{name:'CONTINUE'}));}};
it('does not describe the default illustration as an explicitly selected booking service',()=>{mount(<CtaBanner/>);expect(screen.getByText('Choose with our team')).toBeVisible();});
it('carries explicit matrix selection into the request and editable enquiry topic without submitting',async()=>{
 mount(<><Services/><CtaBanner/></>);fireEvent.click(screen.getByRole('button',{name:'Explore Battery Services'}));
 expect(screen.getAllByText('Battery Services')).toHaveLength(3);
 fireEvent.click(screen.getByRole('link',{name:/ENQUIRE NOW/}));expect(await screen.findByRole('heading',{name:'Service request.'})).toBeVisible();
 revealService();expect(screen.getByLabelText('Service Needed')).toHaveValue('Battery Services');fireEvent.change(screen.getByLabelText('Service Needed'),{target:{value:'Battery consultation'}});expect(screen.getByLabelText('Service Needed')).toHaveValue('Battery consultation');
});
it('synchronizes keyboard service choice and useful 2D component focus without loading a renderer',()=>{
 const {container}=mount(<Services/>);fireEvent.click(screen.getByRole('button',{name:'Explore Battery Services'}));
 fireEvent.focus(screen.getByRole('button',{name:'Explore Spare Parts & Repairs'}));fireEvent.click(screen.getByRole('button',{name:'Inspect component'}));
 expect(container.querySelector('[data-highlight="wheel"]')).not.toBeNull();expect(screen.getByRole('button',{name:'Return to vehicle'})).toBeVisible();
 fireEvent.click(screen.getByRole('button',{name:'Explore Premium Detailing'}));expect(container.querySelector('[data-highlight]')).toBeNull();expect(loader).not.toHaveBeenCalled();
});
it.each(['phone','reduced motion'])('keeps service information and the front photo usable without WebGL for %s',mode=>{
 if(mode==='phone')vi.stubGlobal('innerWidth',390);else reduced=true;const {container}=mount(<Services/>);fireEvent.click(screen.getByRole('button',{name:'Explore Battery Services'}));fireEvent.click(screen.getByRole('button',{name:'Inspect component'}));
 expect(screen.getByText('Amaron battery repair, replacement and maintenance. Ask which option is appropriate for your vehicle.')).toBeVisible();expect(container.querySelector('[data-highlight="battery"]')).not.toBeNull();expect(container.querySelector('canvas,[data-scene-dock],.vehicle-stage-loading')).toBeNull();expect(loader).not.toHaveBeenCalled();
});
it('shows actual process steps through one live description',()=>{mount(<HowItWorks/>);fireEvent.click(screen.getByRole('button',{name:'Explore step: Discuss next steps'}));expect(screen.getByRole('button',{name:'Explore step: Discuss next steps'})).toHaveAttribute('aria-pressed','true');expect(screen.getByRole('heading',{name:'Discuss next steps'})).toBeVisible();expect(screen.getByText(/An appointment is confirmed directly/)).toBeVisible();});
it('opens nested trust information before navigating and honors reduced motion',()=>{
 document.body.innerHTML='<details><summary>Gallery</summary><section id="gallery"></section></details>';reduced=true;expect(navigateExperience('gallery')).toBe(true);expect(document.querySelector('details')!.open).toBe(true);expect(HTMLElement.prototype.scrollIntoView).toHaveBeenCalledWith({behavior:'auto'});expect(navigateExperience('missing')).toBe(false);
});
it('provides discoverable chapter navigation and closes the menu with Escape, restoring focus',()=>{
 mount(<ExperienceNavigation/>);const menu=screen.getByRole('button',{name:'Open navigation menu'});fireEvent.click(menu);expect(screen.getByRole('button',{name:'Close navigation menu'})).toHaveAttribute('aria-expanded','true');expect(screen.getByRole('navigation',{name:'Experience chapters'})).toBeVisible();fireEvent.keyDown(window,{key:'Escape'});expect(menu).toHaveAttribute('aria-expanded','false');expect(menu).toHaveFocus();
});
it('carries actual service context and preserves edits when returning to the same requested service',async()=>{
 mount(<><Services/><CtaBanner/></>);fireEvent.click(screen.getByRole('button',{name:'Explore Battery Services'}));fireEvent.click(screen.getByRole('link',{name:/ENQUIRE NOW/}));revealService();expect(screen.getByLabelText('Service Needed')).toHaveValue('Battery Services');
 fireEvent.change(screen.getByLabelText('Service Needed'),{target:{value:'Battery consultation'}});fireEvent.click(screen.getByRole('button',{name:'Back to Toli Motors'}));fireEvent.click(screen.getByRole('button',{name:'Explore Battery Services'}));fireEvent.click(screen.getByRole('link',{name:/ENQUIRE NOW/}));revealService();expect(screen.getByLabelText('Service Needed')).toHaveValue('Battery consultation');
 fireEvent.click(screen.getByRole('button',{name:'Back to Toli Motors'}));fireEvent.click(screen.getByRole('button',{name:'Explore Spare Parts & Repairs'}));fireEvent.click(screen.getByRole('link',{name:/ENQUIRE NOW/}));revealService();expect(screen.getByLabelText('Service Needed')).toHaveValue('Spare Parts & Repairs');
});
it('retains the chosen process step independently of every vehicle image',()=>{
 const {container}=mount(<><Services/><HowItWorks/></>);fireEvent.click(screen.getByRole('button',{name:'Explore Battery Services'}));fireEvent.click(screen.getByRole('button',{name:'Explore step: Discuss next steps'}));fireEvent(window,new Event('resize'));
 expect(container.querySelector('[data-scene-dock],canvas')).toBeNull();expect(screen.getAllByAltText('Isuzu MU-X — front three-quarter view')).toHaveLength(2);expect(screen.getByRole('button',{name:'Explore step: Discuss next steps'})).toHaveAttribute('aria-pressed','true');expect(loader).not.toHaveBeenCalled();
});

it.each([1024,390])('keeps the standalone Book Service URL fallback without preselection at width %s',async width=>{
 vi.stubGlobal('innerWidth',width);mount(<><ExperienceNavigation/><Hero/><Services/></>);
 fireEvent.click(screen.getByRole('button',{name:'Explore Battery Services'}));
 expect(screen.queryByRole('link',{name:'Book Service'})).toBeNull();
 for(const name of ['Book Service ↗']){
  const trigger=screen.getByRole('link',{name});expect(trigger).toHaveAttribute('href','/enquire-now/');fireEvent.click(trigger);
  expect(await screen.findByRole('heading',{name:'Service request.'})).toBeVisible();await waitFor(()=>expect(screen.getByLabelText('Name *')).toHaveFocus());revealService();expect(screen.getByLabelText('Service Needed')).toHaveValue('');
  fireEvent.click(screen.getByRole('button',{name:'Back to Toli Motors'}));expect(await screen.findByRole('heading',{name:/Expert car care/})).toBeVisible();
 }
 expect(loader).not.toHaveBeenCalled();expect(scene.technical).not.toHaveBeenCalled();
});

it('pauses and resumes the existing homepage renderer around the shared popup without losing service selection',async()=>{
 vi.spyOn(HTMLElement.prototype,'getBoundingClientRect').mockImplementation(function(this:HTMLElement){return {top:this.closest('#hero')?-700:100,bottom:this.closest('#hero')?-200:600,left:0,right:600,width:600,height:500} as DOMRect;});
 const {default:PopupProvider}=await import('@/components/ServiceRequestDialog');
 render(<MemoryRouter><PopupProvider><JourneyProvider><ExperienceNavigation/><Hero/><VehicleStudio/></JourneyProvider></PopupProvider></MemoryRouter>);
 near([{isIntersecting:true} as IntersectionObserverEntry],{} as IntersectionObserver);await waitFor(()=>expect(loader).toHaveBeenCalledOnce());fireEvent.click(screen.getByRole('button',{name:'03 Battery Services'}));
 const before=scene.present.mock.calls.length;fireEvent.click(screen.getByRole('button',{name:'Book Service ↗'}));expect(scene.pause).toHaveBeenCalled();fireEvent(window,new Event('resize'));expect(scene.present).toHaveBeenCalledTimes(before);
 fireEvent.click(screen.getByRole('button',{name:'Close Service Request'}));await waitFor(()=>expect(scene.present.mock.calls.length).toBeGreaterThan(before));expect(scene.select).toHaveBeenLastCalledWith(2);expect(loader).toHaveBeenCalledOnce();
});
