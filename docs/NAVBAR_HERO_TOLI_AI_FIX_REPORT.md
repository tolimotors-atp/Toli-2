# Navbar, Hero information and TOLI AI fixes — 5 November 2026

Project: `/home/thunder/shared/tolimotors-main1/toli-static-website`.
Saved-source preview: http://127.0.0.1:8190/Toli-2/ . Production preview: http://127.0.0.1:8200/Toli-2/ . No deployment or Git commit performed.

## A. Navbar

The previous broad bright-red banner felt disconnected from the Dark Garage Hero. `navbar-brand.css` now uses the Hero's charcoal `#17181c`, metallic `#3b3e45`, graphite `#222329` and a bounded automotive-red reflection. A restrained white key light and glossy upper edge provide depth. Light mode uses pearl/silver, dark control text and a red booking action.

Navbar geometry, official logo pill, silver car artwork and animation, HELP+, theme switching, Book Service and MENU+ behavior are preserved. The existing compact mobile navigation still prioritizes functional controls; HELP remains available through its existing mobile menu placement.

## B. Hero text

Added `hero-corner-visibility.css`, imported after existing theme/responsive styles. Local translucent backplates sit behind the location and contact groups without scaling the Hero or adding a broad overlay. Dark mode uses pearl text; light mode uses dark ink and burgundy location emphasis. Stronger weights and restrained shadows improve contrast. The phone icon is visible on small layouts, both existing numbers and `tel:` links are unchanged, and mobile corner-group spacing is slightly increased to keep the backing surfaces clear.

Desktop groups remain in their existing upper-left/right positions below the navbar. Existing mobile/tablet positioning stacks or separates them according to available space. No Hero assets, logo pill, heading, caption, background, vehicle scale or camera code changed. Minor corner text/gap adjustments are the only Hero layout-related changes.

[Before desktop](navbar-hero-ai-evidence/before-desktop.jpg) · [After desktop dark](navbar-hero-ai-evidence/opening-dark-1440.jpg) · [After desktop light](navbar-hero-ai-evidence/opening-light-1440.jpg) · [Side-by-side](navbar-hero-ai-evidence/before-after-desktop.jpg).

[Archived mobile baseline](navbar-hero-ai-evidence/before-mobile-archived.jpg) · [After mobile dark](navbar-hero-ai-evidence/opening-dark-320.jpg) · [After mobile light](navbar-hero-ai-evidence/opening-light-320.jpg) · [Tablet](navbar-hero-ai-evidence/opening-dark-768.jpg). The mobile before image comes from the immediately preceding theme task, not a fresh capture in this task.

## C. TOLI AI diagnosis and repair

### Confirmed issues

1. The baseline launcher and typed Enter submission worked in the initial production check, but the supported question “Tell me about TOLI Motors” fell through to the unknown-question reply. There was no business-about intent/knowledge entry. Contact knowledge also omitted the second verified number; unknown questions had no direct enquiry action.
2. A development-preview interruption produced a failed dynamic request for the click-time `ToliAIPanel.tsx` URL. The server subsequently became unavailable. This exposes the existing extra lazy-import dependency: if that import rejects, React's module-level lazy component retains the rejected load. It was a load-availability failure, not a proven broken React click handler. No blanket claim that all launcher failures were reproduced is made.
3. Viewport handling had no window-resize fallback when `visualViewport` was absent, and errors thrown by the synchronous answer function escaped the event handler.

### Saved fixes

- Bundle the small panel with the already route-lazy homepage rather than fetching another optional module at launcher-click time. Preserve the error boundary, conversation state and booking integration. No new libraries or cloud services.
- Add an ABOUT intent using approved existing workshop information, both verified contact numbers, explicit unverified-hours guidance and useful Service Request actions for unsupported questions.
- Catch local answer failures and retain the visitor's message alongside a useful fallback/action. Subsequent questions can still work.
- Track both visual-viewport and window resizing; restore panel bounds when the viewport expands again.
- Keep the existing single-line input and native Enter form submission. Prevent Enter during IME composition from accidentally submitting unfinished text. No multiline editor was introduced.

Supported topics include workshop identity, all nine services, servicing/repairs, booking/enquiry instructions, location and contact. Hours, prices, availability, policies and certifications are not invented. The assistant remains a deterministic local FAQ helper, not a cloud language model or vehicle diagnostic tool.

### Browser evidence

[Baseline wrong reply](navbar-hero-ai-evidence/before-ai.jpg) · [Verified interaction transcript](navbar-hero-ai-evidence/ai-interactions.json) · [Repaired desktop conversation](navbar-hero-ai-evidence/ai-desktop.jpg).

Actual saved-source browser interactions verified typed questions via **both Enter and Send**, supported business/services/contact answers, honest hours/unsupported fallback, repeated questions, visible message rendering and Escape/focus restoration. Production checks verified the AI's booking action opens the canonical Service Request popup with its service context. Final production console had no warnings/errors.

A direct resilience check loaded the development homepage, stopped only the agent-started dev server, then opened the assistant and submitted a new location question successfully. The dev server was restored afterward. [Evidence](navbar-hero-ai-evidence/ai-server-unavailable-after-load.jpg). This demonstrates local operation after page load; it does not promise a first visit can load without the website server or replace deployment asset-retention requirements.

## D. Local file verification

All edits were saved directly under the actual target project as each logical change completed. The dev preview visibly rendered the saved gradient and contact links. Current file sizes/SHA-256 values are recorded in [saved-source-manifest.json](navbar-hero-ai-evidence/saved-source-manifest.json); this is a saved-file inventory, not a full before/after repository hash comparison. The directory is not a Git repository, so no Git diff, reset or commit was used.

Implementation/test files changed:

- `src/components/journey/navbar-brand.css`
- `src/components/journey/hero-corner-visibility.css` (new)
- `src/main.tsx` (new corner stylesheet import)
- `src/components/AIChatWidget.tsx`
- `src/components/ToliAI/ToliAIPanel.tsx`
- `src/ai/assistant.ts`
- `src/ai/intents.ts`
- `src/ai/knowledge.ts`
- `src/ai/types.ts`
- `src/test/toli-ai.test.tsx`
- `src/test/fixtures/separation-protected.json` (only the two authorized assistant component hashes updated)

Supporting files: this report, [concise change log](NAVBAR_HERO_TOLI_AI_CHANGELOG.md) and `docs/navbar-hero-ai-evidence/`.

Services/theme finish, Gallery, booking/WhatsApp implementation, advertising code/configuration and separate 3D/original sibling projects were not edited. Existing unrelated changes were retained. Protected artwork/retained-source regression tests pass.

## E. Validation

- Focused navbar tests: 5 PASS.
- Focused Hero tests: 4 PASS.
- Focused AI tests: 35 PASS, including six new tests for approved/fallback knowledge, empty/repeated submissions, Escape/focus, answer-error recovery, visual-viewport keyboard resizing and window-only resizing.
- Final full suite: **394 PASS across 55 files**.
- Production build: PASS (17.50s). Existing large-chunk/Tailwind utility warnings remain.
- TypeScript application/node/QA: PASS. Two intermediate type errors in the new handler/test were corrected before the final checks.
- Lint: PASS.
- Both themes tested at **320×568, 360×640, 390×844, 430×932, 768×1024, 1440×900, 1920×1080**.
- At every width, document width stayed within the viewport and location/contact rectangles did not overlap. Dark measurements also show both groups below the navbar. Phone links retain `tel:+919908303888` and `tel:+918074946335`; phone calls were not initiated.
- AI panel and input bounds fit every listed viewport in both themes. A live 390×400 viewport check enabled compact mode and kept the input bottom at 379px; restoring 390×844 restored the available panel height. Unit tests additionally exercise visual-viewport height/offset changes. This simulates constrained keyboard space; physical Android/iOS keyboard behavior is **not certified**.
- Gallery, service selection, canonical request routing, WhatsApp handoff and ad safeguards retain their existing automated regression coverage. No enquiry or message was sent externally.

[Responsive corner measurements](navbar-hero-ai-evidence/responsive.json) · [Light AI bounds](navbar-hero-ai-evidence/ai-responsive.json) · [Dark AI bounds](navbar-hero-ai-evidence/ai-responsive-dark.json). Screenshots for every requested size/theme are included in the evidence folder.

### Current performance check

Fresh final-build Lighthouse 13.6.0 / Chromium mobile simulation: **Performance 60, Accessibility 100, Best Practices 100, SEO 100**; LCP **5.4s**, TBT **780ms**, CLS **0**. Raw report: [lighthouse-current.json](navbar-hero-ai-evidence/lighthouse-current.json).

The historical 59/100/100/100 is not a fresh baseline. There was no controlled before/after performance run in this task, so no improvement or no-regression claim is made. Performance remains a launch concern; TBT is not field INP. Bundling the small assistant with the already route-lazy homepage trades a little initial homepage JavaScript for reliable click-time availability. No external AI dependency, expensive blur, new artwork or continuously running effect was added.

Previous legal/owner confirmations, advisory remediation, production hosting/asset retention and physical-device/cross-browser validation remain outstanding. This task is not a launch approval.

## Acceptance

| Criterion | Status |
|---|---|
| NAVBAR MATCHES HERO THEME | PASS |
| ANANTAPUR TEXT READABLE | PASS |
| CONTACT DETAILS READABLE | PASS |
| CONTACT LINKS WORKING | PASS — correct existing telephone destinations |
| TOLI AI OPENS | PASS |
| TOLI AI ACCEPTS MESSAGES | PASS |
| TOLI AI GENERATES RESPONSES | PASS — supported local FAQ scope |
| TOLI AI MOBILE FUNCTIONALITY | PASS in listed browser checks; physical keyboard certification outstanding |
| LOCAL SOURCE FILES UPDATED | PASS |
| LOCAL PREVIEW REFLECTS CHANGES | PASS |
| EXISTING FUNCTIONALITY PRESERVED | PASS for full automated suite and checked browser flows |
| ADSENSE SAFEGUARDS PRESERVED | PASS — source untouched, regression tests pass |
| SEPARATE 3D WEBSITE UNCHANGED | PASS — no files edited |
| DEPLOYMENT | NOT PERFORMED |
