import { afterEach, expect, it, vi } from 'vitest';
import { act, cleanup, fireEvent, render, screen, waitFor } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import * as assistant from '@/ai/assistant';
import { answer } from '@/ai/assistant';
import AIChatWidget from '@/components/AIChatWidget';
import { ServiceRequestDialogContext } from '@/components/service-request-dialog-context';
afterEach(()=>{cleanup();vi.restoreAllMocks();vi.unstubAllGlobals();});
it.each([
 ['hello','GREETING'],['what services do you provide','SERVICES_OVERVIEW'],['battery problem','BATTERY'],["my car won't start",'BATTERY'],['I need spare parts','SPARE_PARTS'],['I want detailing','DETAILING'],['vehicle inspection','VEHICLE_INSPECTION'],['pickup my car','DOORSTEP_PICKUP'],['AMC','AMC'],['book service','BOOK_SERVICE'],["tell me tomorrow's weather",'UNKNOWN'],['batery','BATTERY'],['detaling','DETAILING'],['servce','AUTOMOBILE_SERVICE'],['inspecion','VEHICLE_INSPECTION'],['car repair','REPAIR'],['I want consultation','CONSULTATION'],['Do you provide installation','INSTALLATION'],['where are you located','LOCATION'],['Contact TOLI','CONTACT'],['help','HELP'],['what do you guys do','SERVICES_OVERVIEW'],['wash my car','DETAILING'],['pick up my car','DOORSTEP_PICKUP'],['check my vehicle','VEHICLE_INSPECTION'],['How much is battery service','UNKNOWN'],['opening hours','UNKNOWN'],
])('recognizes %s', (query,intent)=>expect(answer(query).intent).toBe(intent));
it('uses cautious starting guidance and remembers the service for a request',()=>{
 const result=answer("my car won't start");expect(result.text).toContain('several causes');expect(result.text).not.toMatch(/battery is dead|diagnosis complete/i);
 const followup=answer('How do I request it?',result.context);expect(followup.service).toBe('Battery Services');expect(followup.action).toBe('Request Battery Services');
 expect(answer('book battery service').service).toBe('Battery Services');
 expect(answer('my brakes make noise').text).toContain('professional inspection');
});
it('answers without network or persistence and opens the existing request action',async()=>{
 const fetch=vi.fn(()=>{throw Error('Network forbidden');});vi.stubGlobal('fetch',fetch);
 const open=vi.fn();render(<MemoryRouter><ServiceRequestDialogContext.Provider value={{isOpen:false,open}}><AIChatWidget/></ServiceRequestDialogContext.Provider></MemoryRouter>);
 const launcher=screen.getByRole('button',{name:'TOLI AI'});fireEvent.click(launcher);
 await screen.findByRole('dialog');fireEvent.click(screen.getByRole('button',{name:'Battery Services'}));
 expect(await screen.findByText(/Amaron battery/)).toBeInTheDocument();
 fireEvent.change(screen.getByRole('textbox',{name:'Ask about a service'}),{target:{value:'How do I request it?'}});fireEvent.click(screen.getByRole('button',{name:'Send message'}));
 const actions=screen.getAllByRole('button',{name:'Request Battery Services ↗'});fireEvent.click(actions[actions.length-1]);
 expect(open).toHaveBeenCalledWith('Battery Services',launcher);expect(fetch).not.toHaveBeenCalled();
 await waitFor(()=>expect(screen.queryByRole('dialog')).toBeNull());fireEvent.click(launcher);await screen.findByRole('dialog');
 fireEvent.click(screen.getByRole('button',{name:'Close TOLI AI'}));await waitFor(()=>expect(launcher).toHaveFocus());
});

const mountAssistant=async()=>{
 render(<MemoryRouter><AIChatWidget/></MemoryRouter>);
 const launcher=screen.getByRole('button',{name:'TOLI AI'});
 fireEvent.click(launcher);await screen.findByRole('dialog');
 return {launcher,input:screen.getByRole('textbox',{name:'Ask about a service'})};
};
it('answers approved business questions and gives an actionable, honest fallback',()=>{
 expect(answer('Tell me about TOLI Motors')).toMatchObject({intent:'ABOUT',action:'Request Service'});
 expect(answer('Tell me about TOLI Motors').text).toContain('multi-brand car workshop');
 expect(answer('contact').text).toContain('9908303888');
 expect(answer('opening hours').text).toContain('not verified');
 expect(answer('services offered').intent).toBe('SERVICES_OVERVIEW');
 expect(answer('unsupported spaceship question').action).toBe('Request Service');
 expect(answer('what does battery service cost').intent).toBe('UNKNOWN');
});
it('ignores empty input, sends typed questions and retains repeated messages',async()=>{
 const {input}=await mountAssistant();const send=screen.getByRole('button',{name:'Send message'});
 expect(send).toBeDisabled();fireEvent.change(input,{target:{value:'   '}});fireEvent.submit(input.closest('form')!);
 expect(document.querySelectorAll('.toli-ai-message.user')).toHaveLength(0);
 for(let i=0;i<2;i++){fireEvent.change(input,{target:{value:'Where are you located?'}});fireEvent.click(send);}
 expect(document.querySelectorAll('.toli-ai-message.user')).toHaveLength(2);
 expect(screen.getAllByText(/TOLI Motors is at/)).toHaveLength(2);
 expect(input).toHaveValue('');expect(input).toHaveFocus();
 fireEvent.change(input,{target:{value:'unrecognized question'}});fireEvent.submit(input.closest('form')!);
 expect(screen.getByText(/I don’t have verified information/)).toBeVisible();
});
it('closes with Escape and restores keyboard focus to the launcher',async()=>{
 const {launcher,input}=await mountAssistant();expect(launcher).toHaveAttribute('aria-expanded','true');
 fireEvent.keyDown(input,{key:'Escape',code:'Escape'});
 await waitFor(()=>expect(screen.queryByRole('dialog')).toBeNull());
 expect(launcher).toHaveFocus();expect(launcher).toHaveAttribute('aria-expanded','false');
});
it('keeps messages and an enquiry action visible if the local answer function fails',async()=>{
 const {input}=await mountAssistant();vi.spyOn(assistant,'answer').mockImplementationOnce(()=>{throw new Error('local answer failure');});
 fireEvent.change(input,{target:{value:'Battery question'}});fireEvent.click(screen.getByRole('button',{name:'Send message'}));
 expect(screen.getByText('Battery question')).toBeVisible();
 expect(screen.getByText(/I could not answer that question/)).toBeVisible();
 expect(screen.getByRole('button',{name:'Request Service ↗'})).toBeVisible();
 fireEvent.change(input,{target:{value:'contact'}});fireEvent.click(screen.getByRole('button',{name:'Send message'}));
 expect(screen.getByText(/Call \+91-8074946335/)).toBeVisible();
});
it('adapts to visual viewport keyboard resizing and restores the full-height panel',async()=>{
 const visual=Object.assign(new EventTarget(),{height:420,offsetTop:120});vi.stubGlobal('visualViewport',visual);
 await mountAssistant();const panel=screen.getByRole('dialog');expect(panel).toHaveAttribute('data-compact','true');
 expect(panel.style.getPropertyValue('--ai-height')).toBe('420px');
 visual.height=780;visual.offsetTop=0;act(()=>{visual.dispatchEvent(new Event('resize'));});
 await waitFor(()=>expect(panel).toHaveAttribute('data-compact','false'));
 expect(panel.style.getPropertyValue('--ai-top')).toBe('0px');
});
it('updates the panel when window resizing is the only available viewport signal',async()=>{
 vi.stubGlobal('visualViewport',undefined);vi.stubGlobal('innerHeight',800);await mountAssistant();
 vi.stubGlobal('innerHeight',390);fireEvent(window,new Event('resize'));
 await waitFor(()=>expect(screen.getByRole('dialog')).toHaveAttribute('data-compact','true'));
 expect(screen.getByRole('dialog').style.getPropertyValue('--ai-height')).toBe('390px');
});
