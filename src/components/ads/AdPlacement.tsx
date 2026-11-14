import { lazy, Suspense } from 'react';
import { advertising, type AdPlacementId } from '@/lib/advertising';
import './advertising.css';
const Simulation = import.meta.env.DEV ? lazy(()=>import('@/dev/AdLayoutSimulation')) : null;
/** Disabled production slots occupy no space and make no requests. Live rendering is deliberately unreleased. */
export default function AdPlacement({placement}:{placement:AdPlacementId}) {
  if(Simulation && new URLSearchParams(location.search).has('adLayout'))return <Suspense fallback={null}><Simulation placement={placement}/></Suspense>;
  // A real unit and Google-certified consent integration must be reviewed together before enabling.
  if(!advertising.enabled || !advertising.liveAdsAuthorized)return null;
  return null;
}
