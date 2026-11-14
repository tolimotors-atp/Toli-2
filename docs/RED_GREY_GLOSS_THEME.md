# Red and metallic-grey finish — 4 November 2026

Target: `/home/thunder/shared/tolimotors-main1/toli-static-website`.
Preview: http://127.0.0.1:8200/Toli-2/ . Deployment: NOT PERFORMED.

## Changes

Updated only `src/workshop-surfaces.css` (plus this report and its evidence). No application logic, images, fonts, dependencies, business information or advertising configuration changed.

Services now has a graphite-to-red room gradient, polished charcoal rows, glossy red selection with a bounded red halo, a metallic detail panel and a shiny red Request Service action. All nine options and their order remain intact. The same metal material is used for Journey, Trust/About/quality, booking, Contact and other information cards. Gallery containers have fine highlights and depth; images themselves are unchanged. Inside Toli, Gallery, booking, Contact and footer use varying light directions. Enquiry panels and selected form controls share the finish. Legal surfaces inherit the room materials.

The assistant uses graphite with a red reflection in dark mode and pearl/silver with dark ink in light mode. Its content and local response logic are unchanged.

## Materials and motion

Reused Hero colors: charcoal `#17181c`, graphite `#222329`, metallic grey `#3b3e45`, silver `#96999f`/`#caccd0`, pearl `#f4f3f2`, automotive red `#d91f31`, red depth `#b51b29`/`#921824`, with a small `#64131b` reflection. Existing `--workshop-*`, `--environment-*` and semantic panel variables carry the changes below the Hero and inside content portals.

Polish uses static white key-light gradients, diagonal metallic reflections, inset hairlines and bounded shadows. No blur filters, backdrop blur, new assets, continuous animations or compositing hints were added. Hover rules are restricted to hover-capable devices, and new transitions are disabled under `prefers-reduced-motion: reduce`. Mobile uses shallower panel shadows. Card dimensions, stacking and touch targets remain unchanged.

Light mode uses cream/pearl `#fffdf9`/`#f4f1eb`, silver `#e5e3de`/`#d7d8d7`, dark text and restrained red. The assistant is explicitly light rather than retaining its previous dark panel.

## Visual evidence

All links below are local captures in [the evidence folder](red-grey-gloss-evidence/).

| View | Before | After |
|---|---|---|
| Dark desktop 1440×900 | [Before](red-grey-gloss-evidence/before-dark-1440.jpg) | [After](red-grey-gloss-evidence/after-dark-1440.jpg) |
| Light desktop 1440×900 | [Before](red-grey-gloss-evidence/before-light-1440.jpg) | [After](red-grey-gloss-evidence/after-light-1440.jpg) |
| Dark mobile 390×844 | [Before](red-grey-gloss-evidence/before-dark-390.jpg) | [After](red-grey-gloss-evidence/after-dark-390.jpg) |
| Light mobile 390×844 | [Before](red-grey-gloss-evidence/before-light-390.jpg) | [After](red-grey-gloss-evidence/after-light-390.jpg) |

Side-by-side section sheets (before left, after right) cover Services, components, Journey, Trust, Inside Toli, Gallery, booking, Contact and footer in both themes at desktop/mobile widths. Example: [Services](red-grey-gloss-evidence/comparison-dark-1440-services.jpg), [Trust](red-grey-gloss-evidence/comparison-dark-1440-trust.jpg), [light mobile Services](red-grey-gloss-evidence/comparison-light-390-services.jpg).

[Assistant before](red-grey-gloss-evidence/before-assistant-dark-390.jpg), [dark after](red-grey-gloss-evidence/after-assistant-dark-390.jpg), [light after](red-grey-gloss-evidence/after-assistant-light-390.jpg). [Booking before](red-grey-gloss-evidence/before-booking-dark-390.jpg), [dark after](red-grey-gloss-evidence/after-booking-dark-390.jpg), [light after](red-grey-gloss-evidence/after-booking-light-390.jpg).

Full-page images capture default visible section layouts. Collapsed Trust content is not shown as expanded before/after; offscreen lazy media can appear in its normal placeholder state. Fixed navigation markers reflect the scroll state at capture and are not evidence of changed selection behavior.

## Validation and limits

- Production build: PASS. Existing chunk-size and ambiguous Tailwind utility warnings remain.
- TypeScript app/node/QA checks: PASS.
- Lint: PASS.
- Automated tests: 388 PASS, 55 files. Existing React Router future-flag notices remain.
- Both themes: 320, 360, 390, 412, 430, 768, 1440 and 1920px widths checked. Document width never exceeded viewport width (`responsive.json`). Desktop/tablet/phone captures included.
- Keyboard Space selected Battery Services and updated the matching detail heading; a 2px focus outline remained visible.
- Header and Services booking actions opened the existing popup. Toyota/Innova survived switching directly to Review. No external enquiry or WhatsApp message was sent.
- Final production booking check: form visible and console empty of warnings/errors.
- Light assistant background and text were checked in the rendered page. Its layout remains touch-friendly.
- Browser reports `(hover:hover)` false even at desktop viewport sizes, so it correctly suppresses hover-only glow. Actual mouse-hover rendering could not be certified in this touch-emulated browser. `hover-light-1440.jpg` is a pointer/touch inspection, not proof of active hover-media styling.
- Reduced-motion rules were inspected and existing motion tests passed; the available browser controls do not expose reduced-motion emulation. Physical-device/OS reduced-motion and cross-browser checks remain unverified.

## Protection

A fresh source/asset comparison found only `src/workshop-surfaces.css` changed in the static project. Hero, navbar, three Hero cars, official logo pill, workshop background, service/form/WhatsApp/gallery/AI logic and AdSense safeguards are untouched. Protected projects: 1,393 files in `toli-3d-website` and 2,948 in the original `tolimotors-main` sibling unchanged (`project-protection.json`). Generated build/docs/dependency directories are excluded from that comparison.

Hero/navbar computed background, font and text colors match the before snapshot; navbar height remains 64px. Raw dimension snapshots differ by the browser's transient 10px scrollbar gutter (and corresponding 1.25px fluid Hero height), so exact pixel identity is not claimed from those snapshots. No rules target the Hero or main navigation and their source/assets are unchanged.

## Performance

Fresh local Lighthouse 13.6.0 / Chromium 156 default-mobile measurements, separate from the historical 59 score:

| Metric | Before | Concurrent resizing run | Isolated run | Final release |
|---|---:|---:|---:|---:|
| Performance | 72 | 52 | 66 | 66 |
| Accessibility | 100 | 100 | 100 | 100 |
| Best Practices | 100 | 100 | 100 | 100 |
| SEO | 100 | 100 | 100 | 100 |
| LCP | 5.3s | 5.3s | 5.7s | 5.4s |
| TBT | 340ms | 790ms | 490ms | 550ms |
| CLS | 0 | 0 | 0 | 0 |

The final result is lower than the fresh baseline, so the no-regression gate is **FAIL / needs investigation**, rather than a clean pass. Concurrent resizing likely contaminated the 52 sample; it is retained for transparency. No statistical or physical-device conclusion can be drawn from these few local runs. TBT is not field INP.

Investigation: compressed main CSS transfer grew by only 900 bytes (53,346 to 54,246). Script evaluation increased from about 791ms to 1,106ms; style/layout from 912ms to 1,043ms; rendering decreased from 130ms to 116ms. These observations do not isolate the cause. Lighthouse still estimates 37KiB unused JavaScript, and existing large-chunk warnings remain. The update adds no scripts, dependencies, imagery or running animations. CSS lighting stays static and shadows are bounded; mobile shadows are shallower. Further performance work needs controlled repeated baseline comparisons and startup profiling, while preserving the approved Hero. Current LCP and blocking-time results remain below launch targets.

No launch-readiness claim is made. Existing legal/owner approvals, dependency advisory remediation, production hosting/TLS/cache/asset-retention verification, mobile performance targets and physical-device/cross-browser checks remain outstanding; see [the pre-launch audit](PRE_LAUNCH_AND_ADSENSE_AUDIT.md).

## Acceptance

| Criterion | Result |
|---|---|
| RED/GREY GRADIENT CONSISTENCY | PASS |
| METALLIC SHINE EFFECTS | PASS |
| SOFT RED GLOW EFFECTS | PASS for selected states and ambient surfaces; mouse hover not certified |
| SERVICES SECTION REDESIGNED | PASS |
| ALL SECTIONS VISUALLY UNIFIED | PASS for inspected default layouts and overlays |
| HERO AND NAVBAR UNCHANGED | PASS — source/assets protected |
| LIGHT THEME PRESERVED | PASS |
| MOBILE OPTIMIZED | PASS for listed browser widths; physical devices unverified |
| FUNCTIONALITY PRESERVED | PASS for automated suite and browser checks |
| ADSENSE SAFEGUARDS PRESERVED | PASS — code untouched, tests pass |
| PERFORMANCE REGRESSION CHECK | FAIL — final sample 66 vs 72 baseline; follow-up required |
| 3D WEBSITE UNCHANGED | PASS |
| DEPLOYMENT | NOT PERFORMED |
