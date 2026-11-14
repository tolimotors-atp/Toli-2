import {render,screen,fireEvent,waitFor,cleanup} from '@testing-library/react';
import {afterEach,it,expect,vi} from 'vitest';
import {MemoryRouter} from 'react-router-dom';
import ExperienceNavigation from '@/components/journey/ExperienceNavigation';
afterEach(()=>{cleanup();vi.restoreAllMocks();});
it('opens the disclosure predictably from keyboard and restores focus on Escape',async()=>{
 render(<MemoryRouter><ExperienceNavigation/></MemoryRouter>);
 const trigger=screen.getByRole('button',{name:'Open navigation menu'});trigger.focus();fireEvent.click(trigger,{detail:0});
 await waitFor(()=>expect(document.querySelector('#experience-menu>button')).toHaveFocus());
 expect(document.querySelector('#experience-menu')).toHaveTextContent('Services');fireEvent.keyDown(window,{key:'Escape'});
 expect(trigger).toHaveFocus();expect(document.getElementById('experience-menu')).toBeNull();expect(trigger).toHaveAttribute('aria-expanded','false');
 expect(screen.getByRole('link',{name:'Book Service ↗'})).toHaveAttribute('title','Book Service');
});
it('returns menu focus without cancelling navigation to a section',()=>{
 const scroll=vi.spyOn(window,'scrollTo').mockImplementation(()=>{});
 const {container}=render(<MemoryRouter><ExperienceNavigation/><section id="services" data-stack-document-top="900"/></MemoryRouter>);
 (container.querySelector('#services') as HTMLElement).style.setProperty('--stack-top','68px');
 const trigger=screen.getByRole('button',{name:'Open navigation menu'}),focus=vi.spyOn(trigger,'focus');
 fireEvent.click(trigger,{detail:1});fireEvent.click(screen.getByRole('button',{name:'02 Services ↗'}));
 expect(scroll).toHaveBeenCalledWith(expect.objectContaining({top:832}));
 expect(focus).toHaveBeenCalledWith({preventScroll:true});expect(trigger).toHaveFocus();
});
