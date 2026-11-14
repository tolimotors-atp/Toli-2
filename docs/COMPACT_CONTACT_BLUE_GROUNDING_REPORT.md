# Compact contact, ice-blue accents and desktop grounding — 6 November 2026

Changes saved in the static website only. No deployment performed.

## Contact pill
Mobile phone text is 13.5px, bold and explicitly nonwrapping; padding is 2px/8px, the icon is 12px, and links retain 36px target height. On 360–599px screens, the contact pill shares the upper information row with the unchanged location pill. At 320px it retains a separate row to avoid a collision. Right inset is max(2px,safe-area-inset-right).

Tablet padding is 1px/6px, icon 11px, text 13.5px and links 32px high. The information row expands toward the right using the Hero's container width, accounting for content padding and centered/max-width layouts. Right inset is max(3px,safe-area-inset-right). A legacy mobile order rule is neutralized within this row so ANANTAPUR stays on the left. Existing left-pill material, text and positioning are retained.

| Width | Contact before | Contact after | Right gap |
|---|---|---|---|
| 320px | 147×98px | 126×78px | 2px |
| 390px | 147×98px | 126×78px | 2px |
| 640px | 143×74px | 121×68px | 3px |
| 768px | 143×74px | 121×68px | 3px |
| 1024px | 141×74px | 121×68px | 3px |

The phone icon midpoint matches the complete phone block midpoint (0px measured difference). Both existing tel links are unchanged and passed direct hit testing. All phone numbers fit without horizontal clipping. Desktop contact-pill dimensions and 1px edge positioning are unchanged.

## Supporting accent
Replaced the non-Hero champagne token with ice blue #38BDF8, using deep blue #0B5D83 for small labels on light surfaces. Thin chapter separators and inactive service indices share this supporting accent. The assistant's small SERVICE ASSISTANT label and launcher icon receive blue. Chapter label precedence was corrected so the actual rendered label is rgb(56,189,248) in dark mode and rgb(11,93,131) in light mode.

All 01–06 numbers and their edges remain champagne gold (#D1A65B/#E6C783), with the same red/graphite active surface and raised state. Main headings, logo, Hero environment, large surfaces, primary buttons and service-card surfaces remain red/grey/graphite/silver. The roughly 10% supporting-accent goal is a visual guideline, not a pixel-coverage measurement.

## Grounding investigation and fix
The vehicle artwork is one transparent composition, not three independently transformed elements. It has no uniform transparent bottom padding to remove: alpha bounds cover its 1600×372 canvas, while individual tire baselines intentionally differ for perspective. Existing CSS already contains the artwork and bottom-aligns it. The central sedan is lower/closer, and neither vehicle geometry nor framing needed a uniform downward translation.

Read-only source-alpha sampling found little or no shadow immediately beneath portions of the side-car tires (for example, below the SUV front tire the sampled median alpha was 0/255 and maximum 11/255). These weak contact patches allow the bright reflective floor texture to dominate at contact points. Previous hydraulic removal is intact; no lift structures or image pixels were added or regenerated.

At >=1200px, two static pseudo-elements match the image's native 1600:372 aspect ratio and bottom alignment. Their coordinates scale with the contained image, not the taller car track. Six tight tire-contact patches and three wider underside fades map to the SUV, sedan and coupe's separate contact baselines. Indicative front contact anchors are 21.5%/75%, 46.5%/95% and 82.5%/77% of the image. The second layer adds faint silver, red and graphite light pools immediately below each vehicle. No mirror copy, flat platform, hard ellipse, continuous animation, blur filter or new renderer was added.

All six desktop vehicle-image rectangles are byte-for-byte identical in the before/after measurement JSON: the fix does not move, scale, distort or crop the cars. The original vehicle and garage assets are unchanged. Mobile/tablet framing and shadows receive no desktop pseudo-elements.

## Files modified
- `src/mobile-responsive.css`: compact phone/tablet geometry, safe-edge positioning and intermediate flex-row order.
- `src/components/journey/hero-corner-visibility.css`: no-wrap phone links and final compact icon/column widths, preserving frost/blur/fallback.
- `src/workshop-surfaces.css`: supporting blue token, small decorative trims and assistant technical accents.
- `src/components/journey/hero.css`: desktop-only contact shadows and restrained reflections.
- `src/test/fixtures/separation-protected.json`: only the authorized hero.css hash updated. Every other protected baseline matches.
- This report and `docs/compact-contact-grounding-evidence`.

## Validation
Production build PASS; all TypeScript projects PASS; lint PASS. Relevant automated suite: **83 tests in 6 files PASS**, covering Hero, lineup, protected assets, navigation, shared request flow and TOLI AI.

**40 final browser checks**: 20 sizes in both themes. Mobile/tablet: 320×568, 360×640, 375×667, 390×844, 412×915, 430×932, 600×960, 640×960, 768×1024, 820×1180, 1024×768, 960×600, 844×390 and 667×375. Desktop: 1280×720, 1366×768, 1440×900, 1600×900, 1920×1080 and 2560×1440. Final results show loaded vehicle assets, no horizontal overflow, no corner-pill/logo/heading/caption overlaps, no clipped phone text and correctly centered icons. See responsive-results.json.

Desktop tire contact inspected across all six sizes; full before/after screenshots and six close-up comparisons retained. Mobile and mini-tablet before/after evidence retained. The preview server had stopped at the beginning of QA; initial captures with an unloaded vehicle were discarded and recaptured with successful asset-load checks before implementation. An earlier development-tab Router warning was retained in browser history; final production-origin warning/error capture was empty.

Phone links pass hit tests without launching calls. TOLI AI opens; its light badge color was checked. Chapter navigation updates the active gold indicator. Existing automated request-flow and assistant tests pass. No external enquiry sent and no live ads enabled.

Existing build warnings about ambiguous Tailwind utilities and the large loader chunk remain; test runner retains existing Router/jsdom notices. No source/asset writes occurred in the independent 3D or original project.

## Acceptance
| Requirement | Result |
|---|---|
| Mobile contact compressed / moved right | PASS |
| Tablet contact compressed / moved right | PASS |
| Ice-blue supporting accent | PASS |
| Blue kept subtle | PASS — small labels/trims/icons only |
| 01–06 champagne gold retained | PASS |
| Silver SUV grounded | PASS — visual checks at six desktop sizes |
| Red sedan grounded | PASS — closer/lower baseline preserved |
| Graphite coupe grounded | PASS — separate contact patches |
| Realistic contact shadows | PASS — static, feathered tire/underside shading |
| No hydraulic supports in vehicle presentation | PASS |
| Mobile three-car view preserved | PASS |
| Mini-tablet scene synchronization preserved | PASS |
| Local files updated | PASS |
| Separate 3D website unchanged | PASS — no writes |
| Deployment | NOT PERFORMED |

## Limits
Browser viewport emulation is not physical-device certification. No new Lighthouse/performance audit was run; the prior performance regression remains unresolved. Grounding is a static 2D compositing refinement, with subjective visual approval still up to the owner. No image asset or vehicle model was replaced.

Preview: http://127.0.0.1:8200/Toli-2/
