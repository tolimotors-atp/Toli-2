# Pre-launch baseline — 4 November 2026

Target: `toli-static-website`; protected siblings are excluded from changes.

React 18 + Vite 5 + TypeScript + Tailwind, with Three.js illustration modules. `index.html` → `src/main.tsx` → `App.tsx`; HashRouter exposes homepage, canonical `/enquire-now`, three legal pages and a catch-all. Homepage is lazy loaded; below-fold modules and request steps are split. Existing 54 test files cover booking, navigation, imagery, themes, scene lifecycle and separation protection.

No AdSense/adsbygoogle script, publisher configuration, ad units or ads.txt found. No live ad requests are authorized. Existing integrations: click-to-load Google Maps, Google Fonts, external brand image CDN, user-initiated WhatsApp, optional unused Supabase client. Enquiry drafts live in an in-memory Map, AI answers locally; no server submission was found in the active request flow.

Initial concerns: legal-page placeholders and inaccurate privacy statements; unguarded localStorage consent read; fabricated-looking map embed identifier requiring removal/verification; contact card has two numbers with one call target; missing public domain prevents canonical/sitemap generation; inherited hash routing limits separate-page SEO; production 404 logs raw user route to console. Hosting TLS/headers/DNS cannot be verified locally. Three Hero assets and official logo must remain unchanged.

Baseline file hashes are retained in the audit evidence. Prior mobile screenshots in `docs/mobile-first-responsive` describe the previous implementation, not fresh evidence for this audit. Current build, tests, security audit and browser results will be recorded separately.
