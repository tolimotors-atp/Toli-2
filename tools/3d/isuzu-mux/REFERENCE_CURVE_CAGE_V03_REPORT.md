# Curve cage V03 — join and surface-flow review

**Decision B — V03 IMPROVES THE JOINS BUT SPECIFIC REGIONS STILL REQUIRE CURVE TUNING.**

Blender **5.2.2 LTS**, executable `/usr/bin/blender`. V01/V02 source files, V01/V02 diagnostic folders, original V02 construction code and native trace data are preserved. This pass modifies local curve flow over V02; it does not restart the body or generate body surfaces.

## Join results

|Join|Visual verdict|Change and remaining limitation|
|---|---|---|
|J01 bonnet/fender|IMPROVED-BUT-NEEDS-WORK|Five transverse bonnet sections now include fender roll; the bridge crosses the body rather than borrowing longitudinal tangent directions. Crown-to-fender strength and leading corner still need tuning.|
|J02 cowl/A pillar|IMPROVED-BUT-NEEDS-WORK|Cowl-root blend and bowed lower screen connect existing anchors. Pillar-root thickness and cowl contour still need a better reference match.|
|J03 A pillar/roof|PASS|Exact shared endpoints and endpoint handles retained. Neighbouring handle lengths change as part of lower-pillar/rear-roof work; the broad passing visual join is retained, not certified as G2.|
|J04 roof/D pillar|IMPROVED-BUT-NEEDS-WORK|Nonlinear roof handles, shared tangent and flared D-pillar base; new D-body section. Pillar termination and glass/frame shape remain too schematic.|
|J05 shoulder/rear quarter|IMPROVED-BUT-NEEDS-WORK|Shoulder now reaches a shared quarter/lamp anchor. Asymmetric axle-centred rear-crown influence and compatible continuation replace a detached tiny bridge. Quarter crown/shoulder hierarchy still requires tuning.|
|J06 quarter/lamp|IMPROVED-BUT-NEEDS-WORK|Lamp wrap revised in X; quarter and outer lower lamp share an anchor; lamp envelope remains a defined cut. Upper lamp/quarter integration still unresolved.|
|J07 quarter/bumper|IMPROVED-BUT-NEEDS-WORK|Quarter and bumper share an anchor, with separate upper/main/lower depth and coherent returns. Bumper width progression and corner curvature still require tuning.|
|J08 D pillar/rear|IMPROVED-BUT-NEEDS-WORK|D base, glass rake/lower width and rear sections coordinated. Tailgate/glass/quarter composition is not yet reference-convincing.|

These are visual decisions after reviewing main and enlarged local comparisons. Numeric continuity does not automatically promote a join to PASS.

## Five-view comparison versus V02

|View|Result|Assessment|
|---|---|---|
|Front|SIMILAR|More coherent bonnet/fender section scaffold and front corner connection; front identity envelopes are largely retained, not visibly resolved enough for surface approval.|
|Front 3/4|BETTER|Bonnet roll and fender/shoulder/cowl relationships are clearer.|
|Side|SIMILAR|Main silhouette, side-window geometry, roof/bonnet centre rails and wheel anchors remain protected. Local shoulder/rear guide changes do not replace the main silhouette. The D-body section was lowered to fit the rear-roof envelope and lower bumper guides were tucked inward after visual review.|
|Rear 3/4|BETTER|Pillar flare, shared shoulder/quarter anchor, lamp wrap and layered bumper read more coherently.|
|Rear|SIMILAR|New rear sections clarify depth/width, but glass/lamp/bumper identity needs further tuning.|

The rear-three-quarter reference is the compatible `18-17-31` image, matching the rendered side orientation. No photograph was mirrored or mixed with an incompatible body generation. Front/side/rear references remain the same compatible family. Cage cameras, lighting and comparison crop windows match between V02 and V03. Reference camera poses are not calibrated or fitted.

## Surface-flow assessment

- **Bonnet:** broad crown continues into an explicit edge roll, rather than ending at an isolated edge.
- **Front fender:** transverse roll and longitudinal shoulder guide now have distinct functions; exact fender strength remains unresolved.
- **Cowl:** common existing root and modest lower-screen bow, with a local blend guide; the reference-defined rake break remains.
- **Greenhouse:** principal window geometry unchanged, with local pillar/glass integration improved.
- **Roof:** existing position/crown retained; chord-length-aware handle progression and rear transition refined.
- **Shoulder:** smoother rear-door approach to quarter volume; now shares its downstream anchor.
- **Rear quarter:** axle-centred influence has different front/rear falloff; does not move the wheel or uniformly squeeze the rear body.
- **Rear body:** additional D/glass, lamp, tailgate and upper/lower bumper sections explain the intended volume; still not a finished surface scaffold.

## Curvature-aware diagnostics

`curvature-audit.json` samples cubic derivatives/curvature before and after every internal control junction of the relevant curves. `curvature-v02.json` retains the equivalent baseline. `cage-validation.json` contains actual cross-rail join samples and character-cut classification. Curvature values are in the nominal model scale, not measurements of the real vehicle.

|Cross-rail continuation|V02 gap → V03 gap, nominal m|Relative endpoint-curvature jump V02 → V03|
|---|---:|---:|
|J03|0 → 0|0.904 → 0.847|
|J04|0 → 0|0.312 → 0.301|
|J05|0.068746 → 0|0.593 → 0.103|
|J07|0.106506 → 0|0.153 → 0.490|

The old V02 bridge-endpoint audit passed; the gaps above measure the actual adjacent rail anchors, a different and more useful constraint. J07 connectivity improves while its relative curvature jump increases: this remains visible in the report, not hidden or called a curvature pass. J03 retains its passing positional/tangent geometry but still has a substantial curvature trend change. No G2 claim is made.

A heuristic flags relative internal curvature jumps above 65% for review. There are **43 warning records**, including repeated curve/junction entries referenced by more than one join and intentional cuts. They are retained in `curvature-warnings.json`, not suppressed or used as automatic visual verdicts. Highest sampled internal curvature is approximately 33.20 per nominal metre. Cross-join J03 samples peak around 34.81. Both need contextual review, not automatic smoothing.

`flow-normal-proxies.json` uses longitudinal/transverse guide-tangent cross-products at the five bonnet stations. Adjacent proxy directions vary approximately **2.75–5.78 degrees**. These are implied cage directions, not actual surface normals; no body faces exist.

Optional **Curvature Combs** cover bonnet edge, front fender crown, shoulder, roof edge, D pillar and rear-quarter return. Comb length is capped at 0.12 nominal units for display, so numeric sampling remains the authoritative diagnostic for large values. **Join Debug** isolates the selected join, neighbouring curves, relevant width station and applicable wheel pair. All eight selections and restoration of previous visibility were tested. Reference planes remain available outside the isolated view. Diagnostic visibility changes do not delete geometry.

## Preserved foundation and control-point policy

Length/width/height parameters, wheelbase, wheel centres, tire size, main silhouette, side-window envelope, bonnet/roof centre rails, eight stations and seven independent width levels remain unchanged. J03 shared endpoints and handles are restored exactly after neighbouring edits. Existing controls and handles were refined first.

The five bonnet sections remain five sections. Each grows from five to nine controls because the old section could represent the bonnet crown/edge but had no separate outer fender and roll controls. Two necessary roll/fender controls per side were added. Existing longitudinal curves keep their point counts. New section curves are limited to the requested D/glass, lamp, tailgate and upper/lower bumper diagnostics; local cowl/fender/corner guides express the specifically requested transitions. No detail geometry, new body type, interior or opening systems were added.

## Validation

- Reproducible delete/regenerate of curve coordinates, explicit handles and diagnostic base colours: **PASS**.
- J03 shared endpoint/handle preservation: **PASS**.
- Main side silhouette/window/centre-rail preservation: **PASS**.
- Four wheel anchors/tire dimensions: **PASS**.
- Five bonnet-section count: **PASS**.
- Join Debug selections J01–J08 / visibility restoration: **PASS**.
- Curvature Comb toggle and finite curvature sampling: **PASS**.
- Cage control-point symmetry: **0 mm**, without relaxing tolerance.
- Python source parse check: **PASS**.
- Preview topology regression: **0 degenerates / 0 non-manifold edges**.
- Quality topology regression: **0 degenerates / 0 non-manifold edges**.

Topology results refer to the unchanged legacy soft-body regression only: Preview 5,166 vertices / 10,296 triangles; Quality 12,638 vertices / 25,240 triangles. V03 contains curves, not approved body topology. No threshold was loosened. Website build/browser/lint checks were not run because no website source or assets changed.

## Artifacts

Source:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v03.blend`

Main comparison:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v03/reference-v02-v03-comparison.jpg`

Seven-join comparison:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v03/join-comparison.jpg`

Depth sections:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v03/depth-sections-v03.jpg`

Individual `join-j01.jpg`, `join-j02.jpg`, `join-j04.jpg`, `join-j05.jpg`, `join-j06.jpg`, `join-j07.jpg`, `join-j08.jpg` are saved alongside the board. Each uses dedicated 1100 × 700 matched local camera renders in `joins/v02/` and `joins/v03/`, rather than upscaling tiny main-view crops. The comparison panel photos are local reference evidence, not pixel-registered overlays. Full five-view render pairs are in the same folder and `baseline-v02/`. Native registration overlays are supplemental, not camera calibration proof.

## Reproduction

From the static project:

```
blender -b --python tools/blender-addons/toli_mux_generator/run_cage_v03.py
blender -b --python tools/blender-addons/toli_mux_generator/check_cage_v03.py
blender -b --python tools/blender-addons/toli_mux_generator/diagnostics_cage_v03.py
blender -b --python tools/blender-addons/toli_mux_generator/join_evidence_v03.py
blender -b --python tools/blender-addons/toli_mux_generator/render_joins_v03.py
python tools/blender-addons/toli_mux_generator/boards_cage_v03.py
```

V02 is read for comparison only; output/save locations are confined to V03 artifacts. The archived V02 add-on remains under `tools/3d/isuzu-mux/code-generator/reference-cage-v02-addon/`.

Existing add-on files modified: `cage_ui.py`, `parameters.py`, `panels.py`. New files: `geometry/flow_cage.py`, `join_debug.py`, `run_cage_v03.py`, `check_cage_v03.py`, `diagnostics_cage_v03.py`, `join_evidence_v03.py`, `render_joins_v03.py`, `boards_cage_v03.py`. Old V02 depth generator and original trace data are unchanged.

## Final stop state

**Surfacing: NOT STARTED. Deep detailing: NOT STARTED. Website: UNCHANGED. GLB: NOT EXPORTED. Hero/navigation/TOLI AI: UNCHANGED. Controlled capture: PRESERVED. Protected sibling projects: UNCHANGED / NO WRITES. Cost: ₹0 / $0. Deployment: NOT PERFORMED. Git commit: NOT PERFORMED.**

`preservation.json` records before/after hashes of static source/public files, controlled-capture files, V01/V02 source files and V01/V02 diagnostics. No protected sibling paths were written. Depth remains inferred from uncontrolled photographs; V03 is not an exact or camera-calibrated reconstruction. Stop here for cage review. A future pass must resolve J01/J02 and the rear pillar/lamp/bumper composition before first surface patches.
