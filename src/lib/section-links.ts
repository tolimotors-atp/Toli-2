import { navigateExperience } from "./experience-navigation";
const sections = new Set(["services", "offers", "about", "gallery", "customer-stories", "why-us", "contact", "hero", "process", "trust", "booking", "connect", "components", "whatsapp"]);
/** Normalize links saved before the site switched to browser routes. */
export function migrateLegacyLocation(base = import.meta.env.BASE_URL) {
  if (location.pathname !== base && location.pathname !== base.slice(0, -1)) return;
  let route = location.hash.slice(1);
  if (route.startsWith('%2F')) {
    try { route = decodeURIComponent(route); } catch { return; }
  }
  if (!route.startsWith('/') || route.startsWith('//') || route.includes('\\')) return;
  const url = new URL(base + route.slice(1), location.origin);
  if (url.origin !== location.origin || !url.pathname.startsWith(base)) return;
  const path = url.pathname.endsWith('/') ? url.pathname : url.pathname + '/';
  history.replaceState(history.state, '', path + (url.search || location.search) + url.hash);
  return true;
}
export function installSectionLinks() {
  let observer: MutationObserver | undefined;
  let timer: ReturnType<typeof setTimeout> | undefined;
  const navigate = () => {
    if (migrateLegacyLocation()) window.dispatchEvent(new PopStateEvent('popstate', { state: history.state }));
    observer?.disconnect(); clearTimeout(timer);
    const id = location.hash.slice(1);
    if (!sections.has(id)) return;
    const scroll = () => {
      const node = document.getElementById(id);
      if (!node) return false;
      navigateExperience(id);
      observer?.disconnect(); clearTimeout(timer); return true;
    };
    if (!scroll()) {
      observer = new MutationObserver(scroll);
      observer.observe(document.body, { childList: true, subtree: true });
      timer = setTimeout(() => observer?.disconnect(), 10000);
    }
  };
  // Clicking the current hash emits no hashchange; repeat anchors must still scroll.
  const repeat=(event:MouseEvent)=>{
    if(event.button!==0||event.ctrlKey||event.metaKey||event.shiftKey||event.altKey)return;
    const link=event.target instanceof Element?event.target.closest<HTMLAnchorElement>('a[href]'):null;
    if(!link||link.download||link.target&&link.target!=='_self')return;
    const url=new URL(link.href,location.href);
    if(url.origin!==location.origin||url.pathname!==location.pathname||url.search!==location.search||url.hash!==location.hash)return;
    const id=url.hash.slice(1);
    if(!sections.has(id))return;
    event.preventDefault();navigateExperience(id);
  };
  document.addEventListener('click',repeat,true);
  navigate(); window.addEventListener("hashchange", navigate);
  return () => { document.removeEventListener('click',repeat,true); observer?.disconnect(); clearTimeout(timer); window.removeEventListener("hashchange", navigate); };
}
