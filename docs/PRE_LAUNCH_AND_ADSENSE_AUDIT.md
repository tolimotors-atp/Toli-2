# TOLI MOTORS — Pre-launch and AdSense audit

Audit date: **4 November 2026 (Asia/Kolkata)**. Target: `/home/thunder/shared/tolimotors-main1/toli-static-website`.

## A. Executive summary

**Decision: NOT READY — BLOCKERS REMAIN.** The local application builds and the checked enquiry/navigation workflows work. This is a completed local audit and preparation pass, not authorization to publish or activate ads.

Release blockers:

1. Legal pages still need owner-approved legal entity, effective date, retention period, warranty/bailment and jurisdiction details. Draft warnings were added instead of inventing missing facts.
2. Dependency security audit still reports **24 affected package records: 2 critical, 2 high, 20 moderate** after compatible updates (initially 27: 2 critical, 18 high, 7 moderate). Records include transitive effects, not 24 distinct exploits. Critical findings involve development/test tooling (Vitest/Tinypool); high findings include Zod and Vite. Major upgrades/targeted mitigation and full compatibility testing are required before release sign-off. Development servers must remain private; do not deploy node_modules or the development server.
3. The final throttled mobile Lighthouse performance score is **59**, with LCP **5.4 seconds**, above the 2.5-second target. CLS is 0 in this lab run. This is not a field Core Web Vitals pass.
4. No approved production domain/hosting configuration is supplied. Canonical URL, sitemap, DNS, TLS, deployment headers, caching, monitoring and rollback cannot be signed off on localhost.
5. Firefox, dedicated Chrome/Edge, Safari/WebKit, physical devices, native 200% text zoom and real virtual-keyboard behavior were not validated in this run. Only the available Chromium browser and Lighthouse mobile emulation were exercised.
6. Live AdSense is intentionally unreleased. Publisher and ad-unit identifiers, ownership verification, ads.txt, reviewed privacy disclosures and consent integration must be completed in a separately authorized release.

Recommended next actions: resolve owner/legal facts; migrate/mitigate vulnerable dependencies; reduce initial CSS/JavaScript/layout work and remeasure; complete named-browser/device checks; configure a private staging host and public URL. Keep live ads disabled until that gate passes.

## B. Baseline, UI findings and fixes

The [baseline inspection](PRE_LAUNCH_BASELINE.md) records the React 18/Vite/TypeScript/HashRouter structure, entry points, existing tests and integrations before implementation. No AdSense setup or ad containers existed.

Preserved: red navbar, metallic logo pill, official logo artwork, silver navbar sports car, three Hero vehicles, workshop imagery, dark/light themes and existing section structure. No Hero redesign or separate-showroom changes were made.

Applied fixes:

- Self-hosted the same Inter and Bebas Neue font resources with their OFL licenses, removing Google Fonts requests and the external stylesheet dependency. Existing font family names and typography remain.
- Added a lossless WebP delivery alternative for the original logo: **333,374 → 189,188 bytes**. Original PNG is retained as fallback/source. Decoded alpha and all nontransparent pixel colors are identical; only invisible RGB values under fully transparent pixels differ. No recoloring, cropping or artwork regeneration.
- Added a 64px favicon: **4,530 bytes** (original favicon retained). Corrected navbar image intrinsic dimensions to match its actual source ratio, without changing artwork or CSS placement.
- Gallery reserves a neutral aspect-ratio slot while its source is deferred, rather than showing a broken image icon. A failed photo does not poison the next image in the lightbox.
- Fixed prohibited ARIA on animated statistics; excluded decorative step indices from accessible names; included the service-card notes in accessible names; underlined the map policy link. Final Lighthouse Accessibility is 100.
- Guarded map consent reads when browser storage is unavailable. Added explicit consent revocation. Replaced the unverified hand-written map embed token with an address query using the existing project address. Actual pin accuracy still needs owner confirmation.
- Both displayed contact numbers now have independent telephone links and touch targets; the second no longer shares the first number's action.
- Removed raw invalid-route console logging. Updated factual privacy/cookie statements for page-memory drafts, local preferences, CDN requests, self-hosted fonts and disabled advertising. Replaced malformed placeholder email links with the existing published business contact; owner confirmation of privacy handling remains required.
- Prepared disabled ad configuration, guarded singleton script utility, two inactive placement boundaries and a development-only simulator. Nothing renders or requests advertisements in normal production.

Evidence: [before phone](pre-launch-evidence/before-390.jpg), [before desktop](pre-launch-evidence/before-1440.jpg), [final phone](pre-launch-evidence/viewport-390x844.jpg), [all opening views](pre-launch-evidence/viewport-overview.jpg).

## C. Responsive testing

Fresh browser measurements and screenshots cover all 12 required viewports. PASS below means the inspected application layout has no measured horizontal document overflow, no paragraph/heading bounding boxes beyond the viewport, and the request dialog has no internal horizontal overflow. It does not imply a physical-device or full accessibility certification. Short screens intentionally scroll.

| Viewport | Layout | Screenshots |
|---|---|---|
| 320 × 568 | PASS | [Opening](pre-launch-evidence/viewport-320x568.jpg) · [Sections](pre-launch-evidence/sections-320x568.jpg) · [Form](pre-launch-evidence/form-320x568.jpg) |
| 360 × 640 | PASS | [Opening](pre-launch-evidence/viewport-360x640.jpg) · [Sections](pre-launch-evidence/sections-360x640.jpg) · [Form](pre-launch-evidence/form-360x640.jpg) |
| 375 × 667 | PASS | [Opening](pre-launch-evidence/viewport-375x667.jpg) · [Sections](pre-launch-evidence/sections-375x667.jpg) · [Form](pre-launch-evidence/form-375x667.jpg) |
| 390 × 844 | PASS | [Opening](pre-launch-evidence/viewport-390x844.jpg) · [Sections](pre-launch-evidence/sections-390x844.jpg) · [Form](pre-launch-evidence/form-390x844.jpg) |
| 393 × 852 | PASS | [Opening](pre-launch-evidence/viewport-393x852.jpg) · [Sections](pre-launch-evidence/sections-393x852.jpg) · [Form](pre-launch-evidence/form-393x852.jpg) |
| 412 × 915 | PASS | [Opening](pre-launch-evidence/viewport-412x915.jpg) · [Sections](pre-launch-evidence/sections-412x915.jpg) · [Form](pre-launch-evidence/form-412x915.jpg) |
| 430 × 932 | PASS | [Opening](pre-launch-evidence/viewport-430x932.jpg) · [Sections](pre-launch-evidence/sections-430x932.jpg) · [Form](pre-launch-evidence/form-430x932.jpg) |
| 844 × 390 | PASS | [Opening](pre-launch-evidence/viewport-844x390.jpg) · [Sections](pre-launch-evidence/sections-844x390.jpg) · [Form](pre-launch-evidence/form-844x390.jpg) |
| 768 × 1024 | PASS | [Opening](pre-launch-evidence/viewport-768x1024.jpg) · [Sections](pre-launch-evidence/sections-768x1024.jpg) · [Form](pre-launch-evidence/form-768x1024.jpg) |
| 1024 × 768 | PASS | [Opening](pre-launch-evidence/viewport-1024x768.jpg) · [Sections](pre-launch-evidence/sections-1024x768.jpg) · [Form](pre-launch-evidence/form-1024x768.jpg) |
| 1440 × 900 | PASS | [Opening](pre-launch-evidence/viewport-1440x900.jpg) · [Sections](pre-launch-evidence/sections-1440x900.jpg) · [Form](pre-launch-evidence/form-1440x900.jpg) |
| 1920 × 1080 | PASS | [Opening](pre-launch-evidence/viewport-1920x1080.jpg) · [Sections](pre-launch-evidence/sections-1920x1080.jpg) · [Form](pre-launch-evidence/form-1920x1080.jpg) |

Full-page screenshots include below-fold placeholders that intentionally wait for viewport proximity. They are layout evidence, not simultaneous activation of every renderer. Actual gallery photo loading was separately checked in-view. Screenshots captured during resize/reveal transitions can show intermediate positions; raw geometry is in `viewport-matrix.json` and `form-matrix.json`. The previous mobile report's 200% text-resize emulation is historical evidence only, not a fresh native-zoom test.

## D. Functional testing

- **Booking:** real browser required-field validation; name/mobile entry; keyboard search and selection of Toyota; manual Corolla model; Vehicle Inspection service; review showing all values; direct return to Vehicle step retained brand/model. Form and Review checked at all required sizes. Escape returns to the page. [Review evidence](pre-launch-evidence/booking-review-390.jpg).
- **WhatsApp:** existing automated tests cover encoded draft values, consent validation, blocked popup handling and duplicate handoff prevention. Browser QA stopped before sending/opening an external draft. No WhatsApp message delivery, backend receipt or real booking confirmation is claimed.
- **Navigation:** all six main menu destinations and all five secondary actions invoked through browser UI; menus closed without errors. Contact landing separately checked after smooth scrolling settled. `navigation.json` contains immediate scroll positions, which may precede animation completion. Existing integration tests cover canonical routes and section navigation. Legal Privacy/Cookie/Terms pages and Back to Home were opened.
- **Gallery:** first photographs loaded with nonzero intrinsic widths in-view; image preview opened with keyboard, Next showed photo 02/16, Escape closed it. [Gallery evidence](pre-launch-evidence/gallery-open.jpg).
- **TOLI AI:** local Vehicle Inspection suggestion returned scoped service guidance and a request action; no cloud LLM integration added. [Assistant evidence](pre-launch-evidence/assistant-390.jpg).
- **Themes:** phone light/dark switching tested, including route transitions. Existing automated theme/form tests passed. [Light phone](pre-launch-evidence/light-390.jpg).
- **Contacts:** telephone, mail and map links inspected. External destinations/delivery were not comprehensively crawled or contacted. Map access stays opt-in; blocked storage and revocation tested without loading Google's service in automated tests.
- **404:** catch-all UI exists and its route tests pass. GitHub Pages redirect file exists. Actual deployment HTTP status/fallback behavior still requires the selected host.

## E. Performance

Lighthouse **13.6.0**, installed Chromium **156**, default mobile simulated throttling against the same local production preview. Single lab runs vary with CPU/network/cache; these are measurements, not statistically controlled field results.

| Category | Before | Final release |
|---|---|---|
| performance | 53 | 59 |
| accessibility | 93 | 100 |
| best-practices | 96 | 100 |
| seo | 100 | 100 |

| Lab metric | Before | Final release | Target |
|---|---|---|---|
| LCP | 5.8 s | 5.4 s | ≤2.5 s — NOT MET |
| CLS | 0 | 0 | ≤0.1 — MET in this run |
| Total blocking time | 1,020 ms | 820 ms | Diagnostic, **not INP** |
| INP | Not measured | Not measured | ≤200 ms — UNVERIFIED |

Intermediate performance runs scored 50 (after fonts/ARIA) and 60 (after image delivery). The reported final score is the last full-build run, **59**, not the best result. Original and final JSON reports are retained. No failing network requests appeared in the measured final navigation. Lab scores of 100 for accessibility/SEO do not establish legal compliance, complete screen-reader compatibility or production indexability.

Initial CSS/JavaScript and style/layout work remain costly; further reduction requires a scoped performance pass, not removal of approved imagery. Large-chunk advisory remains. Original Hero imagery, original logo source, lazy gallery/scene loading and reduced-motion behavior remain. No heavy advertising library or new animation dependency was added.

## F. Security, privacy, business and SEO

### Security

Compatible dependency updates changed the lockfile, not the declared framework major versions. Full tests pass afterward. See `toli-dependency-audit.json`, `toli-dependency-after.json` and the fix log. Remaining advisories must be assessed by reachability and deployment surface; they are not silently suppressed. No forced major upgrade was performed.

A limited source scan found no private-key blocks, live secret-key patterns or AWS access-key patterns. This is not a penetration test or exhaustive secret audit. The optional Supabase client uses deployment-owned public configuration and is not part of the active enquiry handoff. Never place service-role credentials in VITE variables. Enquiry values remain in page memory until the user's WhatsApp handoff; no new customer-data logging was added.

Hosting must provide HTTPS redirects, valid TLS, appropriate HSTS after rollout verification, MIME protection, referrer policy and a tested CSP that accommodates existing inline theme/bootstrap code and only approved integrations. No untested CSP was inserted that might break the application. Local Vite headers do not establish production security. Persistent customer record retention and hosting logs need owner/host confirmation.

### SEO

Existing title, description, language, robots `index, follow`, OG/Twitter metadata, favicon, H1 and AutoRepair structured data remain. No ratings/reviews/certifications were invented. `VITE_SITE_URL` already gates canonical and generated sitemap output; it is unset locally, so neither can be verified for a production domain. HashRouter legal/enquiry routes share the document and limit separate-page indexing/metadata. Production URL/base path `/Toli-2/` must agree with hosting. Submit the generated sitemap only after a real canonical domain is set. Root-origin ads.txt is a separate requirement from the repository subpath.

Build reference check found no missing `/Toli-2/assets/…` file references. Legal links now use valid existing email destinations. No exhaustive external-link availability guarantee is made. Production DNS, HTTPS, redirects and Search Console ownership remain unverified.

### Business information

Name, two published phone numbers, WhatsApp destination and address were checked against existing project content, not externally certified. Owner confirmation remains required for legal entity, address/pin, privacy contact responsibility, retention, 20-year experience/75-point/21+ brand claims, actual service availability, testimonials and any warranty/insurance promises. Hero currently invites insurance **enquiries** and makes no universal cashless claim. No opening hours, GSTIN, ratings or certification were fabricated. Existing legal placeholders remain visible and explicitly draft-marked; public launch is blocked until approved.

## G. AdSense readiness

**PARTIAL — inactive scaffolding and layout simulation prepared; live ad rendering is intentionally not released.** Technical preparation does not guarantee Google account/site approval.

- Central configuration: `src/lib/advertising.ts`, default `enabled:false`, `liveAdsAuthorized:false`, empty publisher/unit identifiers. No real or fake publisher record was inserted into production configuration.
- `AdPlacement` returns null in production. Even changing configuration alone does not ship a real unit; a separately reviewed renderer/CMP release is required. This is intentional fail-closed scaffolding, not a claim of a completed live AdSense integration.
- The script utility rejects missing IDs, authorization or consent and reuses one script promise. It is not called by current production UI. Map consent cannot stand in for ad consent.
- Simulator is gated by `import.meta.env.DEV` and `?adLayout=…`. It cannot create live impressions/clicks and never includes Google scripts. Production contains no simulation labels or units in the normal view. Disabled/failed/blocked states reserve **zero** ad space. Simulated large and delayed states reserve space before content appears.
- Privacy, About, Contact and legal navigation exist, but policy placeholders and owner facts prevent policy sign-off. Obtain content/image/testimonial rights confirmation. No account settings, advertiser approvals or domain ownership were verified.
- No ads.txt was generated without the real publisher details. Future ads.txt must be served at the production origin's `/ads.txt` using the account-provided record.

### Auto ads recommendation

Use manually reviewed responsive in-page units, initially at most one placement. Keep Auto ads **off** for this application unless a later account-level audit demonstrates compliance. Reject anchors, vignettes, side rails, intent overlays and placements inside enquiry/AI workflows. These formats can conflict with sticky navigation, chapter controls, assistant and forms. CSS cannot reliably control Google-managed overlays; no CSS hiding/cropping/manipulating real ads was added.

Google currently documents overlay-format switches, anchor position/dynamic-anchor controls, in-page settings, excluded areas and excluded pages. Excluded areas apply to in-page formats and are not a blanket overlay guarantee. Account-level preview/settings must be reviewed after ownership verification. For applicable EEA/UK/Swiss advertising, plan a Google-certified CMP/TCF integration; region/legal scope must be confirmed before activation. No claim that a homemade map toggle satisfies Google's advertising consent requirements.

Official sources checked 4 November 2026:

- [Google AdSense placement policies](https://support.google.com/adsense/answer/1346295?hl=en): avoid accidental clicks and misleading labels; use a permitted advertisement label for actual units.
- [Auto ads settings](https://support.google.com/adsense/answer/9305577?hl=en): supported format controls, exclusions and preview.
- [Consent management guidance](https://support.google.com/adsense/answer/7670013?hl=en) and [Google CMP/TCF explanation](https://support.google.com/adsense/answer/16918505?hl=en-GB): consent/disclosures and certified CMP requirements.

## H. Placement map and advertisement testing

| Location | Decision | Reason / behavior |
|---|---|---|
| After Gallery, before Service Request section | Candidate only; owner/account approval still required | Separate in-flow region; 64px outer spacing desktop/tablet, 48px phone; clear label; no card/button imitation. Recheck actual creative sizes and accidental-click proximity before live release. |
| Before Footer, after contact content | Secondary simulation candidate only | Disabled by default; used only in multiple-placeholder scenario. Avoid density near contact actions; prefer leaving unused. |
| Navbar, Hero, cars, headings, logo | Rejected | Brand visibility and essential content protected. |
| Gallery controls, service cards, sticky chapter rail | Rejected | Accidental-click risk and interaction obstruction. |
| Request steps, consent, submit, AI dialog | Rejected | Transactional interaction and privacy/focus protection. |
| Fixed bottom/top overlays, vignettes and side rails | Rejected | Conflict with navigation/support/mobile controls and interruption risk. |

**28 screenshot-backed cases:** none, small, large, slow, failed, blocked and multiple at 390×844, 844×390, 768×1024 and 1440×900. Every case had zero ad script elements and zero horizontal overflow. Visible placeholders were normal relative/in-flow regions, not fixed overlays. [Phone](pre-launch-evidence/ad-overview-0.jpg), [landscape](pre-launch-evidence/ad-overview-1.jpg), [tablet](pre-launch-evidence/ad-overview-2.jpg) and [desktop](pre-launch-evidence/ad-overview-3.jpg) scenario sheets and per-case images are in evidence. `ad-matrix.json` records geometry; multiple scenarios rendered two distinct slots. Failed/blocked states are simulated outcomes, not real ad-blocker/network tests against Google.

The delayed placeholder changed text after four seconds while its measured container height stayed **362.5px → 362.5px** (`slow-stability.json`). This demonstrates reservation stability for the simulator, not a promise of zero CLS for every real Google creative. No actual ad dimensions are forcibly cropped or overridden. Future units need supported responsive sizing and separate empty/blocked/no-fill testing.

## I. Regression evidence and deployment checklist

| Check | Result |
|---|---|
| Production build | PASS; 12.32s final build, large-chunk advisory retained |
| TypeScript (app/node/QA) | PASS |
| ESLint | PASS |
| Unit/integration suite | **388 passed, 55 files** after final source changes |
| Browser workflows | Chromium UI-driven checks listed above; no external enquiry sent |
| Lighthouse | Final 59 / 100 / 100 / 100 |
| Dependency audit | Executed; residual high/critical findings remain |
| Source/build asset checks | No matched private-key patterns; no missing referenced built assets |
| Production console | No errors observed in checked browser flows |
| Cross-browser | PARTIAL: available Chromium only; named browsers/physical devices not signed off |
| 3D/original protection | 1,393 and 2,948 audited files respectively; zero changed/added/removed |

Existing test-run warnings include jsdom's unimplemented scrollTo in some legacy integration cleanups and React Router future-flag notices; they did not fail the final suite and were not seen as production console failures. No claim is made that every possible interaction was exhaustively tested.

Before any deployment:

- Resolve the release blockers in A; re-run tests and Lighthouse after dependency/performance work.
- Approve business/legal content, image rights, privacy and retention; remove all draft placeholders.
- Supply the real HTTPS canonical domain and matching deployment base path; verify sitemap/robots and structured-data addresses.
- Configure DNS/TLS, HTTP→HTTPS redirect, host 404/hash redirect behavior and security headers; validate from outside localhost.
- Cache hashed assets immutably, keep HTML short-lived/revalidated, enable compression, retain previous hashed assets for returning sessions.
- Produce a versioned immutable build archive plus checksums; retain the previous known-good release; test atomic switch and rollback to that artifact on private staging.
- Configure minimal uptime/error monitoring with PII redaction and owner-approved retention. Alert on asset/route failures. No telemetry service was invented or activated.
- Complete Chrome, Edge, Firefox, Safari/WebKit, native zoom, reduced motion, keyboard/assistive technology and physical Android/iOS checks.
- Keep ads off; any later AdSense activation needs explicit approval, real identifiers, consent integration, origin-root ads.txt and fresh real-placement/no-fill checks.

Development simulation: `http://127.0.0.1:8190/Toli-2/?adLayout=large`.
Normal production preview: `http://127.0.0.1:8200/Toli-2/`.
Neither is a deployment. No publication, live ad request, live ad impression or external form submission was performed.

## J. Final acceptance decision

| Requirement | Result |
|---|---|
| Desktop UI | PASS for inspected layouts |
| Mobile responsiveness | PASS in Chromium emulation |
| Tablet responsiveness | PASS in Chromium emulation |
| Hero layout | PASS; approved assets/composition preserved |
| Navigation | PASS for checked actions and automated routes |
| Service booking | PASS through Review; actual appointment unverified |
| WhatsApp enquiry | PASS for tested draft construction/error handling; delivery NOT TESTED |
| TOLI AI | PASS for checked local guidance flow |
| Performance | PARTIAL — mobile target not met |
| Accessibility | PASS for automated/keyboard checks; native zoom and assistive-technology sign-off outstanding |
| Security | FAIL release gate — remaining high/critical dependency findings and host configuration unverified |
| SEO | PARTIAL — local score 100, production domain/indexability not signed off |
| Business information | NEEDS CONFIRMATION |
| AdSense technical readiness | PARTIAL — disabled scaffolding, not authorized live integration |
| Ad content obstruction | PASS for 28 development simulation cases only |
| Ad responsive behavior | PASS for simulated slots only |
| Ad layout stability | PASS for measured simulated delayed slot; live creatives unverified |
| Cross-browser compatibility | PARTIAL |
| Production build | PASS |
| Separate 3D project unchanged | PASS |
| Deployment | NOT PERFORMED |

**NOT READY — BLOCKERS REMAIN.** This report records actual local evidence and the remaining gates; it does not certify AdSense approval, full accessibility compliance, production security or real-device readiness.

## Modified files

The following source/asset changes are confined to the static project. Generated dist and audit documentation are additional outputs. Protected artwork/source assets remain unchanged; new delivery variants are additive.

- `package-lock.json`
- `index.html`
- `src/index.css`
- `src/components/Services.tsx`
- `src/components/ToliLogoPill.tsx`
- `src/components/Hero.tsx`
- `src/components/GalleryImage.tsx`
- `src/components/Contact.tsx`
- `src/components/Stats.tsx`
- `src/components/HowItWorks.tsx`
- `src/components/LegalPageShell.tsx`
- `src/components/journey/NavbarPerformanceCar.tsx`
- `src/pages/Index.tsx`
- `src/pages/NotFound.tsx`
- `src/pages/TermsAndConditions.tsx`
- `src/pages/PrivacyPolicy.tsx`
- `src/pages/CookiePolicy.tsx`
- `src/test/gallery-editorial.test.tsx`
- `src/test/hero-reference.test.tsx`
- `src/test/fixtures/separation-protected.json`
- `src/dev/AdLayoutSimulation.tsx`
- `src/assets/big-transparent-lossless.webp`
- `src/assets/fonts/Inter-LICENSE.txt`
- `src/assets/fonts/Bebas-Neue-LICENSE.txt`
- `src/assets/fonts/inter-latin.woff2`
- `src/assets/fonts/bebas-neue-latin.woff2`
- `src/lib/advertising.ts`
- `src/components/ads/AdPlacement.tsx`
- `src/components/ads/advertising.css`
- `src/test/prelaunch.test.tsx`
- `public/favicon-64.png`
