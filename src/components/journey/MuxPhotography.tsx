import frontSmall from '@/assets/vehicles/isuzu-mux/isuzu-mux-red-toli-front-3q-640.webp';
import frontLarge from '@/assets/vehicles/isuzu-mux/isuzu-mux-red-toli-front-3q.webp';
import './mux-photography.css';

export default function MuxPhotography({ highlight }: { highlight?: 'wheel' | 'battery' }) {
  return <figure className="mux-photography" data-mux-view="front" data-highlight={highlight}>
    <img src={frontSmall} srcSet={`${frontSmall} 640w, ${frontLarge} 1100w`} sizes="(min-width: 900px) 48vw, (min-width: 768px) 44vw, calc(100vw - 40px)" alt="Isuzu MU-X — front three-quarter view" width="1100" height="660" loading="lazy" decoding="async"/>
    {highlight && <span className="mux-area-marker" aria-hidden="true">{highlight==='wheel'?'Front wheel & brake area':'Under-bonnet area'}</span>}
  </figure>;
}
