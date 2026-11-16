import { lazy, Suspense, useEffect, useRef } from 'react';
import { advertising, canRequestAds, loadAdvertisingScript, type AdPlacementId } from '@/lib/advertising';
import { useConsent } from '@/lib/consent';
import './advertising.css';
const Simulation = import.meta.env.DEV ? lazy(()=>import('@/dev/AdLayoutSimulation')) : null;
/** Renders nothing (no space, no request) unless every gate in canRequestAds passes. Home page only. */
export default function AdPlacement({placement}:{placement:AdPlacementId}) {
  const {choice}=useConsent();
  const allowed=canRequestAds(advertising,placement,choice==='all');
  const pushed=useRef(false);
  useEffect(()=>{
    if(!allowed)return;let live=true;
    loadAdvertisingScript(advertising,placement,true).then(ok=>{
      if(!ok||!live||pushed.current)return;pushed.current=true;
      try{((window as unknown as {adsbygoogle:unknown[]}).adsbygoogle??=[]).push({});}catch{/* ad blocked or failed: the reserved box stays empty */}
    });
    return()=>{live=false;};
  },[allowed,placement]);
  if(Simulation && new URLSearchParams(location.search).has('adLayout'))return <Suspense fallback={null}><Simulation placement={placement}/></Suspense>;
  if(!allowed)return null;
  return <aside className="ad-slot" aria-label="Advertisement" data-ad-placement={placement}>
    <p className="ad-slot-label">Advertisement</p>
    <div className="ad-slot-box"><ins className="adsbygoogle" style={{display:'block',height:'100%'}} data-ad-client={advertising.publisherId} data-ad-slot={advertising.units[placement]} data-ad-format="auto" data-full-width-responsive="true"/></div>
  </aside>;
}
