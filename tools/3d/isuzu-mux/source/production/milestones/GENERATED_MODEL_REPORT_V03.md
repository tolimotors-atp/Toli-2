# ISUZU MU-X — V03 proportion-first exterior rework

## Final decision
**C — NOT BETTER THAN V02; STOP BEFORE DETAILING.**

The new shell and common-surface greenhouse are cleaner and materially different from V02. However, V03 is **not clearly better in all five required recognition regions**: its front remains generic, and side/rear identity have not clearly improved. Therefore the identity gate is not passed. This records the brief's stop condition, not abandonment or a claim that every local change is worse. No further detailing, panel separation, clearance work, GLB export or automatic restart followed the gate.

This is a **reference-based visual reconstruction**, not a factory CAD replica. No badge or identifying model text was used on the vehicle to imply recognition.

## V02 preservation — PASS
Byte-preserved original V02:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/milestones/isuzu-mux-generated-v02.blend`

The actual project milestone was opened in Blender before new geometry was built; SHA256 is recorded in `source/production/generated/v02-preserved-open.json`. V01, the V02 milestone, the V02 working master and prior experiments remain unchanged. V02's report is archived at `source/production/milestones/GENERATED_MODEL_REPORT_V02.md`.

Blender: **5.2.2 LTS**, `/usr/bin/blender`.

## V03 source
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-generated-v03.blend`

The V02 master `isuzu-mux-generated-master.blend` was **not** replaced. V03 is separate and opens at its identity-review stage with a clearly recorded failed identity decision.

## Retained and replaced
**113 V02 wheel/interior/engine mesh/curve parts retained**, with base-geometry, world-transform and material-slot signatures checked against V02:
- Four wheel assemblies, tires, rim components and original wheel centers.
- Basic RHD dashboard, seats, console and cabin components.
- Simplified engine-bay masses, battery, intake, reservoirs and structural masses.

All existing material definitions, neutral studio lights, ground and five comparison cameras remain. Retained internal parts are hidden during exterior renders, remain in `V02_RETAINED_COMPONENTS`, and are **not yet fitted/approved against V03**. Wheels remain visible in `V03_WHEELS_REUSED`.

**V02 exterior reused as control cage: NO.** Old body, greenhouse, exterior modules and functional panels are archived in hidden `V02_REFERENCE_BODY`. They are not the V03 foundation and are excluded from all V03 geometry counts. V03's new half-shell is a separate datablock made from eleven new guide stations. No old cage or failed calibration/NURBS geometry was deformed or subdivided again.

New organization:
- `V03_LANDMARK_GUIDES`
- `V03_EXTERIOR`
- `V03_CONSTRUCTION_CUTTERS`
- `V03_WHEELS_REUSED`
- `V02_RETAINED_COMPONENTS`
- `V02_REFERENCE_BODY`

## Hard points and source confidence
Coordinate system: X forward negative, Y left positive, Z up, ground Z=0. Axles remain at X=−1.4225 m and +1.4225 m, tire-center Z=0.382 m, wheel-center Y=±0.785 m. No wheel was moved to fit the new body.

|Anchor|Value|Evidence/limit|
|---|---:|---|
|Wheelbase|2.845 m|Official India same-body-family dimensional guide.|
|Overall length|4.825 m|Official guide; new shell measured 4.825001 m.|
|Overall width, excluding mirrors|1.860 m nominal|Official guide; new shell measured 1.860098 m.|
|Overall height|1.860 m nominal|Official guide. Current shell crown is 1.817521 m; no new roof rails or finishing components added.|
|Front/rear overhang|0.905 / 1.075 m|Official guide.|
|Front/rear track|1.570 m|Official guide; retained wheel centers.|
|Retained tire diameter|0.764 m|Actual retained tire geometry, grounded at Z=0.|
|Nominal 255/60 R18 diameter|0.7632 m|18×25.4 mm + 2×255×0.60 mm; supports retained diameter to within 0.8 mm, not proof of loaded tire shape.|

Sources: [official India MU-X brochure](https://www.isuzu.in/images/Brochure/pdf_area/ISUZU%20mu-X%20brochure.pdf), dimensional drawings and wheel specifications; [official MU-X specification page](https://www.isuzu.in/mux.html), 255/60 R18. These are compatible family-scale anchors; the photographed exact year/trim is not established. No trim-specific promotional feature was transplanted blindly.

Body-section widths/heights, cowl, belt, roof crown, glazing perimeter and curvature remain **visual estimates** from the canonical supplied photos. They are not claimed manufacturer dimensions.

## Guide and proportion decisions
A visible ground/centerline/wheel landmark system and simple side-profile/arch curves were established before the shell. Named landmarks include front/rear tips and axles, bonnet, cowl, roof front/peak/rear, windscreen top/bottom, A/B/C/D pillars, belt front/rear, quarter/rear glass and both arches. Overall-height and nominal-width markers are included in the final source.

Normalized ratios used:
- wheelbase_length: 0.5896.
- height_wheelbase: 0.6538.
- bonnet_length_length: 0.2668.
- roof_length_length: 0.4808.
- front_overhang_wheelbase: 0.3181.
- rear_overhang_wheelbase: 0.3779.
- tire_diameter_height: 0.4108.
- windscreen_rise_height: 0.2392.

The side-overlay study uses four explicitly declared horizontal anchors (front tip, front axle, rear axle, rear tip), approximate height scale and a sloping apparent ground line. This accommodates apparent perspective compression for a **visual normalized comparison**; it is not a recovered camera, photogrammetry or a measured trace. The strongest canonical side photo and other views informed the chosen broad proportions.

## Stages and gates
|Gate|Result|Meaning|
|---|---|---|
|Side silhouette|**PASS**|Guide-level profile and arches plausibly follow the canonical reference under documented normalized mapping.|
|Five-view silhouette|**PASS**|Broad new blockout envelope, stance, overhangs and transverse taper reviewed; not an identity or surface-finish pass.|
|Greenhouse|**PASS** at blockout layout level|Common-surface windscreen/roof/side-window/quarter/rear-glass system is coherent and retains an upright quarter-glass front edge. Transparency, seals and production surfaces are not approved.|
|Front identity|**NEEDS WORK**|Nose and lamp/fender/bumper relationships remain too generic and shallow.|
|Side identity|**NEEDS WORK**|Reference shoulder, fender/door volumes and lower-side sculpture are missing.|
|Rear identity|**NEEDS WORK**|Broad split lamps alone do not establish the correct rear-quarter/hatch/bumper identity.|
|Surface quality|**NOT REACHED**|Formal production reflection/surface pass deferred because identity failed. Existing cap/shoulder shading defects remain.|
|Recognition without badges|**NEEDS WORK**|Unlabelled render does not convincingly communicate the intended MU-X family.|

The shell was first rendered without identity parts. A second macro iteration replaced n-gon cap fans with quad strips, restrained cowl/roof/rear-cabin transitions and compensated subdivision width loss. No detailing was used to conceal the first silhouette issues.

Only then was the greenhouse added. Every glazing-study vertex derives from the same evaluated new shell via surface projection. These are **opaque graphite study regions**, not finished transparent glass or separate floating frames. Projection direction/sampling was corrected after the first review showed buried patches.

The identity stage contains only projected broad lamp, grille-bar, intake and rear-lamp envelopes. These are shape studies, **not finished optical assemblies or true open ducts**. Initial overlaps and overextended projection were corrected before the final renders. No lamp internals, grille mesh, badges, handles, fine trim, rail/step details or panel cuts were added.

## V02 → V03 judgment
|Category|Judgment|Reason/limit|
|---|---|---|
|Overall proportions|**IMPROVED**|A clean new envelope respects the fixed hard points and produces coherent roof/cowl/body taper instead of assembled exterior pieces.|
|Front|**WORSE**|The shallow, over-smoothed lamp/fascia treatment loses the required volumetric headlamp/fender relationship; simpler geometry has not improved recognition.|
|Greenhouse|**IMPROVED**|Window regions agree on one shell, avoiding V02's independent frame-gap system. Still only a blockout design study.|
|Side|**UNCHANGED**|Cleaner continuity is not sufficient to claim recognizable side identity.|
|Fenders|**UNCHANGED**|Broad width changes exist, but convincing MU-X flare/shoulder/door transitions are not established.|
|Rear|**UNCHANGED**|The split/wrapped layout is present but the surrounding rear volume remains generic.|
|Surface quality|**IMPROVED** at macro-continuity level|Fewer disconnected assemblies and gaps; not a formal surface-quality PASS.|

The mandatory requirement for clear improvement across all identity regions is therefore not met. No production-detailing recommendation is made.

## Geometry
Initial reviewed new exterior blockout (shell only, excluding reused wheels):
- Control vertices: **150**.
- Control faces: **130**.
- Evaluated vertices: **1,118**.
- Evaluated triangles: **2,232**.

This is a few-thousand-triangle shell, not a 50,000-triangle blockout.

|Current V03 inventory|Evaluated vertices|Evaluated triangles|
|---|---:|---:|
|New exterior including greenhouse/identity study regions|8,199|14,328|
|New exterior + visible reused wheels|13,319|24,344|
|New exterior + all 113 retained parts, including hidden/unfitted internals|17,759|32,984|

The last row is the **current complete stored V03 component inventory**, not a finished or fitted functional model. Stored V02 reference geometry, studio, landmarks and cutters are excluded. Study regions use conservative surface sampling; they are not an optimized web mesh. Existing 12-material definitions retained; four used by the new exterior study, ten used across V03 plus retained parts. No image textures added.

## Functional status
- Functional panels: **NOT YET REBUILT** for V03. The old animated V02 panels remain hidden reference only.
- Interior: **RETAINED — not yet fitted/approved against the new shell**.
- Engine bay: **RETAINED — not yet fitted/approved against the new shell**.
- New-panel clearance: **NOT REACHED**, deliberately not attempted while exterior identity fails.
- Retained wheel grounding: PASS, all four tire minima Z=0.000 m.

## Diagnostic paths
All requested sheets are under `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/renders/v03/`:
- `v03-side-guide-gate.jpg`
- `v03-silhouette-gate.jpg`
- `v03-greenhouse-gate.jpg`
- `v03-identity-gate.jpg`
- `v02-v03-comparison.jpg`
- `v03-recognition-no-badges.png`

Five individual PNGs for each blockout, greenhouse and identity stage are retained beside the sheets. The V02/V03 sheet uses the same unchanged comparison-camera rig, studio lights, 960×640 resolution and neutral silver material. Reference photos are side-by-side evidence, not claimed matched camera projections. The recognition PNG is a direct unlabelled render with no vehicle badges or identifying text.

## Saved milestones
Under `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/milestones/`:
- `isuzu-mux-generated-v02.blend` — immutable V02.
- `isuzu-mux-v03-guides.blend`.
- `isuzu-mux-v03-blockout.blend`.
- `isuzu-mux-v03-greenhouse.blend`.
- `isuzu-mux-v03-identity.blend`.

First blockout/greenhouse/identity attempts are also retained separately. Required major milestones and final V03 working source were reopened. Stage scripts and exact checks live in `source/production/generated/v03_*.py` and `v03-*.json`.

## Five largest remaining defects
1. Front fascia is too soft and shallow, particularly the lamp-to-fender/bonnet seating; the projected envelopes do not create the canonical front volume.
2. Front/rear fender bulges, shoulder and lower-door sculpture are still insufficiently characteristic.
3. Rear-cabin/D-pillar taper and glazing borders need closer multi-view shape matching despite their improved coherence.
4. Tailgate/rear-quarter/bumper volumes remain generic; broad red lamp regions are insufficient recognition evidence.
5. End-cap and shoulder reflections still reveal pinching/flat transitions. These need control-layout refinement after identity direction is reviewed, not added trim or subdivision.

## Protection and validation
- V02 preserved and opened before rework: PASS.
- V02 exterior reused as new control cage: **NO**, independent new data verified.
- 113 retained parts' geometry/transforms/material slots unchanged: PASS.
- Five comparison cameras unchanged versus V02: PASS.
- Finite evaluated geometry and retained tire grounding: PASS.
- Guide, blockout, greenhouse, identity and final-source reopening: PASS.
- Website files, V01/V02 milestones, original V02 master, references, prior research and protected projects checked against the preservation inventory; exact coverage/results in `source/production/generated/v03-preservation.json`.

No website build/TypeScript/lint/browser regression suite was run because no application/public asset changed. Modeling scripts compile and include invariant checks. No new-panel functional or continuous clearance tests were run because their stage was not reached.

External/paid vehicle assets: **NONE**. Budget: **₹0 / $0**. GLB: **NOT EXPORTED**. Website: **UNCHANGED**. Integration: **NOT PERFORMED**. Protected projects: **UNCHANGED**. Deployment: **NOT PERFORMED**. No Git commit.
