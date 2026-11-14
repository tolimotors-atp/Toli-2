# Curve-first MU-X — first construction gate

**Decision C — CURVE APPROACH DID NOT IMPROVE THE VEHICLE.** The curve engine works, but this first curve dataset does not yet recover the original MU-X cut. Stop before surface generation. This is a saved construction-network milestone, not a new complete vehicle.

## Source and preservation

Scene: `tools/3d/isuzu-mux/source/production/isuzu-mux-curve-generated-v01.blend`.

Current add-on: `tools/blender-addons/toli_mux_generator/`. Prior V02 add-on preserved under `tools/3d/isuzu-mux/code-generator/v02-addon/`; earlier V01 archive, V01/V02 blend files, V04, audits and experiments remain intact. No V04 geometry was read into the new curve network. All code edits are in the target static project. No Hero/navigation/TOLI AI/application edits, controlled-capture changes, production GLB overwrite, protected-project changes, deployment or Git commit. ₹0 / $0; no purchased geometry, cloud processing or paid API.

## Architecture and UI

- `mux_curve_data.py`: normalized named 3D Bezier control polygons and source associations. X/length, Y/half-width, Z/height.
- `geometry/curves.py`: reusable curve creation, paired mirror generation, axle-derived arch curves and transverse guide curves. Real Blender Bezier datablocks are generated first; existing V02 mesh sections are not the new body source.
- `curve_ui.py`: Generate/Regenerate Construction Curves, reference/curve visibility, curve-render operator. Existing V02 collection, if present, is hidden rather than deleted. Start with an empty scene for isolated diagnostics.
- `parameters.py`: Show Construction Curves and four reference toggles; existing dimensional/curve controls feed normalized points.
- `panels.py`, `__init__.py`, `run_milestone.py`: current UI/default runner now curve-first. Legacy surface implementation remains preserved but is not presented as the next approved step.
- `run_curve.py`: separate scene, deterministic regeneration, fixed five-view cameras, saved construction milestone and renders.
- `check_curve.py`: registered-operator, mode, parameter, handle reproducibility and unpacked reference tests.
- `boards_curve.py`: five-view board and approximate photographic overlays.

Bezier AUTO handles are supported by the installed Blender 5.2.2. No NURBS were added simply to satisfy a technology list; these first constraints do not yet justify a NURBS surface system. Direct tangent/handle constraints and a shared endpoint registry are **not implemented**; AUTO tangents alone are not G1 continuity across separate curves. That is a real limitation of this first gate.

The UI exposes bonnet center-height, roof crown, shoulder/belt height, fender crown, windscreen run and rear taper, plus dimensions and tire diameter. These act on curve data rather than generated mesh vertices. They are coarse controls, not a certified safe parameter range. Right-side names for explicit LEFT curves use RIGHT; other paired curves use MIRROR suffixes.

Reference toggles create local Blender image empties (front, side, rear, front three-quarter), not packed image binaries or exportable vehicle geometry. They are viewport references, not rendered or camera-calibrated planes. Files remain linked to the authoritative folder; nothing is embedded, uploaded or altered. User manual curve edits remain diagnostic only and are replaced by regeneration.

## Reference decisions

The existing 18-image atlas and original reference decisions were retained. Main shape constraints use the compatible older silver closed-body screenshot set. Front/bonnet: 2026-11-06 **18-17-10 / 18-17-27**. Side, belt, arches and roof: **18-17-14 / 18-17-21**, checked against front and rear three-quarter views. Rear, quarter glass and D-pillar: **18-17-18 / 18-17-31 / 18-17-35**. Open-panel images provide structural context only; interior/engine images do not control closed exterior curves. Promotional/differing-generation imagery is not averaged into the network.

Normalized points are **VISUAL APPROXIMATIONS informed by those views**, not calibrated traced coordinates or factory CAD. Existing image ratios remain contextual evidence. The station guides are still coarse transverse constraints and are not claimed to reproduce exact MU-X sections. No photogrammetric solve or exact camera matching was performed.

## Generated network and tests

**61 curves, 315 Bezier control points.** Side master, bonnet center/edges/front/rear, shoulder, belt, lower body, sill, windscreen boundaries, A-pillars, roof center/edges, side-window envelope, quarter-glass boundaries, D-pillars, front/rear arch and fender crown, rear-quarter return, rear glass, tailgate, lamp envelopes, grille envelopes and bumper guides are present. Seven transverse guide curves supplement the longitudinal network.

Curve-control symmetry: **PASS, 0 m reported discrepancy**, replacing the historic 1.61 mm issue. Coordinates are mirrored from one side using one centerline. The .0001 m validation threshold was not increased. This is a control-network result, not a claim about future lofted-surface symmetry.

The regression check also rejects duplicate partial-spline objects. A caught first-run implementation bug created such duplicates; it was fixed before the final saved milestone and evidence.

Registered Generate/Regenerate operator: PASS. Show Construction Curves: PASS. Reference toggle creates an unpacked linked original: PASS. Delete/recreate curves, including generated Bezier handles: PASS. Preview/Quality retain identical design/control/handle fingerprints: PASS. Quality doubles curve evaluation resolution from 12 to 24. Changing bonnet control changes the generated fingerprint: PASS. Saved tests: `addon-tests.json`.

No finished surfaces exist. Preview/Quality vehicle-mesh vertices/triangles: **N/A (not generated)**. Construction tube bevels exist only to make curves render; they are not a vehicle mesh. Non-manifold/degenerate vehicle-surface counts: **N/A**. Surface deletion/regeneration and overall curves-plus-surfaces reproducibility: **NOT REACHED**, not a false PASS.

The curve-only runner uses the supplied baseline dimensions for scaling; it does not certify overall car dimensions from decorative curve extremities. Individual fascia curves can project beyond nominal body length; that needs correction before a surface bound can be accepted.

## First curve gate — NEEDS WORK

All following regions are **NEEDS WORK**: side master, bonnet, front fender, wheel arches, windscreen, roof, shoulder, side glass, quarter glass, D-pillar, rear quarter and rear profile. Presence of a named spline does not establish a reference match.

Five curve renders reveal unresolved issues: front envelope curves are too rounded and poorly seated; bonnet/cowl transitions do not share exact boundaries; generic transverse guides cross the intended cabin/shoulder network; quarter-glass and D-pillar terminations lack a coherent common boundary; rear returns still read as a generic SUV. The network suggests broad proportions but not original MU-X surface character. The first curve gate is not acceptable for lofting.

**Front / front-three-quarter / side / rear-three-quarter / rear curve-to-reference checks: NEEDS WORK.** Qualitative visible identity evidence against V04: **WORSE in all five views and overall**. A full 3D surface-volume comparison is not evaluable because a surface was deliberately not generated. No claim that a curve diagram is directly equivalent to a finished V04 mesh.

Surface construction method/regions/shared boundaries/G1 continuity: **NOT REACHED**. Shared boundary enforcement is missing in the current network, which is a reason for stopping. Bonnet, fenders, side, greenhouse, rear cabin and rear original-cut gates: **NEEDS WORK**. Clay, reflection-strip finish and surface-flow inspection: **NOT REACHED**, because the required curve gate failed. No lamp internals, badges, handles, interior, engine or moving panels were added to hide this failure.

## Diagnostics

Directory: `tools/3d/isuzu-mux/code-generator/renders/curve-validation/`.

- `front.png`, `front34.png`, `side.png`, `rear34.png`, `rear.png`: construction curves only.
- `reference-v04-curves.jpg`: reference | V04 | construction network for five views.
- `overlay-front.jpg`, `overlay-front34.jpg`, `overlay-side.jpg`, `overlay-rear34.jpg`, `overlay-rear.jpg`: reference plus curve raster.
- `region-bonnet.jpg`, `region-front-fender.jpg`, `region-windscreen-a-pillar.jpg`, `region-side-shoulder.jpg`, `region-quarter-glass-d-pillar.jpg`, `region-rear-quarter.jpg`, `region-rear.jpg`: enlarged overlay crops for local inspection. They inherit the approximate overlay alignment, not an exact regional fit.
- `validation.json`, `addon-tests.json`: actual checks.

Overlays fit the transparent curve render into a manually chosen photographic vehicle rectangle, preserving aspect ratio. They are visibly labeled **approximate 2D box-fit, not solved photo cameras**. They expose qualitative curve errors but cannot establish camera-calibrated agreement, a measured reconstruction error or exact depth. No automated silhouette-score claims.

## Stop decision

**C — CURVE APPROACH DID NOT IMPROVE THE VEHICLE.** Preserve this engine and failed-gate evidence; do not loft or detail it. The next meaningful curve pass would require exact shared boundary/end-point constraints, reference-specific tangent/handle data and corrected front/cabin/rear envelopes, then a new curve-only gate. Do not simply turn this unapproved wire network into a body.

GLB **NOT EXPORTED**. Website **NOT UPDATED**; existing V04 remains active. Hero/navigation/TOLI AI unchanged. Controlled capture preserved. Protected projects unchanged. No deployment or commit. Website tests were not rerun because no website source or production asset changed.
