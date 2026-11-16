import { useSyncExternalStore } from 'react';
/** 'all' = ads may use cookies; 'essential' = no Google request is made. null = not chosen yet. */
export type Consent = 'all' | 'essential';
const KEY = 'toli-ad-consent';
const listeners = new Set<() => void>();
let reopened = false;
export function readConsent(): Consent | null {
  try { const v = localStorage.getItem(KEY); return v === 'all' || v === 'essential' ? v : null; } catch { return null; }
}
const emit = () => listeners.forEach(l => l());
export function setConsent(choice: Consent) {
  const withdrawn = readConsent() === 'all' && choice === 'essential';
  try { localStorage.setItem(KEY, choice); } catch { /* choice then lasts only for this page view */ memory = choice; }
  reopened = false;
  // Google's script cannot be unloaded, so withdrawing after ads loaded needs a fresh page.
  if (withdrawn && document.querySelector('script[data-toli-adsense]')) { location.reload(); return; }
  emit();
}
let memory: Consent | null = null; // used only when storage is blocked
export const currentConsent = () => readConsent() ?? memory;
export function reopenConsent() { reopened = true; emit(); }
const snapshot = () => `${currentConsent()}|${reopened}`;
const subscribe = (l: () => void) => { listeners.add(l); return () => listeners.delete(l); };
export function useConsent() {
  const [choice, open] = useSyncExternalStore(subscribe, snapshot, () => 'null|false').split('|');
  return { choice: (choice === 'null' ? null : choice) as Consent | null, reopened: open === 'true' };
}
