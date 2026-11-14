# ISUZU MU-X — V04 regional identity reconstruction

## Final decision
**B — PARTIAL IMPROVEMENT; STOP BEFORE DETAILING.**

Front improvement over both V02 and V03: **YES**. Side improvement: **NO**. Rear improvement: **NO**. Multi-view consistency: **NEEDS WORK**. Badgeless recognition: **NEEDS WORK**.

The front is more coherently seated and has real recess depth, but the side remains too slab-like and the rear composition still does not convincingly establish MU-X identity. The brief's all-three-regions threshold is **not met**. No V05 was created. No final surface polish, panel rebuilding, refitting, clearance, export, integration, deployment or commit followed this decision.

This remains a **reference-based visual reconstruction**, not factory CAD. The report does not claim that the candidate is production-ready or accurately recognizable merely because Blender files and tests exist.

## V03 preservation — PASS
Immutable milestone:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/milestones/isuzu-mux-generated-v03.blend`

It was byte-preserved, opened and verified before V04 geometry work. Its fingerprint and actual opened project path are recorded in `source/production/generated/v04-v03-preserved.json`. V01/V02/V03 sources and milestones remain unchanged. V03's report is archived as `source/production/milestones/GENERATED_MODEL_REPORT_V03.md`.

V04 working source:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-generated-v04.blend`

Blender: **5.2.2 LTS**, `/usr/bin/blender`. All V04 geometry work continued from V03's existing macro shell in a separate V04 file; the vehicle was not restarted, and no V02 cage deformation was resumed.

## Primary and secondary references
All files below are under `/home/thunder/shared/tolimotors-main1/Isuzu MU-X`, named `Screenshot From 2026-11-06 <time>.png`.

|Region|PRIMARY|SECONDARY 1|SECONDARY 2|Use|
|---|---|---|---|---|
|Front|18-17-10|18-17-25|18-17-27|Straight-front layout; three-quarter depth/fender/bonnet transitions.|
|Side / fenders|18-17-14|18-17-25|18-09-40|Side mass and shoulder; 3Q volume; open-panel side used only where fixed exterior remains visible.|
|Rear cabin|18-17-35|18-17-18|18-17-14|D-pillar/quarter volume and cross-car taper; rear width; quarter-glass rhythm.|
|Rear|18-17-18|18-17-35|18-17-31|Rear composition; lamp/quarter depth and bumper projection.|
|Surface character|18-17-25|18-17-35|18-17-14|Broad fender/shoulder/quarter reading, not final reflection polishing.|

Five separate reference boards were created. Interior/engine images were not used to infer exterior geometry. The canonical compatible silver body family remains authoritative. Secondary perspectives constrain transitions; they were not averaged into a purported shared camera solution.

## Normalized front/rear grids
Manual visible-envelope estimates from the designated primary images. Body width is normalized to 1.000, excluding mirrors. Image front/rear height is roof-to-tire-ground span. Uncertainty is approximately ±5 pixels / ±0.02 in the ratios; these are visual guidance, **not physical millimetre measurements**.

|Front relationship|Approximate ratio|
|---|---:|
|Body width|1.000|
|Grille width / body width|0.606|
|Headlight outer span / body width|0.897|
|Headlight height / front height|0.157|
|Grille height / front height|0.180|
|Bonnet leading height from ground / front height|0.497|
|Lower opening width / body width|0.494|

|Rear relationship|Approximate ratio|
|---|---:|
|Body width|1.000|
|Rear glass width / body width|0.844|
|Rear glass height / rear height|0.235|
|Lamp outer span / body width|0.957|
|Lamp height / rear height|0.128|
|Tailgate width / body width|0.882|
|Bumper height / rear height|0.131|

Front grid image bounds: [375, 130, 705, 480]; rear grid: [354, 142, 700, 478]. The photos are not perfectly registered orthographic views. V04's spatial setbacks, skin thickness, pressing depth and curvature are **approximated modeling parameters**, not measured dimensions recovered from the photos.

## Front composition
**V02:** independent protruding lamp/fog modules and weak grille/body integration.

**V03:** cleaner macro shell but shallow projected lamp/grille shapes, insufficient fascia depth and incorrect lamp-to-fender relationships.

**V04:** the complete nose was treated together. The existing V03 macro body remains the foundation; only its forward identity region was replaced/seated:
- New curved common fascia skin with actual openings.
- Physical recess returns and dark backing envelopes for lamps, grille and bumper openings.
- Bonnet leading bridge and fender-front returns into the existing shell.
- Opaque lamp placeholders with outer-wrap/depth; no projectors or optics.
- Upper chrome surround and lower broad bar forming the characteristic double-bar arrangement, with no badge or grille mesh.
- Local fender crown/leading shoulder corrections to remove the initial high fascia edge and visible gap.
- Landmark guides for lamp corners/edges, grille corners, bonnet leading corners, widest fender points and lower bumper corners.

**V04 BETTER THAN V02 AND V03: YES**, as a regional identity blockout. This is a relative improvement judgment, not a final likeness, surface-quality or manufacturing claim. The outer lamp/bonnet/quarter transitions remain angular and imperfect.

Successful front milestone:
`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/milestones/isuzu-mux-v04-front.blend`

It was saved only after the straight-front and front-three-quarter comparison improved.

## Side / fenders
**V02:** slab-like separated side panels with rudimentary arch treatment.

**V03:** continuous macro shell with limited fender/shoulder character.

**V04:** raised/continued the shoulder through existing cross-sections; introduced restrained lower-door dish and arch-local volume. The first low-density point adjustment did not show a clear improvement. The existing visible mirror/subdivision result was then applied, with local edge subdivision around the arch regions only, to support radial cross-section deformation. This is continued V03-derived regional work, not another complete shell. X/Z side-profile positions were held during that second volume adjustment; tire centers and roof were untouched.

Visible Blender guide sections were recorded at X=−1.90 m (ahead), −1.4225 m (wheel center), −1.04 m (behind) and −0.78 m (door transition). These are model-coordinate inspection stations, not physical positions inferred from photo pixels. Exact sampled sections are in `v04-fender-sections.json`.

**V04 SIDE BETTER THAN BOTH EARLIER VERSIONS: NO.** Numeric deformation and increased local edge density did not establish an obvious MU-X-specific fender/shoulder/door relationship. No side-pass milestone was created. Doors remain uncut.

## Rear cabin / rear composition
**V02:** weak rear glass/frame fit, small disconnected split lamps and crude rear body context.

**V03:** coherent common shell but generic rear taper, small rear-window study and projected lamp/body identity.

**V04:** changed the whole upper rear volume, not merely one window:
- Cross-car taper adjusted through the upper C/D/rear-glass area; roof centerline X/Z trajectory kept.
- Rear side/quarter glass re-derived from the changed body surface, with the upright quarter-glass front edge retained.
- Rear glass envelope widened/tallened to better approach the primary rear proportions; still an opaque study surface, not finished glass.
- New shared rear skin incorporates hatch mass/central pressing and bumper projection.
- Split rear-lamp envelopes are seated in openings; the outer lamp uses a sampled curved quarter wrap instead of a single detached quad.
- Broad garnish and recessed lower bumper insert establish only the large composition; no lamp internals or tiny details.
- The first review exposed buried rear-window edges and fragmented lamp wrap. Projection clearance and wrap sampling were corrected. Remaining border/seating artifacts are still visible.
- A final bounds check caught roughly 9 mm of unintended rear-bumper overshoot from the pressing profile. The profile was corrected, all five views refreshed and the frozen-length check passed.

**V04 REAR BETTER THAN BOTH EARLIER VERSIONS: NO.** There is new depth and coupled taper, but hatch/quarter/bumper identity remains too generic and sharp, with unresolved rear-window/region joins. No rear-pass milestone was created.

## Multi-view and badgeless decision
Five unchanged neutral comparison cameras were used: `CAM_COMPARE_FRONT`, `CAM_COMPARE_FRONT_34`, `CAM_COMPARE_SIDE`, `CAM_COMPARE_REAR_34`, `CAM_COMPARE_REAR`. The original studio lights and neutral silver material remain. Comparisons use V02, V03 and V04 with the **same model-camera pixel crop**, and separately declared photographic crops. Images are fitted with aspect ratio preserved to approximately match vehicle framing/scale; they are not photogrammetrically registered.

Multi-view consistency: **NEEDS WORK**. Macro placement remains coherent, but the front/rear regional surfaces and side character do not yet read as one convincing MU-X exterior.

Badgeless recognition: **NEEDS WORK**. The diagnostic vehicle has no ISUZU badge, MU-X text, identifying caption or applied reference image. Simpler placeholders are not treated as proof of recognition.

## Frozen macro checks and retained components
Expected retained wheel/interior/engine mesh/curve parts: **113**. Actual: **113**. Their base geometry, world transforms and material slots are unchanged against V03. Existing material definitions are reused; no image textures or external vehicle geometry were introduced.

- Wheelbase markers: **2.845 m**, unchanged.
- Nominal length/width/height markers: **4.825 / 1.860 / 1.860 m**, unchanged.
- Retained tire diameter: **0.764 m**, unchanged; all four actual tire meshes remain grounded at minimum Z=0.000 m.
- Evaluated new exterior bounds: length **4.825000 m**, width **1.860098 m**, roof maximum Z **1.817521 m**. Nominal 1.860 m height includes components such as rails not rebuilt in this study, as in V03.
- Main roof centerline heights at X=−0.34, 0.28, 1.14, 1.98 m: **0.000000 m delta** versus V03.
- Existing front windscreen/front-side-glass geometry and all five cameras: unchanged.
- Complete inventory width including old retained wheel geometry: **1.870000 m**; this legacy wheel-part extent was not altered to force a different nominal body width.

The 113 internals remain available but were not refitted. Old V02 exterior and superseded V03 identity pieces remain hidden reference only. V04 did not reuse/deform the old V02 body cage.

## Geometry
|Inventory|Evaluated vertices|Evaluated triangles|
|---|---:|---:|
|V03 original macro shell|1,118|2,232|
|V04 V03-derived body foundation after regional work|1,830|3,656|
|V04 new exterior, including glazing and regional envelopes|**8,293**|**15,354**|
|V04 exterior + all 113 retained components|17,853|34,010|

V04 exterior base vertices: 6,308; mesh/curve objects: 43; used exterior materials: 4. The original 12-material definitions remain available. Counts include evaluated curves, exclude cutters/studio/guides and hidden old exterior reference geometry. The full retained inventory is not a finished/fitted functional model. No web copy or GLB size exists.

More geometry was introduced only for physical regional seats and local fender sampling. The failed side gate is documented honestly; added topology is not considered a visual success.

## Diagnostic renders
Exact requested files:
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/renders/v04/v04-front-gate.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/renders/v04/v04-side-gate.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/renders/v04/v04-rear-gate.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/renders/v04/v04-turnaround.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/renders/v04/v04-badgeless-recognition.jpg`

Also saved: five `reference-board-*.jpg` files, front/rear normalized-grid PNGs, enlarged front/rear reference details, front/side candidate PNGs and five final neutral PNGs. Exact crop coordinates are in `v04-evidence-crops.json`. Additional intermediate turnaround angles were not added after the partial identity result; all five required views were rendered.

## Five remaining geometric defects / failed assumptions
1. Side arch/fender/shoulder shaping still assumes too simple a continuous side field; it does not capture the reference's stamped flare and lower-door character.
2. Rear hatch/quarter/bumper depth distribution still reads too flat/boxy despite the new pressing and curved corners.
3. Rear-window/D-pillar joins retain visible edge/seating artifacts; common-surface projection alone is insufficient for finished glazing borders.
4. Front outer-lamp wrap and bonnet/fender junctions remain too angular; their depth is improved but envelope proportions/transitions still need review.
5. Regional return boundaries and cap/shoulder shading are not resolved. Surface polish was deliberately withheld because side/rear identity did not pass.

These are geometric modeling limitations, not an insistence on unknowable manufacturer CAD accuracy. No new iteration was automatically started to conceal the failed gates.

## Files, verification and protection
- V03 milestone and source byte-preserved; reopened: PASS.
- Only successful regional milestone created: `isuzu-mux-v04-front.blend`. No side/rear PASS milestone.
- Final V04 source saved and reopened; decision recorded inside the Blender scene and `V04_REVIEW_STATUS` text.
- Python scripts compile. Finite geometry, frozen exterior bounds, camera consistency, front glazing, main roof samples, grounding and 113 retained-part signatures pass (`v04-validation.json`).
- Exact installed-file reopening and preservation coverage/results are recorded in `v04-installed-open.json` and `v04-preservation.json`.
- Website application/public assets, reference originals, V01/V02/V03 models and protected projects remain unchanged. Only V04 research/source/render outputs and this report were updated.

External/paid vehicle assets: **NONE**. Functional panels: **NOT REBUILT**. Interior/engine: **NOT REFITTED**. Clearance: **NOT PERFORMED**. GLB: **NOT EXPORTED**. Website integration: **NOT PERFORMED**. Website/protected projects: **UNCHANGED**. Deployment and Git commit: **NOT PERFORMED**.

Website build, TypeScript, lint and browser tests were not run because no application file changed. Surface polish, new-panel clearance and web-export tests were intentionally not reached. Known risk: this remains a failed all-region identity candidate and must not be activated.
