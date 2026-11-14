# MU-X CODED IDENTITY V02

2026-11-09 — corrected existing coded candidate, five controlled iterations, isolated from production.

## Decision

**C — STILL GENERIC / MULTI-VIEW IDENTITY NOT ACHIEVED.**

Same-car resemblance: **FAIL**. Website integration: **DEFERRED**. Section 03: **OLD CAR PRESERVED**. Section 05: **OLD CAR PRESERVED**. Section 02 also unchanged.

Stop at this candidate. Five passes produced local construction/proportion improvements, but they did not achieve the user's required same-car recognition. This is not a success claim based on dimensions, topology, tests, material quality or render completion. Iteration 5 is preserved as the most useful corrected diagnostic state, alongside all earlier checkpoints and the pre-identity baseline. No further generic-generator pass or detailing was undertaken after this decision.

## Evidence and reference locks

The error map was written before geometry corrections: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/IDENTITY_ERROR_MAP_V02.md`. Existing architecture was inspected, then the five primary full-resolution silver family images were compared before editing. Compatible intermediate red fender closeup is secondary only. No latest-generation grille/rear design was mixed into the silver reference family.

| Lock | Exact supplied source |
|---|---|
| FRONT_REFERENCE | /home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-10.png |
| FRONT_34_REFERENCE | /home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-27.png |
| SIDE_REFERENCE | /home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-14.png |
| REAR_34_REFERENCE | /home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-31.png |
| REAR_REFERENCE | /home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-18.png |
| GREENHOUSE_REFERENCE | /home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-14.png |
| BONNET_REFERENCE | /home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-27.png |
| FRONT_FENDER_REFERENCE | /home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot 2026-11-08 213436.png |
| REAR_QUARTER_REFERENCE | /home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-31.png |

SHA256 locks are in `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v02/reference-locks.json`; all original reference files are unchanged. These uncalibrated photos support visible surface/outline characteristics, not factory CAD, millimetre or photogrammetric accuracy.

## What was preserved

The pre-identity Section 03/05 candidate is frozen at `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/source-snapshots/section-03-05/`. Its diagnostic HTML now imports that frozen validation module, not mutable current source. Original V01 snapshot/entry also preserved. The requested `reference-v01-v02-five-view.jpg` uses the immediately previous Section 03/05 candidate as the **pre-identity baseline**, explicitly labelled in the board; it does not silently substitute the oldest V01.

The only current factory remains `src/components/three/mux/MuxVehicle.ts`. There is no new vehicle generator, Blender workflow, model download, AI 3D or external reconstruction service. Wheels and materials reuse the existing construction. Existing live renderer imports never switched to this candidate.

## Corrected curves, sections and local influences

Full numerical before/after arrays: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v02/control-change-log.json`. Complete data and source at every pass: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/source-snapshots/identity-v02/iteration-01` through `iteration-05`; matching controls/geometry/snapshot JSON files in `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v02`. Values below are authored metres and visual estimates, not measured factory coordinates.

| Control/function | Old purpose and mismatch | Correction | Views checked and result |
|---|---|---|---|
| bonnetCentre / bonnetSide | Upper bonnet; rear limit x=-0.83 made it read too long | Rear limit -1.00; mid-rear x -1.02 to -1.18; final centre rear z 1.240, side 1.215 | Front34/side placement better; recognizable crown/roll still FAIL |
| fenderCrown / bonnetPoint / fenderTop | Independent hood/fender leading edges produced fin-like discontinuity | Shared fascia-top front roll; Coons leading correction vanishes on side boundaries | Front/front34 local improvement; corner volume remains FAIL |
| bodyStations | Upper painted door/shoulder bands too high | Independent upper-Z controls at normalized x .295/.340/.385/.440/.510/.570/.650/.720 to .656/.648/.640/.638/.640/.645/.655/.665 | Glass/body ratio better; side still NEEDS WORK; lower bands not globally scaled |
| roofCentre / roofSide | Front roof/cabin too far back | Front x -.40 to -.57; next -.15 to -.32; rear roof retained with coordinated glass edge | Front34/side/rear34 checked; crown not redesigned |
| cabinOutline / windscreen | A-root and window belt disconnected from cowl | Lower cowl x -1.00, z 1.235; upper x -.61; front painted roof anchors -.57/1.715 and -.32/1.760 | Cowl placement better; windscreen corner depth unresolved |
| frontWindow / rearWindow / quarterWindow | Shallow rectangular glass | Lower bases around 1.220/1.230/1.275; controlled upper corner trajectory; quarter rear x 2.030 | Larger glazing; generic outline and D-pillar still FAIL |
| greenhouseY / cabin | Arbitrary width profile and large triangles on a curved surface | Width derives from actual section top to roofSide, plus .008 sin curvature; one midpoint split then weld before normals | Small local subdivision only; curved projection helps, not recognition proof |
| rearGlass / screen(true) | Rear screen separate from roof and hatch | Lower z 1.220; top from actual roof cross-section; base from actual fascia top; .020 centre X bow | Boundary improves in rear/rear34; glass/hatch ratio remains wrong |
| section local influences | Fenders read as narrow strips | Front Gaussian x=-1.370, sigma=.38, upperLift=.045/lateralLift=.045; rear x=1.475, sigma=.44, .032/.035; upper-band blend only | No axle/ground movement; wheel-surround volume still insufficient |
| fasciaSections.rear / terminal blend | Flat hatch and weak lower bumper | Independent lower rows at z .39/.48/.62/.76/.95/1.15/1.22; corresponding half widths .80/.86/.88/.87/.86/.85/.79 | Rear broad envelope improves locally; bumper tangent/shape FAIL |
| grilleUpper / grilleLower / headlamp / tailLamp | Narrow generic envelopes | Upper grille half width .53 to .62, lower .48 to .53; swept headlamp lower corners .865/.825; rear lamp broad envelope revised | Front/rear broad proportions better; no tiny internals added; identity FAIL |
| fasciaPoint / final outline cleanup | Nose corner upsweep too pointed; roof painted corner mismatch | Corner Z lift .07 front / .035 rear to .025; cabin upper anchors meet roof-side data | Local highlight/edge cleanup, no camera change; reflection FAIL |

Unchanged: nominal dimensions, axles, tyre diameter, wheel construction, materials, live camera, Hero and navbar. No global whole-station scaling or doubled mesh budget.

## Five controlled iterations

BETTER/SIMILAR compare with the preceding pass (iteration 1 vs frozen pre-identity baseline). These are local visual judgments, **not recognition PASS grades**. All five views were rendered per pass. The full matrix was reviewed for regressions; no view reaches activation quality.

| Iteration | Front | Front34 | Side | Rear34 | Rear | Observation |
|---|---|---|---|---|---|---|
| 1 | BETTER | BETTER | BETTER | SIMILAR | SIMILAR | Forward cowl; lower upper door bands; shared bonnet/nose leading boundary. Still a utility-vehicle silhouette. |
| 2 | SIMILAR | BETTER | BETTER | SIMILAR | SIMILAR | Taller glazing and curved greenhouse; D-pillar remains a generic wedge. |
| 3 | SIMILAR | SIMILAR | SIMILAR | BETTER | BETTER | Local rear quarter influence and connected rear screen boundary; connection improves, recognition does not pass. |
| 4 | BETTER | SIMILAR | SIMILAR | SIMILAR | BETTER | Broader grille/headlamp envelopes; rear bumper profile depth. Identity remains failed. |
| 5 | BETTER | BETTER | SIMILAR | SIMILAR | SIMILAR | Reduced nose-corner lift and coordinated cabin/roof control corners; stubborn side and rear flattening remains. |

Iteration 5 selected for preservation: shared boundary fixes and stronger broad fascia envelopes are retained without losing the useful earlier cowl/window changes. All five snapshots remain available. There is no claim that selecting the best failed candidate makes it production ready.

## Same geometry and comparison-camera protection

All iteration checkpoints assert unchanged camera definitions and bbox-fitting code against the frozen baseline. Camera-code SHA256: `9415c526c229d810b0785eaba0f574640481a40dee7315663e4db40a66db2f8e`. FOV **34 degrees**, target `(0,0,.95)`, comparison distance slider **1.0** throughout. No camera-dependent mesh deformation, FOV/yaw fitting, image stretch or warp.

Primary diagnostic button names are `front`, `front-right`, `right`, `rear-right`, `rear`. Their negative-Y side corresponds to the supplied front-left/left/rear-left appearance; these historical button labels describe camera quadrants, and are preserved unchanged. Straight front/rear are existing perspective diagnostics, not falsely labelled calibrated orthographic renders.

Silhouettes are actual black-body renderer captures. Overlay alignment uses only approximate manually picked wheel centres and **one uniform scale plus X/Y translation** per view; zero rotation, no anisotropic scale or per-region fitting. Photo outlines and internal landmarks are approximate hand picks. All source coordinates, transform values and legends are in `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v02/overlay-registration.json`. Different reference camera pitch/foreshortening remains visible, especially in the quarter views. No IoU or precision score is presented as same-car proof. The renderer's camera stayed unchanged; overlays are inspection tools, not a workaround for geometry.

## Visual identity gates

| Gate | Result | Specific limitation |
|---|---|---|
| Overall mass | NEEDS WORK | Dimensions/wheel anchors retained, but painted lower body still too slab-like. |
| Bonnet | FAIL | Long hood/upper fender relationship and front corner rise still unlike source. |
| Front fenders | FAIL | Insufficient arch-surround volume; exposed white crescents and abrupt upper transition. |
| Bonnet/fender/cowl | FAIL | Shared nose improves construction; upper-fender/cowl tangent still does not read as one automotive surface. |
| Windscreen | NEEDS WORK | Forward lower edge improves placement; transverse corner/rake agreement still insufficient. |
| Greenhouse | FAIL | Taller glass helps, but cabin remains boxy compared with the reference. |
| Window shape | FAIL | Front/rear/quarter outlines are not the source family shape. |
| D-pillar | FAIL | Inclination, painted surround and quarter termination remain wrong. |
| Side body | NEEDS WORK | Length/wheelbase plausible; door crown and arch relationship remain generic. |
| Rear quarter | FAIL | Rear wheel surround lacks the source shoulder/quarter volume. |
| Rear 3/4 | FAIL | D-pillar/glass/tailgate/quarter depth hierarchy still generic. |
| Rear | FAIL | Rear glass/hatch height balance and lamp envelope not reconciled. |
| Bumper wrap | FAIL | Common positions do not guarantee tangent continuity; shape remains too barrel-like. |
| Clay recognition | FAIL | Unbadged neutral body is not convincingly the same MU-X. |
| Badgeless recognition | FAIL | No branding exists in candidate; removing recognition aids exposes the generic identity. |
| Reflection flow | FAIL | Side flat spots, patch-normal seams and rear recess waviness remain. |

Additional primary-view grades: **Front FAIL; Front 3/4 FAIL; Side NEEDS WORK; Rear 3/4 FAIL; Rear FAIL.** All mandatory gates have not passed. No activation.

The unresolved depth relationships are bonnet crown vs full front arch mass, cowl/A-pillar vs windscreen corner width, quarter-window/D-pillar vs rear glass, and rear shoulder/hatch/bumper wrap. Current section/patch interpretation cannot reconcile them convincingly across the supplied views. The photographs are uncalibrated, so exact depth is underdetermined, but this is **not** evidence that the references make a better model impossible. It is the limit of this candidate/pass. Further tiny detail or more triangles would not solve these primary volumes. Do not activate or automatically continue another generic refinement cycle.

## Geometry and efficiency

- Vertices: **57,241 mesh-instance vertex entries**, not a count of globally welded unique positions (previous 55,391; +3.3%).
- Vehicle triangles: **88,528** (previous 85,740; +3.3%, below existing 100,000 gate).
- Mesh instances / vehicle draw calls: **51**; actual diagnostic draw calls **52 including floor**, debug groups off.
- Materials: **5**; textures **0**, texture resolution N/A. No GLB export in this coded task.
- Invalid coordinates **0**; degenerate triangles **0**; unpaired mirrored primary-surface vertices **0** at 1e-5 m tolerance. Symmetry test excludes wheel spoke pattern.
- Measured coded bounds **4.829641 x 1.860000 x 1.860000 m**; nominal authored envelope **4.825 x 1.860 x 1.860 m**. Small broad-envelope projection offset is reported, not disguised as factory accuracy.
- Wheelbase **2.845 m**; tyre diameter **.764 m**; ground Z about **7.2e-10 m** (floating-point zero), four tyres retained.
- Deterministic SHA256 for two independent regenerations: **feed75c7b89feb3eb44aadfde367d7f84cd5e3f6b270b557c27bca75673df8e2**. Exact match.

No doors, bonnet/tailgate hinges, detailed interior/engine, sensors, wipers, badges, tiny trim, lamp internals or grille internals were added. Exterior gates failed first.

## Protection and actual browser checks

Hero: **UNCHANGED / NO INTENTIONAL CHANGE**. Viewport 1000x900 (captured 990x891) used before and after with the same 960w background asset. **Hero region below navbar is pixel-identical**. Full screenshot has only 455 differing pixels, confined to the existing animated navbar car highlight at x319–359/y15–32. Full mean absolute RGB difference 0.00054341/255. Navbar: source unchanged; tiny animation-phase variance means whole-header byte/pixel identity is **not** claimed. No styles temporarily patched and no animation disabled to manufacture equality.

Protected checksum audit: **7,781 files checked, 0 changed, 0 missing**, covering supplied references, protected sibling projects and baseline historical/source assets. Current task source baseline: **368 files checked; 6 changed; 0 missing**. Only isolated candidate source/test changed. Hero/navbar/CSS/live section code/loaders/public vehicle assets unchanged. Exact manifests: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v02/protected-after.json` and `source-after.json`.

Section 03 / HowItWorks and Section 05 / CtaBanner still use JourneyDock → shared load-vehicle-scene / vehicle-scene → existing model manifest. Section 02 shares that established renderer and remains unchanged. Current coded factory is only reached by the isolated diagnostic validation entry and test; no homepage import path was changed.

TOLI AI: **PASS**. Opened over the actual Section 05 existing-vehicle scene, clicked local Services suggestion, received service-category reply; DOM centre hit-test confirms dialog above scene. Closed successfully. Screenshot `ai.jpg`. No message sent externally. Candidate has no live canvas to intercept assistant input.

Activation-dependent seven-viewport 03/05 responsive matrix: **NOT RUN for this candidate**, because activation was rejected. No claim of mobile production readiness. Existing unchanged responsive protections are covered by the full suite and source checks, not falsely presented as fresh physical-device testing.

## Validation — actual results

| Check | Result |
|---|---|
| `npm run typecheck` | PASS — app, node and QA TypeScript projects |
| `npm run lint` | PASS |
| `npm run build` | PASS — actual production static-site build |
| `npx vite build --config tools/3d/isuzu-mux/code-reference-car/vite.config.mjs` | PASS — original V01, frozen Section03/05 and Identity V02 diagnostic entries |
| `npm test` | PASS — **52 test files / 361 tests** |
| Deterministic geometry | PASS — both regenerations identical; all five checkpoint tests pass |
| Browser diagnostics | PASS — all five cameras in five passes, clay/reflection/wireframe/silhouette; zero diagnostic console warnings/errors |
| Existing site browser | No console errors observed; two existing React Router future-flag warnings in development |
| Hero/nav visual protection | PASS for no intentional change; exact pixel/animation qualifications above |
| Protected files | PASS — 7,781 baseline files unchanged |
| Same-car visual gate | **FAIL** — tests do not override this |

Both production builds retain the existing >500kB chunk warning; no extra library was added. Logs are saved at `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/analysis/identity-v02`: `typecheck.log`, `lint.log`, `tests.log`, `build.log`, `diagnostic-build.log`.

Diagnostic preview (local development, not deployed):
`http://127.0.0.1:8190/Toli-2/tools/3d/isuzu-mux/code-reference-car/identity-v02.html`

Homepage preserved:
`http://127.0.0.1:8190/Toli-2/`

## Render paths

- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/identity-error-map.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/reference-v01-v02-five-view.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/iterations-five-view.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/front-reference-overlay.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/front34-reference-overlay.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/side-reference-overlay.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/rear34-reference-overlay.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/rear-reference-overlay.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/internal-landmarks.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/clay-five-view.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/reflection-five-view.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/wireframe-five-view.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/front34-closeup.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/greenhouse-closeup.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/dpillar-closeup.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/rear34-closeup.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/hero-regression.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/navigation-regression.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/ai.jpg`

Raw five-view captures and per-frame actual projected landmarks/stats: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/renders/identity-v02/iteration-01/` through `iteration-05/`. Raw reflection/wireframe/silhouette captures in matching subdirectories. Closeups are labelled native crops of the same render, not differently tuned perspective shots. Section03/05 final activated screenshots: **N/A — candidate not activated**.

## Files modified and saved

Current source files changed against start-of-task baseline:
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/test/mux-coded-reference.test.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxReferenceData.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxValidation.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxVehicle.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxGeometry.ts`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/validation.ts`

Supporting isolated files: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-reference-car/identity-v02.html`, `section-03-05.html` (freeze old import), `vite.config.mjs` (diagnostic inputs only), `analysis/IDENTITY_ERROR_MAP_V02.md`; `analysis/identity-v02/` controls/checkpoints/manifests/logs/evidence scripts; versioned `source-snapshots/section-03-05/` and `source-snapshots/identity-v02/`; `renders/identity-v02/`; this report. Isolated build output is local diagnostic output only.

All edits saved to disk. Separate 3D website and original project: **UNCHANGED**. Original references: **UNCHANGED**. External vehicle model **NONE**. AI-generated 3D **NONE**. Cost **₹0 / $0**. Deployment **NOT PERFORMED**. Git commit **NOT PERFORMED**.

## Remaining limitation / handoff

Preserve V02 and baseline; do not expose it in 03/05. Remaining work is primary exterior depth and volume, not texture/badge polish. This five-pass attempt stops with Decision C. Physical-device performance and activation-specific responsive checks were not performed because the identity gate failed.
