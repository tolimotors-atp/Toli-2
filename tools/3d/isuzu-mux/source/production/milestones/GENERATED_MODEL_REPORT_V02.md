# ISUZU MU-X — exterior recognition refinement V02

## Decision
**MAJOR REWORK REQUIRED.** V02 does not yet convincingly reproduce the canonical MU-X exterior. Local changes improve several cues, but the fundamental assembled-looking fascia, slab-like body and disconnected glazing/pillar transitions remain. This is a saved refinement of V01, not an approved production model. No automatic restart, GLB export, website integration, purchase, deployment or commit was performed.

Blender **5.2.2 LTS**, executable `/usr/bin/blender`, executed successfully. External/paid vehicle assets: **NONE**. Reference authority remains the 18 images at `/home/thunder/shared/tolimotors-main1/Isuzu MU-X`, with the silver open-panel family canonical. No incompatible later-family geometry was introduced.

## Baseline preserved — PASS
Original V01 milestone, byte-preserved and reopened successfully:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/milestones/isuzu-mux-generated-v01.blend`

Working master:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-generated-master.blend`

Comparison rig:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/milestones/isuzu-mux-v01-comparison-rig.blend`

V02 checkpoint:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/milestones/isuzu-mux-exterior-v02.blend`

Intermediate checkpoints retain the first/second exterior checks and the pre-clearance-correction candidate. The original V01 report is preserved as `source/production/milestones/GENERATED_MODEL_REPORT_V01.md`.

## Method and scope
Loaded the existing master, retained the existing body, roof and windscreen cages, modified existing body/door/bonnet control points, and refined local fascia and lamp components. The constructor from the previous task was **not** executed to build another SUV. Only its small mesh/curve helpers were reused. No calibration, NURBS reconstruction, asset searches, interior detailing, engine detailing, tire tread or website optimization work was performed.

The original body control cage still has 135 vertices, windscreen 77 and roof 40. Retained-part checks compare base geometry, world transforms and material slots for 113 existing wheel/interior/engine parts. They are unchanged. Six animated panel actions are retained. Bonnet and tailgate hinges were adjusted only after broader checks exposed existing cowl/roof interference. Four door hinges remain at their V01 locations.

## Fixed comparison cameras
- `CAM_COMPARE_FRONT`
- `CAM_COMPARE_FRONT_34`
- `CAM_COMPARE_SIDE`
- `CAM_COMPARE_REAR_34`
- `CAM_COMPARE_REAR`

Same saved rig, positions, rotations, lens/projection and image dimensions for V01/V02. The straight-on framing was widened before the final pair of baseline/after sets to prevent roof/tire clipping; both sets were rendered again from the corrected rig. Neutral silver paint, the same broad studio lights and reflection strips, 960×640 Cycles renders with 12 samples/denoising. Photographic references are side-by-side visual studies, not calibrated projections or exact-CAD evidence.

## Exterior results
|Region|Before V01|After V02|Result|
|---|---|---|---|
|Front|Attached rectangular lamp/fog modules and unintegrated grille.|Continuous curved bumper skin, recessed openings, more angular wrapped lamp envelope and crowned chrome upper boundary/two main bars. Still visibly assembled, incorrect lamp-to-fender/bonnet flow.|**NEEDS WORK**|
|Greenhouse|Heavy bright frames, open lower junctions and pinched-looking pillars.|Existing frame expansion reduced, dark seals, lower closure strips and roof/pillar returns. Upright quarter glass retained. Gaps and thickness transitions still inconsistent.|**NEEDS WORK**|
|Fenders|Nearly flat sides and detached-looking arch lips.|Small in-place crown/shoulder displacement and adjusted arch edge positions. Volumes remain insufficiently sculpted and do not capture the reference shoulder/lower-door character.|**NEEDS WORK**|
|Rear|Small rudimentary split lamps, heavy bumper insert and weak hatch context.|Broader tapered split lamps, forward side wrap, separate moving hatch strips and smaller lower bumper insert. Lamp seating and tailgate surround remain crude.|**NEEDS WORK**|
|Broad surfaces|Slab-like volumes, visible gaps, abrupt transitions.|Some better bumper continuity; door skin correction restored clean closed panels after an unsuccessful thinning experiment. Main-body/pillar/fascia transitions still do not pass studio reflection inspection.|**NEEDS WORK**|

There was no interior/engine detail expansion. The door-thinning experiment produced black panel gaps and was reverted. The original door skins, with the V02 broad surface adjustments, are retained; cabin sill pieces were narrowed instead. No claim of improvement is based merely on adding objects or polygons.

## Before/after judgment
|Category|Judgment|Limit|
|---|---|---|
|Overall proportions|**UNCHANGED**|Wheelbase/scale anchors retained; existing massing remains too generic.|
|Front identity|**IMPROVED**|Local lamp/grille/bumper cues are closer, but do not establish convincing recognition.|
|Greenhouse|**IMPROVED**|Thinner/darker framing and closure improve assembly; perimeter fit still fails.|
|Side identity|**UNCHANGED**|The reference's shoulder, door sculpture and fender transitions are not yet captured.|
|Fender volumes|**UNCHANGED**|Small displacement is insufficient for a meaningful visual pass.|
|Rear identity|**IMPROVED**|Broader split/wrapped lamp layout; surrounding rear body remains inaccurate.|
|Surface quality|**UNCHANGED**|Mixed local improvements; no overall automotive-surface PASS.|

## Motion clearance — NEEDS WORK
Each complete moving assembly was tested independently against all other render-visible vehicle mesh/curve parts held closed, at exact 0%, 25%, 50%, 75%, 100% angles. Actual evaluated rotations were asserted. Tests include glass, trim, seals, adjacent panels, interior and engine parts, rather than painted panel versus main shell alone. Five combined opening poses were rendered from both three-quarter cameras for visual inspection. Animation actions were temporarily detached for pose rendering and restored before saving, because render-time animation evaluation otherwise resets manually assigned rotations.

- Doors: 0°, ±13.75°, ±27.5°, ±41.25°, ±55° (left positive, right negative).
- Bonnet: 0°, 14.5°, 29°, 43.5°, 58°.
- Tailgate: 0°, −20.5°, −41°, −61.5°, −82°.

Counts below are distinct intersecting object pairs at each sample, **not** a count of confirmed visible penetration defects. Shared or touching seams are included and require interpretation.

|Assembly|0%|25%|50%|75%|100%|Status|
|DOOR_FL|9|2|0|0|0|**NEEDS WORK**|
|DOOR_FR|9|2|0|0|0|**NEEDS WORK**|
|DOOR_RL|11|3|0|0|0|**NEEDS WORK**|
|DOOR_RR|11|3|0|0|0|**NEEDS WORK**|
|BONNET|6|0|0|0|0|**NEEDS WORK**|
|TAILGATE|3|0|0|0|0|**NEEDS WORK**|

- Doors: early-opening frame/pillar and aperture contacts remain; halfway through fully open samples are clear.
- Bonnet: moving the hinge forward to X=−1.15 m and shortening the rear return removes the sampled opening/windscreen interference. Closed bonnet/insulation contacts with existing engine-bay masses remain.
- Tailgate: hinge moved to X=2.01 m, Z=1.735 m to keep the opening header clear. Closed glass/roof and lower hatch/bumper contacts remain; open samples are clear.
- Painted-panel versus main fixed shell: zero overlap pairs at all 30 exact panel samples, preserving the previous narrower clearance result.
- All four actual tire meshes remain grounded at minimum world Z=0.000 m.

This is discrete surface-intersection sampling, not continuous swept-volume certification or solid-containment proof. No full motion-clearance PASS is claimed. Exact object-pair details: `source/production/generated/motion-v02.json`.

## Geometry
|Measure|V01|V02|Change|
|---|---:|---:|---:|
|Evaluated vehicle vertices|25,193|26,893|+1,700 (6.75%)|
|Evaluated vehicle triangles|48,582|51,732|+3,150 (6.48%)|
|Materials|12|12|0|
|Image textures|0|0|0|

V02 base mesh vertices: 9,134; mesh/curve objects: 256. Evaluated counts include render-visible vehicle meshes/curves and exclude cutters/studio/cameras. No web copy exists; web geometry/file-size measurements and GLB reimport are not reached. Moderate geometry growth is not evidence of better recognition.

## Diagnostic paths
All requested files are saved beneath `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/renders/`:
- `refinement-v02/baseline-v01.jpg`
- `refinement-v02/front-v02.jpg`
- `refinement-v02/greenhouse-v02.jpg`
- `refinement-v02/fenders-v02.jpg`
- `refinement-v02/rear-v02.jpg`
- `refinement-v02/motion-v02.jpg`
- `generated-final-comparison-v02.jpg`
- `generated-surface-v02.jpg`

Individual fixed-camera PNGs and ten motion-pose PNGs are retained under `renders/refinement-v02/`. Surface sheet uses the same neutral reflection-strip studio before and after; motion-pose sheets use neutral Workbench shading to expose apertures rather than claim material quality.

## Five largest remaining exterior defects
1. The headlamp/fender/bonnet/front-bumper assembly still reads as separate mounted pieces; the canonical angular fascia needs integrated surface work.
2. Glazing perimeter, A/C/D pillars and roof/belt junctions still have inconsistent fit, thickness and visibly artificial transitions.
3. The side body remains slab-like; fender bulges, shoulder and lower-door sculpture do not reproduce the MU-X character.
4. Rear-lamp seating, quarter wrap and hatch surround remain rudimentary and disconnected from the rear mass.
5. Broad reflection continuity and closed panel/trim junctions still require controlled surface refinement; adding small details will not solve them.

These require further work on this retained model, not an automatic reconstruction restart. The exterior is not yet approved for production finishing.

## Evidence and limitations
Clearly supported reference features: tall SUV arrangement, upright cabin/quarter-glass family, four doors, bonnet, roof-hinged tailgate, angular projector envelopes, chrome double-bar character, broad split/wrapped rear lamps, steps/rails, RHD interior and visible engine-bay mass arrangement. Current modeled shapes remain approximations, not a claim of exact matching.

Estimated geometry: cross-sections, curvature, skin thicknesses, hinge locations, lens depth and unseen structural returns. Simplified geometry: optical internals, tire tread, interior upholstery, engine plumbing and underside. Silver paint retained for validation. No external vehicle assets, textures or geometry were acquired.

## Validation and protection
- V01 byte-preserved and reopened: PASS (`v01-open-check.json`).
- Existing body/roof/windscreen cage continuity and 113 retained wheel/interior/engine parts: PASS (`retained-parts-v02.json`).
- Fixed cameras, finite geometry and grounding: PASS (`geometry-v02.json`).
- Master reopened with six panel controls and restored animation actions: PASS (`reopen-v02.json`, `retained-parts-v02.json`).
- Motion: checked as above, **NEEDS WORK**.
- Exterior: **MAJOR REWORK REQUIRED**.
- Website application/public assets and protected projects: unchanged; preservation hash coverage/results recorded in `source/production/generated/preservation-v02.json`.
- No application files changed, so website build, TypeScript, lint and browser regression tests were not run, as permitted by this brief. Modeling scripts compile and include invariant checks.
- GLB: **NOT EXPORTED**. Website integration: **NOT PERFORMED**. Deployment: **NOT PERFORMED**. No Git commit.
