import { prefersReducedMotion } from './motion';
export const experienceChapters=[{id:'hero',label:'Entry'},{id:'services',label:'Vehicle'},{id:'process',label:'Journey'},{id:'trust',label:'Toli Motors'},{id:'booking',label:'Request'},{id:'connect',label:'Contact'}];
/** Brief title card and heading entrance so a menu choice reads as arriving somewhere. */
function announceChapter(id:string,node:HTMLElement){
 if(prefersReducedMotion())return;
 const i=experienceChapters.findIndex(c=>c.id===id);
 const flash=document.createElement('div');flash.className='chapter-flash';flash.setAttribute('aria-hidden','true');
 const num=document.createElement('span'),title=document.createElement('strong');
 num.textContent=i>=0?String(i+1).padStart(2,'0'):'→';title.textContent=id==='services'?'Services':i>=0?experienceChapters[i].label:id.replace(/-/g,' ');
 flash.append(num,title);document.body.append(flash);setTimeout(()=>flash.remove(),1200);
 const heading=node.querySelector<HTMLElement>('.chapter-heading,h1,h2,.system-label')??node;
 setTimeout(()=>{heading.classList.add('chapter-arrive');setTimeout(()=>heading.classList.remove('chapter-arrive'),1400);},500);
}
export function navigateExperience(id:string){const node=document.getElementById(id);if(!node)return false;let parent=node.parentElement;while(parent){if(parent instanceof HTMLDetailsElement)parent.open=true;parent=parent.parentElement;}const panel=node.closest<HTMLElement>('[data-stack-document-top]');if(panel){const top=Number(panel.dataset.stackDocumentTop);const offset=parseFloat(panel.style.getPropertyValue('--stack-top'))||64;window.scrollTo({top:top-offset,behavior:prefersReducedMotion()?'auto':'smooth'});}else node.scrollIntoView({behavior:prefersReducedMotion()?'auto':'smooth'});announceChapter(id,node);return true;}
