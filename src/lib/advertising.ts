type Env = Record<string, string | undefined>;
/** Everything is off unless the build supplies these VITE_ variables (see docs/ADSENSE.md). */
export const adsenseConfig = (env: Env) => ({
  enabled: env.VITE_ADS_ENABLED === 'true',
  liveAdsAuthorized: env.VITE_ADS_LIVE_AUTHORIZED === 'true',
  publisherId: env.VITE_ADSENSE_PUBLISHER_ID ?? '',
  units: { 'after-gallery': env.VITE_ADSENSE_SLOT_AFTER_GALLERY ?? '', 'before-footer': env.VITE_ADSENSE_SLOT_BEFORE_FOOTER ?? '' },
});
export const advertising = Object.freeze(adsenseConfig(import.meta.env));
/** True when the consent banner and footer "Privacy choices" link are needed: ads can actually be requested later. */
export const adsConfigured = (c: { enabled: boolean; liveAdsAuthorized: boolean; publisherId: string }) =>
  c.enabled && c.liveAdsAuthorized && /^ca-pub-\d{16}$/.test(c.publisherId);
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
