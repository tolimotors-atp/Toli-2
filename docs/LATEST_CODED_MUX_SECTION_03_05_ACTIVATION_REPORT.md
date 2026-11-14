# Latest coded MU-X — Section 03/05 activation

Date: 2026-11-09. Project: `/home/thunder/shared/tolimotors-main1/toli-static-website`.

## Decision and exact candidate

**ACTIVATED in Sections 03 and 05 only**, following the user's explicit decision to activate despite the previous recognition failure. This is **CODED REFERENCE V04 with the completed exterior-detail addition**, not V01/V02/V03 and not a new reconstruction pass.

The candidate was selected by reviewing `tools/3d/isuzu-mux/CODED_MUX_REFERENCE_V04_DETAILS_REPORT.md`, its final snapshot, actual source and diagnostic captures. Its source is `src/components/three/mux/MuxVehicle.ts`, with `MuxReferenceData.ts`, `MuxReferencePatches.ts`, `MuxGeometry.ts`, `MuxWheels.ts` and `MuxExteriorDetails.ts`. The latest version has curved lamp apertures, revised rear surfaces, two mirrors, four door definitions, four handles and front/rear `TOLI MOTORS` plates. These geometry sources were not modified during activation.

The earlier overall same-car recognition result remains **FAIL**. User-authorized activation does not convert that result into a visual-quality PASS. This is a reference-driven coded model, not factory-CAD accuracy.

## Integration architecture

The existing `createVehicleScene` renderer and its visibility, pause, context-loss, resizing, theme subscription, reduced-motion and quality lifecycle remain in use. A small section guard selects the coded presentation only when the actual host dock is `process` or `completion`.

`src/lib/mux-presentation.ts` creates **one** canonical V04 geometry/material resource set and one presentation scene, lazily on first use. Both target sections reuse this instance and the existing canvas/WebGL renderer. There are no duplicated car implementations or extra per-section WebGL contexts. The existing Section 02 scene/GLB is retained and rendered in all other docks.

- **Section 03 / HowItWorks:** ACTIVE. Fixed front three-quarter view, camera direction `(-6, 2.7, 4.6)`. Content, layout, process steps, transitions and spacing are unchanged.
- **Section 05 / CtaBanner:** ACTIVE. Complementary rear three-quarter view, camera direction `(6, 2.7, 4.6)`. CTA text, buttons, layout, height and spacing are unchanged.
- Both cameras use 34-degree vertical FOV. Visible model vertices, including mirrors and plates, determine distance independently for each canvas aspect with an 8% fit margin. The fit is cached until mode/aspect changes. This avoids empty bounding-box corners making the SUV too small.
- The source model's Z-up axis is converted to the website's Y-up axis once. All four tires retain their existing ground contact. A lightweight procedural contact shadow sits at floor level.
- These are presentation views: the old 360-degree drag affordance is disabled only for these two docks. Their canvas cannot capture scrolling, touch or overlay input. Section 02 retains its existing rotation controls.

## Protection

**Hero: UNCHANGED. Navigation: UNCHANGED. Section 02: UNCHANGED. TOLI AI: UNCHANGED and functional.** No Hero, navbar, component-section, AI, global stylesheet, booking workflow or geometry asset file was edited.

The source/public baseline audit is saved in `docs/mux-activation/source-protection.json`: 367 existing files checked, exactly one changed source file (`src/lib/vehicle-scene.ts`), no missing files, plus the new presentation module and regression test. The 7,781-file protection manifest includes this now-authorized scene modification; it showed zero unexpected changes and zero missing files. Other protected projects/references remain unchanged. This audit is saved separately in `protected-projects.json`.

The actual Section 02 DOM retained `data-model="toli-atelier-r7"`, its original vehicle and its rotation controls. Both target docks reported `data-model="coded-mux-v04-exterior-details"`. Hero screenshots retain all three original cars, workshop background, branding, caption and corner pills.

## Feature checks and known limitations

| Feature | Result |
|---|---|
| Front plate | `TOLI MOTORS`, present, outward-facing, attached |
| Rear plate | `TOLI MOTORS`, present, outward-facing, attached |
| Side mirrors | Both present, attached; selected views expose the appropriate mirror surfaces |
| Doors | Four visual panel definitions, present |
| Handles | Four shallow 3D handles, present |
| Headlights | Latest curved outer aperture/backing geometry present |
| Rear lights | Latest recessed outer aperture/backing geometry present |
| Grounding | Original four-tire ground contact retained |

Lamp lenses, DRLs/projectors and emissive internals were not added: they were absent from this latest completed candidate. Door definitions do not imply working opening-door animations. The known body proportions, greenhouse, front fascia/headlight-fender relationship and rear-quarter shape still need reference convergence. Existing surface artifacts are visible in these unchanged geometry sources. No bronze recolor, excessive bloom or alternate generic low-quality car was introduced.

Plate letters are actual geometry, not a low-resolution texture; the existing outward-normal, fit and mount-contact assertions pass. At small mobile presentation sizes the plate text is naturally small. The full-car screenshots should not be interpreted as a guarantee that every letter is comfortably readable at phone scale.

## Browser and responsive validation

Actual browser checks passed for both sections in **both themes** at:

| Viewport | Section 03 | Section 05 |
|---|---|---|
| 320 × 568 | PASS | PASS |
| 360 × 800 | PASS | PASS |
| 390 × 844 | PASS | PASS |
| 412 × 915 | PASS | PASS |
| 768 × 1024 | PASS | PASS |
| 1366 × 768 | PASS | PASS |
| 1920 × 1080 | PASS | PASS |

All 28 final checks showed the live coded canvas, successful visible-geometry fit and no horizontal overflow. The model stays inside its existing presentation area and does not obscure text/buttons. The short 320px screen retains the existing compact dock height, so its vehicle is smaller than on taller phones. These are browser viewport checks, not physical Android hardware validation.

TOLI AI was opened on desktop and mobile. Desktop input accepted a service question and returned the expected local service-category response. A DOM hit test confirmed the dialog was above the canvas. Closing worked. Section 05's ENQUIRE NOW opened the existing four-step Service Request form and could be closed. No enquiry or external message was sent.

Production preview at `http://127.0.0.1:8207/Toli-2/` rendered both coded sections with **zero console warnings/errors observed**; the console capture is `screenshots/production-console.json`. Development preview retained existing React Router future-flag warnings, with no new errors observed.

## Performance and failure handling

The candidate remains approximately 96,194 triangles, 71,115 position entries, 86 mesh instances and seven materials. The two target presentations render 96,196 triangles/87 draw calls including their shadow plane. Only a small generated 64px contact texture is added; no model texture download, reflection pass, bloom or dynamic shadow maps were added.

Existing DPR caps and downgrade controls remain (desktop at most 1.5, tablet/low at 1). The same coded model remains active on low quality. Offscreen/obscured rendering is paused and presentation cameras remain static, respecting reduced motion. Resource disposal covers vehicle geometry/materials, contact texture and presentation scene. Existing context-loss/fallback lifecycle is preserved so section content remains available. Physical GPU loss and real-device frame rates were not tested in this activation pass.

## Technical checks

- All three TypeScript configurations: **PASS**, command chain exited 0.
- Lint: **PASS**, local ESLint exited 0 (`mux-final-lint.log`).
- Production build: **PASS**, 17.17 seconds (`mux-final-build.log`). Existing greater-than-500-kB chunk advisory remains; vehicle scene chunk is approximately 747 kB / 209 kB gzip.
- Full tests: **53 files, 368 tests PASS**, 141.11 seconds (`mux-final-tests.log`). This was rerun after final camera changes; no old test count was reused.
- New regression tests verify section routing protection, latest detail groups, shared model identity, front/rear camera directions and visible-geometry fit across all seven sizes and both themes.

## Exact screenshots

All paths below are relative to the project root:

- `docs/mux-activation/screenshots/section03-coded-mux-desktop.jpg`
- `docs/mux-activation/screenshots/section05-coded-mux-desktop.jpg`
- `docs/mux-activation/screenshots/section03-coded-mux-mobile.jpg`
- `docs/mux-activation/screenshots/section05-coded-mux-mobile.jpg`
- `docs/mux-activation/screenshots/hero-after-activation.jpg`
- `docs/mux-activation/screenshots/navbar-after-activation.jpg`
- `docs/mux-activation/screenshots/section02-after-activation.jpg`
- `docs/mux-activation/screenshots/toli-ai-after-activation.jpg`
- `docs/mux-activation/screenshots/toli-ai-mobile-after-activation.jpg`
- `docs/mux-activation/screenshots/service-request-after-activation.jpg`
- `docs/mux-activation/screenshots/production-section05.jpg`

Every size/theme has separate `section03-{width}x{height}-{dark|light}.jpg` and `section05-{width}x{height}-{dark|light}.jpg` captures. The 28 outcomes are consolidated from the browser result outputs in `responsive-results.json`. Before captures are `hero-before.jpg`, `section02-before.jpg`, `section03-before.jpg`, `section05-before.jpg`; the navbar is also visible in the before images. The early before captures use the browser's native crop; they are not pixel-registered with the full-width final captures. Source hashes are the exact protection evidence.

## Files changed

Production source: `src/lib/vehicle-scene.ts` (modified), `src/lib/mux-presentation.ts` (new).

Tests: `src/test/mux-activation.test.ts` (new).

Documentation/evidence: this report and `docs/mux-activation/` (baseline, original scene snapshot, audits, logs and screenshots). Build outputs were regenerated locally.

Development preview: `http://127.0.0.1:8190/Toli-2/` — choose 03 Journey or 05 Request.

**Protected projects: UNCHANGED. Deployment: NOT PERFORMED. Git commit: NOT PERFORMED.**
