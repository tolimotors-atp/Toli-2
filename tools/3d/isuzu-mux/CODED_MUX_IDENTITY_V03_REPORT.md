# MU-X CODED IDENTITY V03 — Headlight curves + rear reconstruction

2026-11-09. Continued the existing V02 coded factory. No global vehicle restart.

## Decision

**C — HEADLIGHT/REAR STILL FAIL REFERENCE IDENTITY.**

Headlight quality gate: **FAIL**. Rear quality gate: **FAIL**. Overall same-car recognition: **FAIL**. V03 is saved as an isolated failed candidate. **Section 03 and Section 05 retain their existing cars.** Section 02 also unchanged. No deployment or commit. No further geometry iteration after final visual rejection.

V03 provides real curved lamp depth and more rear depth controls, but that implementation is not proof of a visual match. In particular, the rear is **WORSE in some surface relationships** than V02. The report does not call that a substantial same-car improvement. V02 remains available unchanged and should not be replaced with this candidate in production.

## References inspected before editing

All **43 supplied files** were inspected in two contact sheets (39 distinct images per existing audit). Visible-headlight images, intermediate/front/side variants and rear variants were classified before geometry changes. See `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v03/headlight-reference-analysis.md`, `reference-inventory-0.jpg` and `reference-inventory-1.jpg` in renders. No model-year/trim switch from the silver family.

All source filenames below are in `/home/thunder/shared/tolimotors-main1/Isuzu MU-X`:

| Region | Selected references |
|---|---|
| Direct front / headlight envelope | `Screenshot From 2026-11-06 18-17-10.png` (silver primary); `Screenshot From 2026-11-06 18-08-46.png` (compatible red, clearer boundary) |
| Front-left 3/4 | `Screenshot From 2026-11-06 18-17-27.png` |
| Opposite front 3/4 | `Screenshot From 2026-11-06 18-17-25.png` |
| Lamp/fender close relation | `20250902050117_Isuzu_mu-X_Silver_Metallic[1].avif` |
| Front intermediate | `Screenshot 2026-11-08 213411.png`, `Screenshot 2026-11-08 213436.png` |
| Direct rear | `Screenshot From 2026-11-06 18-17-18.png` |
| Rear-left 3/4 | `Screenshot From 2026-11-06 18-17-31.png` |
| Opposite rear 3/4 | `Screenshot From 2026-11-06 18-17-35.png` |
| Side / quarter | `Screenshot From 2026-11-06 18-17-14.png`, `Screenshot From 2026-11-06 18-17-21.png` |
| Secondary rear wrap checks | `Screenshot 2026-11-08 213459.png`, `213502.png`, `213507.png`, `Screenshot (4).png`–`Screenshot (7).png` |

Reference pixels remain untouched. The AVIF was decoded only for local inspection, not altered in the source folder. Depth controls are authored visual estimates from uncalibrated views; no CAD, millimetre or photogrammetric accuracy is claimed.

## Pre-edit rear error map

Saved **before geometry correction**:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/REAR_IDENTITY_ERROR_MAP_V03.md`

The map covers roof width, D-pillars, glass, shoulder, quarter width, lamp shape, hatch, bumper, corners, lower rear and taper, with the exact responsible V02 functions. Visual before-map: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/rear-error-map.jpg`.

## V02 preservation and working structure

V02 frozen source: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/source-snapshots/identity-v02/final/`.

Its seven module/test copies match the start-of-task source checksums byte for byte. `identity-v02.html` now points to that frozen validation module, so the prior preview continues showing V02. Historical V02 iterations/renders/report are unchanged. V03 final source: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/source-snapshots/identity-v03/final/`. Current working factory remains the same `src/components/three/mux/MuxVehicle.ts` and surface/data modules.

Protected V02 values: cowl placement, windscreen/front-side glass, forward roof, nominal dimensions, axle/track positions, wheel geometry and wheelbase. Local front-corner, rear-quarter, rear-glass/D-pillar and bumper surfaces were changed as requested. Hero, navbar, live loaders and section layout files were never edited.

## H1–H8 headlight network

All XYZ control arrays: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v03/candidate-controls.json`, key `headlightCurves`. These are actual Catmull–Rom controls. H1 and H2 form the upper boundary; H3–H5 form the lower and return boundaries. A Coons patch creates a genuinely three-dimensional lens. H6/H7 influence the depth/crown with a bounded correction; they do not change the perimeter. H8 is a **fender continuation guide**, not a completed stitched fender surface. That unfinished transition is explicitly part of the failed quality gate.

| Curve | Definition / final endpoints in authored metres |
|---|---|
| H1 upper outer | `(-2.150,.740,1.045)` → `(-2.030,.895,1.105)` through swept intermediate point |
| H2 upper inner | `(-2.250,.535,.998)` → H1 start, toward grille |
| H3 lower | `(-2.280,.625,.890)` → `(-2.100,.910,.905)` with a shallow lower bow |
| H4 outer return | H1 end → H3 end, curved in X/Y/Z around outer corner |
| H5 grille junction | H2 start → H3 start via curved inner return |
| H6 front-depth spine | Three controls centred near y .745–.780, X -2.170/-2.195/-2.220 |
| H7 lens crown | Three transverse controls X -2.270/-2.190/-2.070; correction bounded -16/+8 mm |
| H8 fender continuation | H1 tip → `(-1.370,.918,1.255)` via forward-fender crown; debug guide only |

Both sides are mirrored from the same positive-Y definition. Lamp X-span is >.20 m; it is not a projected flat quadrilateral. Obsolete V02 headlamp/tail-lamp quadrilateral controls were removed from current source, retained in frozen V02.

Layers: dark housing/aperture ring, curved dark glass lens, narrow neutral upper signature, one economical reflector ring on each front lamp. No detailed projector, texture, badge, sensor or emissive camouflage. The ring is a simplified reflector, not a fidelity claim. Materials reuse the same five resources.

Actual fascia triangles behind lamp outlines are cut using sampled Y/Z perimeters. **This is not an edge-conforming, watertight aperture rebuild.** Residual cut-edge/fender gaps remain visible. The housing outline does not complete the desired smooth body junction; no production-ready topology claim.

Development-only `headlight-debug` shows H1–H8, control points and the live lens/aperture with body present. H5 is the grille-junction guide and H8 the fender-continuation guide. These controls only exist in the isolated validation entry; they do not alter website UI.

## Rear reconstruction

Actual control arrays: `rearSections`, `rearGlassCurves`, `tailLightCurves`, `bumperCornerCurves` in `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v03/candidate-controls.json`.

- **Cross-sections:** ten independent Z rows at .39/.46/.53/.64/.70/.78/.94/1.10/1.22/1.29 m. Each has separate half-width, centre X and corner depth. Rear face, side terminal and lower return use this profile. Rear-axle quarter receives a localized compound width/crown change, fading before the successful forward cabin.
- **Depth hierarchy:** roof trailing lip near X1.99–2.10; curved glass X1.98–2.29; upper/lamp hatch around X2.285–2.315; broad shallow plate/hatch recess; bumper step/face X2.35–2.4125; lower return X2.295–2.375. These are curved surfaces, not stacked flat cards.
- **Quarter:** local upper taper and mid-band crown; two economical dark rear arch returns provide actual opening depth. Axles/tyres unchanged. The quarter still lacks convincing MU-X compound volume.
- **D-pillar:** only local `cabinOutline`/`quarterWindow` termination changed. Quarter glass lower/rear `(2.075,1.315)` and upper/rear `(1.900,1.665)` in X/Z; outer cabin rear base moved to `(2.190,1.290)`. The resulting surround remains too generic.
- **Glass:** top, bottom and side curves create a Coons surface with rounded tapered returns. A shallow trailing roof lip was added; forward roof controls were not changed. Rear glass/body/roof normals and borders are not fully reconciled.
- **Tail lamps:** upper/lower/inner/outer curves span X1.98–2.335, with real corner wrap and separate quarter/hatch guide curves. Current silhouette still reads too much like a thick horizontal block, protruding incorrectly relative to the quarter. Curve existence alone is not a PASS.
- **Bumper:** dedicated lower/face/step rows, restrained dark lower return and explicit mirrored corner controls. Final corner points range from `(2.375,±.600,.595)` to `(2.115,±.892,.675)`. These control the actual surface, not just the debug display.
- **Mapping correction:** V02's longitudinal end blend could fold back near rear corners. A bounded monotone rear-X mapping replaced it locally and has an explicit regression test. Monotone X does **not** guarantee curvature/tangent continuity; remaining bumper pinching still fails visually.

First build exceeded width by 22 mm through the expanded lamp housing; this was corrected in geometry, not by weakening the dimension test. Housing stays within ±.930 m. Initial overprojected bumper corner controls and excessive lamp projection were refined after actual browser inspection. Final source is the preserved corrected state; neither intermediate nor final candidate was activated.

## V02 vs V03 — actual view assessment

| View | Result | Assessment |
|---|---|---|
| Front | BETTER locally | Curved headlight perimeter and depth replace old wedge; bonnet/grille/body relationship still not the source |
| Front 3/4 | SIMILAR overall | Real lamp wrap improves one region, but aperture/fender junction still disconnected |
| Side | SIMILAR | Forward V02 proportions retained; rear arch return helps depth, but quarter shape remains generic |
| Rear 3/4 | WORSE in surface coupling | Extra depth exposes pinching and a protruding block-like tail lamp; substantial same-car improvement not achieved |
| Rear | WORSE in corner/recess flow | More depth hierarchy, but bumper/hatch highlights and lamp spacing still unlike reference |

The unchanged comparison camera code was checked against frozen V02. FOV34°, same nine directions, same fixed nominal bounding-box fit, target `(0,0,.95)`, zoom1.0 for comparison captures. No per-view deformation, FOV/yaw tuning or camera fitting. Historical button names `front-right/right/rear-right` use the negative-Y side matching supplied front-left/left/rear-left appearance. Additional opposite-side quarter views were captured too.

Debug closeups use the existing distance slider .65 and are clearly labelled; they are not substituted for unchanged-camera comparison views. Closeup crops are uniformly resized for readability, not warped.

## Overlays and numerical verification

Five whole-car reference overlays plus a headlight crop are saved. **Uniform scale and translation only**, copied from V02's wheel-anchor registration because wheels and camera are unchanged. No rotation, anisotropic scaling or per-part alignment. Perspective/height mismatch remains visible, particularly in quarter views.

Magenta lamp boundaries are projections of the actual new Coons surfaces. Purple whole-car outlines come from actual black-silhouette browser captures. The independent numerical camera projection is self-checked against captured wheel pixels (<1e-6 px difference) and asserts unchanged camera source. That checks projection consistency, **not reference accuracy**. Approximate reference headlight contours are annotated separately; H6/H7 are inferred cross-view depth/crown, not single-photo measured curves.

Data/method: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v03/curve-projections.json`, `project-curves.mjs`, `overlay-registration.json`, `headlight-photo-trace.json`. No similarity percentage is claimed.

## Quality gates

| Headlight gate | Result |
|---|---|
| Reference outer silhouette | NEEDS WORK |
| Grille junction | FAIL |
| Fender junction / H8 integration | FAIL |
| Bonnet relationship | FAIL |
| Actual lens depth | PASS technically |
| Front / front-quarter same-car match | FAIL / FAIL |
| Overall headlight gate | **FAIL** |

| Rear gate | Result |
|---|---|
| Believable reference quarter volume | FAIL |
| D-pillar | FAIL |
| Rear glass | NEEDS WORK |
| Lamp envelope / wrap | FAIL / NEEDS WORK |
| Tailgate broad form | FAIL |
| Bumper has real depth | PASS technically |
| Bumper corner curvature and wrap | FAIL |
| Direct rear improves | FAIL |
| Rear-quarter substantially improves | FAIL |
| Overall rear gate | **FAIL** |

Neutral clay / badgeless recognition: **FAIL**. Reflection and zebra strips expose residual flat quarter areas, glass/pillar seam discontinuities and pinched bumper corners. Added depth and curve layers do not override this judgment. **Do not activate V03.**

Remaining specific controls: H3/H4 outer-to-lower lamp transition and H5 grille junction; H8 needs a true edge-conforming fender/aperture continuation; rear upper quarter section widths versus D-pillar/glass side curves; tail-lamp inner/outer X-depth relative to the quarter; rear corner-depth interpolation and the bumper step/hatch normals. Stop at this candidate rather than hiding those errors with textures or more polygons.

## Geometry

| Metric | Final V03 |
|---|---|
| Vertex entries (mesh instances, not globally welded unique vertices) | **60,020** (V02 57,241, +4.9%) |
| Vehicle triangles | **92,007** (V02 88,528, +3.9%) |
| Vehicle mesh instances / draw calls | **65**; diagnostic actual **66 including floor**, debug off |
| Materials / textures | **5 / 0** |
| Degenerate triangles / invalid coordinates | **0 / 0** |
| Primary-surface symmetry unpaired vertices | **0** at 1e-5 m tolerance; wheel spoke pattern excluded |
| Measured coded bounds | **4.829652 × 1.860000 × 1.860000 m** |
| Nominal authored dimensions | **4.825 × 1.860 × 1.860 m**, unchanged |
| Wheelbase / tyre diameter | **2.845 / .764 m**, unchanged |
| Ground Z | ~7.2e-10 m, floating-point zero |

Independent regenerations: identical SHA256 `8bc2076d8499422481f59b3f62ee642b51ac36b31c69de5abb0856edb8606666`. Existing <100,000 triangle gate retained, not relaxed. No added dependency. No GLB export requested/performed; this remains the coded approach.

## Protection and live checks

- **Hero UNCHANGED.** Current screenshot and preserved V02 baseline use same 1000×900 viewport and 960w Hero asset. Below-navbar Hero region is **pixel-identical**. Full-image differences only x319–359/y15–32 inside the existing animated navbar car highlight; mean absolute RGB .000471985/255. No strict byte-identical navbar animation claim.
- **Navigation UNCHANGED.** Source, controls, logo, car, styles and animation unchanged. No temporary browser styling to manufacture a match.
- **Sections 03/05 OLD CARS PRESERVED.** Live JourneyDock → established loader/scene/model path unchanged. Section02 shared renderer also unchanged. No candidate import added to live application.
- **TOLI AI PASS.** Opened above a fully visible existing Section05 canvas (opacity1), local Services suggestion answered, centre hit-test confirmed dialog above scene, closed successfully. No external message sent. Screenshot `ai.jpg`.
- **Protected audit PASS:** 7,781 baseline files unchanged/missing0; 43 original reference files unchanged/missing0. Current source baseline: 376 files, six expected isolated candidate/test changes, missing0. See `protected-after.json`, `references-after.json`, `source-after.json`.
- **V02 preserved:** frozen module/test checksums equal start-of-task source. Current final snapshot checksums verified against disk.
- No activation, so activation-only mobile/tablet/desktop matrix was intentionally not run. No claim of physical-device or production-ready candidate validation.

## Technical validation

| Command/check | Actual result |
|---|---|
| `npm run typecheck` | PASS, app/node/QA projects |
| `npm run lint` | PASS, including diagnostic helper |
| `npm run build` | PASS |
| `npx vite build --config tools/3d/isuzu-mux/code-reference-car/vite.config.mjs` | PASS, preserved entries plus V03 |
| `npm test` | **52 files / 363 tests PASS** |
| Focused geometry suite | Five tests PASS, including mirrored 3D lamp boundaries, actual lamp diagnostic coordinates, unchanged wheel scale and nonfolding rear mapping |
| Geometry invalid/degenerate/deterministic checks | PASS |
| Pure curve-projection self-check | PASS, actual browser wheel anchors agree |
| Isolated browser console | No warnings/errors observed |
| Existing site errors | None observed; existing development Router future-flag warnings are not a visual quality result |
| Clay/reflection/zebra shape gates | FAIL as documented |

Production and diagnostic builds retain existing >500kB chunk-size advisories. Logs: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v03/typecheck.log`, `lint.log`, `tests.log`, `build.log`, `diagnostic-build.log`. Source tests and successful builds do not override failed recognition.

## Saved diagnostics

- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/headlight-reference-curves.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/headlight-front-comparison.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/headlight-front34-comparison.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/rear-error-map.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/rear-reference-comparison.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/rear34-reference-comparison.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/rear-quarter-closeup.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/dpillar-rear-closeup.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/taillight-curves.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/bumper-wrap-closeup.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/v02-v03-five-view.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/v03-clay-five-view.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/v03-reflection-five-view.jpg`

Additional: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v03/front-reference-overlay.jpg`, `front34-reference-overlay.jpg`, `side-reference-overlay.jpg`, `rear34-reference-overlay.jpg`, `rear-reference-overlay.jpg`, `headlight-reference-overlay.jpg`, `v03-zebra-five-view.jpg`, `reference-v03-summary.jpg`, `hero-navbar-protection.jpg`, `ai.jpg`. Raw same-camera captures in `clay/`, `reflection/`, `zebra/`, `silhouette/`. Saved frame metadata retains valid non-lamp anchors; final lamp projections are separately saved from actual V03 surfaces, not obsolete V02 quadrilaterals.

Diagnostic preview: `http://127.0.0.1:8190/Toli-2/tools/3d/isuzu-mux/code-reference-car/identity-v03.html`.

Preserved V02 preview: `http://127.0.0.1:8190/Toli-2/tools/3d/isuzu-mux/code-reference-car/identity-v02.html`.

## Files modified

- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/test/mux-coded-reference.test.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxReferenceData.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxValidation.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxVehicle.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxGeometry.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/validation.ts`

Supporting files: `identity-v02.html` (freeze V02 import only), new `identity-v03.html`, isolated `vite.config.mjs` entry; pre-edit rear error map; V03 analysis/control/projection/checksum/log files; frozen V02/final V03 snapshots; V03 render evidence; this report. All are under the authorized static project. No official logo/image asset or live section layout was modified.

## Final state

**Decision C. V03 saved, not activated. V02 preserved. Existing website cars retained.** The failed rear coupling is visible in the report rather than disguised as improvement. External vehicle model NONE; AI-generated 3D NONE; Blender/photogrammetry NONE; cost ₹0 / $0; deployment NOT PERFORMED; commit NOT PERFORMED. Protected sibling projects and original reference images UNCHANGED.

Skipped activation-only responsive/physical-device tests because recognition failed. Do not substitute V03 for the live vehicles without a further successful geometry and visual gate.
