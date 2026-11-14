# Workshop theme unification — 4 November 2026

Target: `/home/thunder/shared/tolimotors-main1/toli-static-website`.
Preview: http://127.0.0.1:8200/Toli-2/ . No deployment or live advertisement activation performed.

## Result and scope

The sections below the approved Hero now use its graphite, metallic silver and automotive-red visual language. Removed broad burgundy lighting fields from Services, vehicle components, service Journey, Trust/About/quality, Inside Toli, Gallery, booking, Contact, footer and legal-page surfaces. Service Request portals and the assistant use the same neutral metal treatment. Existing section geometry, typography hierarchy, content and interactions remain in place. Red is concentrated in selected services, primary actions, seams and small reflections.

Only implementation files changed:
- `src/workshop-surfaces.css`: shared, locally scoped material tokens and section/panel rules.
- `src/main.tsx`: imports that stylesheet last, after the existing responsive layer.

This report and `docs/workshop-theme-evidence/` are supporting artifacts. No logic, vehicle/photo/logo assets, dependency files or advertising safeguards changed.

## Shared materials

Reused the approved Hero palette: charcoal `#17181c`, graphite `#222329`, metal `#3b3e45`, silver `#96999f`, pearl `#f4f3f2`, red `#d91f31`, action depth `#b51b29`. New `--workshop-*` properties define room lighting, metal panels, borders and subtle red reflections; existing `--environment-*`, semantic background/text/request variables and `--panel-depth` consume them only within the affected content wrappers and portals. No root-level theme changes were introduced.

Room lighting varies in direction across component, Journey, Trust and Gallery sections. Metallic panels use thin borders, a small inset highlight and bounded shadows. Services retain all nine options in their original order; selected service is red and its details are neutral graphite with a red top seam. Light mode uses cream `#f4f1eb`, neutral silver `#e5e3de` and dark text. A visual check caught and corrected inherited pale detail labels in light mode.

## Before and after evidence

Full-page captures include every visible/default homepage section, with matching viewport settings before and after. Offscreen lazy media may appear as its normal placeholder in a full-page capture; the gallery was also opened separately. Collapsed Trust content is not represented as an expanded before/after comparison.

| View | Before | After |
|---|---|---|
| Dark desktop 1440×900 | [Before](workshop-theme-evidence/before-dark-1440.jpg) | [After](workshop-theme-evidence/after-dark-1440.jpg) |
| Light desktop 1440×900 | [Before](workshop-theme-evidence/before-light-1440.jpg) | [After](workshop-theme-evidence/after-light-1440.jpg) |
| Dark mobile 390×844 | [Before](workshop-theme-evidence/before-dark-390.jpg) | [After](workshop-theme-evidence/after-dark-390.jpg) |
| Light mobile 390×844 | [Before](workshop-theme-evidence/before-light-390.jpg) | [After](workshop-theme-evidence/after-light-390.jpg) |

[Services side by side](workshop-theme-evidence/comparison-1440-services.jpg), [Journey](workshop-theme-evidence/comparison-1440-process.jpg), [Trust](workshop-theme-evidence/comparison-1440-trust.jpg), [Gallery](workshop-theme-evidence/comparison-1440-gallery.jpg), [Booking](workshop-theme-evidence/comparison-1440-booking.jpg), [Contact](workshop-theme-evidence/comparison-1440-contact.jpg).

Separate section extracts are saved for Services, components, Journey, Trust, Inside Toli, Gallery, booking, Contact and footer at desktop and mobile sizes in both themes. Mobile comparison sheets are included too.

[Light mobile Services](workshop-theme-evidence/after-light-390-services.jpg), [dark mobile booking](workshop-theme-evidence/booking-dark-390.jpg), [light mobile booking](workshop-theme-evidence/booking-light-390.jpg), [assistant](workshop-theme-evidence/assistant-dark-320.jpg), [gallery preview](workshop-theme-evidence/gallery-dark-320.jpg), [legal page](workshop-theme-evidence/legal-dark-390.jpg).

## Responsive and functional checks

Dark: 320×568, 390×844, 768×1024, 1440×900, 1920×1080. Light: 320×568, 390×844, 768×1024, 1440×900. Measured document widths stayed within the viewport in every case. Existing card stacking, internal mobile service-list scrolling and popup geometry were preserved. These are browser viewport checks, not physical-device or cross-browser certification.

Browser checks confirmed all nine services update their matching detail heading and pressed state (see `service-selection.json`); header Book Service opens the existing popup; Toyota and Innova survive switching directly to Review; mobile popup controls remain available; Gallery opens with its existing keyboard controls; TOLI AI returns its local Battery Services response; theme switching changes the intended surfaces. No customer enquiry or external WhatsApp message was sent. Automated tests cover validation, Back/Continue, drafts, request routing, submission handoff, gallery and ad safeguards.

Hero and main-navbar computed background, text/font styles and measured dimensions at 1440×900 are identical before/after (`protected-before.json`, `protected-after.json`). Their source/assets were not edited. File hashing found exactly one existing implementation file changed (`src/main.tsx`) and one added (`src/workshop-surfaces.css`). All 1,393 tracked-by-audit files in `toli-3d-website` and 2,948 in the original `tolimotors-main` sibling are unchanged; see `project-protection.json`. Generated build/docs directories and dependencies are excluded from this source/asset comparison.

## Validation

- Production build: PASS, final build 17.84 seconds. Existing large-chunk and ambiguous Tailwind utility warnings remain.
- TypeScript app/node/QA checks: PASS.
- Lint: PASS.
- Tests: 388 PASS across 55 files. Existing React Router future-flag notices remain in test output.
- Fresh final-build production tab: booking form opened successfully; console contained no warnings/errors. An older tab encountered a missing lazy-module URL while the preview output was being rebuilt; opening a fresh tab against the completed build resolved it. This local rebuild observation does not certify production asset-retention behavior.
- No new images, libraries, animations, canvas or filters added by this theme layer. Existing reduced-motion behavior is preserved.

### Fresh Lighthouse measurements

Same local production URL, Lighthouse 13.6.0, Chromium 156, default mobile simulation. These are fresh measurements, separate from the user's supplied prior 59 baseline.

| Metric | Before | Intermediate | Final build |
|---|---:|---:|---:|
| Performance | 65 | 63 | 69 |
| Accessibility | 100 | 100 | 100 |
| Best Practices | 100 | 100 | 100 |
| SEO | 100 | 100 | 100 |
| LCP | 5.4s | 5.4s | 5.4s |
| TBT | 550ms | 660ms | 430ms |
| CLS | 0 | 0 | 0 |

No significant regression was observed in these local samples; run variability is visible and these are not statistical or real-device guarantees. LCP remains slow. TBT is not field INP.

Performance investigation: baseline main-thread work was approximately 4.0s, including 1.1s script evaluation and 1.0s style/layout. Lighthouse estimated 37KiB unused JavaScript. Final build still warns about large chunks. Existing startup rendering, script work and Hero delivery remain optimization candidates; this scoped color task deliberately does not alter the approved Hero or application loading architecture. No claim of performance remediation or launch readiness is made.

## Remaining pre-launch blockers

The previous audit's unresolved items remain: legal business/date/address and other owner confirmations; dependency advisory remediation (previous audit recorded 24 package advisory records, including two critical and two high; not re-audited in this theme task); performance target; production domain/hosting/TLS/cache verification; real-device, native zoom and cross-browser validation. See [prior audit](PRE_LAUNCH_AND_ADSENSE_AUDIT.md). Site remains NOT READY for launch until blockers are resolved.

## Acceptance

| Criterion | Status |
|---|---|
| HERO UNCHANGED | PASS |
| NAVBAR UNCHANGED | PASS |
| SERVICES THEME MATCHES HERO | PASS |
| ALL SECTIONS VISUALLY CONSISTENT | PASS for inspected default section layouts and checked overlays |
| PREMIUM GRAPHITE/RED DESIGN | PASS |
| LIGHT THEME PRESERVED | PASS |
| MOBILE RESPONSIVENESS | PASS for listed viewport checks |
| FUNCTIONALITY PRESERVED | PASS for existing automated suite and browser checks |
| ADSENSE SAFEGUARDS PRESERVED | PASS — source untouched, tests pass |
| PERFORMANCE REGRESSION CHECK | PASS for local samples, performance target remains unmet |
| SEPARATE 3D WEBSITE UNCHANGED | PASS |
| DEPLOYMENT | NOT PERFORMED |
