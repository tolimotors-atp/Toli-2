/** Live activation requires a separate approved release and a reviewed consent integration. */
export const advertising = Object.freeze({
  enabled: false,
  liveAdsAuthorized: false,
  publisherId: '',
  units: { 'after-gallery': '', 'before-footer': '' },
});
export type AdPlacementId = keyof typeof advertising.units;
export type AdConfiguration = {enabled:boolean;liveAdsAuthorized:boolean;publisherId:string;units:Record<AdPlacementId,string>};
export function canRequestAds(config:AdConfiguration, placement:AdPlacementId, consentGranted:boolean) {
  return config.enabled && config.liveAdsAuthorized && consentGranted && /^ca-pub-\d{16}$/.test(config.publisherId) && /^\d{10}$/.test(config.units[placement]);
}
/** Singleton script promise. No caller can load it without every release/configuration/consent gate. */
let scriptPromise:Promise<void>|undefined;
export function loadAdvertisingScript(config:AdConfiguration, placement:AdPlacementId, consentGranted:boolean):Promise<boolean> {
  if(!canRequestAds(config,placement,consentGranted))return Promise.resolve(false);
  scriptPromise ??= new Promise<void>((resolve,reject)=>{
    const existing=document.querySelector<HTMLScriptElement>('script[data-toli-adsense]');
    if(existing){if(existing.dataset.loaded==='true')resolve();else {existing.addEventListener('load',()=>resolve(),{once:true});existing.addEventListener('error',()=>reject(new Error('Advertising unavailable')),{once:true});}return;}
    const script=document.createElement('script');script.async=true;script.crossOrigin='anonymous';script.dataset.toliAdsense='true';
    script.src=`https://pagead2.googlesyndication.com/pagead/js/adsbygoogle.js?client=${config.publisherId}`;
    script.onload=()=>{script.dataset.loaded='true';resolve();};script.onerror=()=>{script.remove();scriptPromise=undefined;reject(new Error('Advertising unavailable'));};document.head.append(script);
  });
  return scriptPromise.then(()=>true).catch(()=>false);
}
