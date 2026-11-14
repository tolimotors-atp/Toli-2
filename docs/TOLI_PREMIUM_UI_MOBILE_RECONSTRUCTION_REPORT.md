# TOLI Motors premium UI and mobile reconstruction

## Before

The [pre-edit audit](premium-ui/BEFORE_AUDIT.md) records the current site and identifies the main problems. Mobile Services hid choices behind horizontal scrolling. Booking inherited oversized dark-theme gutters. Vehicle stages left large blank bands on phones. In light mode the Hero service tiles competed with Book Service, the corner pills used mismatched materials, and the daylight photo still carried a visible copy-lightening layer. The gallery put all 16 photos into the page flow, one after another on phones.

## Design changes

- **Palette and materials.** Retained the shared action red (#B51220), graphite (#17191C, #202327, #2A2E33), pearl (#FAF9F6), silver (#E5E5E2) and titanium bronze (#B7834A). Hero tile labels now use the existing raised surface and ink roles. The same photographs and service links remain. Removed their hover lift and glow. The corner pills share pearl and silver in light mode and the existing graphite treatment in dark mode. The pill shadow is quieter.
- **Typography and spacing.** Kept Inter and the responsive chapter type scale. The gallery now uses the same title hierarchy. Chapter content uses a common maximum width with more space between the main desktop sections. The compact view uses short, selectable service labels and full-width reading space for service and booking details. Control, panel and dialog radii reuse the existing 8px, 12px and 18px tokens.
- **Hero and navigation.** The desktop daylight radial is narrower and now peaks at about 62%, down from 65%. Tablet and phone layers peak at about 60%. The source workshop image, floor treatments, three-car artwork, logo, heading, caption and navigation structure remain in place. The phone pill still has one red 30–38px icon spanning the two original telephone links. At 320px the location and contact pills now fit on one row, removing the extra vertical track at that width.
- **Phone and tablet.** Services presents all nine choices in a two-column grid on phones. The process and booking vehicle views use tighter frames, and booking shares the 16px content gutter at 390px in both themes. At 768–1100px, Process and Booking place their existing MU-X image beside the controls or request summary. The original supplied red Isuzu MU-X images were retained. The gutters and reduced-motion tokens now apply at the intended specificity in dark mode.
- **Enquiry and assistant.** Reused the existing enquiry, theme and assistant behavior. The enquiry Back action now shares the secondary control surface. The existing responsive navigation, helper access, viewport adaptation and booking draft behavior were verified.

## Six-photo gallery

The normal page renders six photos in editorial order. All 16 valid files remain in the complete collection.

| Photo | Role |
| --- | --- |
| `gallery-2.webp` | Wide view of the workshop floor, bays and roof structure |
| `gallery-4.avif` | Street-level workshop entrance and signage |
| `gallery-3.webp` | Vehicles and equipment inside a service bay |
| `gallery-5.webp` | Reception and glass partition |
| `WhatsApp Image 2026-08-06 at 8.216.56 AM.webp` | People at a workshop event |
| `WhatsApp Image 2026-08-06 at 8.09.20 AM.webp` | Wider street view of the frontage and parked vehicles |

The desktop layout places two larger photographs above four supporting images. At tablet widths it becomes a two-column grid. Phones use a wide opener and closer, with four images paired between them. Crops preserve the subjects, and the full-size viewer keeps each original aspect ratio. Portrait photos also retain their full frame in the collection.

See More opens a scrollable three-column desktop collection and a full-height, safe-area-aware two-column phone collection. An individual preview replaces the active view in the same dialog. It supports Previous, Next, Arrow keys and Escape. All Photos returns to the collection and restores focus to the opening thumbnail. Closing the dialog restores the page trigger. Direct featured previews cycle through the six featured photos. Collection previews cycle through all 16.

The featured set retains the near-viewport loading gate. The complete collection is mounted only when requested, with responsive lazy thumbnails. The original file is used for an individual preview. Across all 22 browser runs, one gallery-source image was requested at Hero entry because the Hero already reuses the featured workshop image. After the Gallery approached, six gallery photo assets had been requested before See More. No photo outside the featured set was requested in that phase. No new photography or dependencies were added.

## Validation

- Production build, TypeScript and ESLint passed. All 377 tests passed across 55 files. The gallery-focused run passed 26 tests across five files. Existing Vitest environment warnings were separate from the clean production console.
- Chromium passed 22 viewport/theme combinations at 320×568, 360×800, 390×844, 412×915, 768×1024, 1024×768, 1366×768, 1440×900, 1920×1080, 844×390 landscape, and 683×384 reflow. Checked gallery count and requests, thumbnail overlap, keyboard and focus behavior, phone pill alignment, three-car image bounds, navigation hit sizes, booking draft, assistant replies, reduced motion and repeated theme switches. No horizontal overflow, production console warnings, uncaught errors, failed assets or WebGL requests were observed in the checked flows.
- At 390×408, completed all four enquiry steps through Review and checked the assistant input and fallback response in both themes. No live enquiry or WhatsApp message was sent.
- [Desktop comparison](premium-ui/screenshots/desktop-comparison.jpg), [mobile comparison](premium-ui/screenshots/mobile-comparison.jpg), [six photos on desktop](premium-ui/screenshots/gallery-6-desktop-light.jpg), [six photos on mobile](premium-ui/screenshots/gallery-6-mobile.jpg), [desktop collection](premium-ui/screenshots/gallery-see-more-desktop.jpg), [mobile collection](premium-ui/screenshots/gallery-see-more-mobile.jpg), [compact enquiry](premium-ui/screenshots/compact-enquiry-light.jpg), and [browser measurements](premium-ui/browser-validation.json).
- [Local production preview](http://127.0.0.1:8234/Toli-2/).

## Changed files and limits

- Gallery source and styling in `src/components/Gallery.tsx`, `src/components/gallery-editorial.css` and `src/lib/gallery-images.ts`. Removed superseded viewer styles from `src/dark-system.css`, `src/workshop-surfaces.css` and `src/mobile-responsive.css`.
- Mobile layout and Hero materials in `src/components/Services.tsx`, `src/components/journey/experience.css`, `src/components/journey/hero-corner-visibility.css`, `src/mobile-responsive.css`, `src/workshop-surfaces.css` and `src/premium-light.css`.
- Updated the affected gallery regression tests and the retained-source checksums for the four deliberately edited files. Saved the audit, report and evidence under `docs/`.

The 683×384 test approximates 200% desktop zoom. The 408px viewport approximates keyboard space. Physical Android/iOS hardware, native zoom, Safari, Firefox and screen readers were outside this run. Changes were saved locally in the static website. No commit, push or deployment was performed. The protected sibling projects were left untouched.
