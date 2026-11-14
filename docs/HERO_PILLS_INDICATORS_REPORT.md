# Hero pills and left indicators — 6 November 2026

Changed only two source files:
- `src/components/journey/hero-corner-visibility.css`: red #FF4056 ANANTAPUR, centered two-line location text, removed inherited subtitle border/padding, red phone icon centered across both phone lines. Corrected the existing tablet one-column override only within this pill. Both tel links unchanged. Frosted material and text sizing retained.
- `src/components/journey/experience.css`: champagne #D1A65B numbering, metallic graphite inactive surfaces, gold border, deep-red/graphite raised current surface with 5px outward translation and 1.04 scale. Pointer hover uses a small lift; keyboard focus has a champagne outline. Reduced motion disables transformations/transitions while preserving the highlighted border/shadow state.

Reused the existing aria-current state and passive, animation-frame-coalesced scroll tracking; no new observer, listener, library, React change, config or fixture update. Rail remains intentionally hidden at <=900px as before; the existing menu supplies navigation on those sizes. No mobile rail was introduced over Hero content.

## Validation
- Production build PASS, including final rebuild after tablet correction.
- TypeScript PASS (app, node and QA projects).
- Lint PASS.
- Relevant tests PASS: 36 tests in hero-reference, experience and service-request-routing.
- Both themes checked at 360×640, 390×844, 430×932, 768×1024, 1440×900 and 1920×1080. No horizontal overflow. Icon midpoint equals the phone-block midpoint (0px measured difference), including repaired tablet layout. Both telephone hrefs preserved.
- All six chapter controls exercised. Smooth-scroll transitions briefly retain the outgoing section until the new section enters view, as intended; 05 Request and return to 01 confirmed after settling.
- Ordinary two-page downward scroll activated 02 Services, with exactly the current indicator receiving the raised transform. Enter navigation works. Existing navigation/menu routing tests passed.
- Desktop/mobile screenshots saved in `hero-pill-indicator-evidence`. Phone/link readability and unchanged Hero composition visually inspected. Production browser warning/error capture empty.
- Build retains existing Tailwind ambiguity and large-chunk warnings. Relevant tests retain existing Router/jsdom notices.

## Acceptance
| Requirement | Status |
|---|---|
| ANANTAPUR red text | PASS |
| Separator removed | PASS — inherited border removed |
| Location text aligned | PASS |
| Phone icon centered / red | PASS |
| Contact links preserved | PASS |
| 01–06 champagne gold | PASS |
| Active raised effect | PASS |
| Scroll active state | PASS |
| Mobile responsiveness | PASS — existing narrow-screen rail hiding preserved |
| Local files updated | PASS |
| Existing Hero preserved | PASS |
| Deployment | NOT PERFORMED |

Cars, background, logo, heading, caption, navbar structure, other sections, AI logic and separate 3D project were not edited. No artwork regenerated. No new functionality or tests mirroring CSS were added.

Limits: browser viewport emulation, not physical-device certification. Pointer-hover and reduced-motion rules reviewed in source; separate physical mouse/reduced-motion sessions not run. Performance audit not repeated for this small CSS refinement; the previously reported performance regression remains unresolved.

Preview: http://127.0.0.1:8200/Toli-2/
