# TOLI MU-X — coded Section 03 & 05 replacement

Date: 2026-11-09. Target project: `/home/thunder/shared/tolimotors-main1/toli-static-website`.

## Decision

**C — CODED MU-X STILL GENERIC / INCORRECT.**

The shared coded candidate still fails badgeless MU-X recognition after a focused correction pass. **Section 03: OLD CAR PRESERVED. Section 05: OLD CAR PRESERVED.** No incorrect coded candidate was activated. No detailed lamps, badges, grille internals or trim were added to hide the primary-body failure.

Hero: **UNCHANGED**. Navigation: **UNCHANGED**. No live section layout, text, spacing, background, CSS, button, camera, lighting, animation, scroll behavior or fallback was edited. The work remains in isolated geometry/diagnostic infrastructure.

## Rendering audit, completed before source corrections

Full audit: `code-reference-car/analysis/section-03-05/CURRENT_IMPLEMENTATION.md`.

**03 is not ComponentExperience.** The actual Section 03 is `HowItWorks`, labeled **03 / SERVICE JOURNEY**, id `process`.

| Target | Actual path |
|---|---|
| Section 03 | `src/pages/Index.tsx` → `src/components/HowItWorks.tsx` → `JourneyDock mode="process"` |
| Section 05 | `src/pages/Index.tsx` → `src/components/CtaBanner.tsx` → `JourneyDock mode="completion"` |
| Shared rendering | `JourneyDock.tsx` → `[data-scene-dock]` → `JourneyProvider.tsx` → `observeJourney` in `journey-timeline.ts` → `load-vehicle-scene.ts` → `vehicle-scene.ts` |
| Existing solid | `vehicle-model/contract.ts` → `vehicle-model/mux.ts` → `vehicle-model/load.ts` → existing `public/models/vehicles/isuzu-mux/isuzu-mux-web.glb` |

The existing model is the historical project-generated V04 temporary preview. One renderer/canvas and cached model are moved between the visible docks. **Section 02 uses this renderer too.** A global loader/manifest replacement would exceed the requested scope; none was made.

### Section 03 — presentation preserved

Camera: existing 34° perspective, .1/60 clipping. For the imported solid, a rotated bounding-box fit uses target `(0,.75,0)`, direction normalized `(7.4,1.3,4.3)` and 1.13 padding in the existing renderer's Y-up convention. Mobile distance adjusts to aspect ratio.

Lighting: existing procedural studio environment/PMREM, directional key, hemisphere fill, point accent, desktop rim, theme exposure, contact shadows and selected-mesh reflection. No new lighting is active.

Animation: the four process buttons select inspection / pickup / service / ready states through `journey.ts` and `chooseStep`. Existing turn, dolly, scan and clean states remain damped/demand-rendered. Desktop presentation and mobile stack remain unchanged.

### Section 05 — presentation preserved

Camera: same fitted perspective system, with the existing completion presentation. `journey.ts` completion pose has turn -.08, distance .28, target Y .78, height 1.65, scale 1, clean 1.

Lighting: the same existing shared studio/theme system. Animation: existing completion state, scroll/pointer response and managed renderer lifecycle. Enquiry/phone actions remain outside the canvas. No new coded model is active.

### Existing resource, motion and fallback policy

One renderer per page, lazy initialization near a dock, shared cached template, demand rendering, offscreen/hidden/dialog pausing. Existing desktop/tablet budgets cap DPR at 1.5/1; weak hardware/save-data use tablet. Measured frame intervals may downgrade the existing renderer. Reduced-motion preferences interrupt travel/inertia and reduce movement without removing the car. Context loss/restoration is handled; actual failure retains the section with `VehicleIllustration` fallback.

These existing systems were audited and preserved. New LOD tiers or adapter branches were not added for a candidate that failed the primary-body gate.

## References and method

**43 supplied files / 39 distinct reference views → design data → curves → cross-sections → coded Three.js geometry.**

The authoritative folder remains `/home/thunder/shared/tolimotors-main1/Isuzu MU-X`. Reused the completed visual analysis and verified image inventory rather than repeating failed calibration. The silver open/closed reference family remains authoritative; compatible red intermediate views support transitions; overhead is low-confidence support only. No incompatible body family, external vehicle model, Warehouse candidate or generative/image-to-3D API is used.

Primary front/side/rear evidence: MUX-011–018. Intermediate confirmation: MUX-020–040, especially front-quarter 029/030 and rear-quarter 022–026/034–036. MUX-043 supports plan outline only. Engine/interior 003/004/010 and duplicate viewer crops do not constrain primary exterior depth. Exact per-image files and confidence remain in `analysis/reference-inventory.json` and `analysis/DESIGN_MAP.md`.

## Focused correction pass — no model restart

One editable shared factory remains `src/components/three/mux/MuxVehicle.ts`. Presentation stays separate in the isolated `validation.ts`. Both target sections would consume that same factory only after approval; neither currently does.

Four source/test files were modified:

1. `src/components/three/mux/MuxGeometry.ts`
   - Replaced per-interval smoothstep interpolation with slope-continuous, monotone cubic Hermite interpolation. The previous derivative went to zero at every station and generated repeated reflection waves.
   - Evaluated section widths at absolute body height. Previously arch elevation moved the whole width profile upward and distorted shoulder/fender reflections.
   - Increased transverse sampling to 25 points for those curved profiles.
   - Replaced the laterally reversing three-point fender path with monotone lateral interpolation, retaining crown lift and shared bonnet/side endpoints.
   - Blended terminal side sections to the same nose/hatch profile used by the end surfaces, reducing detached boundary mismatches.
2. `MuxReferenceData.ts`: centralized the shared front/rear depth-section profiles alongside existing dimensions, 19 nonuniform body stations, normalized landmarks and named reference curves.
3. `MuxVehicle.ts`: identified the current assembly as the isolated Section 03/05 primary-surface candidate; it was not wired to any live dock.
4. `src/test/mux-coded-reference.test.ts`: saved this pass's measurements separately and added monotonicity/boundedness/interior-slope continuity checks.

Existing bonnet, roof, glazing, wheels and primary envelope architecture was retained. No separate Section 05 model was authored.

### V01 preservation

Before editing, all six V01 source modules, its HTML, test and prior standalone build were copied into `code-reference-car/source-snapshots/v01/`. Each archived source module matches its pre-edit SHA-256. The original isolated `index.html` now imports that immutable snapshot, so V01 remains inspectable. The current correction has a separate `section-03-05.html` entry. Original V01 renders and reports were not overwritten.

## Dimensions and geometry

Design coordinates: X length/front negative, Y width, Z up, ground Z=0. These are an authored interpretation of uncalibrated photographs, not factory CAD or a calibrated depth reconstruction.

| Measurement | Framework | Measured candidate |
|---|---:|---:|
| Length | 4.825 m | **4.829403 m** |
| Width | 1.860 m | **1.860000 m** |
| Height | 1.860 m | **1.860000 m** |
| Wheelbase | 2.845 m | **2.845000 m** |
| Tire diameter | approximately .764 m | **.764000 m** |
| Ground Z | 0 | **7.15×10⁻¹⁰ m** |

Length exceeds the nominal framework by approximately **4.4 mm**, primarily at the projected fascia envelopes. This is reported, not described as exact accuracy.

- Vertices: **55,391**, summed over mesh instances.
- Vehicle triangles: **85,740**.
- Vehicle mesh instances: **51**.
- Observed isolated scene draw calls: **52**, including ground.
- Observed rendered triangles: **85,742**, including ground.
- Vehicle materials: **5**.
- Degenerate triangles: **0**, squared double-area threshold 1×10⁻²⁰.
- Invalid coordinate vertices: **0**.
- Primary-surface symmetry: **0 unmatched positions at 1×10⁻⁵ m tolerance**. Scope is body, glazing and broad fascia; wheel-spoke pattern excluded.
- Deterministic regeneration: **PASS**, fingerprint `9267b48b0a7b085038032a34d9789a0bd941c8c5829404fb193a14576a7f45fa` matched across two independent constructions.

Measurement files: `reports/section-03-05-geometry-validation.json` and `analysis/section-03-05/render-stats.json`. Count/clean topology/dimensions do not approve visual identity.

## Visual gate and remaining fundamental defects

| Gate | Result | Required reconsideration |
|---|---|---|
| Front | FAIL | `fasciaSections.front`, grille/lamp envelopes and the hood leading boundary still form a generic nose. |
| Front 3/4 | FAIL | `fenderTop`/bonnet/fascia boundaries have improved positional consistency but still lack the reference's volume and tangent flow. Fin-like corner behavior remains. |
| Side | NEEDS WORK | Better reflection flow, but body mass/belt/door and arch relationships are not sufficiently MU-X-specific. |
| Bonnet/fender | FAIL | Shared boundary tangency and crown/falloff need a coherent control net; more interpolation samples alone do not solve this. |
| Greenhouse | FAIL | `greenhouseY`, window outlines, A-root/header and roof/screen junctions remain too planar and generic. |
| D-pillar | NEEDS WORK | Quarter-glass termination and the painted surround are not yet faithful in rear-side views. |
| Rear quarter | FAIL | Shoulder/arch/quarter depth and taper remain wrong despite less waviness. |
| Rear 3/4 | FAIL | Quarter-to-glass-to-hatch volume still does not match the supplied reference. |
| Rear | FAIL | Rear profile/recess and lamp/bumper depth hierarchy remain generic. |
| Bumper wrap | FAIL | Terminal joining helps position, but continuous reference-faithful corner shape and tangency are not established. |
| Clay | FAIL | The unbadged body does not read clearly as the supplied MU-X. |
| Reflection | NEEDS WORK | The repeated station waves are reduced, but seam/tangent discontinuities remain obvious. |
| **Badgeless recognition** | **FAIL** | **No Section 03/05 activation.** |

No manufacturer badge, number-plate branding, detailed lighting assembly, material flourish or tiny trim was added to camouflage these defects. Final-material/badge/light-control expansion is deferred by this failed primary-body gate; the existing clay/reflection/wireframe/zebra diagnostics remain available.

## Responsive, regression and functional checks

Both preserved sections were checked at **320×568, 360×800, 390×844, 412×915, 768×1024 and 1440×900**, plus complete 1000×900 desktop evidence. All fourteen settled observations reported ready state, a canvas in the intended dock, opacity 1, no covering/inert state and no document horizontal overflow. Layout rectangle checks found no canvas/control-panel overlap. Screenshots were inspected for whole-vehicle visibility.

Initial screenshots caught existing fade/scroll transitions; they were replaced with settled frames. The final evidence is recorded in `analysis/section-03-05/settled-checks.json`. The browser surface clips wide emulated 1440 captures; the 1000-wide desktop aliases provide complete screenshots, while 1440 layout checks use the actual 1440-wide DOM. No physical Android/iOS or GPU performance certification is claimed.

**Hero regression: PASS. Navigation regression: PASS.** Matching 1000×900 viewport, theme and responsive image source produced pixel-identical before/after captures: mean absolute RGB difference **0**, zero differing pixels for both. The first Hero comparison had a small car-region difference because the browser retained the existing 1600-wide responsive asset after a wider viewport; a fresh page using the original 960-wide source matched exactly. No asset, CSS or source change was used to obtain the match. Screenshot image dimensions are 990×891 for the Hero viewport capture and 990×64 for the navbar crop.

**TOLI AI: PASS** for opening/closing and visibility over the active vehicle. The dialog remained visible above the canvas (computed z-index 66); the renderer reported paused while it was open. No AI implementation was edited. Captured browser error log was empty.

Source protection: all 368 enumerated website source/public/config files were compared. Only the four isolated coded-model/test files listed above changed; no files were missing. Hero, navbar, live sections, global CSS, shared renderer, loader, registry and current vehicle assets were unchanged. The historical/protected/reference baseline checked **7,781 files with zero changed and zero missing**. Its result is saved separately in `analysis/section-03-05/protected-after.json`.

## Tests and builds

- `npm run typecheck`: **PASS**.
- `npm run lint`: **PASS**.
- `npm run build`: **PASS**, 14.12 seconds.
- Standalone diagnostic build with `code-reference-car/vite.config.mjs`: **PASS**, builds both preserved V01 and the new isolated entry.
- `npm test`: **52 files / 361 tests PASS**.
- Targeted geometry/interpolation tests: **3 PASS**.

Existing chunk-size/Tailwind and test-environment warnings remain. The new geometry is not in the website's import/render path. No new performance cost is activated in Section 03/05. The candidate uses shared wheel buffers/materials and demand rendering at diagnostic DPR 1; production tiers/adapters/performance tuning are deferred until recognition passes.

Logs: `analysis/section-03-05/{typecheck,lint,website-build,diagnostic-build,tests,geometry}.log`.

## Exact diagnostic paths

Base directory:

`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/section-03-05/`

Required outputs are saved there:

- `reference-coded-comparison.jpg`
- `coded-mux-five-view.jpg`
- `coded-mux-eight-view.jpg`
- `coded-mux-clay.jpg`
- `coded-mux-reflection.jpg`
- `coded-mux-wireframe.jpg`
- `front-34-closeup.jpg`
- `greenhouse-closeup.jpg`
- `rear-34-closeup.jpg`
- `section-03-desktop.jpg` / `section-05-desktop.jpg` — existing vehicle, complete 1000-wide captures
- `section-03-mobile.jpg` / `section-05-mobile.jpg` — existing vehicle, 390-wide captures
- `hero-regression.jpg` / `navigation-regression.jpg`
- `responsive-contact-sheet.jpg`
- `ai-above-canvas.jpg`

Individual viewport captures are `section-{03,05}-{320,360,390,412,768,1440,1000}.jpg`. Individual candidate cameras are `{clay,reflection,wireframe}-{front,front-left,left,rear-left,rear,rear-right,right,front-right,overhead}.jpg`. Reference comparisons use unwarped images, independent uniform fits and closest useful facing directions, not fabricated calibrated overlays. Closeups may intentionally crop vehicle ends/wheels to expose surface defects.

Isolated current candidate:
`http://127.0.0.1:8190/Toli-2/tools/3d/isuzu-mux/code-reference-car/section-03-05.html`

Preserved original V01:
`http://127.0.0.1:8190/Toli-2/tools/3d/isuzu-mux/code-reference-car/index.html`

## Other file changes and preservation

The isolated `code-reference-car/index.html` was pinned to the V01 snapshot; its `vite.config.mjs` now builds both diagnostic entries. New files include `section-03-05.html`, the V01 source/build snapshot, this report, scoped audit/measurement/log files, `reports/make_section_diagnostics.py` and scoped rendered evidence. The exact artifact manifest is `analysis/section-03-05/files.json`.

One reusable coded candidate: **YES**, isolated only. Current live geometry is already shared by 03/05 and remains active. No second independently modeled section vehicle was created.

Protected projects: UNCHANGED. Original reference images: UNCHANGED. Earlier research: PRESERVED. Hero/navigation: UNCHANGED. Existing 03/05 implementation/fallback: PRESERVED.

External 3D models introduced: NONE. AI-generated/image-to-3D assets: NONE. Paid services: NONE. Cost: ₹0 / $0 in external services. Deployment: NOT PERFORMED. Git commit: NOT PERFORMED.

## Remaining limits

This is a stopped primary-surface correction candidate, not a completed replacement. Badgeless identity, front/rear-quarter shape, greenhouse and tangent-flow gates remain failed. No deep detailing, active integration, new LOD/fallback certification or physical-device validation was performed after that decision.
