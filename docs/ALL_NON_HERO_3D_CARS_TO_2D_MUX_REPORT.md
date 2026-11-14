# All non-Hero vehicle presentations: front-sided 2D MU-X

Date: 2026-11-10  
Project: `/home/thunder/shared/tolimotors-main1/toli-static-website`  
Development preview: <http://127.0.0.1:8190/Toli-2/>

## Final result

| Location | Result |
| --- | --- |
| Section 03 — HowItWorks | FRONT THREE-QUARTER TRANSPARENT 2D MU-X |
| Explore vehicle components | FRONT THREE-QUARTER TRANSPARENT 2D MU-X |
| Section 05 — CtaBanner | FRONT THREE-QUARTER TRANSPARENT 2D MU-X |
| Component-page 360° / DRAG TO ROTATE | REMOVED |
| Production page canvas / scene-host count | 0 / 0 |
| Hero | UNCHANGED |
| Navbar | UNCHANGED |
| TOLI AI desktop/mobile | PASS |
| Historical 3D work | PRESERVED, INACTIVE IN THESE LOCATIONS |
| Deployment | NOT PERFORMED |
| Git commit | NOT PERFORMED |

## Production-path audit

The production homepage in `src/pages/Index.tsx` renders three non-Hero vehicle slots. At the start of this task, Section 03 already used the front transparent image and Section 05 used the rear transparent image. The remaining active WebGL car was in the separate component chapter.

The exact text search traced the component chapter through:

`Index → ComponentExperience → VehicleComponentView → JourneyDock(mode="services")`

`ComponentExperience.tsx` supplies the heading “Explore vehicle components.” `VehicleComponentView.tsx` supplies “ISUZU MU-X / OVERVIEW”, the service-zone buttons and the services dock. This was the actual source of the car in the reported screenshot.

The other paths are:

- `Index → HowItWorks → JourneyDock(mode="process")`
- `Index → CtaBanner → JourneyDock(mode="completion")`

Searches covered vehicle-scene/mux-presentation imports, vehicle initialization, scene hosts, rotation UI and production routes. No fourth car presentation was found in the production route. `VehicleStudio` and the legacy scene/model helpers remain for historical/test use; `Index` does not render VehicleStudio, and production pages do not import it. Standalone modeling/validation sources are not active homepage presentations. No unrelated decorative effects or protected projects were changed.

## One authoritative source and one shared cutout

All 43 supplied reference images were re-inspected through the existing [contact sheet](mux-2d/reference-contact-sheet.jpg). The front master was also checked at full size and against a dark background.

Selected original:

`/home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot 2026-11-08 213542.png`

Dimensions: 1022 × 593. SHA-256:

`7cba4428b536116792a6dcf44ecbd5779e7342a18954b83e2d8a5903e1c53c92`

This supplied front three-quarter view shows the complete fascia, bonnet, headlights, mirrors, roof, front wheel, doors and side body. The same existing source-preserving master cutout is now used in every slot. No new SUV was generated, downloaded or substituted, and no vehicle colors or proportions were changed.

Production assets, reused without regeneration:

| File under `src/assets/vehicles/isuzu-mux/` | Dimensions | Bytes |
| --- | --- | ---: |
| `isuzu-mux-front-3q-transparent-640.webp` | 640 × 384 | 40,262 |
| `isuzu-mux-front-3q-transparent.webp` | 1100 × 660 | 64,766 |

Both files have genuine RGBA transparency, transparent corners and no studio floor or opaque rectangle. The existing manually traced alpha mask retains the original vehicle pixels, windows, tires, trim and manufacturer display plate. The original references remain untouched: all 43 hashes match the saved reference baseline. Existing masks, generator and PNG master remain available under `tools/images/` and `docs/mux-transparent/`.

The reusable component now imports only the front variants. Rear artwork remains archived on disk but is not imported by any of these three slots. All three production images resolved to the same hashed front WebP in the production-preview browser check.

## Implementation

`JourneyDock` treats services, process and completion as photographic presentations. Each renders `MuxPhotography` directly in GPU-ready and fallback states. These branches render no scene host, loading state, technical SVG substitute or canvas.

The component page therefore does not start vehicle geometry, camera, lights, pointer rotation, drag handling or scene updates. Its former 360° and drag hints were created by the legacy renderer; without a scene host that renderer is not initialized and those controls are absent. They were not merely hidden behind the image.

The generic scene loader remains available to historical studio code. On the production homepage, there are no scene hosts for its timeline/visibility logic to activate. The browser confirmed zero canvases and zero `data-scene-dock` elements after visiting all three locations. Tests also assert that service-image presentation does not allocate a renderer, including Strict Mode and mobile/reduced-motion cases.

`MuxPhotography` has a single front view rather than a front/rear selector. It retains responsive `srcset`/`sizes`, intrinsic dimensions, lazy loading, asynchronous decoding and useful “Isuzu MU-X — front three-quarter view” alt text. The same transparent figure and restrained contact/drop shadows work in both themes. No continuous motion, simulated rotation or new animation library was added.

The new component image fills its existing vehicle slot with a complete, more prominent silhouette. Existing section height, headings, button placement and parent grid rules are retained. No Hero/navbar selectors or artwork changed.

## Component-button behavior

Vehicle inspection, Wheel & brake illustration and Battery illustration remain functional and retain semantic pressed states and shared service selection.

- Vehicle inspection returns to the overview and clears component focus.
- Wheel/brake selection shows the useful explanation; Inspect component highlights the front wheel/brake discussion area. Internal brake parts are explicitly described as not visible in the photograph.
- Battery selection shows its explanation; Inspect component labels the under-bonnet discussion area. The text explicitly states that the battery is not visible in this photograph.
- Return to vehicle removes the highlight. Selecting an unrelated service also clears focus.

The labels identify discussion areas; they do not invent visible internal parts or diagnose a vehicle. Accessible explanation text remains available independently of the decorative area marker. Browser interaction verified both labels and overview reset. Automated tests retain keyboard service selection, enquiry context and return-state checks.

## Responsive and visual checks

All three locations were checked in dark and light themes at:

320 × 568; 360 × 800; 390 × 844; 412 × 915; 768 × 1024; 1366 × 768; 1920 × 1080.

All 42 final cases passed: correct front image loaded, complete vehicle within the viewport, no horizontal overflow, transparent vehicle container, no scene host/canvas, no old rotation UI and no following panel obscuring the image center. Roof, mirrors, wheels and tires remain visible. The same original car is used throughout.

Final screenshot overview was inspected visually in addition to DOM checks. Desktop component captures were re-positioned after an initial capture-helper scroll-direction error; the page source did not require a layout correction. Final records are deduplicated in `screenshots/responsive-final.json`; the raw sequence is retained in `screenshots/responsive.json`. Neighboring section content in some images is part of the existing scroll/stack composition.

Required screenshots:

- [Section 03 desktop](all-non-hero-mux/screenshots/section03-front-2d-mux-desktop.jpg)
- [Vehicle Components desktop](all-non-hero-mux/screenshots/vehicle-components-front-2d-mux-desktop.jpg)
- [Section 05 desktop](all-non-hero-mux/screenshots/section05-front-2d-mux-desktop.jpg)
- [Section 03 mobile](all-non-hero-mux/screenshots/section03-front-2d-mux-mobile.jpg)
- [Vehicle Components mobile](all-non-hero-mux/screenshots/vehicle-components-front-2d-mux-mobile.jpg)
- [Section 05 mobile](all-non-hero-mux/screenshots/section05-front-2d-mux-mobile.jpg)
- [Three presentations together](all-non-hero-mux/screenshots/three-front-mux-presentations.jpg)
- [All viewport/theme captures](all-non-hero-mux/screenshots/overview.jpg)
- [Hero regression](all-non-hero-mux/screenshots/hero-regression.jpg)
- [Navbar regression](all-non-hero-mux/screenshots/navbar-regression.jpg)
- [Wheel focus](all-non-hero-mux/screenshots/component-wheel-focus.jpg)

## Regression and runtime validation

A protection baseline compared 390 existing source/public files. Hero, navbar, their vehicle assets, TOLI AI, original references and all historical 3D model source remain unchanged. No independent 3D showroom project files were edited.

The production preview confirmed all three front WebPs loaded, zero canvas elements, zero scene hosts and no 360°/drag text. The console contained zero warnings/errors. Header Book Service opened the canonical Service Request dialog and Name field; no request was submitted. Existing automated booking/enquiry and draft-preservation tests pass.

TOLI AI answered a local service question on desktop and remained usable on mobile. See [desktop AI](all-non-hero-mux/screenshots/ai-desktop.jpg), [mobile AI](all-non-hero-mux/screenshots/ai-mobile.jpg) and [recorded response](all-non-hero-mux/screenshots/ai.json).

There is no vehicle WebGL rendering cost in these three locations. All three reuse one responsive image resource. No FPS, battery, memory or speed percentage is claimed. The historical dynamic vehicle-scene chunk is still emitted by the build because its optional loader is retained, but the production homepage no longer supplies a host to initialize it. The existing build advisory for a chunk above 500 kB remains.

## Technical validation

| Check | Result |
| --- | --- |
| TypeScript app/node/qa | PASS |
| Lint | PASS |
| Production build | PASS, 21.25 seconds |
| Full test suite | PASS, 55 files / 373 tests |
| Responsive checks | PASS, 42 final cases |
| Production console | 0 warnings / 0 errors |
| Production canvas / scene-host count | 0 / 0 |
| Original reference protection | PASS, 43 unchanged |
| Hero/navbar/TOLI AI source protection | PASS |

Obsolete tests expecting service WebGL/loading states were replaced with front-image, focus, no-renderer and responsive-source assertions. The removed Section 02 renderer expectation is no longer a requirement. Historical standalone renderer tests remain valid as tests of preserved inactive development code.

## Files modified

Production:

- `src/components/journey/JourneyDock.tsx`
- `src/components/journey/MuxPhotography.tsx`
- `src/components/journey/VehicleComponentView.tsx`
- `src/components/journey/mux-photography.css`

Tests/fixtures:

- `src/test/mux-photography.test.tsx`
- `src/test/phase2-services.test.tsx`
- `src/test/default-selections.test.tsx`
- `src/test/experience.test.tsx`
- `src/test/vehicle-accessibility.test.tsx`
- `src/test/fixtures/separation-protected.json` — only the two authorized component hashes updated.

Added documentation/evidence:

- This report.
- `docs/all-non-hero-mux/` baseline, protection metadata, logs and screenshots.

No production image file was modified; the approved front cutout was reused. No deployment or Git commit was performed. Physical-device performance was not measured; responsive checks used browser viewport emulation. Internal battery/brake geometry is not depicted by the photograph.
