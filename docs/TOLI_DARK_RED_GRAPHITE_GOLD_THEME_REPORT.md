# TOLI Motors dark theme

> **Superseded 13 Nov 2026:** the coloured chapter backgrounds were removed from every page except the hero, at the client's request. Non-hero surfaces are now transparent over a fixed hero-garage backdrop, and content cards/panels have no fills. The 50% distributions, palette rationale and guardrail bands below describe the earlier design and are retained as history.

## Audit

The existing theme already had graphite surfaces, red action states and bronze details. The browser showed flat graphite across the nine main sections below the Hero. Older atmospheric CSS still exists, but the shared workshop surface rules overrode it across the main page. Review cards, enquiry fields and the AI panel already had distinct neutral surfaces.

## Palette and lighting

| Role | Colors |
| --- | --- |
| Graphite | `#111214` controls and footer finish, `#17191C` page and section edges, `#202327` quiet depth, `#2A2E33` raised cards and metallic depth |
| Red | `#8F111B` burgundy reflection, `#B51220` primary action and faint reflected red, `#C71929` action hover, `#EA3442` selected details, `#FF7886` focus |
| Gold | `#9A6B32` outer reflection, `#D8B477` inner reflection, `#E2C596` small labels, review stars and process numerals |
| Text and borders | `#F4F3F0` headings, `#C7C8C6` secondary text, `#AEB3B9` muted text, `#41464D` structural rules and `#747A82` control borders |

Two static radial reflections sit over one graphite depth gradient. Shared graphite edges join adjacent sections. Reflections stay toward the edges, and gold occupies less area than red. Cards and inputs retain solid neutral fills. Red continues to signal primary actions and active states.

| Surface | Treatment |
| --- | --- |
| Services | Left burgundy reflection and right gold. Service cards retain the neutral fill and existing red selection. |
| Vehicle components | Right burgundy and left gold around the MU-X. Image and TOLI plate retain their original colors. |
| Process | Softer burgundy and a quieter graphite midpoint. Small gold numerals on inactive steps and red selection on the active step. |
| Workshop and About | Warmer graphite surrounds the editorial content, with a smaller burgundy reflection low on the right. |
| Gallery | Opposing side reflections behind the Gallery. Six featured photos and See More retain their behavior and original artwork. |
| Google Reviews | Left burgundy and right gold behind a neutral rail. Warm stars and a muted border on hover. |
| Booking and standalone enquiry | Stronger burgundy around the conversion section. The primary action stays red. The direct form and popup use a quiet graphite finish with solid inputs and a red keyboard focus ring. |
| Contact and footer | Contact continues the opposing lights. The footer narrows the reflections and closes in deep graphite. |
| Legal pages and 404 | Quiet graphite with smaller burgundy lighting. |
| TOLI AI | Subtle light on the open panel. Message bubbles, input and launcher keep their existing treatments. |

Phones use shorter light pools with alternate corner origins, so vertical sections have graphite space around text and between reflections. The gradients fill existing full-width section boxes and respect existing dynamic viewport and safe-area layout. The change adds no JavaScript, requests, filters or animated background layers. Physical device performance was outside this browser pass.

## Validation

- Production build, TypeScript, and ESLint passed. Vitest passed 380 tests in 56 files. Vitest printed existing jsdom and React diagnostics.
- Chromium passed both themes at 320×568, 360×800, 390×844, 412×915, 768×1024, 1024×768, 1366×768, 1440×900, 1920×1080 and landscape 844×390. No document-level horizontal overflow, console errors, warnings or failed requests during the homepage workflow. The dark layout was visually inspected at all ten sizes.
- The review rail showed five cards on desktop, two on phones and three on tablet and landscape at the tested widths. Buttons, keyboard, horizontal wheel and touch dragging worked. The supplied Google Maps review link remained present. Gallery showed six featured photos and sixteen in See More. All three MU-X images decoded.
- The booking popup and standalone form opened. The review link, Gallery controls and TOLI AI known-answer and fallback paths worked. No live service request was sent.
- Chromium verified the dark and light states on the enquiry page, legal pages, 404, booking popup and AI panel. Four successive theme switches on desktop and mobile confirmed the gradients appear only in dark mode.
- Hero and navbar before-and-after images were pixel-identical at 1366 and 390 pixels in both themes. The desktop light homepage was pixel-identical at the matching capture state. Visible chapter controls and asset files were untouched.
- Sampled dark contrast ratios were 16.89:1 for form text, 7.39:1 for the input focus outline against its field, 8.24:1 for review stars on graphite and 6.84:1 for the primary booking button text.
- Preview is local. The separate 3D website was untouched. Deployment was not performed.

## Screenshots

- [Full desktop homepage](dark-red-graphite-gold-evidence/dark-gradient-full-page-desktop.jpg)
- [Desktop Services](dark-red-graphite-gold-evidence/dark-gradient-services-desktop.jpg)
- [Desktop Gallery](dark-red-graphite-gold-evidence/dark-gradient-gallery-desktop.jpg)
- [Desktop Google Reviews](dark-red-graphite-gold-evidence/dark-gradient-google-reviews-desktop.jpg)
- [Desktop MU-X](dark-red-graphite-gold-evidence/dark-gradient-vehicle-desktop.jpg)
- [Desktop booking](dark-red-graphite-gold-evidence/dark-gradient-booking-desktop.jpg)
- [Mobile Services at 390 px](dark-red-graphite-gold-evidence/dark-gradient-mobile-390.jpg)
- [Mobile Google Reviews at 390 px](dark-red-graphite-gold-evidence/dark-gradient-reviews-mobile-390.jpg)
- [Mobile Gallery at 390 px](dark-red-graphite-gold-evidence/dark-gradient-gallery-mobile-390.jpg)
- [Light theme regression](dark-red-graphite-gold-evidence/light-theme-regression.jpg)

## Files

`src/workshop-surfaces.css` carries the theme; `tools/theme-colour-guardrail.cjs` and the `guardrail:theme` script in `package.json` add the automated check. This report and its eleven screenshots are in `docs/`.

## 50% RED COLOR DISTRIBUTION REVISION

### What this percentage means

`50% RED = APPROXIMATE VISUAL COLOR DISTRIBUTION ACROSS THE PAGE`

It is **not** red opacity, `rgba(..., 0.5)`, a 50% transparent overlay, or `filter: opacity(50%)`. The dark theme is composed from opaque red fields, red-to-graphite tonal gradients, graphite surfaces and tiny gold reflections. No full-page tint or filter is used anywhere, so photography, the MU-X and the Hero keep their natural colour.

### Previous distribution

The first red push moved the page from graphite-dominant to roughly red/graphite parity, but a second pass overshot: measurement of its 1366px capture read as 62.5% red-family / 34.2% graphite / 3.2% gold. Services, Gallery, Reviews and Contact were fixed, yet the reddest chapters had become too uniform:

| Region | Red family | Graphite | Gold |
| --- | --- | --- | --- |
| Whole non-Hero page | 62.5% | 34.2% | 3.2% |
| Vehicle components | 73.1% | 21.4% | 5.5% |
| Process | 70.4% | 26.5% | 3.1% |
| About / Why choose us | 78.2% | 19.2% | 2.5% |
| Footer | 67.1% | 28.8% | 4.2% |

Those four chapters carried the overshoot; gold was still a very small accent.

### Current visual distribution

The rebalanced dark page measures as follows below the Hero at 1366px (hue classification of the rendered capture; the large fields now read as rich automotive lacquer, with deeper ruby retained at the transitions):

| Region | Red family | Graphite (incl. near-black) | Gold |
| --- | --- | --- | --- |
| Whole non-Hero page | 52.8% | 41.9% | 5.2% |
| Services | 52.1% | 47.8% | 0.1% |
| Vehicle components | 53.2% | 38.8% | 8.0% |
| Process | 60.7% | 35.0% | 4.3% |
| About / Why choose us | 52.7% | 40.5% | 6.8% |
| Gallery | 47.2% | 48.0% | 4.8% |
| Google Reviews | 48.9% | 45.3% | 5.8% |
| Booking | 54.7% | 39.4% | 5.9% |
| Contact | 49.7% | 45.4% | 4.9% |
| Footer | 61.3% | 32.3% | 6.4% |

Expensive-red, simplified: the lacquer face is one token, `--red-lacquer:#CD1C2F`; the shadow and mid stops reuse the existing brand reds (`--brand-pressed:#8F111B`, `--brand-primary:#B51220`), so the field has one bespoke red instead of three. The separate white specular overlay was removed — each chapter is built from two background layers, the gold reflection plus the three-stop red gradient, which keeps the ruby depth without hazing the graphite. Contact panels use a two-stop `brand-pressed → lacquer face` gradient, and the map footer sits on brand reds rather than a bespoke dark red. Graphite and gold values are unchanged.

Mobile is deliberately re-composed rather than scaled down: the 390px page measures 52.2% red-family, 45.6% graphite and 2.2% gold below the Hero (360px: 52.2% / 45.6% / 2.2%). Gold stays a micro-accent (stars, numerals, thin seams and reflected light) instead of a large gold field, per the "no large gold backgrounds" rule. Its pixel share is therefore about 5% on desktop rather than the brief's 10% area weight, but it is roughly 1.5× the previous pass and remains the premium tertiary detail.

### Automated colour-share guardrail

`npm run guardrail:theme` builds the site, launches its own local preview, captures 1366, 390 and 360 full pages in dark mode and classifies every pixel below the Hero as red-family, graphite (including near-black) or gold. It exits non-zero when the balance leaves these accepted bands:

| Viewport | Red | Graphite | Gold |
| --- | --- | --- | --- |
| Desktop | 47–54% | 38–48% | 3–8% |
| Mobile | 46–54% | 41–52% | 1–5% |

Every chapter must also keep red between 42% and 68%, so a section cannot quietly collapse back to graphite or flare into flat red. The script is `tools/theme-colour-guardrail.cjs`; to check a running dev server instead, use `THEME_GUARDRAIL_URL=http://127.0.0.1:8190/Toli-2/ node tools/theme-colour-guardrail.cjs`. Current run: desktop 52.8% / 41.9% / 5.2%, mobile 52.2% / 45.6% / 2.2%, mobile-small 52.2% / 45.6% / 2.2%; all pass, with Contact at 49.7% in the guardrail's own section crop. Section output also reports graphite and gold so the report can quote the full composition.

### Red shades used

| Role | Value |
| --- | --- |
| Deep ruby shadow / pressed | `#8F111B` (`--brand-pressed`) |
| Ruby field / action | `#B51220` (`--brand-primary`) |
| Lacquer face (field high) | `#CD1C2F` (`--red-lacquer`, the only field-only red) |
| Selected / highlight | `#EA3442` (`--brand-selected`) |
| Map footer | brand-pressed → brand-primary, no bespoke shade |

Gold remains muted metallic: `#D8B477` reflected light, `#9A6B32` deep reflection, `#E2C596` labels, stars and numerals. Graphite is unchanged as the structural material: `#17191C` page, `#202327` quiet depth, `#2A2E33` raised cards, `#41464D` rules.

### Section-by-section treatment

| Section | Treatment |
| --- | --- |
| Services | Balanced red field (graphite 24%, wine 44%, TOLI red 76%) across the right and lower composition. Cards stay readable: graphite rails, alternating panels with a quiet wine wash, every third panel carrying a deep-red edge, selected service on stronger red. |
| Vehicle components | Red environment (graphite 38%, wine 56%, TOLI red 86%) builds around the naturally coloured MU-X; the graphite lets gold reflected light read on the right without touching the image. |
| Process | Bright TOLI-red region (graphite 40%, wine 59%, red 92%) with graphite step surfaces, red selection in the active step and small gold numerals only. |
| About / Why choose us | Red editorial environment (graphite 40%, wine 59%, red 92%, inherited from Process) with graphite statistic slabs and gold micro-labels; the graphite returns through the chapter. |
| Gallery | Red-dominant surround (graphite 24%, wine 42%, TOLI red 75%) with a deep-red left/lower field. All six photographs keep their original colour; See More remains a graphite control. |
| Google Reviews | Balanced red and graphite environment (graphite 30%, wine 48%, red 82%); cards stay graphite/metallic, stars muted gold, CTA TOLI red. |
| Booking | Red → TOLI red → graphite environment (graphite 34%, wine 52%, red 84%); the request panel stays graphite so the red CTA remains distinguishable and the form fields stay neutral. |
| Contact | Red chapter carried by two-stop ruby lacquer panels (`#8F111B → #CD1C2F`) and a 10px ruby frame with a brand-red footer strip around the map. The map itself stays graphite; on mobile the third card alternates back to graphite so the phone composition remains near 50%. The chapter measures ~50% red, up from 37%. |
| Footer | Deep red settles against graphite (graphite 36%, wine 60%, red 96%), with a small gold reflection; no plain black ending. |
| Legal pages, 404, dialogs, TOLI AI | Same wine/graphite language at lower intensity; forms remain graphite with a red focus ring. |

Gradients use red at different angles per chapter (124°, 231°, 248°, 158°, 285°, 78°, 252°, 236°) so the page does not repeat one diagonal. A thin warm metallic seam (`#D8B477` at low alpha) separates chapters; it is a 1px detail, not a gold band.

### Protected areas

No rule in this revision targets the Hero, its background, cars, lighting, typography or pills, or the navigation, navbar background, car, logo or controls. The changes are confined to below-hero dark-theme selectors in `src/workshop-surfaces.css`. Light mode rules are untouched; the light screenshot shows the same pearl/silver theme with controlled red.

### Desktop screenshots

- [Full page at 1366px](dark-50-red-evidence/dark-50-red-full-page-1366.jpg) and [1920px](dark-50-red-evidence/dark-50-red-full-page-1920.jpg)
- [Services](dark-50-red-evidence/dark-50-red-services.jpg), [Gallery](dark-50-red-evidence/dark-50-red-gallery.jpg) and [Google Reviews](dark-50-red-evidence/dark-50-red-google-reviews.jpg)
- [MU-X vehicle section](dark-50-red-evidence/dark-50-red-vehicle.jpg), [Booking](dark-50-red-evidence/dark-50-red-booking.jpg) and [Contact](dark-50-red-evidence/dark-50-red-contact.jpg)

### Mobile screenshots

- [Dark theme at 390px](dark-50-red-evidence/dark-50-red-mobile-390.jpg)
- [Dark theme at 360px](dark-50-red-evidence/dark-50-red-mobile-360.jpg)

### Light-theme regression

- [Light theme full page](dark-50-red-evidence/light-theme-regression.jpg) — pearl, white, silver and graphite with the existing controlled red accents; the 50% red fields appear only under `html[data-theme=dark]`.

### Validation results

- TypeScript (`tsc` app/node/qa), ESLint and the production Vite build passed.
- 79 relevant tests across 9 suites passed (dark palette, site theme, testimonials, editorial gallery, services, TOLI AI, MU-X photography, Hero reference, navbar motion). Vitest printed existing jsdom/act warnings only.
- Chromium at 1366×900, 1920×1080, 390×844 and 360×800: no document-level horizontal overflow (scrollWidth equals clientWidth at every size) and both themes render.
- Google Reviews: five cards fully visible at 1366px, two at 390px/360px; the rail scrolls horizontally (button test moved scrollLeft from 0 to 233px desktop and 0 to 183px mobile) and the `View reviews on Google` link points at the Google Maps review URL.
- Gallery: six featured photographs, See More opens the complete gallery with sixteen photos.
- Rebalance re-check after the colour-share tuning: ESLint and the production build passed; Chromium at 1366px and 390px still shows no horizontal overflow, five/two fully visible review cards and six featured gallery photos. TypeScript and the test suite are unaffected because the rebalance only changes CSS values.
- Simplification pass: removed a duplicate mobile stop block, let About inherit the Process field stops and dropped an unnecessary `!important` from the contact panels.
- Contact fix: the contact cards moved from graphite to ruby lacquer, the map gained a ruby frame and brand-red footer strip, and the third mobile card returns to graphite. Contact rose from 37.4% to ~50% red; desktop overall settled at 52.8% red / 41.9% graphite / 5.2% gold. No horizontal overflow was introduced.
- Expensive-red pass: the fields moved to a ruby lacquer with a brighter face than the brand mid red, keeping the richness without the earlier flat scarlet. A review pass then reduced the palette to one field-only token (`--red-lacquer`) plus the existing brand reds, and removed the extra white specular layer. The guardrail stayed in band (desktop 52.8 / 41.9 / 5.2, Contact 49.7), and the contact cards' warm-white text remains.
- `npm run guardrail:theme` passed with exit 0 and released its preview port; the build it runs also passed. It checks 1366, 390 and 360.
- Theme toggle switched dark → light and back; TOLI AI answered a services question from its built-in knowledge base.
- Screenshots were captured with animations paused and lazy images forced to load. Every selector added in this pass is scoped to the section stack, gallery, reviews, booking, contact, footer or dialogs; no Hero or navbar rule was edited. Physical devices, live service submission and deployment were outside this local pass.
