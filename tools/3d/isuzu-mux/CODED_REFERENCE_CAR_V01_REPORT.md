# MU-X CODED REFERENCE CAR V01

Date: 2026-11-09. Project: `/home/thunder/shared/tolimotors-main1/toli-static-website`.

## Decision

**C — CODED BODY STILL GENERIC / INCORRECT.**

Badgeless MU-X recognition: **FAIL**. Primary-body work is stopped at V01. The implementation and its diagnostic evidence are preserved. No deep detailing, vehicle replacement, Hero change, website integration, model download, AI generation, deployment or Git commit followed this failed gate.

The code runs and its geometry is deterministic, finite and free of collapsed triangles under the stated threshold. Those facts do not approve the body. The front three-quarter, greenhouse and rear quarter remain visibly different from the supplied MU-X. Reflection and zebra modes expose severe surface waviness and unfinished transitions. Do not camouflage those failures with badges, detailed lamps, grille internals or materials.

## Method and scope

**SUPPLIED IMAGES → REFERENCE ANALYSIS → CODED CURVES/CROSS-SECTIONS → GENERATED THREE.JS GEOMETRY.**

This is new authored TypeScript/Three.js r180 primary geometry, using the project's installed library. No old Manual Overlay, Curve Cage V04, surface prototype, Existing-photo mesh, generic SUV or Warehouse candidate is loaded, deformed or relabeled. Existing procedural studio-radiance code is reused solely for lighting diagnostics. No vehicle texture or photographic background is used to create the coded shape. No Blender edits, GLB or exported asset are the source of truth.

The isolated HTML page imports the new geometry directly. No homepage/app-route module imports it. Production website content, Hero, navigation, AI and the existing service vehicle remain unchanged. The separately built diagnostic artifact is not wired into the website build.

## References

Authoritative folder: `/home/thunder/shared/tolimotors-main1/Isuzu MU-X`.

**43 readable files / 39 distinct visual references.** Current hashes were checked against the existing complete inventory. The complete 39-view contact sheet was reviewed; key front/side/rear images were enlarged. All 43 per-file roles, paths, dimensions, hashes and limits are saved in:

`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/reference-inventory.json`

Canonical shape/trim authority: silver open-panel 006–009, with compatible closed silver 011–018 for contours. Compatible red viewer images supply intermediate visual confirmation. They do not establish a common calibrated camera or a single physical vehicle. Original paint colours are ignored.

| Required view | Primary evidence |
|---|---|
| Front | MUX-011 — Screenshot From 2026-11-06 18-17-10.png |
| Front-left 3/4 | MUX-016 — Screenshot From 2026-11-06 18-17-27.png |
| Left-front intermediate | MUX-030 — Screenshot 2026-11-08 213441.png |
| Left side | MUX-012 — Screenshot From 2026-11-06 18-17-14.png |
| Left-rear intermediate | MUX-022 — Screenshot (3).png |
| Rear-left 3/4 | MUX-017 — Screenshot From 2026-11-06 18-17-31.png |
| Rear | MUX-013 — Screenshot From 2026-11-06 18-17-18.png |
| Rear-right 3/4 | MUX-018 — Screenshot From 2026-11-06 18-17-35.png |
| Right side | MUX-014 — Screenshot From 2026-11-06 18-17-21.png |
| Front-right 3/4 | MUX-015 — Screenshot From 2026-11-06 18-17-25.png |
| Overhead, low confidence | MUX-043 — images.jpg |

Secondary: compatible 001/002/005/019 and red 020–040, with primary entries above taking precedence. 003/004/010 are engine/interior evidence and do not constrain this exterior. Four duplicate viewer crops (032/033/041/042) add no independent shape information. Exact distinctions remain in the inventory. No EXIF/lens/camera pose or factory-CAD accuracy is invented.

Design analysis is saved before geometry construction in `code-reference-car/analysis/DESIGN_MAP.md`. It covers overall proportions, bonnet/front, front fenders, cowl, greenhouse, window boundaries, side body, rear quarter and rear, with evidence assignments and inferred depth noted. `analysis/39-distinct-reference-review.jpg` preserves the reviewed contact sheet.

## Dimension framework and measured result

X = length, front negative; Y = width; Z = height. Ground Z=0. Camera left/right labels are a world-coordinate viewing convention, not recovered camera poses. Comparison pairs use the closest saved facing direction when that naming differs from the historical source labels. No photo or render is mirrored or geometrically warped.

| Dimension | Supplied framework | Measured constructed result |
|---|---:|---:|
| Length | 4.825 m | **4.827414 m** |
| Width | 1.860 m | **1.860000 m** |
| Height | 1.860 m | **1.860000 m** |
| Wheelbase | 2.845 m | **2.845000 m** |
| Approximate tire diameter | 0.764 m | **0.764000 m** |
| Lowest tire Z | 0 | **7.15×10⁻¹⁰ m**, floating-point zero |

The 2.4 mm excess length comes from broad projected fascia envelopes. It is reported rather than described as exact. These are design-unit measurements of this generated candidate, not factory-CAD accuracy or measured physical dimensions. Axles are locked at -1.370/+1.475; track is an inferred 1.570 m. Nominal overhangs and transverse section depth are authored estimates. The optional basic roof-rail envelopes account for overall height; there is no rail detailing.

Normalized image landmarks are manually estimated fractions of the full source canvas, not recovered 3D points. They constrain visual ratios only; perspective/crop means those pixel ratios must not be called orthographic metrology. Central editable data:

`/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxReferenceData.ts`

## Geometry and curve architecture

- **MuxReferenceData.ts**: dimensions, axles, normalized image landmarks, 19 nonuniform longitudinal body stations, named longitudinal/window/front/rear curves and fixed view names.
- **MuxGeometry.ts**: indexed patch generation, body-band interpolation, explicit circular arch anchors, bonnet crown/falloff, fender patches, crowned roof, separate curved screens, painted pillar network with window holes, broad front/rear depth surfaces and projected apertures.
- **MuxWheels.ts**: rounded lathed tire carcass/shoulder, barrel, curved extruded spokes, hubs, brake discs and simple calipers. Four fixed wheel groups; no detailed tread.
- **MuxVehicle.ts**: assembly, neutral materials, primary surface groups, broad identity envelopes, curve/section/landmark diagnostics and resource disposal.
- **MuxValidation.ts**: dimensions, tire/axle measurements from constructed objects, finite-coordinate, degeneracy and primary-surface symmetry inspection.
- **validation.ts**: isolated renderer, neutral studio, nine fixed cameras, clay/reflection/wireframe/zebra controls and visibility controls. Demand rendering; no continuous animation.

Body bands cover sill/lower/max/shoulder/belt widths, with greenhouse and roof patches supplying the upper bands. Bonnet/roof/fender curves directly drive those patches. Some shoulder/belt/lower/rear guides are currently diagnostic guides alongside the station network, rather than independently enforced shared surface boundaries. Their inconsistency with the generated patches is part of the failed quality gate.

Cabin glass is separate from painted pillars. Curved polygon boundaries use local quadratic corner rounding. The primary body is mirrored mathematically. Shared Three.js geometry is reused across wheels. Standard capsule-pole collapsed faces were removed during construction; the final independent triangle check found zero remaining degenerates.

Only primary body, bonnet/fenders, roof/greenhouse, windows, quarters, broad fascia and wheels are attempted. There are no badges, handles, sensor meshes, detailed lamps/grille, wipers, hinges, interior, engine or detailed underbody. No deep-detail pass was started.

## Geometry statistics and reproducibility

Final measurements:

- **45,707 vertices**, summed across vehicle mesh instances; not a welded unique-vertex count.
- **66,476 triangles** in the coded vehicle.
- **51 vehicle mesh instances / 52 observed scene draw calls** including one ground mesh.
- **66,478 rendered triangles** in clay/reflection mode, including the ground.
- **5 vehicle materials**.
- **0 invalid coordinate vertices**.
- **0 degenerate triangles** at squared double-area threshold 1×10⁻²⁰ in design units.
- **0 unpaired primary-surface positions** at a 1×10⁻⁵ m quantization tolerance. Scope: body, glazing and broad front/rear surfaces; wheel spoke patterns are excluded. This is effectively symmetric within the tested tolerance, not proof of continuity or visual correctness.

Regeneration fingerprints matched:

`d0a3f566b6e4b870ca59160c86394b3185c8747542d00e1d14ab92d9da24d385`

The test constructs two independent vehicles and compares their mesh-buffer fingerprints, then checks dimensions, ground, bounds, finite coordinates, triangles and symmetry. Geometry statistics and hashes: `code-reference-car/reports/geometry-validation.json`. Actual browser view/mode/draw-call observations: `reports/render-measurements.json`.

## Visual gate and exact failure causes

| Region | Result | Reference-driven discrepancy and responsible code/data |
|---|---|---|
| Front | FAIL | Front profile widths/projection and projected grille/lamp envelopes form generic slits and insufficient MU-X corner structure. `frontProfile`, `fasciaPoint`, `grilleUpper/Lower`, `headlamp`. |
| Front 3/4 — primary gate | FAIL | Hood edge/fender connection pinches, with fin-like corners and discontinuous curvature. `bonnetSide`, `fenderCrown`, `fenderTop`, front body stations and fascia termination do not share one compatible boundary. |
| Side | NEEDS WORK | Correct nominal anchors and tall cabin are insufficient; broad flat door volume and incorrect belt/arch flow resemble a generic utility body. `section` bands and `bodyStations`. |
| Greenhouse | FAIL | A-root/header transition and side glass remain too planar and angular. `cabinOutline`, `frontWindow`, `rearWindow`, `greenhouseY`, roof/screen boundaries. |
| D-pillar | NEEDS WORK | Quarter opening is separate, but the painted surround/roof-to-hatch transition is still generic. `quarterWindow`, `cabinOutline`, rear roof stations. |
| Rear quarter | FAIL | Required volume is not established coherently; shoulder/arch reflections scallop and the taper has unfinished joins. Rear `bodyStations`, `section`, `rearShoulder` guide. |
| Rear 3/4 | FAIL | Rear glass, quarter and hatch/fascia do not form the reference's continuous wrapped volume. `rearGlass`, `rearProfile`, `fascia(true)`. |
| Rear | FAIL | Plate/hatch/bumper relationships remain generic and the lamp envelopes do not establish the correct broad depth hierarchy. `rearProfile`, rear recess term and `tailLamp`. |
| Bonnet/fender transition | FAIL | Lateral patch interpolation folds/overshoots near the outer fender, rather than forming the reference's controlled crown and falloff. `fenderTop` versus `bonnet` boundaries. |
| Clay recognition | FAIL | Lack of recognizability persists without badges/texture/colour. |
| Reflection flow | FAIL | Severe repeated waviness on doors/fenders/quarter; smoothstep station interpolation and arch-relative height bands are not an automotive-quality control net. |
| Badgeless MU-X recognition | **FAIL** | The important views do not meet the reference identity gate. |

Zebra/reflection images are diagnostic evidence of these flaws, not a successful finish. No global bevel or fine trim was used to conceal them. This report stops at C; it does not propose another uncontrolled restart.

## Fixed-camera visual outputs

All original browser captures and composite images are saved under:

`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/v01/`

Required outputs:

- `coded-five-view.jpg`
- `coded-eight-view.jpg`
- `reference-coded-comparison.jpg`
- `front-34-closeup.jpg`
- `rear-34-closeup.jpg`
- `greenhouse-closeup.jpg`
- `clay-five-view.jpg`
- `reflection-five-view.jpg`
- `wireframe-five-view.jpg`
- `cross-sections.jpg`
- `zebra-front-34.jpg`

Individual screenshots: `mux-v01-{clay,reflection,wireframe}-{front,front-left,left,rear-left,rear,rear-right,right,front-right,overhead}.jpg`. They come from the actual Three.js renderer, not Blender or generated visual artwork. The selected camera directions/FOV and bbox fit are fixed in validation.ts across captured modes.

Reference comparison is also at:

`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/comparisons/reference-coded-comparison.jpg`

References and coded captures are uniformly fitted independently into panels. Perspectives differ; no calibrated overlay, nonuniform stretch, homography or manufactured pixel agreement is claimed. Source images are unmodified. Closeups intentionally use the range control's nearer setting and may crop wheels/ends to expose surface defects; full standard views retain the complete vehicle.

## Technical validation

| Command / check | Result |
|---|---|
| `npm run typecheck` | PASS, including new source/tests |
| `npm run lint` | PASS |
| `npm run build` | PASS — existing website, 12.22 s |
| `node node_modules/vite/bin/vite.js build --config tools/3d/isuzu-mux/code-reference-car/vite.config.mjs` | PASS — isolated diagnostics |
| `npm test` | **52 files / 360 tests PASS** |
| Targeted deterministic/geometry test after final measurement correction | **2 tests PASS** |
| Browser | Nine cameras × clay/reflection/wireframe captured, plus zebra/closeups/curve-section-landmark views; error log empty |

The full suite passed before the final measurement-only correction; both new geometry tests, TypeScript and lint passed again afterward. No visual surface code changed after the saved captures. The isolated diagnostic was rebuilt after that correction. Existing production chunk-size/Tailwind and unit-test environment warnings remain; none is claimed resolved by this task. The diagnostic bundle is roughly 789 kB minified including Three.js: a local evaluation tool, not a production mobile release.

Logs are preserved in `code-reference-car/reports/`: typecheck.log, lint.log, website-build.log, diagnostic-build.log, full-tests.log and geometry-tests.log. The local app remains at `http://127.0.0.1:8190/Toli-2/`. Isolated development entry:

`http://127.0.0.1:8190/Toli-2/tools/3d/isuzu-mux/code-reference-car/index.html`

For repeatable inspection: run the existing `npm run dev`, open that isolated URL, select a camera/material, then capture. `reports/make_diagnostics.py` assembles the saved browser captures into panels; it does not generate model images itself.

## Exact new files / preservation

New source files are the six modules listed above in `src/components/three/mux/`, plus `src/test/mux-coded-reference.test.ts`. Isolated infrastructure: `tools/3d/isuzu-mux/code-reference-car/index.html`, `vite.config.mjs`, `reports/make_diagnostics.py`, analysis/reference-data/report/render/build artifacts, and this new report. A complete absolute-path file manifest is saved at `code-reference-car/reports/new-files.json`.

There are **no intentional edits to pre-existing website, historical research or reference files**. The before/after SHA-256 preservation audit covers the enumerated prior baseline plus all 43 authoritative originals. The completed comparison checked **7,781 files**, with **zero changed and zero missing**. Its exact result is in `code-reference-car/reports/preservation-after.json`; do not infer coverage of unenumerated files from it.

Website: UNCHANGED except isolated test infrastructure. Hero: UNCHANGED. Navigation: UNCHANGED. TOLI AI: UNCHANGED. Current website vehicle: UNCHANGED. Historical MU-X work: PRESERVED. Protected sibling projects: UNCHANGED. Authoritative original images: UNCHANGED.

External 3D model: NONE. AI-generated 3D: NONE. Paid services: NONE. Cost: ₹0 / $0 in external services. Deployment: NOT PERFORMED. Git commit: NOT PERFORMED.

## Remaining limitations

Badgeless identity and surface-flow gates fail. The references are uncalibrated; the control network is an authored visual interpretation with inferred depth. Physical device/GPU performance, factory CAD conformity and final exterior production readiness are not certified. No detail pass or website activation is authorized by this result.
