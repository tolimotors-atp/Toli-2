import vehicles from '@/assets/hero/workshop-three-cars-960.webp';
import vehiclesLarge from '@/assets/hero/workshop-three-cars-1600.webp';

/** One transparent, coherently lit composition; no renderer or model-specific claims. */
export default function HeroVehicleLineup() {
 return <picture className="hero-three-cars">
  <source srcSet={`${vehicles} 960w, ${vehiclesLarge} 1600w`} sizes="(max-width:900px) 100vw, 70vw"/>
  <img src={vehicles} alt="Silver SUV, red sedan and graphite coupe" width="1600" height="372" decoding="async" {...{fetchpriority:'high'}}/>
 </picture>;
}
