import {useEffect,useState} from 'react';
import type {AdPlacementId} from '@/lib/advertising';
const scenarios=['none','small','large','slow','failed','blocked','multiple'] as const;
export default function AdLayoutSimulation({placement}:{placement:AdPlacementId}) {
 const value=new URLSearchParams(location.search).get('adLayout');
 const scenario=scenarios.find(s=>s===value)??'none';
 const [loaded,setLoaded]=useState(false);
 useEffect(()=>{if(scenario!=='slow')return;const timeout=setTimeout(()=>setLoaded(true),4000);return()=>clearTimeout(timeout);},[scenario]);
 if(scenario==='none'||scenario==='failed'||scenario==='blocked'||(placement==='before-footer'&&scenario!=='multiple'))return null;
 return <aside className={`ad-layout-region ad-layout-${scenario}`} aria-label="Development advertisement layout simulation" data-ad-placement={placement} data-ad-scenario={scenario}>
  <p className="ad-layout-label">ADVERTISEMENT · DEVELOPMENT LAYOUT ONLY</p>
  <div className="ad-layout-placeholder" role="img" aria-label="Development placeholder. No advertisement or ad request.">{scenario==='slow'&&!loaded?'Reserved space · simulated slow load':'Layout simulation · no live advertisement'}</div>
 </aside>;
}
