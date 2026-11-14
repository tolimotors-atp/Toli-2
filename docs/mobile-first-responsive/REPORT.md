# TOLI MOTORS — Mobile-first responsive implementation

Target: `/home/thunder/shared/tolimotors-main1/toli-static-website`.

## Layout changes

- Dedicated mobile content flow below 900px: location, verified contact links, original metallic logo, workshop subtitle, heading, enlarged white/red slogan, vehicle composition and service cards. Natural scrolling preserves readable text instead of squeezing everything into one viewport.
- Safe-area-aware sticky red navbar, 44px controls and wrapping for enlarged text. Decorative navbar car is omitted where space is constrained; Help remains in the existing menu. Booking, theme and menu actions remain available.
- Mobile heading 26–34px; brand slogan 20.4–24px; location 20–24px. Logo scales up to 320px without changing the official artwork or metallic treatment.
- Same three-car imagery and colors. Central red sedan dominates phones; tablet retains the complete three-car arrangement. Vehicle height responds to available screen height. Original workshop imagery uses separate portrait and short-landscape framing.
- Service cards use two columns, with a single-column image/text layout below 359px. Image atlas quadrants retain proportions and readable labels.
- Services, components, journey, trust, Inside Toli, gallery, booking, contact and footer receive mobile spacing, typography and wrapping adjustments. Scene regions reserve space and remain lazy-loaded; existing static fallback remains available.
- AI launcher sits in normal mobile flow after Hero, avoiding vehicle/card obstruction. Help-menu AI and lazy assistant panel remain intact. Optional Help portals stay beneath dialogs.
- Request dialog follows the visual viewport, scrolls internally and uses a compact header/progress/footer on short screens. Existing draft, validation, step navigation and submission code is unchanged.
- Fixed a real menu navigation regression: restoring focus now uses `preventScroll`, so it no longer cancels the section scroll. Added a regression test.

## Responsive matrix

Browser viewport emulation. Opening views and section layout sheets were inspected at all 14 required sizes. No horizontal document overflow was found. Short phone views intentionally scroll; they do not force every element above the fold.

| Viewport | Layout result | Evidence |
|---|---|---|
| 320 × 568 | PASS | [Before](evidence/before-320x568.png) · [After](evidence/after-320x568.png) · [Form](evidence/modal-320x568.png) · [Sections](evidence/sections-320x568.png) |
| 360 × 640 | PASS | [Before](evidence/before-360x640.png) · [After](evidence/after-360x640.png) · [Form](evidence/modal-360x640.png) · [Sections](evidence/sections-360x640.png) |
| 375 × 667 | PASS | [Before](evidence/before-375x667.png) · [After](evidence/after-375x667.png) · [Form](evidence/modal-375x667.png) · [Sections](evidence/sections-375x667.png) |
| 390 × 844 | PASS | [Before](evidence/before-390x844.png) · [After](evidence/after-390x844.png) · [Form](evidence/modal-390x844.png) · [Sections](evidence/sections-390x844.png) |
| 393 × 852 | PASS | [Before](evidence/before-393x852.png) · [After](evidence/after-393x852.png) · [Form](evidence/modal-393x852.png) · [Sections](evidence/sections-393x852.png) |
| 412 × 915 | PASS | [Before](evidence/before-412x915.png) · [After](evidence/after-412x915.png) · [Form](evidence/modal-412x915.png) · [Sections](evidence/sections-412x915.png) |
| 430 × 932 | PASS | [Before](evidence/before-430x932.png) · [After](evidence/after-430x932.png) · [Form](evidence/modal-430x932.png) · [Sections](evidence/sections-430x932.png) |
| 667 × 375 | PASS | [Before](evidence/before-667x375.png) · [After](evidence/after-667x375.png) · [Form](evidence/modal-667x375.png) · [Sections](evidence/sections-667x375.png) |
| 844 × 390 | PASS | [Before](evidence/before-844x390.png) · [After](evidence/after-844x390.png) · [Form](evidence/modal-844x390.png) · [Sections](evidence/sections-844x390.png) |
| 600 × 960 | PASS | [Before](evidence/before-600x960.png) · [After](evidence/after-600x960.png) · [Form](evidence/modal-600x960.png) · [Sections](evidence/sections-600x960.png) |
| 768 × 1024 | PASS | [Before](evidence/before-768x1024.png) · [After](evidence/after-768x1024.png) · [Form](evidence/modal-768x1024.png) · [Sections](evidence/sections-768x1024.png) |
| 1024 × 768 | PASS | [Before](evidence/before-1024x768.png) · [After](evidence/after-1024x768.png) · [Form](evidence/modal-1024x768.png) · [Sections](evidence/sections-1024x768.png) |
| 1440 × 900 | PASS | [Before](evidence/before-1440x900.png) · [After](evidence/after-1440x900.png) · [Form](evidence/modal-1440x900.png) · [Sections](evidence/sections-1440x900.png) |
| 1920 × 1080 | PASS | [Before](evidence/before-1920x1080.png) · [After](evidence/after-1920x1080.png) · [Form](evidence/modal-1920x1080.png) · [Sections](evidence/sections-1920x1080.png) |

Additional checked geometries: 344×740, 480×800, 820×1180, 360×720, 360×780, 360×800, 360×840 and 720×540. These cover intermediate widths and 18:9, 19.5:9, 20:9, 21:9 and 4:3 cases. Standard landscape and desktop include 16:9 cases.

**Evidence notes:** Full-page section sheets capture offscreen lazy content before activation. Their gallery slots may therefore show alternative text, and scene slots show preparation placeholders. Actual in-view gallery photographs were confirmed loaded; keyboard opening, Next and Escape were checked. The active Journey view rendered its existing static vehicle fallback without console errors. Section sheets are layout evidence, not proof that every offscreen renderer is simultaneously active. Some form captures taken during viewport transitions reflect intermediate animation positions; the settled 844×390 and 768×1024 captures were replaced after inspection.

## Functional and accessibility checks

- Menu navigation to Services, Journey, Toli Motors and Gallery checked through real UI. Services lands below the sticky header rather than snapping back to top.
- Header booking opens the canonical four-step request dialog. Local test data completed Details → Toyota/Corolla → Vehicle Inspection → Review. Review preserved correct values. No external enquiry was sent.
- AI suggestion and request-service action checked on phone and short landscape.
- Gallery opened with keyboard, advanced to image 2, and closed with Escape. Gallery dialog controls have a minimum 44px mobile target.
- Light/dark theme checks at phone, tablet and desktop. Original theme-specific background/logo surfaces remain in place.
- Controlled 200% text-resize emulation at 320×568 and 844×390 exposed and resolved long heading, email, preset-button and WhatsApp-button wrapping issues. Final scan found no visible text extending beyond viewport boundaries. The temporary development harness was removed. This is not a claim of native-browser zoom or physical on-screen keyboard validation.
- Existing focus styles, labels and reduced-motion behavior retained. No new continuous animation.

## Performance

No dependencies, vehicle assets or workshop assets added. Existing vehicle WebP variants are 61,512 bytes (960px) and 134,894 bytes (1600px). Responsive image size hints now match the actual displayed width: 175vw below 600px, 100vw through tablet and 70vw desktop. This avoids selecting the larger image unnecessarily on standard-density phones. Existing workshop crops are 121,586 / 102,338 / 233,162 bytes; service atlas is 98,724 bytes. Below-fold modules, gallery photographs and AI panel retain deferred loading. No FPS or physical low-end Android benchmark is claimed.

## Regression validation

| Check | Result |
|---|---|
| Production build | PASS; existing large-chunk advisory remains |
| TypeScript app/node/QA configurations | PASS |
| Lint | PASS |
| Full tests | 385 passed across 54 files |
| Navigation tests after TypeScript test-option correction | 2 passed |
| Fresh production preview console | No warnings/errors observed in checked flow |
| Desktop visual comparison | Composition preserved at 1440×900 and 1920×1080; screenshots differ slightly due focus/animation, not layout |
| Protected siblings | No changed, added or removed audited files |

## Files modified

- `src/mobile-responsive.css` (new scoped responsive rules).
- `src/main.tsx` (imports responsive stylesheet last).
- `src/pages/Index.tsx` (AI launcher moved into main content flow; desktop stays fixed).
- `src/components/journey/HeroVehicleLineup.tsx` (responsive image sizing hints).
- `src/components/journey/ExperienceNavigation.tsx` (focus restoration without scroll cancellation).
- `src/test/phase1-navigation.test.tsx` (navigation regression test).
- `src/test/fixtures/separation-protected.json` (intentional hashes for authorized static changes).
- This report and evidence files.

## Protection and status

Official logo, metallic pill, vehicle assets, workshop assets, desktop composition, backend and request logic preserved. Hash audit excludes dependencies, generated builds, repository metadata and docs; protected `toli-3d-website` and `tolimotors-main` have zero changes.

| Acceptance criterion | Result |
|---|---|
| Mobile Hero optimization | PASS |
| Aspect-ratio adaptation | PASS in browser emulation |
| Mobile navbar | PASS |
| Hero typography | PASS |
| Vehicle composition | PASS |
| Workshop background | PASS |
| Service cards | PASS |
| Full website responsiveness | PASS for inspected browser layouts; physical-device verification not performed |
| Desktop design preserved | PASS |
| Functional regression | PASS for automated suite and checked UI flows |
| 3D website protection | PASS |
| Deployment | NOT PERFORMED |

Development preview: http://127.0.0.1:8190/Toli-2/
Production preview: http://127.0.0.1:8200/Toli-2/

Physical Android/iOS testing and real virtual-keyboard behavior remain outside this browser-emulation validation. No deployment or external form submission was performed.
