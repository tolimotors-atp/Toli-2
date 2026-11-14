# ISUZU MU-X 2D production replacement

Date: 2026-11-10
Project: `/home/thunder/shared/tolimotors-main1/toli-static-website`
Preview: <http://127.0.0.1:8190/Toli-2/>

## Result

Sections 03 and 05 now display the actual supplied MU-X imagery instead of the coded V04/V05 approximation. Section 03 uses a front three-quarter view; Section 05 uses a rear three-quarter view. Both are normal responsive images, not canvases or simulated rotating vehicles. V04/V05 source remains intact and inactive for rollback.

| Required result | Status |
| --- | --- |
| Section 03 supplied MU-X visual active | PASS |
| Section 05 supplied MU-X visual active | PASS |
| Coded 3D runtime removed from 03/05 | PASS |
| V04/V05 work preserved | PASS |
| Hero | UNCHANGED |
| Navbar | UNCHANGED |
| Section 02 presentation | UNCHANGED |
| TOLI AI | PASS |
| Responsive framing, both themes | PASS |
| Deployment | NOT PERFORMED |
| Git commit | NOT PERFORMED |

## Reference selection

All 43 images in `/home/thunder/shared/tolimotors-main1/Isuzu MU-X` were inspected in the contact sheet, followed by full-size inspection of the selected pair. See [reference contact sheet](mux-2d/reference-contact-sheet.jpg) and [inventory](mux-2d/reference-inventory.json).

- Front: `Screenshot 2026-11-08 213542.png`, 1022 × 593. It clearly shows the complete grille, lamps, bonnet, mirrors, doors, roof and wheels in a clean front three-quarter composition.
- Rear: `Screenshot 2026-11-08 213451.png`, 972 × 511. It clearly shows the complete rear glass, tailgate, lamps, bumper, side body and wheels.

This matched red catalogue/studio pair has clean surroundings, consistent vehicle identity and no viewer controls over the vehicle. It avoids combining incompatible model generations. These are supplied vehicle images, not photographs of the TOLI workshop. The manufacturer display plates read ISUZU mu-X, not a personal registration number, so no plate replacement was necessary.

The source files are unchanged. No AI replacement, downloaded substitute, recoloring, badge invention, geometry alteration or destructive background removal was used.

## Production assets and presentation

Production copies live in `src/assets/vehicles/isuzu-mux/`. Each view has AVIF and WebP at 640 × 384 and 1100 × 660. `tools/images/prepare_mux_assets.py` reproduces them from the supplied originals.

Processing is limited to proportional fitting, safe white studio padding, resizing and encoding. Source pixels are not upscaled before padding. The complete original vehicle, natural floor/contact shadow and surrounding studio photograph are retained. The image is displayed with `object-fit: contain` inside a curved studio aperture with a restrained depth shadow. The safe padding keeps the curved perimeter away from the vehicle. No false view rotation, parallax distortion or continuous animation was added.

The shared `MuxPhotography` component supplies useful view-specific alt text, intrinsic dimensions, lazy loading, asynchronous decoding, AVIF sources and WebP fallback. Neither section depends on the raw reference folder at runtime.

| Asset | AVIF bytes | WebP bytes |
| --- | ---: | ---: |
| Front 640 | 18,591 | 25,912 |
| Front 1100 | 36,932 | 50,706 |
| Rear 640 | 18,325 | 24,324 |
| Rear 1100 | 36,082 | 47,652 |

All eight files total 258,524 bytes on disk. A browser chooses one format and size per view; it does not download all variants. The two AVIF views total 36,916 bytes at 640 or 73,014 bytes at 1100. Exact source hashes, processing and dimensions are recorded in [assets.json](mux-2d/assets.json).

## Runtime changes

`JourneyDock` renders photographs for process/completion modes before any GPU-loading/fallback presentation. There are no `data-scene-dock` markers, WebGL elements, SVG substitute cars or loading statuses in those modes, even when GPU support is unavailable.

The production scene no longer imports or allocates the coded MU-X presentation. Its model, camera, lighting, frame updates and disposal branch are no longer in the active production scene bundle. `JourneyProvider` no longer maintains the process-only camera-step override. Process step selection and descriptions remain functional independently of a canvas. The shared renderer pauses when the photo-only chapters are active.

Infrastructure needed by Section 02 remains. Browser inspection confirmed its original `toli-atelier-r7` renderer, rotation support, 318 draws and 68,032 triangles; the photo count there is zero. Model-helper source and 14 coded-model source files remain unchanged for rollback.

The vehicle-scene production chunk decreased from approximately 747.33 kB to 649.90 kB (208.63 kB to 172.74 kB gzip). This is about 97.43 kB raw / 35.89 kB gzip less scene JavaScript. Lazy image downloads are additional, so this is not a claim that total transferred bytes always decrease. Section 03/05 require zero vehicle WebGL canvases or draw work. Physical-device FPS, battery and memory were not measured. The existing build advisory for a chunk over 500 kB remains.

## Responsive and visual verification

Both sections were checked at all seven requested sizes in dark and light themes: 320 × 568, 360 × 800, 390 × 844, 412 × 915, 768 × 1024, 1366 × 768 and 1920 × 1080. All 28 cases loaded the selected image, retained complete vehicle framing, used contain sizing, had no horizontal overflow and had no photo-section canvas/scene dock.

Final visual review caught an initial 1920 × 1080 Section 03 capture scrolled into the next sticky-panel transition. This was a capture-position error. Rechecking with normal 03 Journey navigation showed the full vehicle unobscured in both themes; the next panel began below the image. No section-stack source or layout was changed. Corrected screenshots and [tall-desktop evidence](mux-2d/screenshots/tall-desktop-correction.json) are saved separately from the original automated DOM measurements.

Mobile prioritizes a complete vehicle and preserves the existing vertically arranged content. Desktop keeps the existing text/image columns. The studio surface and shadow provide separation in both themes without changing vehicle color. Existing page/section transitions and captions remain.

Evidence:

- [Section 03 desktop](mux-2d/screenshots/section03-isuzu-mux-desktop.jpg)
- [Section 05 desktop](mux-2d/screenshots/section05-isuzu-mux-desktop.jpg)
- [Section 03 mobile](mux-2d/screenshots/section03-isuzu-mux-mobile.jpg)
- [Section 05 mobile](mux-2d/screenshots/section05-isuzu-mux-mobile.jpg)
- [Both sections](mux-2d/screenshots/both-sections-isuzu-mux.jpg)
- [Responsive overview](mux-2d/screenshots/responsive-overview.jpg)
- [Hero](mux-2d/screenshots/hero-unchanged.jpg)
- [Navbar](mux-2d/screenshots/navbar-unchanged.jpg)
- [Section 02](mux-2d/screenshots/section02-unchanged.jpg)
- [TOLI AI desktop](mux-2d/screenshots/toli-ai-unchanged.jpg)
- [TOLI AI mobile](mux-2d/screenshots/toli-ai-mobile-unchanged.jpg)
- [Canonical request form](mux-2d/screenshots/service-request-preserved.jpg)

## Regression and technical checks

Hero, navbar, TOLI AI and existing style/asset sources were not edited. A final hash comparison of 375 existing source/public files found only the eight authorized source/test/fixture changes listed below. All 43 original references remain unchanged. Independent 3D/original projects were not modified.

Browser regression confirmed the original Section 02 vehicle, TOLI AI response to a local service question, AI overlay above the imagery, mobile AI opening/closing, Section 05 Enquire Now and header Book Service opening the canonical request dialog. No customer enquiry was submitted.

| Check | Actual result |
| --- | --- |
| TypeScript app/node/qa | PASS, exit 0 |
| Lint | PASS, exit 0 |
| Production build | PASS, 13.47 seconds |
| Full automated tests | PASS, 55 files / 374 tests |
| Production preview image loads | PASS, hashed AVIF assets |
| Production console warnings/errors | 0 / 0 |
| Responsive cases | 28, both themes; corrected tall-desktop visual evidence retained |
| Encoded asset/screenshot decoding | PASS |

Tests intentionally requiring the old process/completion renderer were changed to require image presentation and independent process UI. The archived V04 test now describes inactive rollback work. The separation fixture updates only JourneyDock/JourneyProvider hashes; protection assertions for other files remain. New photography tests cover both GPU states, front/rear views, responsive picture markup and Section 02 separation.

Scoped browser QA was used for this change. No unrelated whole-site redesign or whole-site design-kit gate is claimed. Logs and machine-readable evidence are in [mux-2d](mux-2d/), including validation-results.json, source-protection.json, bundle-check.json and screenshots/production-check.json.

## Changed files

Existing production files:

- `src/components/journey/JourneyDock.tsx`
- `src/components/journey/JourneyProvider.tsx`
- `src/lib/vehicle-scene.ts`

New production files:

- `src/components/journey/MuxPhotography.tsx`
- `src/components/journey/mux-photography.css`
- Eight optimized image files under `src/assets/vehicles/isuzu-mux/`

Tests/fixtures:

- `src/test/mux-photography.test.tsx` (new)
- `src/test/phase2-services.test.tsx`
- `src/test/experience.test.tsx`
- `src/test/default-selections.test.tsx`
- `src/test/mux-activation.test.ts`
- `src/test/fixtures/separation-protected.json`

Supporting files:

- `tools/images/prepare_mux_assets.py`
- This report
- Evidence, logs, screenshots and audit metadata under `docs/mux-2d/`

No deployment or Git commit was performed. Physical Android/device performance was not measured; responsive checks used browser viewport emulation. The WebP fallback is covered by markup tests and asset decoding; this browser selected AVIF.
