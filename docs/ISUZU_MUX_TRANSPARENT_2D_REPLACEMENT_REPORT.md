# ISUZU MU-X transparent 2D replacement

Date: 2026-11-10  
Project: `/home/thunder/shared/tolimotors-main1/toli-static-website`  
Local preview: <http://127.0.0.1:8190/Toli-2/>

## Result

| Requirement | Result |
| --- | --- |
| Section 03 | TRANSPARENT 2D FRONT THREE-QUARTER MU-X ACTIVE |
| Section 05 | TRANSPARENT 2D REAR THREE-QUARTER MU-X ACTIVE |
| Active coded/WebGL vehicle in 03/05 | NONE |
| Section 02 | UNCHANGED |
| Hero | UNCHANGED |
| Navbar | UNCHANGED |
| TOLI AI desktop/mobile | PASS |
| Historical 3D source/diagnostics | PRESERVED |
| Deployment | NOT PERFORMED |
| Git commit | NOT PERFORMED |

The preceding task had already disconnected the coded MU-X from Sections 03/05. This update replaces the opaque studio images and white aperture with genuinely transparent vehicle artwork. It does not hide a canvas behind an image. No additional renderer deletion was needed, and no shared renderer infrastructure was removed.

## Exact supplied sources

All 43 supplied references were reviewed using the existing [reference contact sheet](mux-2d/reference-contact-sheet.jpg), followed by full-size inspection of the selected pair:

- Section 03: `Screenshot 2026-11-08 213542.png`, 1022 × 593.
- Section 05: `Screenshot 2026-11-08 213451.png`, 972 × 511.

Both originals are in `/home/thunder/shared/tolimotors-main1/Isuzu MU-X`. The matched red MU-X pair provides complete roof, mirrors, glazing, bumpers, tires and wheels with clear front/rear identity and a plain source background. It avoids mixing generations or using the lower-resolution, obstructed or viewer-UI reference images. The plate is a manufacturer ISUZU mu-X display plate, not a personal registration number; it remains unchanged.

All 43 original files retain their previous SHA-256 hashes. See [protection.json](mux-transparent/protection.json).

## Transparent assets

Final artwork uses the original source vehicle pixels, not a generated substitute. A background-extraction preview was rejected because it changed fine details; none of that candidate's artwork is used by the website.

The reproducible final method is a manually traced silhouette mask applied to the original image, followed by slight alpha-edge smoothing, proportional fitting and WebP encoding. The mask includes the dark underbody, complete tire edges, mirrors and vehicle glazing. It does not classify windows or dark car parts as background. The original studio floor, floor lettering and shadow are outside the retained silhouette. There is no opaque photograph rectangle, baked checkerboard or background panel in the asset.

Masks and generator:

- `tools/images/mux-masks/front.svg`
- `tools/images/mux-masks/rear.svg`
- `tools/images/prepare_mux_transparent.mjs`

Rebuild with `node tools/images/prepare_mux_transparent.mjs` from the project directory. This reads the originals and writes separate production copies; it never writes to the reference directory.

| Production asset in `src/assets/vehicles/isuzu-mux/` | Dimensions | Bytes |
| --- | --- | ---: |
| `isuzu-mux-front-3q-transparent-640.webp` | 640 × 384 | 40,262 |
| `isuzu-mux-front-3q-transparent.webp` | 1100 × 660 | 64,766 |
| `isuzu-mux-rear-3q-transparent-640.webp` | 640 × 384 | 38,040 |
| `isuzu-mux-rear-3q-transparent.webp` | 1100 × 660 | 60,950 |

All four variants total 204,018 bytes on disk. The selected pair is 78,302 bytes at 640 or 125,716 bytes at 1100; a browser selects the applicable variant rather than downloading every copy. Fresh production mobile checks selected the hashed 640 WebPs. PNG masters under `docs/mux-transparent/` preserve alpha for inspection and are not imported into the app.

The generator asserts RGBA output, transparent outer corners, substantial transparent area and substantial opaque vehicle area. Large front/rear WebPs contain respectively 383,100 and 367,040 fully transparent pixels. Separate opaque spot checks sampled body/glass/wheels. These numerical checks support, and do not replace, visual inspection.

See [asset metadata](mux-transparent/assets.json), [edge checks](mux-transparent/edge-checks.json), and the dark/light edge-inspection images in `docs/mux-transparent/`.

## Presentation and grounding

`MuxPhotography` remains the shared vehicle-only component for the two existing slots. It now imports only responsive transparent WebPs and renders an image with intrinsic dimensions, `srcset`, responsive `sizes`, lazy loading, asynchronous decoding and useful front/rear MU-X alt text. It does not describe the image as 3D.

The white picture surface, border radius, frame and frame shadow have been removed. Its replacement is a transparent figure with a restrained CSS elliptical tire-contact shadow and a small silhouette drop shadow. The car itself is not transformed, recolored, perspective-warped or animated as if it had unseen views. The same transparent artwork works against both themes. No heavy library or continuously running effect was added.

All existing headings, text, buttons, section dimensions, spacing rules and captions remain. Only the vehicle component/style and its directly affected test changed. The transparent car occupies more of the existing slot than the padded studio photograph, without changing the parent section layout. `object-fit: contain` retains the complete silhouette.

## 3D removal and Section 02 protection

Sections 03/05 contain zero canvas or `data-scene-dock` elements. Both remain images when GPU state is ready or fallback. The existing production scene still has no import/allocation of `createMuxPresentation`; historical V02/V03/V04/V05 work remains inactive and was not deleted.

Section 02 still runs its existing renderer. Browser inspection confirmed model marker `toli-atelier-r7`, rotation readiness, 318 draw calls and 68,032 triangles. There are no `MuxPhotography` images in Section 02. Its source, vehicle assets and shared runtime were not edited in this task.

No FPS or battery improvement percentage is claimed. The measurable distinction remains zero vehicle WebGL work in the two photo sections, with responsive lazy image loading instead. The existing shared scene chunk remains approximately 649.90 kB and retains the existing build size advisory because Section 02 still needs it.

## Responsive and visual verification

Both sections were checked in dark and light themes at:

- 320 × 568
- 360 × 800
- 390 × 844
- 412 × 915
- 768 × 1024
- 1366 × 768
- 1920 × 1080

All 28 recorded cases loaded the correct view, used contain sizing, retained transparent container backgrounds, and had no horizontal overflow, vehicle-slot control overlap or photo-section WebGL elements. Complete mirrors, roof and tires remain visible. The original windows, headlamps and rear lamps are retained. Dark/light edge previews were inspected at larger than display size; the traced contours were corrected around tires, bumper and roof before the final export.

Screenshot review found stale captures from an intermediate mask export and scroll-position captures taken during an existing section transition. Those captures were replaced after final export. At 1920, normal chapter entry was used so the next sticky panel did not obscure Section 03. At 390, viewport captures and independent production rear-image evidence were used to avoid stale document-coordinate capture offsets. This required no page-layout change. Some screenshots show neighboring section content outside the vehicle area as part of the existing scroll composition.

Screenshot evidence:

- [Section 03 desktop](mux-transparent/screenshots/section03-2d-mux-desktop.jpg)
- [Section 05 desktop](mux-transparent/screenshots/section05-2d-mux-desktop.jpg)
- [Section 03 mobile](mux-transparent/screenshots/section03-2d-mux-mobile.jpg)
- [Section 05 mobile](mux-transparent/screenshots/section05-2d-mux-mobile.jpg)
- [Both desktop presentations](mux-transparent/screenshots/both-transparent-sections.jpg)
- [Responsive overview](mux-transparent/screenshots/responsive-overview.jpg)
- [Hero regression](mux-transparent/screenshots/hero-regression.jpg)
- [Navbar regression](mux-transparent/screenshots/navbar-regression.jpg)
- [Section 02 regression](mux-transparent/screenshots/section02-regression.jpg)
- [TOLI AI desktop](mux-transparent/screenshots/toli-ai-desktop.jpg)
- [TOLI AI mobile](mux-transparent/screenshots/toli-ai-mobile.jpg)

## Functional and source regression

TOLI AI accepted a local service question and returned the service-category response. Its desktop and mobile dialogs opened and closed normally. The source and behavior were not changed. Booking/enquiry code, gallery, Hero, navigation, theme system, Titanium Bronze styling and all historical 3D source remain unchanged.

A baseline comparison checked 386 existing source/public files. Exactly three changed:

1. `src/components/journey/MuxPhotography.tsx`
2. `src/components/journey/mux-photography.css`
3. `src/test/mux-photography.test.tsx`

There were no protected-file changes or original-reference changes. Four new WebP assets were added. No independent 3D showroom or original-project files were modified.

## Technical validation

| Check | Actual result |
| --- | --- |
| TypeScript app/node/qa | PASS |
| Final lint | PASS |
| Final production build | PASS, 7.08 seconds |
| Full test suite | PASS, 55 files / 374 tests |
| Asset generator alpha assertions | PASS |
| Opaque glass/body/wheel spot checks | PASS |
| Production front/rear image loading | PASS, hashed 640 WebPs on mobile |
| Production console warnings/errors | 0 / 0 |
| Screenshot decoding | PASS |
| Original reference protection | 43 unchanged |

The image test now requires transparent WebP sources and responsive sizes instead of obsolete AVIF/source markup. It still verifies both front/rear views, GPU-ready/fallback behavior, absence of canvas infrastructure and Section 02 separation.

Logs are under `docs/mux-transparent/validation-*.log`. Browser results, production checks and capture corrections are under `docs/mux-transparent/screenshots/`. `validation.json` and `protection.json` record the final results. Source was saved on disk and the local development and production previews were checked; no temporary browser styling is used.

## Files added

- Four WebPs listed above.
- `tools/images/prepare_mux_transparent.mjs`
- Two SVG alpha masks under `tools/images/mux-masks/`
- This report.
- PNG masters, edge previews, logs, metadata and screenshots under `docs/mux-transparent/`.

The previous opaque imagery and historical source remain available for rollback, but are no longer imported by these two slots. No deployment or Git commit was performed. Physical-device performance was not measured; responsive QA used browser viewport emulation. The source photographs set the maximum available detail—this change does not invent additional resolution or unseen vehicle geometry.
