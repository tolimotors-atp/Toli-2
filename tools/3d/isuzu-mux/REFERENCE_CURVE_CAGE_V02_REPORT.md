# Curve cage V02 — decision B

**V02 IS IMPROVED BUT SPECIFIC DEPTH/JOIN REGIONS STILL REQUIRE TUNING.**

Blender 5.2.2 LTS, `/usr/bin/blender`. This is a curve cage, not a finished vehicle or surface-quality approval. Reviewed front, front three-quarter, side, rear three-quarter, rear and transverse diagnostics against the canonical compatible silver reference family. No incompatible newer-body details imported. Depth remains inferred from uncontrolled photographs, not calibrated or millimetre-accurate.

## Improvements and remaining work

|Region|Change|Remaining limitation|
|---|---|---|
|Front depth|Separate bonnet, lamps, grille, lower intake and bumper X positions; curved outer returns|Face-to-side transitions still need a less schematic flow|
|Front three-quarter|Five bonnet sections and explicit outer fender wrap guides make depth legible|Bonnet/fender/corner junction is not yet a convincing surface scaffold|
|Bonnet crown|Leading / 25% / 50% / 75% / cowl sections anchor centre and outer rail heights, with intermediate falloff|Crown distribution is estimated; leading edge needs tuning|
|Front fender|Arch and crown retained; three transverse wraps added around fixed wheel; bonnet/door bridges|Local curvature and bonnet-side integration need work|
|Greenhouse|Lower/upper windscreen registered to cowl/roof; mid-windscreen and front/B/C/D roof sections|Pillar thickness and transverse crown remain envelope-level|
|D pillar|Shared roof endpoint and tangent, independent rear greenhouse width; glass return|Rake/depth relationship to quarter glass remains insufficiently specific|
|Rear quarter|Independent shoulder trajectory, fixed-wheel wraps, lamp and bumper connections|Quarter/lamp transitions still read as connected guide wires|
|Rear depth|Raked rear glass, separate lamp/tailgate/bumper X layers and return curves|Tailgate/quarter and glass junction still require volumetric refinement|

## Preservation and width stations

Main side silhouette, bonnet centre, front/rear side windows and quarter-glass X/Z coordinates remain locked to V01. Overall length, wheelbase, roof and bonnet rail lengths, wheel centres/radius/width unchanged. Named A-pillar endpoints and the D-pillar upper endpoint were registered to existing bonnet/roof points; maximum local join edit is approximately 0.142 in the nominal family-scale coordinate system. This is not a measured real-vehicle error. No other side tracing restart.

Eight stations: front bumper, front wheel, cowl, B pillar, C pillar, rear wheel, lamp, rear bumper. Each has seven independently authored half-width values: sill, lower body, maximum body, shoulder, belt, greenhouse and roof. Smoothstep interpolation is used between stations; roof/window taper is not a constant multiple of body taper. Exact values are in `cage-validation.json` and `geometry/depth_cage.py`. These are inferred constraints, not measured dimensions. Width-station debug polylines use fixed level heights for comparing width controls; they are not finished body slices and do not certify bumper/roof occupancy.

`Show Width Stations` and `Width Station` in the Blender sidebar expose optional individual/all transverse profiles. Near-side curves are dominant and mirrored far-side curves subdued through materials; all geometry remains present. Wheel axles and centreline remain visible. No surfaces generated.

## J01–J08 audit

All registered endpoint gaps and depth discrepancies are zero. Soft-join handle directions are collinear to measured precision; intentional character cuts are not forced to G1. These numeric checks do not establish reference-correct surface flow.

|Join|Type|Visual result|Reason|
|---|---|---|---|
|J01 bonnet/fender|Soft bridge|NEEDS WORK|Shared endpoints/tangents exist, but bridge shape and fender falloff remain estimated|
|J02 cowl/A pillar|Character cut|NEEDS WORK|Common cowl point; cowl breadth and pillar foot still need refinement|
|J03 A pillar/roof|Soft|PASS|Common roof anchor with compatible tangent; broad side envelope retained|
|J04 roof/D pillar|Soft|NEEDS WORK|Common endpoint/tangent; D-pillar identity/rake/depth still insufficient|
|J05 shoulder/rear quarter|Soft bridge|NEEDS WORK|Endpoint/tangent continuity fixed; rear-quarter bulge flow unresolved|
|J06 rear quarter/lamp|Character cut|NEEDS WORK|Shared connection; lamp wrap into quarter needs another pass|
|J07 rear quarter/bumper|Soft bridge|NEEDS WORK|Dedicated curved return; corner flow not yet convincing|
|J08 D pillar/rear|Character cut|NEEDS WORK|Glass return connected; glass/quarter/tailgate relationship still estimated|

Mechanical measurements for every join and the windscreen/roof are in `cage-validation.json`. The join verdicts above are visual, stricter than endpoint checks.

## Reference comparison versus V01

Front: **SIMILAR** — source face envelopes retained; section scaffolding added.

Front three-quarter: **BETTER** — visible crown, outer volume and face layering, still below surfacing gate.

Side: **SIMILAR** — strong traced outline and glazing preserved; local join changes only.

Rear three-quarter: **BETTER** — independent width taper, raked glass and corner returns, still needs tuning.

Rear: **SIMILAR** — compatible face outlines preserved; transverse guides add diagnostic information.

`reference-v01-v02-comparison.jpg` contains all five views at 2400 × 2810. Baseline V01 re-rendered from its preserved source into this V02 diagnostic folder, never overwriting V01. Cameras, lights and crop windows match between cages; V02 additionally subdues far-side geometry as requested. Reference photographs are perspective views, not fitted cameras. Native front/side/rear overlays compare source landmarks in amber to V02 registered control polygons in cyan; not a camera-reprojection accuracy claim. `depth-sections.jpg` plots actual saved Y/Z controls, not a body surface.

## Checks

- Delete/regenerate from code, including explicit control handles: PASS.
- Main side silhouette/window X/Z preservation: PASS.
- Four fixed wheel anchors: PASS.
- Cage control-point symmetry: **0 mm**, unchanged tolerance.
- Independent width profiles and five crowned bonnet sections: PASS.
- Registered Blender action, cage-only toggle and individual section visibility: PASS.
- J01–J08 endpoint and compatible soft-handle checks: PASS mechanically; visual verdicts remain above.
- Preview topology regression: **0 degenerate faces / 0 non-manifold edges**.
- Quality topology regression: **0 degenerate faces / 0 non-manifold edges**.

Topology numbers apply to the unchanged legacy soft-body generator regression, not to a surfaced V02 body. No V02 body faces exist to approve. Detailed counts remain in `topology-regression.json`. No area-threshold or symmetry-tolerance relaxation. No website build, browser testing or deployment needed/performed because website source/assets were not modified.

## Saved outputs and reproduction

- Source: `tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v02.blend`
- Five-view comparison: `tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v02/reference-v01-v02-comparison.jpg`
- Sections: `tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v02/depth-sections.jpg`
- Per-view renders: `front.png`, `front34.png`, `side.png`, `rear34.png`, `rear.png` in the same folder.
- Native overlays: `native-traces-front.jpg`, `native-traces-side.jpg`, `native-traces-rear.jpg`.
- V01 add-on snapshot: `tools/3d/isuzu-mux/code-generator/reference-cage-v01-addon/`.

Run from the static project:

```
blender -b --python tools/blender-addons/toli_mux_generator/run_cage_v02.py
blender -b --python tools/blender-addons/toli_mux_generator/check_cage_v02.py
blender -b --python tools/blender-addons/toli_mux_generator/diagnostics_cage_v02.py
python tools/blender-addons/toli_mux_generator/boards_cage_v02.py
```

## Files changed

Existing add-on: `cage_ui.py` (V02 action/section visibility), `parameters.py` (optional station controls), `panels.py` (expose requested controls).

New add-on files: `geometry/depth_cage.py`, `run_cage_v02.py`, `check_cage_v02.py`, `diagnostics_cage_v02.py`, `boards_cage_v02.py`. New source, report, diagnostics and archived V01 add-on only. Original `reference_cage.py` / `traced_data.py` remain unchanged.

## Stop state

Surfacing: **NOT STARTED**. Deep detailing: **NOT STARTED**. GLB: **NOT EXPORTED**. Website/Hero/navigation/TOLI AI: **UNCHANGED**. Controlled capture: **PRESERVED**. Protected sibling projects: **UNCHANGED / NO WRITES**. Cost: **₹0 / $0**. Deployment: **NOT PERFORMED**. Git commit: **NOT PERFORMED**.

Existing website/public and controlled-capture files and V01 source were hash-checked before/after (`preservation.json`). No protected sibling paths were written. Do not activate or surface this cage based on code/test success; the specific visual issues above require another cage review.
