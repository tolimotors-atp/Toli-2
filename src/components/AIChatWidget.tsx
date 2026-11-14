import { useRef, useState } from 'react';
import AssistantBoundary from './ToliAI/AssistantBoundary';
import { Bot } from 'lucide-react';
import { useServiceRequestDialog } from './service-request-dialog-context';
import { useLocation } from 'react-router-dom';
import './ToliAI/toli-ai.css';
// The homepage is already route-lazy. Bundle this small local panel with it so
// a later launcher click cannot depend on a stale optional chunk URL.
import Panel from './ToliAI/ToliAIPanel';
export default function AIChatWidget(){
 const [open,setOpen]=useState(false),[loaded,setLoaded]=useState(false);
 const launcher=useRef<HTMLButtonElement>(null), request=useServiceRequestDialog(), location=useLocation();
 const hidden=request?.isOpen||(location.pathname!=='/'&&location.pathname!=='/classic');
 return <div className="toli-ai" hidden={hidden}>
  <button ref={launcher} className="toli-ai-launcher" aria-haspopup="dialog" aria-expanded={open} onClick={()=>{setLoaded(true);setOpen(true);}}><Bot size={18} aria-hidden="true"/>TOLI AI</button>
  {loaded&&<AssistantBoundary onClose={()=>{setOpen(false);setLoaded(false);launcher.current?.focus();}}><Panel open={open&&!hidden} onClose={()=>setOpen(false)} onReturnFocus={()=>launcher.current?.focus()} onRequest={service=>{setOpen(false);request?.open(service,launcher.current!);}}/></AssistantBoundary>}
 </div>;
}
