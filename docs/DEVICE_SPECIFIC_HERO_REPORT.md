# Device-specific Hero optimization — 6 November 2026

Saved directly in the static website. No deployment or edits to the independent 3D/original projects.

## Files changed
- `src/mobile-responsive.css`: Hero-only device framing, spacing, contact placement and desktop edge rules. Existing navbar/AI/other-section styling retained.
- `src/components/journey/HeroVehicleLineup.tsx`: responsive image `sizes` corrected from 175vw on phones to 100vw through 900px, matching the new contained layout. Same src/srcset, intrinsic aspect ratio and priority.
- `src/test/hero-lineup.test.tsx`: verifies the updated responsive image size contract.
- `src/test/fixtures/separation-protected.json`: updated the authorized lineup component hash and the stale experience.css hash left by the prior approved gold-indicator refinement. No experience.css changes in this task. Every protected-file hash now matches.
- This report and screenshots/measurements under `docs/device-hero-evidence`.

## Mobile
Car picture width changes from roughly 172% to 100% of its track, with centered object containment. All three cars fit, including the SUV and coupe. The central sedan stays dominant because its size/position relative to the side cars is embedded in the unchanged image. Vehicle track height is width-aware via clamp(100px,25vw,210px), with separate short-landscape rules. Brand width is capped at 280px instead of 320px, grid gaps reduce from 12 to 8px (6px on short landscapes), subtitle spacing reduces, and padding aligns with the existing responsive gutter. Text itself and heading/caption fonts are retained.

The contact pill uses a compact two-line grid aligned to the right at max(8px,safe-area-inset-right), with 44px-high phone-link targets. Its icon spans both lines and stays red/centered; frost, fallback, blur and both tel links remain unchanged. More space is deliberately retained for readable contact details rather than forcing the entire Hero into one screen.

The Hero includes four existing service cards and contact/actions below the vehicle scene; those remain in natural flow.

| Viewport | Full Hero height before → after | Car picture width before → after |
|---|---|---|
| 320×568 | 1464px → 1415px | 471px → 278px |
| 360×640 | 1418px → 1320px | 540px → 318px |
| 390×844 | 1474px → 1349px | 592px → 348px |
| 430×932 | 1523px → 1393px | 660px → 386px |
| 600×960 | 1653px → 1498px | 554px → 542px |
| 640×960 | 1679px → 1523px | 594px → 579px |
| 768×1024 | 1729px → 1585px | 698px → 702px |
| 1440×900 | 1092px → 1092px | 860px → 860px |

Heights measure the entire Hero, not just the vehicle strip. Before/after measurements use identical viewports and dark theme; browser scrollbar/gutter availability is included in the recorded rectangles. At 390px the vehicle track reduces from about 203px to 100px. The image is never stretched.

## Mini tablet and tablet
The garage image is now a decorative grid item spanning the same first five grid rows as corner info, branding, heading/caption and cars through 900px. Its height follows content rather than the full Hero and service cards. Portrait garage art is used below 600px; the existing wide garage asset serves 600–900px. Both use center-bottom cover framing. The floor continues below the wheels with a short blend into the lower Hero. No image asset was regenerated or changed.

Mini-tablet track height uses clamp(150px,22svh,210px); short landscape has its own svh cap. At 640px, the car strip fits fully within the Hero and the garage floor remains visible underneath. At 768px the full group is preserved rather than applying the phone enlargement.

Between 600–1199px, contact padding reduces to 4px/10px, number text to 14px, icon to 12px, with 32px link targets. At 640px the pill changes from approximately 164×106px to 143×74px. At 901–1199px only the central brand pill's displayed width is limited to clamp(320px,36vw,420px) to avoid the location/logo collision found at 960px landscape. Artwork and metallic treatment are unchanged.

## Desktop
At >=1200px, the Hero is an inline-size container and its two information pills escape the content padding with container-relative positioning. Their tops stay aligned. Offsets from the Hero's rendered edges are 1px left and 0.984–1px right (subpixel rounding). This is the content edge, excluding the browser scrollbar. Desktop Hero height, vehicle group, heading, caption and logo dimensions remain unchanged. At 1440px the full Hero remains 1092px high and car picture width remains 860px.

## Validation
- Production build PASS, including final rebuild after landscape correction.
- All TypeScript projects PASS.
- Lint PASS.
- Relevant automated tests: 48 PASS in 5 files (hero-lineup, hero-reference, workshop protection, experience and service-request-routing). An initial stale protection-fixture failure was corrected as described above; final run passes.
- Production browser matrix: all 19 requested sizes in both themes, plus 960×600, 960×640 and 1024×720 in both themes: **44 final checks**. See responsive-results.json for exact rectangles, dimensions and outcomes.
- No horizontal overflow, no intersection among the location pill/contact pill/logo/heading/caption, and complete car picture containment in every final check. Screenshots captured for each category and representative landscape sizes.
- Navbar Book Service still opens the four-step request popup. Mobile menu exposes Request Service. Chapter navigation changes the active indicator; champagne numbering remains rgb(209,166,91). Both verified tel hrefs unchanged. No enquiry sent.
- Final production tab console warning/error capture empty. A local preview connection was restarted during QA; no application error remained.
- Existing build warnings about ambiguous utility names and a large loader chunk remain. Existing Router/jsdom test notices remain.

## Acceptance
| Criterion | Status |
|---|---|
| Mobile Hero compressed | PASS |
| All three cars visible on mobile | PASS |
| Mobile contact pill right aligned | PASS — 8px safe-area-aware inset |
| Tablet contact compressed | PASS |
| Mini-tablet background/car sync | PASS |
| Desktop left pill 1px | PASS |
| Desktop right pill 1px | PASS — fractional rounding noted above |
| Hero design preserved | PASS — same assets, text and themes; device framing only |
| Left 01–06 navigation preserved | PASS |
| Local files updated | PASS |
| Responsive regression checks | PASS |
| Separate 3D website unchanged | PASS — no writes outside static project |
| Deployment | NOT PERFORMED |

## Limits
Viewport emulation is not physical Android/iOS testing. Physical safe-area behavior and other browser engines are unverified. No new performance audit was requested/run; the earlier reported performance regression is still unresolved. No new library, scroll listener, renderer or image asset was added.

Preview: http://127.0.0.1:8200/Toli-2/
