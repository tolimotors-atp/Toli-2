# Curve cage V04 — final reference-convergence review

## Decision C

**V04 REGRESSED OR THE CURRENT CURVE-CAGE METHOD HAS REACHED ITS USEFUL LIMIT.**

The applicable branch is **method limit**, not a claim that the main silhouette regressed. Frontal width relationships improved and an artificial rear-glass centre loop was removed. However, the enlarged comparisons do not show a single reference-convincing bonnet/fender/cowl or rear-pillar/quarter/lamp/bumper form. Calling this “close enough” or passing seven joins would be misleading. Parameter-only tuning of independently projected outlines has reached its useful limit in this representation.

**STOP: no V05, no surfacing, no detailing, no GLB, no integration.** V04 is preserved for review. Blender 5.2.2 LTS at `/usr/bin/blender`. All earlier sources and diagnostic folders are preserved.

## Join gate

|Join|Verdict|What changed; what still prevents PASS|
|---|---|---|
|J01 bonnet/fender|NEEDS WORK — NOT PASSED|Roll drop reduced from .120 to .095 nominal units, intermediate roll from .035 to .026; existing bridge tuned. Bonnet edge, front face and fender crown still do not describe a consistently reference-matched compound volume.|
|J02 cowl/A pillar|NEEDS WORK — NOT PASSED|Painted cowl half-width .790 and separate narrower inner screen establish frame allowance. Lower pillar depth, cowl rake/height and fender relationship remain estimated; the pillar is not convincingly planted as in the photo.|
|J03 A pillar/roof|PASS|V03 shared endpoint coordinates and endpoint handles restored exactly. No visual regression identified at the established local join. Not a G2 certification.|
|J04 roof/D pillar|NEEDS WORK — NOT PASSED|D middle/base half-width .735/.820; shorter quarter-glass corner handles and balanced soft continuation. The rear upper frame remains too generic and its thickness/termination does not closely follow the reference in 3/4.|
|J05 shoulder/rear quarter|NEEDS WORK — NOT PASSED|Reduced competing crown peak; asymmetric .48/.68 falloff and stronger shared continuation. The arch/crown/shoulder still read as separate guide systems rather than a fully defined rear-quarter mass.|
|J06 quarter/lamp|NEEDS WORK — NOT PASSED|Outer/inner lamp spans fitted, outer wrap depth bounded and corner handles tightened. The lamp/quarter/hatch transition is still schematic and too loop-like in 3/4.|
|J07 quarter/bumper|NEEDS WORK — NOT PASSED|Broader upper/lower bumper, matching sections and bounded handle balancing. Lower return still folds tightly toward a separate trim guide; depth and section flow are not convincingly reference-defined.|
|J08 D pillar/rear body|NEEDS WORK — NOT PASSED|Rear glass broadened; the same six controls reordered into an open mirrored half-perimeter, eliminating the false centre closure. D pillar, glass, hatch and lamp boundaries still lack a unified 3D composition.|

Visual verdicts are independent of endpoint gaps, tangent alignment or warning counts. J03 remains the protected local result. All other requested PASS targets were attempted but were not achieved.

## Five-view comparison versus V03

|View|Verdict|Evidence|
|---|---|---|
|Front|BETTER|More appropriate headlamp gap, grille width, lower intake position/width and inner-screen proportion.|
|Front 3/4|SIMILAR|Prior depth foundation preserved; the small roll/cowl changes do not resolve the reference-critical volume.|
|Side|SIMILAR|Main side silhouette, wheel anchors and principal side-window controls preserved. Local rear/cowl guides only.|
|Rear 3/4|SIMILAR|Cleaner glass boundary and bounded wrap changes; rear-quarter mass and pillar/lamp depth remain unresolved.|
|Rear|BETTER|False aperture centre loop removed; glass, lamp and bumper widths closer to the photographed composition.|

This is a modest image-space improvement, not a successful final body reconstruction. V04 does not meet the all-join surface gate.

## Front proportion correction

Body normalization: paired visible front-body landmarks **377..717 = 340 px**, excluding mirrors. Feature centres differ because of perspective/yaw; they were not forced to one photographic centre. Ratios are approximate image-space evidence. Hand readings carry roughly ±5–8 px uncertainty and additional unquantified perspective bias. Rendered ratios are sampled Bezier projections through unchanged orthographic cameras, normalized to existing body-width anchors.

|Feature|Reference fraction|V03 rendered|V04 rendered|
|---|---:|---:|---:|
|Body width|1.000|1.000|1.000|
|Bonnet leading width|0.853|0.861|0.853|
|Lower windscreen width|0.771|0.882|0.780|
|Headlamp outer span|0.859|0.887|0.864|
|Headlamp inner span|0.429|0.301|0.430|
|Upper grille width|0.406|0.358|0.406|
|Grille surround width|0.588|0.418|0.588|
|Lower grille width|0.397|0.327|0.397|
|Lower opening width|0.529|0.448|0.530|
|Bumper width|0.971|0.967|0.976|
|Tire-centre span|0.847|0.844|0.844|

The two biggest corrections were the grille surround and inner windscreen width. Not every number moved closer: the front bumper slightly overshoots its manual target after Bezier sampling, within the landmark uncertainty. Fit targets, control proportions and actual rendered proportions are recorded separately; control widths are not substituted for rendered widths.

## Rear proportion correction

Body normalization: paired rear-body landmarks **359..694 = 335 px**, excluding mirrors. The glass-side band is a derived projected margin, not a measured physical D-pillar thickness.

|Feature|Reference fraction|V03 rendered|V04 rendered|
|---|---:|---:|---:|
|Body width|1.000|1.000|1.000|
|Rear roof termination|0.687|0.687|0.687|
|Rear glass lower width|0.857|0.823|0.865|
|Lower glass side band|0.072|0.088|0.068|
|Shoulder termination|0.970|0.965|0.969|
|Lamp outer span|0.994|0.983|0.982|
|Lamp inner span|0.481|0.465|0.479|
|Tailgate width|0.806|0.809|0.809|
|Quarter maximum width|1.000|1.000|1.000|
|Upper bumper width|0.958|0.945|0.962|
|Lower bumper width|0.857|0.820|0.855|

Roof/quarter/tire dimensions were not changed to force image ratios. Some small differences remain, including lamp outer span and tailgate width. These are not calibrated real-world measurements.

## Reference-critical traceability

Each remaining region has an exact source filename, visible transition, existing controlling curve, parameter and V03 mismatch in `reference-evidence.json`. Sources are the same compatible canonical silver body family; no newer/incompatible MU-X details were mixed in. Paint colour was not used to choose geometry.

- **J01:** `18-17-10` front + `18-17-27` front 3/4; bonnet roll above the arch; existing five sections / `FENDER_TO_BONNET`; roll-drop parameters.
- **J02:** `18-17-27` + `18-17-14`; narrower screen inside painted cowl/A-root; `WINDSCREEN_BOTTOM`, `BONNET_EDGE`, `A_PILLAR`, `COWL_ROOT_BLEND`; width parameters.
- **J04:** `18-17-14`, `18-17-31`, `18-17-18`; quarter-glass cut and D-frame termination; existing `D_PILLAR`, `QUARTER_GLASS`, roof/glass return; lateral offsets and handle lengths.
- **J05:** `18-17-14` + `18-17-31`; shoulder growing into wheel mass; existing shoulder/crown guides; peak and asymmetric influence.
- **J06:** `18-17-31` + `18-17-18`; lamp taper and outer corner wrap; existing lamp/quarter guides; span, wrap X and corner-handle parameters.
- **J07:** `18-17-31` + `18-17-18`; broad upper bumper tapering to lower undercut; existing bumper/return/section guides; widths and limited handle balancing.
- **J08:** `18-17-31` + `18-17-18`; flared lower rear glass over hatch/lamp band; existing six glass controls, D-frame and sections; lower width and corrected perimeter order.

The only curve-path topology correction is local to the rear glass: V03 closed each half through the aperture centre. Existing controls are now ordered **top centre → upper mid → upper outer → side → lower outer → lower centre**, with each half open and mirrored. No controls were added. This removes an artificial construction line; the intentional centre/depth guide remains a separate diagnostic object.

## Remaining reference differences / why more parameter tuning is unlikely to help

1. **Bonnet/fender/headlamp-side volume:** independent front and side registrations imply different local heights/depths. Matching a face width does not locate the compound transition in X/Z.
2. **Cowl/A-root:** screen and painted frame widths now differ appropriately, but the lower pillar/cowl/fender relationship still depends on estimated depth.
3. **D pillar and quarter glass:** local silhouette cuts can be made sharper without establishing correct frame thickness and rearward termination across views.
4. **Rear quarter/lamp/hatch:** separately placed envelope curves share anchors but do not establish one reference-supported corner section.
5. **Lower bumper return:** its tight turn toward the trim rail is not a demonstrated soft automotive return; passing its endpoint constraint would not resolve this.

A further V05 of small offsets/handle edits would continue trading one projection against another. The current independently projected trace method needs a coherent cross-view depth/section constraint stage or better registered reference evidence before more tuning can be justified. This is a limit of the **current method**, not a claim that no modeller could improve the vehicle from the images. No replacement workflow was started.

## Surface-flow readiness

|Region|Readiness|
|---|---|
|Bonnet|Broad crown guide retained; fender/leading-corner compound flow BLOCKED.|
|Front fenders|Fixed wheel anchoring retained; crown/bonnet/shoulder integration BLOCKED.|
|Cowl|Improved inner-glass/frame allowance; planted root and rake/depth BLOCKED.|
|Greenhouse|Main side envelope and J03 retained; rear termination BLOCKED.|
|Roof|Central crown usable as guidance; D-frame transition prevents full readiness.|
|Side body|Strong side placement retained; width/section flow remains guide-level.|
|Rear quarter|Crown influence more controlled; integrated reference-matched mass BLOCKED.|
|Rear body|Better frontal proportions and correct glass perimeter; unified corner composition BLOCKED.|

Broad smooth surfaces and tighter character cuts remain distinct in the cage. Lamp/window cuts were not globally smoothed away. No body surface was generated to conceal unresolved cage differences.

## Curvature-comb findings

|Soft continuation|V03 relative jump|V04 relative jump|
|---|---:|---:|
|J04|0.301|0.011|
|J05|0.103|0.035|
|J07|0.490|0.163|

These V03→V04 figures are relative curvature jumps of the actual sampled soft continuations, not a visual quality score. The separate `handle-balance.json` records the local pre/post-balancing state; its “before” is after V04 position edits, not the V03 baseline. Balancing is limited to ±15% handle-length factors and excludes J03.

Heuristic internal warning records: **43 → 28**. Records include curves referenced by multiple joins and intentional cuts, not a count of independent physical faults. Maximum sampled internal curvature **33.20 → 58.91** per nominal metre: the increase is concentrated at tightened lamp/quarter-glass corners. It is reported, not hidden. Refer to the saved detailed sample arrays; these nominal model values are not real-vehicle measurements.

Local comb images cover bonnet/fender, cowl, roof/D pillar, shoulder and rear-quarter/bumper return in `comb-renders/`. Cowl/bumper combs reuse the existing sampler and debug mechanism. Display lengths are capped at 0.12 nominal units; numeric samples retain uncapped values. Soft-region warnings remain at the fender bridge and lower bumper return. High peaks at lamp/quarter-glass corners coincide with defined cuts and were not automatically erased. **Neither fewer warnings nor aligned tangents changed the failed visual gate.**

## Validation

- No added structural curves or control points: **PASS** (full per-object counts asserted against generated V03).
- Eight width stations / seven body-level definitions: **UNCHANGED**.
- Main side silhouette, front/rear side-window geometry and centre rails: **PASS / preserved**.
- Quarter-glass control landmarks: preserved; corner handles deliberately shortened.
- J03 shared endpoints/handles: **PASS / exact preservation**.
- Fixed wheel centres, tire dimensions, overall dimensions: **PASS / unchanged**.
- Numerical control-point symmetry: **0 mm**, with unchanged strict precision.
- Delete/regenerate coordinates, explicit handles and diagnostic base colours: **PASS**.
- Join Debug J01–J08, visibility restoration, comb toggle and finite curvature sampling: **PASS**.
- Open rear-glass half-perimeter and unchanged six-control count: **PASS**.
- Python source parse check: **PASS**.
- Preview topology regression: **0 degenerates / 0 non-manifold edges**.
- Quality topology regression: **0 degenerates / 0 non-manifold edges**.

Topology checks apply to the unchanged legacy soft-body regression, not to a surfaced V04. V04 remains a curve cage; wheel support meshes are retained. No topology/symmetry tolerance was loosened. Website build/browser/lint checks were not run because website files were not changed.

## Saved artifacts

Source: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v04.blend`

Main comparison: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04/reference-v03-v04-comparison.jpg`

Enlarged regions:

- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04/region-front.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04/region-j01-j02.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04/region-d-pillar.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04/region-rear-quarter.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04/region-rear.jpg`

Depth sections: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04/depth-sections-v04.jpg`

Also saved: `join-comparison.jpg` plus seven individual join boards; native registration overlays; `front-proportion-map.jpg`, `rear-proportion-map.jpg`, `PROPORTION_MAPS.md`, `reference-proportions.json`, `reference-evidence.json`, control-width data, actual sampled projection data, curvature audits/warnings, `FINAL_GATE.json`, checks and preservation logs. Source photos remain untouched. Local comparison cameras share view/scale/target between V03 and V04; source-photo crops are uncalibrated evidence, not registered reprojections.

## Reproduction and files

Run separately from the static project:

```
blender -b --python tools/blender-addons/toli_mux_generator/run_cage_v04.py
blender -b --python tools/blender-addons/toli_mux_generator/check_cage_v04.py
blender -b --python tools/blender-addons/toli_mux_generator/diagnostics_cage_v04.py
blender -b --python tools/blender-addons/toli_mux_generator/join_evidence_v04.py
blender -b --python tools/blender-addons/toli_mux_generator/measure_proportions_v04.py
blender -b --python tools/blender-addons/toli_mux_generator/render_joins_v04.py
python tools/blender-addons/toli_mux_generator/boards_cage_v04.py
blender -b --python tools/blender-addons/toli_mux_generator/render_combs_v04.py
```

Optional single-comb execution: `MUX_COMB_JOIN=J07 blender -b --python tools/blender-addons/toli_mux_generator/render_combs_v04.py`.

Existing file changed: `cage_ui.py` points the current action/render folder to V04. New files: `convergence_data.py`, `geometry/converged_cage.py`, and versioned V04 generation/check/measurement/render/board scripts. V03 add-on archived at `tools/3d/isuzu-mux/code-generator/reference-cage-v03-addon/`. Old V03/V02/V01 geometry generators, source trace data, existing parameters/panel and Join Debug are unchanged. V04 adds only diagnostic comb polylines outside the structural cage collection.

## Final recommendation and protection

**Stop the parameter-only curve pass. No V05. No surfacing.** The current trace-cage method has reached its useful limit for the unresolved bonnet/fender/cowl and rear-corner composition. Review the preserved candidate and decide on improved cross-view evidence/constraints before authorizing a different construction stage.

Website: **UNCHANGED**. GLB: **NOT EXPORTED**. Hero: **UNCHANGED**. Navigation: **UNCHANGED**. TOLI AI: **UNCHANGED**. Controlled capture: **PRESERVED**. Protected sibling projects: **UNCHANGED / NO WRITES**. Cost: **₹0 / $0**. Deployment: **NOT PERFORMED**. Git commit: **NOT PERFORMED**.

Before/after hashes verify **467 unchanged earlier files**: static source/public, controlled capture, V01/V02/V03 sources and all prior diagnostics. The old generators and debug tools were compared to the archived V03 add-on. See `preservation.json`.

Depth remains inferred from uncontrolled photographs. No exact physical surface reconstruction or calibrated depth is claimed.
