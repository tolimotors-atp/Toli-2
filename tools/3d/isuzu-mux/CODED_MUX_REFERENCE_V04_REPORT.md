# MU-X CODED REFERENCE V04

2026-11-09. Fresh reference traces → new local patches → fixed-camera validation. Continued the existing code/render architecture.

## Final decision

**C — REFERENCE-DRIVEN PATCH RECONSTRUCTION STILL CANNOT REPRODUCE THE CAR.**

Same-car resemblance **FAIL**. Clay recognition **FAIL**. Badgeless recognition **FAIL**. **V04 NOT ACTIVATED.** Existing production cars remain active in Sections 03 and 05; Section02 unchanged. Hero, navigation, TOLI AI and protected projects unchanged. **Stop here; no V05 created or started automatically.**

The new apertures are integrated more directly into the body than V03's separate lamp shells, and the worst internal tessellation cracks were reduced. However, the resulting grille/headlight/front corner shapes still do not match the MU-X. The quarter and rear remain generic. These are not merely remaining trim issues, so Decision B is not justified.

## Original images re-inspected

All **43 readable original image files / 39 distinct visual references** were re-inspected from `/home/thunder/shared/tolimotors-main1/Isuzu MU-X`. Fresh contact sheets were generated from the originals, then full-resolution front, both front quarters, side, rear and both rear quarters were inspected again. No V03 surface was treated as a shape reference.

Inventory with SHA256 and image dimensions: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/reference-data/v04/original-image-manifest.json`. All 43 originals are unchanged. Silver-family views are primary; compatible red views are supporting contour/wrap evidence only. No different-generation grille/rear shape or colour-based averaging.

| Region | Primary original filename | Supporting evidence |
|---|---|---|
| Direct front | `Screenshot From 2026-11-06 18-17-10.png` | `Screenshot From 2026-11-06 18-08-46.png`, silver AVIF |
| Front-left quarter | `Screenshot From 2026-11-06 18-17-27.png` | `Screenshot 2026-11-08 213411.png`, `213436.png` |
| Opposite front quarter | `Screenshot From 2026-11-06 18-17-25.png` | Compatible front intermediate views |
| Side / greenhouse | `Screenshot From 2026-11-06 18-17-14.png` | `Screenshot From 2026-11-06 18-17-21.png` |
| Direct rear | `Screenshot From 2026-11-06 18-17-18.png` | Silver rear quarters |
| Rear-left quarter | `Screenshot From 2026-11-06 18-17-31.png` | `Screenshot 2026-11-08 213459.png` |
| Opposite rear quarter | `Screenshot From 2026-11-06 18-17-35.png` | `Screenshot 2026-11-08 213502.png` |
| Bonnet / lamp / fender detail | `20250902050117_Isuzu_mu-X_Silver_Metallic[1].avif` | Front/quarter pair above |

Absolute source filenames are recorded in `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/reference-data/v04/reference-locks.json` and `image-traces.json`.

## Fresh traces and cross-view reconciliation

**Checkpoint 1 was saved before major geometry changes.** Dataset: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/reference-data/v04`.

`image-traces.json` contains new manual pixel-space design polylines for bonnet leading/centre/side edges, grille, headlight boundaries, bumper, openings, arches, fender crown, shoulder, windscreen, roof/windows/quarter glass, D-pillar, rear glass, lamp wrap, hatch and lower rear. Original image sizes are stored. Opposite-front windscreen/lamp and opposite-rear pillar/lamp picks were corrected after the initial trace boards exposed misplaced picks.

`cross-view-landmarks.json` contains **12 shared semantic constraints**, with corresponding observations across front/quarter, side/quarter and rear/quarter views. The one 3D model uses the same points in every camera. Priorities: front image constrains lateral outline, side constrains longitudinal placement, quarters constrain ordering of depths. In particular, outer headlight is rearward of its grille junction; rear lamp outer return lies forward of the hatch-facing section; quarter/D-pillar borders meet one rear shell.

This is **manual semantic reconciliation and authored depth estimation**, not a calibrated multi-view solve or optimized photo reprojection fit. Source perspective, cropping and camera height remain uncertain. Different views were not averaged into independent per-camera meshes. Exact depth/tangent recovery was not achieved.

## Preserved regions and historical candidates

- Nominal dimensions, wheelbase/track/centres, tyre/wheel geometry, forward cowl and forward roof retained.
- Central body skin is retained between X=-1 and X=1. Forward cabin is clipped at X=1.30; the retained vertices use the original surface rather than a globally rescaled body.
- Stable material/renderer, camera definitions and diagnostic infrastructure retained. No new dependency, external asset, Blender generator, photogrammetry or AI3D.
- V02 and V03 remain frozen in `source-snapshots/identity-v02/final/` and `source-snapshots/identity-v03/final/`. Checksums match their saved pre-edit source baselines. Their reports and original model source remain preserved. V03 diagnostic entry was redirected to its frozen source so it does not silently show V04.
- New final source checkpoint: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/source-snapshots/reference-v04/checkpoint-06/`. Earlier checkpoint source/measurement files remain saved.

## V03 local shapes discarded from the active V04 model

Active V04 does **not** call V03's headlight lens/housing/reflector system, rear lamp shells, rear face/corner-depth blend, rear quarter skin or rear glass/D-pillar assembly. Those functions remain available in frozen history and retained legacy utilities, but do not drive V04's new local regions.

New local module: `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxReferencePatches.ts`. Its `design` arrays are also serialized in `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/reference-v04/candidate-controls.json` under `v04Design`.

### New front construction

- A new closed Y/Z aperture contour follows the freshly traced upper trajectory, outer tip/return, lower trajectory and inner return. The same contour is mapped into the new three-dimensional front body surface; it is not a uniformly extruded flat lamp.
- New front body depth uses section rows and an elliptical corner return between the centre/front and side-edge X=-2.12. Aperture depth changes across its width because it lies in that same shell.
- New fascia is triangulated with actual aperture holes. Recessed dark backing is 3mm inside the body map. No V03 protruding housing or projector remains.
- New bonnet/fender patch network shares the bonnet-side, front upper surround and side-skin boundaries. Grille openings are holes/backing in the same shell. Leading bonnet/fender/front-face positions are sampled from shared functions.
- **Failure:** the ellipse-based corner volume and smoothed aperture boundaries remain too rounded and generic. The grille openings read as soft ovals rather than the source design. Sharing an edge did not establish the correct MU-X normal/tangent field.

### New D-pillar / rear-glass group

Forward cabin is preserved, while a new side-frame patch owns the quarter-glass aperture and rear border. A new rear-frame patch owns the glass opening and meets the body at Z=1.30 and the retained rear roof at its trailing edge. A shared rear-edge curve ties the side frame and rear frame together. Glass holes use fresh rounded/tapered contours rather than V03's separate screen.

**Failure:** quarter glass and pillar remain too generic, and roof/glass/pillar highlight flow is not convincingly the reference. Position agreement alone is insufficient.

### New rear-quarter group

Separate local X sections span rear door termination, axle/arch, lamp approach and corner. Independent vertical bands control lower body, crown, shoulder and belt. The physical rear axle remains X=1.475 with .437m arch radius. A new arch-depth return uses the new side skin rather than V03's mismatched return.

**Failure:** the rear wheel still lacks the correct reference surrounding crown/shoulder mass, and the quarter tapers incorrectly toward the lamp region.

### New tail-lamp / tailgate group

A new closed tail-lamp contour is cut into the new rear body surface first. Its recessed backing shares that shell map, eliminating the independently protruding V03 lamp. New tailgate depth is controlled by vertical sections rather than the old superposed corner/recess deformations.

**Failure:** the aperture outline, quarter relationship and broad hatch form still do not match the reference. No lens/signature/emissive detail was added to hide this.

### New bumper group

Body rows control upper transition, face and lower return; centre, intermediate and elliptical corner sections meet the side edge X=2.12. At checkpoint5 the final bumper profile restores the locked nominal vehicle length. No generic bevel, diffuser or decorative trim was added.

**Failure:** broad centre/side depth and curvature remain too generic, with remaining visible seam/reflection problems. The rounded return does not reproduce the MU-X's structured bumper form.

## Checkpoints and corrections

| Checkpoint | Actual result | Evidence / correction |
|---|---|---|
| 1 | TRACES SAVED | All original files re-read. New primary front/side/rear pixel traces and 12 shared semantic landmarks; opposite-view picks corrected after full-resolution review. No geometry changed. |
| 2 | OUTER IDENTITY FAIL | New headlight/body aperture and front-fender patches replace V03. Shared end-profile and explicit mirrored tessellation corrections made. Geometry tests pass, but front mass/apertures do not look like source. |
| 3 | LOCAL CONSTRUCTION IMPROVED; IDENTITY FAIL | New quarter/D-pillar/glass shell, clipped forward cabin retained. Repeated section allocation caused initial 15s test timeout; precomputed join sections and reusable width evaluations fixed it, without raising timeout. |
| 4 | INCOMPLETE BUMPER / BOUNDS FAIL | V03 protruding lamp shells and rear face removed; body apertures/tailgate added. Temporary rear base profile made length 4.792486 m: existing bounds check correctly failed by 32.5mm. This stage was not accepted as complete. |
| 5 | BOUNDS RESTORED; VISUAL FAIL | Final section-defined bumper restores nominal length. Front/rear crack artifacts and patch-normal issues remained visible. No gate relaxation or activation. |
| 6 | TECHNICAL PASS; IDENTITY FAIL | Winding aligned with normals; nonconforming adaptive tessellation replaced by two consistent levels; simple aperture backings use one level. Shared arch return and sampled patch joins tested. Major cracks reduced; shape and reflection seams still fail recognition. |

The checkpoint5 write initially failed because automatic approval review hit a usage limit; **that command did not execute**. After the user's continuation, source was checked and the same authorized action was retried successfully. It was not bypassed.

The front outer gate never passed. Phases7/8 (headlight internals, lens/DRL/projector detail, rear lamp signatures and emission) were therefore **deferred**. Local patch-only clay captures were also recorded for inspection independently of the retained central body. They are final diagnostic inspections, not a claim that every earlier join had already passed.

## Patch continuity and topology limits

Final sampled positional gap: **0.000000130 m**. Maximum sampled undirected corner tangent angle: **0.139677°**. Scope: front/rear side terminals, front-fender leading boundary, rear frame/body boundary. These numbers describe internal consistency of authored functions, **not photo/CAD accuracy**.

Initial per-triangle adaptive subdivision created T-junction cracks on curved surfaces. Final body maps use two consistent refinement levels; small recessed backings use one. Winding and supplied normals now agree; duplicate entries were indexed. Major cracks reduced in the rendered review. Remaining seams/reflection errors are visible and fail the visual gate. No global watertightness or C1/C2 certification is claimed. The sampled join test cannot override those visible defects.

Actual ray tests confirm the new headlight and tail-lamp backing are visible through their apertures in the quarter views; the test excludes hidden guide lines. It does not prove the correct reference contour.

## Fixed-camera comparisons and overlays

The five **primary** final V02/V03/V04 comparison captures all use a **964×520 canvas**, unchanged 34° FOV, the original direction vectors, target `(0,0,.95)` and original nominal-box framing code. No per-view mesh deformation, FOV/yaw fitting or image distortion. Frozen candidates are re-rendered through equal-size comparison entries; their geometry is not modified.

Seven required directions were captured, including opposite front/rear quarters. Capture tooling produced inconsistent supplementary viewport metadata on a few auxiliary/checkpoint frames. Those supplementary images are used **qualitatively only**, not as registered numerical overlays. Primary five-view dimensions were explicitly checked. Checkpoint2's first front capture also has a differing recorded canvas size; its historical contact sheet is not used to claim pixel-matched improvement. Actual metadata is saved with each capture rather than hidden.

Primary silhouette outlines come from actual black-silhouette renders. Internal outlines are projections of actual V04 aperture surfaces and shared 3D landmarks. The numerical projection is independently checked against the recorded wheel pixels for the **five primary views** (<1e-6px difference). Approximate photo registration uses only the unchanged wheel-anchored uniform scale plus translation; no rotation, anisotropic stretch or per-part fitting.

No overlap percentage or reference accuracy score is asserted. Files: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/reference-v04/curve-projections.json`, `project-curves.mjs`, `overlay-registration.json`. Source observations are in `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/reference-data/v04/cross-view-landmarks.json`.

## V02 / V03 / V04 assessment

| View/region | V04 assessment |
|---|---|
| Front | **WORSE / FAIL identity**: too rounded fascia/opening design, wrong bonnet/headlight/arch mass |
| Front quarter | **FAIL**: cleaner aperture construction than V03, but local/body normal field still does not read as the same car |
| Side | **SIMILAR generic proportions**: stable wheels/central cabin retained; front/rear volume still wrong |
| D-pillar / quarter glass | **FAIL**: new shared frame, insufficient reference shape convergence |
| Rear quarter | **FAIL**: reduced protruding lamp construction, but wheel surround and shoulder/taper still wrong |
| Rear | **FAIL**: smoother than swollen V03 regions in places, but broad hatch/bumper identity not achieved |
| Tail-lamp integration | **NEEDS WORK / FAIL**: placed in body aperture, contour/depth relationship not reference-correct |
| Bumper wrap | **FAIL**: mathematical shared corner does not establish the source curvature |
| Clay / badgeless recognition | **FAIL / FAIL** |
| Reflection / strip flow | **FAIL**: broad curvature and seam errors remain |

This is not Decision B: the errors remain primary body volumes, not a short list of finishing details.

## Precisely unresolved shape/depth relationships

1. Transverse bonnet crown, shoulder of the front fender and outer-lamp normal field; the current smooth return does not create the source's raised arch mass and controlled leading roll.
2. Relative grille, lamp and bumper planes. The new rounded contour interpolation lost the source's more defined boundaries and depth changes.
3. Rear-axle crown versus door-side volume and upper-quarter taper. The side silhouette does not constrain the required transverse bulge reliably enough in this authored model.
4. Quarter-glass rear termination, D-pillar twist and rear-glass rake as one coherent normal field.
5. Tail-lamp outer wrap versus hatch-facing inset, and tailgate shoulder/corner depths.
6. Upper bumper step, face crown and side return curvature without the remaining seam and over-rounding.

The uncalibrated photos leave exact depth uncertain, but this result is also a limitation of the authored interpretation. It is **not** evidence that a better reconstruction from these images is impossible. Stop this V04 attempt; do not automatically create V05 or add cosmetic detail.

## Geometry and performance

| Metric | Final V04 |
|---|---|
| Vertex entries | **64,692**, mesh-instance entries, not globally unique welded vertices |
| Vehicle triangles | **98,404**, V03 92,007; existing <100,000 gate retained |
| Mesh instances / draw calls | **60 vehicle**, **61 diagnostic including floor**, debug off |
| Materials / textures | **5 / 0** |
| Invalid coordinates / degenerate triangles | **0 / 0** |
| Primary-surface unpaired mirrored vertices | **0**, 1e-5m tolerance; wheel spoke pattern excluded |
| Measured coded bounds | **4.824951 × 1.860000 × 1.860000 m** |
| Nominal authored bounds | **4.825 × 1.860 × 1.860 m**, unchanged |
| Wheelbase / tyre diameter | **2.845 / .764 m**, unchanged |
| Ground contact | ground Z ~7.2e-10m, floating-point zero |

Two independent regenerations match SHA256 `cb6a3aee4c4520a03c7e839cdc33ebc3be22da38c918ff25332b86a33ebf7091`. Efficient indexing and reduced backing tessellation kept the conforming mesh inside the budget. No higher polygon-count target was used to claim quality. No GLB export is part of this coded task.

## Technical validation — actual results

| Check | Result |
|---|---|
| TypeScript app/node/QA projects | PASS; a duplicate checkpoint field in test metadata was detected and removed before final pass |
| Lint | PASS |
| Production build | PASS |
| Diagnostic build | PASS, including historical comparison entries |
| Tests | **52 files / 365 tests PASS** |
| Deterministic regeneration | PASS |
| Invalid coordinates / degenerates | PASS: 0 / 0 |
| Bounds / wheelbase / ground | PASS |
| Sampled joins / actual aperture ray visibility | PASS within stated numerical scope |
| Primary projection consistency | PASS, five stable views |
| Visual recognition | **FAIL** |

Both builds retain the existing >500kB chunk advisory. Candidate browser console: no warnings/errors observed. Live-site error log: no errors observed. Logs are saved in `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/reference-v04` as `typecheck.log`, `lint.log`, `build.log`, `diagnostic-build.log`, `tests.log`.

## Website and historical protection

- **Hero UNCHANGED:** source/assets/styles/layout/camera not edited. A current live screenshot is saved; no new pixel-identity claim is made across different browser viewport conditions.
- **Navigation UNCHANGED:** logo, car, controls, styles and behavior untouched. Chapter navigation also exercised by keyboard.
- **Section03 OLD CAR PRESERVED; Section05 OLD CAR PRESERVED; Section02 UNCHANGED.** The live JourneyDock/loader/scene/model path never imported V04.
- **TOLI AI UNCHANGED AND FUNCTIONAL:** opened over the existing Section05 vehicle canvas by keyboard; Services suggestion answered locally; DOM hit-test confirms dialog above the canvas; close worked. No message sent externally.
- **Protected audit:** 7,781 baseline protected files checked, changed0/missing0; all 43 original image files unchanged; V02/V03 frozen source checksums verified. Current source baseline: 376 files checked, six expected candidate/test modifications and one new patch module, no missing files.
- Conditional activation-only responsive/device QA was not run because recognition failed. No production-ready candidate or physical-device readiness claim.

## Required diagnostics

- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/fresh-reference-contact-sheet.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/fresh-front-traces.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/fresh-rear-traces.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/cross-view-landmarks.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/new-headlight-curves.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/headlight-fender-patch.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/headlight-reference-comparison.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/rear-patch-network.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/rear-quarter-reference-comparison.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/dpillar-reference-comparison.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/taillight-reference-comparison.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/bumper-wrap-reference-comparison.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/v02-v03-v04-five-view.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/v04-clay-five-view.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/v04-badgeless-five-view.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/v04-reflection-five-view.jpg`

Additional artifacts: all seven views, checkpoint matrix, silhouette/internal-aperture overlays for the five primary views, two-angle front headlight/fender/grille closeups and two-angle D-pillar/quarter/tail-lamp/bumper closeups. Native closeups are uniformly enlarged crops, not perspective warps. Badgeless and clay boards are identical by design because no branding exists in the candidate; they are not presented as independent evidence of a pass.

Raw actual frame data and render captures are under `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/reference-v04/06/`, `comparison-v02/`, `comparison-v03/`, `comparison-checkpoint-02/` through `05/`, and `modes/`.

## Files changed and saved

- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/test/mux-coded-reference.test.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxReferenceData.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxValidation.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxVehicle.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxGeometry.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/validation.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxReferencePatches.ts`

Supporting isolated files: new `reference-v04.html`; frozen V03 entry redirect; isolated Vite diagnostic entries; `comparisons/` HTML pages (render saved versions only); `reference-data/v04/`; `analysis/reference-v04/`; `source-snapshots/reference-v04/`; `renders/reference-v04/`; this report. All changes are within the authorized static project. No Hero/navbar/live section/public vehicle file was changed.

Preview: `http://127.0.0.1:8190/Toli-2/tools/3d/isuzu-mux/code-reference-car/reference-v04.html`.

**Final: Decision C. V04 saved and isolated. Existing website cars preserved. No V05, activation, deployment or Git commit.** External model NONE; AI3D NONE; cost ₹0 / $0. Separate 3D project and other protected projects UNCHANGED.
