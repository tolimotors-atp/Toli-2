# V04 exterior-detail addition

## Release decision

**Overall same-car recognition: FAIL / Decision C. Integration: DEFERRED.** This remains isolated V04, not V05. The primary body, headlight/fender transition, rear-quarter/D-pillar and bumper wrap still fail reference convergence. The underlying-body and badgeless renders were reviewed; details cannot override that result. Current Section 03/05 cars remain active. No deployment or commit.

## Construction and reference evidence

Original controlled studio photographs remain the authority. No incompatible model-year features, external vehicle assets or AI-generated accessories were used. Reference crops and observations are recorded in `code-reference-car/reference-data/v04/exterior-details/reference-audit.json` and `feature-observations.json`. Sources include 18-17-10 front, 18-17-14 side, 18-17-18 rear, 18-17-27 front-quarter and 18-17-31 rear-quarter screenshots. Mirror depth and mounts are estimated from partly occluded views. Cost: zero.

- Mirrors: curved volumetric upper/lower shells, base, stalk and separate glass. Approximate authored housing 240 × 150 × 190 mm. Front-quarter, side and rear-quarter comparison saved. Housing is still too rounded and needs more accurate mounting relationships. No indicator strip was invented where chrome/reflection is ambiguous.
- Doors: four closed rounded surface-following ribbons, 3 mm wide and approximately 2.5 mm offset. They evaluate the existing body and greenhouse surface, without trenches, holes or detached panels. These are visual panel definitions, not opening doors. Exact boundaries remain dependent on correcting the body.
- Handles: four shallow tapered swept 3D forms, approximately 200 mm long with 20 mm bridge projection. Side-reference placement is used; scale and relationship still need visual convergence.
- Plates: front/rear 460 × 115 × 6 mm physical backings, two mounting standoffs each, shared bundled 3D font geometry and exact text **TOLI MOTORS**. Text is centred, readable, outward-facing and fits its backing. Mounts intersect the measured body surface rather than floating. No registration from a photograph is copied.
- Lamps: explicit outer control points use restrained rounded-corner interpolation instead of over-rounded closed Catmull contours. Backings are recessed about 3 mm into the front/rear body faces. Outer shape and integration remain unapproved. Lenses, DRLs, projectors and emission are deferred until those gates pass.

## Individual visual gates

| Feature | Result | Next correction |
|---|---|---|
| Side mirrors | NEEDS WORK | Housing curvature and A-pillar mounting relationship. |
| Headlight shape | NEEDS WORK | Original envelope and grille relationship. |
| Headlight/fender integration | FAIL | Bonnet/grille/fender/fascia transition. |
| Rear-light shape | NEEDS WORK | Inner termination and side wrap. |
| Rear-light body integration | NEEDS WORK | Rear-quarter/tailgate surface flow. |
| Doors | NEEDS WORK | Exact boundaries after body correction. |
| Door handles | NEEDS WORK | Scale/placement convergence. |
| Front TOLI MOTORS plate | PASS | Readable, outward-facing, physically mounted. |
| Rear TOLI MOTORS plate | PASS | Readable, outward-facing, physically mounted. |

The main body must be corrected before further lamp internals or website activation.

## Diagnostics and measured geometry

All six development toggles were checked in the browser. All features enabled: 87 draw calls including floor. Disabling mirrors: 77; headlights: 85; rear lights: 85; door cuts: 83; handles: 83; plates: 79. Restoring each returns to 87. Local-patch visibility preserves an unchecked headlight state.

Default camera settings remain unchanged at zoom 1.0. Closeups use zoom 0.65, front plate/full rear 0.90; these do not change default FOV. Captures are visual evidence, not pixel-registered reconstruction measurements.

- 96,194 triangles; 71,115 position entries; 86 mesh instances; 7 materials; 0 textures.
- Body envelope: 4.82428 × 1.86000 × 1.86000 m.
- Full envelope including mirrors/plates: 4.83853 × 2.20000 × 1.86000 m. Body and accessory bounds are reported separately.
- Wheelbase 2.845 m; tire diameter 0.764 m; grounding error below 1 nanometre.
- Zero invalid coordinates or degenerate triangles; primary symmetry passes and paired-mirror assertions cover the additions.
- Deterministic repeated hash: `e1ccd147ae26046e791722282d8f51bfdcb524edd0ec19d8f041771e2a9e4fa5`.
- No Blender/GLB export or activation was required for this code-authored candidate.

## Validation and protection

Production build PASS; isolated diagnostic build PASS; TypeScript PASS; lint PASS. Full suite: **52 files / 366 tests PASS**. Final focused geometry rerun: **8 tests PASS**, adding text-fit, outward normals, body-contact mounts, mirror symmetry and surface-following door checks. Full suite preceded the final additional plate assertions; focused tests, types and lint ran afterward. Existing build advisory: chunks greater than 500 kB.

Final isolated browser console: no warnings/errors observed. Live Hero heading and TOLI AI opening, Services response, modal layering and closing were checked. Physical-device performance was not checked in this pass.

Protection audit: **7,781 protected files, zero changed/missing; 43 reference files, zero changed**. Source baseline: 377 files, five modified plus one new source module. Hero, navbar, TOLI AI, Section 02 and protected projects remain unchanged. Historical candidate reports and milestones are preserved.

## Changed files and saved milestones

Source: `src/components/three/mux/MuxExteriorDetails.ts` (new), `MuxVehicle.ts`, `MuxReferencePatches.ts`, `MuxValidation.ts`, `validation.ts`, and `src/test/mux-coded-reference.test.ts`.

Diagnostic wiring: `code-reference-car/reference-v04.html`, isolated `vite.config.mjs`, and `comparisons/v04-pre-details.html`. Reference observations, reports, screenshots, logs and snapshots are tooling artifacts.

Snapshots: `code-reference-car/source-snapshots/reference-v04/pre-exterior-details/` and `exterior-details/`. Final hashes were verified against current disk files. Data, logs, toggle checks and evidence assembler: `code-reference-car/analysis/reference-v04-details/` (raw browser checks also in render `raw/`).

## Evidence

All render paths below are relative to `code-reference-car/renders/reference-v04/exterior-details/`:

- `details-summary.jpg`, `details-five-view.jpg`, `badgeless-five-view.jpg`, `underlying-body-comparison.jpg`.
- `feature-scale-validation.jpg`: front-quarter, side and rear-quarter feature checks.
- `mirror-reference-comparison.jpg`, `doors-reference-comparison.jpg`, `lamp-reference-comparison.jpg`, `details-reflection.jpg`.
- Required closeups: `front-headlight-reference-closeup.jpg`, `front-headlight-coded-closeup.jpg`, `mirror-reference-comparison.jpg`, `door-handle-side-closeup.jpg`, `door-cuts-side-closeup.jpg`, `rear-light-reference-closeup.jpg`, `rear-light-coded-closeup.jpg`, `rear-number-plate-closeup.jpg`, `front-number-plate-closeup.jpg`, `rear-full-detail.jpg`. All ten files were decoded and verified.

Preview: http://127.0.0.1:8190/Toli-2/tools/3d/isuzu-mux/code-reference-car/reference-v04.html

Previous candidate comparison: http://127.0.0.1:8190/Toli-2/tools/3d/isuzu-mux/code-reference-car/comparisons/v04-pre-details.html
