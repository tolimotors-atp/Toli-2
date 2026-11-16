import { Link } from 'react-router-dom';
import { adsConfigured, advertising } from '@/lib/advertising';
import { setConsent, useConsent } from '@/lib/consent';

/** Shown only when ads are configured. Nothing from Google loads until a choice is made. */
export default function ConsentBanner() {
  const { choice, reopened } = useConsent();
  if (!adsConfigured(advertising) || (choice && !reopened)) return null;
  const btn = 'rounded-full px-4 py-2 text-sm font-medium border border-border transition-colors focus-visible:outline focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-primary';
  return (
    <section role="dialog" aria-modal="false" aria-labelledby="consent-title" aria-describedby="consent-text"
      className="fixed bottom-3 left-3 right-[84px] md:right-auto md:left-1/2 md:-translate-x-1/2 md:w-[28rem] z-[2147483000] rounded-2xl border border-border bg-background text-foreground p-4 shadow-2xl">
      <h2 id="consent-title" className="font-display text-base tracking-wider mb-1">PRIVACY CHOICES</h2>
      <p id="consent-text" className="text-sm text-muted-foreground mb-3">
        This site may show Google ads, which use cookies. Accept to allow them, or reject to keep ads off.
        See our <Link to="/cookie-policy/" className="text-primary underline">Cookie Policy</Link>.
      </p>
      <div className="flex flex-wrap gap-2">
        <button type="button" autoFocus={reopened} className={`${btn} bg-primary text-primary-foreground`} onClick={() => setConsent('all')}>Accept all</button>
        <button type="button" className={`${btn} bg-background`} onClick={() => setConsent('essential')}>Reject non-essential</button>
      </div>
    </section>
  );
}
