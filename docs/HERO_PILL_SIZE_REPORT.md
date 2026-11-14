# Hero pill and typography sizing — 6 November 2026

Changed only `src/components/journey/hero-corner-visibility.css` in application source. No markup, handlers, imports, tests, fixtures or other source/assets changed. No deployment.

## Result
Both pills are approximately 20–23% smaller in width/height (desktop left height reduction is 19.6% at 1920px, rounding to 20%). ANANTAPUR remains bold red; the subtitle remains white and centered. Both phone numbers remain white, unbroken and linked to the same verified tel destinations. Fonts shrink by roughly 17–18%, icons by 17–20%.

| Width | Left pill before → after, px | Contact pill before → after, px |
|---|---|---|
| 360px | 183×62 → 144×48 | 126×78 → 99×62 |
| 390px | 183×62 → 144×48 | 126×78 → 99×62 |
| 430px | 183×62 → 144×48 | 126×78 → 99×62 |
| 600px | 183×62 → 144×48 | 121×68 → 96×54 |
| 768px | 183×62 → 144×48 | 121×68 → 96×54 |
| 1440px | 213×67 → 167×54 | 177×82 → 140×65 |
| 1920px | 240×78 → 189×63 | 192×82 → 152×65 |

## Typography
- ANANTAPUR: clamp(20px,1.6vw,30px) → clamp(16.4px,1.312vw,24.6px).
- Subtitle: desktop clamp(12px,.9vw,15px) → clamp(10px,.738vw,12.3px); mobile/tablet 12px → 10px. Letter spacing reduces modestly.
- Contact numbers: mobile/tablet 13.5px → 11.25px; desktop clamp(15px,1.1vw,18px) → clamp(12.3px,.902vw,14.76px).
- Phone icon: desktop 15px → 12px; mobile 12px → 10px; tablet 11px → 9px.
- Link target heights: 28px mobile, 25px tablet and 25.6px desktop; numbers do not wrap or clip and their center points resolve to the intended anchor.

Padding and gaps were reduced independently by device. Pill curvature stays fully rounded. Existing translucent gradients, metallic border, upper shine, static shadow/glow, 5px small-screen / 8px desktop backdrop blur and unsupported-filter fallback are unchanged. No whole-element scaling, opacity fading or opaque replacement was introduced.

## Composition protection
The information row retains its approved occupied height while the visible capsules shrink. This avoids moving the central logo, headings, caption or cars. Exact before/after DOM rectangles match for the Hero, logo, heading, caption and vehicle image at every requested viewport. Desktop corner pills remain approximately 1px from the edges; right gaps remain 2px on phones and 3px on tablets. The left mobile/tablet position is unchanged. The icon is vertically centered on both lines (0px midpoint difference).

No changes to the navbar, main logo, car images, grounding shadows, garage, champagne rail, active popover, AI, other sections or independent 3D project. Protected-file hash audit shows no changes to any frozen source/artwork.

## Validation
- Production build PASS.
- All TypeScript projects PASS.
- Lint PASS.
- Relevant tests: 36 PASS across hero-reference, experience and service-request-routing.
- Browser checks: 360×640, 390×844, 430×932, 600×960, 768×1024, 1440×900 and 1920×1080 in both themes: 14 PASS. No horizontal overflow, no pill/logo/heading/caption intersection, no clipped phone text, both tel targets clickable. See audits.json.
- Production browser warnings/errors: none captured.
- Before/after screenshots and exact dimension/font records retained in hero-pill-size-evidence.
- Existing build warnings about ambiguous utilities and the large loader chunk remain; test runner retains existing Router/jsdom notices.

## Acceptance
| Criterion | Status |
|---|---|
| Left pill size reduced | PASS |
| Right pill size reduced | PASS |
| Left font size reduced | PASS |
| Contact font size reduced | PASS |
| Phone icon proportionally reduced | PASS |
| Mobile/tablet responsiveness | PASS |
| Desktop corner positioning preserved | PASS |
| Local files updated | PASS |
| Hero otherwise unchanged | PASS — exact rectangle checks |
| Deployment | NOT PERFORMED |

Limits: browser viewport testing only; physical devices and a fresh performance audit were not tested. The previously reported performance regression remains unresolved.

Preview: http://127.0.0.1:8200/Toli-2/
