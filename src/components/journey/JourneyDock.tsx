import { useJourney } from './journey-context';
import { sceneService } from '@/lib/journey';
import VehicleIllustration from './VehicleIllustration';
import MuxPhotography from './MuxPhotography';
import type { JourneyDockMode } from '@/lib/journey';
export default function JourneyDock({mode,label}:{mode:JourneyDockMode;label:string}) {
  const {selected,componentFocus,state}=useJourney();
  const photographic=mode==='services'||mode==='process'||mode==='completion';
  return <div className={`journey-dock journey-dock-${mode}`} data-component={mode==='completion'?0:sceneService(selected)}>
    <div className="vehicle-stage-label" aria-hidden="true"><span>{label}</span><span>TOLI / CARE</span></div>
    {photographic?<MuxPhotography highlight={mode==='services'&&componentFocus?(selected===1?'wheel':selected===2?'battery':undefined):undefined}/>:state==='fallback'?<VehicleIllustration focus={false} technical={false} service={selected} mode={mode}/>:<div className="vehicle-stage-loading" role="status">Preparing vehicle view</div>}
    {!photographic&&<div data-scene-dock={mode} className="journey-webgl" aria-hidden="true"/>}
    <div className="vehicle-stage-bottom"><span>{!photographic&&state==='fallback'?'Static fallback · ':''}Illustrative vehicle · not a diagnostic result</span></div>
  </div>;
}
