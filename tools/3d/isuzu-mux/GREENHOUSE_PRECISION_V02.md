# MU-X greenhouse precision pass — V02

**OVERALL GREENHOUSE GATE = FAIL. STOP before any other body region.**

Reference family unchanged: canonical silver-reference tall MU-X body, angular projector/chrome double-bar fascia family, upright quarter glass and broad split rear lamps. Exact year/trim unverified. Paint colors are ignored. Route B remains manual reference-constrained reconstruction; V02 calibration is not used as validated geometry.

## Source and preservation
Continued from `source/reconstruction/isuzu-mux-reference-constrained-v01.blend`; V01 is unchanged. New source: `source/reconstruction/isuzu-mux-reference-constrained-v02.blend`. Blender 5.2.2 LTS at `/usr/bin/blender`.

V01's eight wheel/tire proxy meshes and three stance curves are retained. Their vertex coordinates and transforms were compared exactly before and after saving/reopening. Wheel centers ±0.5 longitudinal, ±0.286 lateral; tire radius/center height 0.137, wheelbase=1. Tire ground height is -1.97e-9 from floating-point roundoff. No stance changes. These remain estimated normalized proportions, not physical measurements.

## Changes made
- Removed only V01 greenhouse surfaces/frames/cameras; retained stance and reference family.
- Added G01–G11 width, tumblehome, height and crown controls; widths vary longitudinally. No extrusion of one side profile across the vehicle.
- Windscreen has separate top/base widths, transverse bow and longitudinal curvature. Rounded corners use a sampled UV perimeter and concentric quad rings with a small central fan. Rear glass is separately curved and wrapped.
- Side windows use broad Bezier boundary control and curved Coons patches, all mapped onto the same three-dimensional side field. No thick trim or window seals were added.
- Rebuilt A/B/C/D structural supporting surfaces around the actual glass boundaries, retaining upright quarter glass.
- Added a Hermite header transition using incoming windscreen and outgoing roof directions, rather than the old hard straight link.
- Roof has longitudinal station interpolation and an explicit transverse crown. It is not flat; the roof-edge normal transition is nevertheless still unacceptable.

## Saved logical milestones
`source/reconstruction/greenhouse-v02/milestones/depth-stations-v02.blend`

`source/reconstruction/greenhouse-v02/milestones/curved-glass-pillars-v02.blend`

Final inspected V02 source is separate. Diagnostic reflection scene is saved separately, leaving the master with neutral materials. References are packed (14 images) and the final source is reopened to check them.

## Greenhouse reference board
`renders/greenhouse-reference-board-v02.jpg`. Every region has primary, secondary and validation images:

|Region|Primary|Secondary|Validation|
|---|---|---|---|
|Windscreen|O06|O11|O10|
|A-pillar|O07|O06|O09|
|Roof|O07|O11|O12|
|Front side glass|O07|O09|O11|
|B-pillar|O07|O09|O11|
|Rear side glass|O07|O09|O12|
|C-pillar|O07|O12|O09|
|Quarter glass|O07|O12|S21|
|D-pillar|O12|O08|O13|
|Rear glass|O08|O12|S19|

These are manual comparison assignments, not statistically independent calibration holdouts. O07/O09 are opposite profiles; O06/O08 constrain front/rear appearances; O10–O13 check both 3Q directions; S19/S21 supplement compatible rear geometry. Open-panel images do not define closed displaced panel edges.

## Geometry counts — greenhouse only
- Base mesh/cage vertices: **3341**.
- Evaluated vertices: **3341**.
- Evaluated triangles: **4960**.
- Greenhouse mesh objects: **44**.

Counts exclude unchanged stance meshes, diagnostic guide/cut curves, emitters, cameras and packed images. No subdivision modifiers; base and evaluated counts are equal. Eleven broad station controls and a small set of Bezier boundary controls generate sampled surface meshes; the samples are not separate photographic fitting constraints. No production retopology performed. Radial glass patch topology and separate unjoined surface strips are study geometry and contribute to reflection/normal defects; not a production shell.

## Explicit stations and actual cuts
`source/reconstruction/greenhouse-v02/stations.json` records G01 cowl, G02 lower A, G03 upper A, G04 front roof, G05 front-door cabin, G06 B, G07 rear-door cabin, G08 C, G09 quarter glass, G10 D, G11 rear glass.

`cross-section-cuts.json` contains actual triangulated mesh/plane intersections at all eleven x positions. The saved Blender source includes `G01 ACTUAL ...` through `G11 ACTUAL ...` curves, plus separately named `Guide Gxx` construction envelopes. The cross-section image plots actual cuts in white and construction guides in orange. They are not interchangeable. In particular the bowed windscreen/header and rear wrap are not fully reconciled with the idealized envelopes at G01–G03/G10–G11. This is a remaining depth-control failure, not evidence of a passed section solve. Lower section gaps are intentional: no doors or lower body were built.

## Gates after visual inspection
|Category|Status|Evidence / limitation|
|---|---|---|
|Windscreen proportions|**FAIL**|Width/height/rake are improved but corner/base shape and lateral A relationship are not accepted across front and 3Q.|
|Windscreen curvature|**FAIL**|Strip bunching and uneven lower-edge flow remain; curved geometry exists but is not acceptable automotive glass.|
|A-pillars|**FAIL**|Gap closed and rake improved; lower origin/cowl junction remains pointed and lateral thickness needs correction.|
|Roof longitudinal shape|**PASS**|Gross longitudinal trajectory now follows O07/O09 roof evidence; this is not a reflection-continuity pass.|
|Roof cross-car crown|**FAIL**|Non-flat crown exists, but side falloff/normal transition is still abrupt at the roof edge.|
|Front side glass|**FAIL**|Outline improved; diagnostic reflections still show uneven surface flow. Outline alone is insufficient.|
|B-pillar|**PASS**|Simple position, rake and width agree with the profile references at this study stage.|
|Rear side glass|**FAIL**|Rounded rear outline improved, but curvature consistency with the frame/adjacent glass remains unresolved.|
|C-pillar|**FAIL**|Rebuilt from shared side field; roof/junction curvature still changes abruptly.|
|Quarter glass|**FAIL**|Upright outline retained; depth and integration with C/D frame are not yet convincingly validated.|
|D-pillar|**FAIL**|Rear wrap and rear-glass/header junction retain a visible crease/pinch.|
|Rear glass|**FAIL**|Width/rake/curvature explicitly authored, but header and corner flow remain too abrupt.|
|Cross-car cabin depth|**FAIL**|Varying widths/tumblehome are explicit, but windscreen/rear wrap and station envelope reconciliation remain unresolved; no calibrated depth proof.|
|Three-quarter MU-X identity|**FAIL**|All four 3Q views inspected. Profile improvement has not established accepted cabin identity in depth.|
|Reflection continuity|**FAIL**|Header pinching, lower windscreen waviness and rear header/D-junction discontinuities visible.|

**Overall FAIL.** Gross side-roof trajectory and simple B-pillar placement improved. The remaining major geometry/depth/continuity failures prevent any further body construction.

## Diagnostic outputs and scope
- `renders/greenhouse-profile-overlay-v02.jpg`: actual mesh boundary projected orthographically and manually aligned using the same wheelbase/floor anchors as V01. It is not a calibrated projection or pixel-RMS validation; hidden windscreen curvature cannot be established from it.
- `renders/region-greenhouse-v02.jpg`: side, front, rear, front3Q, rear3Q and neutral perspective comparisons.
- `renders/greenhouse-cross-sections-v02.jpg`: actual mesh intersections plus idealized station guide differences; normalized units.
- `renders/greenhouse-reflection-v02.jpg`: preliminary fault-finding strip-reflection inspection. Formal reflection finish is NOT passed or authorized as the next stage. Opaque neutral diagnostic material, CPU Cycles 24 samples; emitters hidden from camera so geometry is not obscured. No production glass/PBR finish, cinematic lighting or materials used to mask defects.
- All four neutral 3Q outputs: `greenhouse-front-left-v02.png`, `greenhouse-front-right-v02.png`, `greenhouse-rear-left-v02.png`, `greenhouse-rear-right-v02.png`.
- Individual side/front/rear/neutral images retained. Camera poses are illustrative, not claimed as solved reference cameras.

## Remaining greenhouse work only
1. Reconcile the windscreen/header's true cross-car sections with the station envelope and correct lower A-pillar/cowl origin and thickness.
2. Replace glass patch/edge flow that bunches reflections near the windscreen base; correct surface curvature rather than adding trim.
3. Integrate transverse roof falloff with side surfaces without a normal crease; remove header pinching.
4. Rebuild C/D and rear-header junction flow, preserving the upright quarter-glass outline and correcting rear-glass corner wrap.
5. Recheck both front and rear depth against the same board and all four 3Q views. No exact dimensional fidelity is claimed from the mixed screenshots.

## Validation / protection
Final source saved and reopened; 14 references packed; stance compared exactly; all eleven sections intersect actual geometry; finite mesh coordinates checked. Source scripts compiled. Blender emitted environment audio/cache and API deprecation warnings; they do not establish clean rendering by themselves. Files, renders and reopen checks are the evidence.

Protection is verified by pre/post SHA256 over website src/public/config, all pre-existing MU-X research files, and both protected projects' source/config. Full dependency trees and every protected binary asset are outside this audit scope. No writes to protected projects. Existing research/audit reports are not overwritten; this is a new dedicated report.

Website unchanged; Inside TOLI state unchanged. No bonnet, fascia, fenders, door/body surfaces, wheel arches, rear body, interior, engine, details or functional parts. No GLB, integration, Git commit or deployment. Website build/TypeScript/lint/browser/device tests not repeated because executable website source/public assets are unchanged.
