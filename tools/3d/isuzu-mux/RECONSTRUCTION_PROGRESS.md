# New authored exterior branch — v01

**NEW AUTHORED BODY / NOT PASS-3 DEFORMATION**

**OVERALL AUTHORED BODY GATE: FAIL.** A separate, low-density development body exists, but it does not independently resemble the canonical MU-X closely enough. No master promotion, detailing, functional panels, GLB or website integration performed. Do not proceed automatically to another dense deformation pass.

## Method and preservation
The builder starts with Blender factory-empty state. It never opens, copies, shrinkwraps or reads vertices/topology from any prior body. Fresh explicit control coordinates, landmark curves, transverse sections, frame loops and quad patches create the new half-body. Mirror across Y and one diagnostic subdivision level follow construction. This is programmatically constructed authored control geometry, not a claim of completed manual/Class-A automotive surface modeling.

Passes 1–3, their renders, audit and earlier reports are preserved. The existing master is not overwritten. All new geometry lives under `source/authored/`. An initial-volume checkpoint is retained as `isuzu-mux-authored-initial-volume.blend`; the current candidate is `isuzu-mux-authored-v01.blend`. Pass 2 rollback hash was verified unchanged. No production source files or protected projects were written.

## Reference rig — PASS (organization, not calibrated accuracy)
Dedicated `REFERENCE_RIG` collection contains `REF_FRONT`, `REF_LEFT`, `REF_RIGHT`, `REF_REAR`, `REF_FRONT_3Q`, `REF_REAR_3Q`, `REF_OPEN_PANELS`. Canonical front/side/rear/open images are packed and labeled. Three-quarter closed photos are labeled secondary and used only for compatible broad envelopes, not incompatible trim/fascia details. Reference images remain separate, non-rendering geometry aids; collections are hidden by default and can be enabled in Blender.

The canonical silver open-panel decision is unchanged. No guessed model year, third-party mesh, downloaded vehicle, badge or photographic body texture introduced. Open bonnet/hatch/doors are not blindly traced as closed contours.

## Camera/reference calibration — FAIL as a full calibration
All six views have separate estimated camera objects with 70mm constrained lens and documented locations/heights/aim. A coordinate-descent fit of the canonical left view uses manually marked tire centers/top/bottom anchors, the estimated 2.85m wheelbase and .39m tire radius. It achieves approximately **0.875 pixels RMS** at the native **1060×522** reference size. The left comparison render and silhouette mask use that native aspect; other comparisons use 1000×650.

This fit is partial and non-unique; it does not recover the real lens or prove body accuracy. It uses simplified tire circles and uncertain manual anchors. Front, rear and three-quarter views are still estimates. Full multi-view calibration therefore FAILS, despite the useful left-anchor fit. `source/authored/side-camera-fit.json` records the pose/error/limits; fitted `CAL_left` is saved in the source. Other estimates are in `camera-estimates.json`. No numeric silhouette-lock claim.

## Coordinates and curves
Metres; +X front, +Y vehicle left, +Z up, floor Z=0. Measurement envelope: wheel centers X=±1.425, Y=±.83, Z=.39; .39m tire radius, 2.85m wheelbase, 1.66m track. These remain approximate photographic authoring aids, not manufacturer dimensions. Body bounds are about X=-2.38 to +2.30 and half-width up to .97. Roof crown about 1.835m.

Landmark curves — PASS as saved construction aids: roof, bonnet, belt, shoulder, rocker, windscreen side and outline, three side-glass perimeters, distinct front/rear arch profiles, front/rear bumper guides, grille/headlamp envelopes, bonnet transverse crown, front fender crown, front roof width, rear roof/glass/D-pillar/shoulder/tailgate/lamp guides. Curves are constraints/intent, not completed features.

Cross-sections — PASS as a saved 13-station rig: bumper, grille/headlamp region, front axle, bonnet rear, cowl, A/cabin, front door, B-pillar, rear door, rear axle, quarter, hatch/lamp and rear bumper. Endpoints follow hood/windscreen/roof/hatch regions where applicable. Half-width, lower body, broad curvature, shoulder and belt are represented. None of these construction-aid PASS results implies visual-body approval.

## New surface construction
Main side volume is specified independently. Separate front/rear width controls establish fender/quarter bulges; the two shaped seven-point arch profiles differ rather than copying a generic circle. Openings modify lower side rows after broad side volume is established. Roof and bonnet are distinct structured patches joined to fresh cabin boundaries. Side glass has explicit diagonal front contour and separate rear-door/quarter contours; it is not inherited rectangular material cells. Windscreen/hatch are structured half-grids and share their surrounding boundaries. Front/rear closures use transfinite quad grids with different depth planes, avoiding Pass 2/3 radial closure fans.

Initial patch-edge sample mismatch was corrected by common edge parameters and matching bonnet/side samples. A non-planar glass n-gon produced jagged glazing; it was replaced with simple glass-only triangle fans and restrained study refraction. No pole fan was added to painted fascia panels. The final body has one edge-connected face component, but 136 half-cage boundary edges remain; this is not certified as a watertight final vehicle. Broad surface continuity is judged visually, not inferred from that connectivity count.

No exact fascia/headlamp/grille/tail-lamp recesses or detailed panel cuts completed. The front/rear are scaffold major volumes only. Earlier volume/greenhouse gates did not justify advancing to identity cuts or details. Do not mistake the landmark curves for modeled grille/headlight recesses.

## Cage density at checkpoints
| Study | Body base vertices | Evaluated vehicle vertices | Evaluated vehicle triangles |
|---|---:|---:|---:|
| Initial basic volume A | 410 | 3,899 | 7,152 |
| Shared cabin edge repair | 512 | 4,637 | 8,656 |
| Bonnet/side edge repair | 536 | 4,811 | 9,040 |
| Current B/C/E diagnostic candidate | **539** | **5,099** | **9,616** |

Current half-cage has 516 base faces. Evaluated totals include the fresh four tire envelopes and four simple rim studies, exclude the studio floor/guide curves, and use Mirror + one subdivision level on the body. Extra topology above 410 was added for matching boundaries and usable glazing, not extra overall subdivision. D identity geometry was not reached: no separate density increase. Production textures: zero. Packed reference photographs are modeling aids, not vehicle textures.

## Checks A–E and specific gates
| Check | Status | Precise reason |
|---|---|---|
| A — Basic volume | FAIL | SUV envelope is plausible but canonical bonnet, front corner, rear-quarter and roof-end shapes not locked |
| B — Greenhouse | FAIL | Cleaner diagonal front window, but windscreen corner/frame contour and rear quarter-glass/D-pillar shape remain insufficiently matched |
| C — Fender/arch volume | FAIL | Broad volume exists; lips remain angular and the upper shoulder/arch transition is too generic |
| D — MU-X fascia identity | FAIL / NOT REACHED | Only scaffold multi-depth closures; actual grille/headlamp/fog/tail-lamp envelopes not reconstructed |
| E — Surface continuity | FAIL | Moving-strip views show kinks under rear glass, pillar/shoulder transitions and fender/arch creases |
| Windscreen | FAIL | New, not inherited, but contour/curvature not convincingly canonical |
| A-pillars | FAIL | New diagonal structure; thickness and corner transitions not validated in all three views |
| Side glass | FAIL | New perimeter geometry, still generic quarter-window and pillar proportions |
| Front fenders | FAIL | Insufficiently reference-specific crown and opening transition |
| Rear quarters | FAIL | Flat/slab-like lower panel and uneven upper shoulder |
| Wheel arches | FAIL | Distinct profiles exist, but do not yet match canonical openings convincingly |
| Front fascia | FAIL | Unfinished identifying recesses and bumper-corner shape |
| Rear identity | FAIL | Generic hatch/bumper, absent canonical lamp/plate-recess volumes |
| Overall proportions | FAIL | Partial anchor fit does not establish whole-body likeness; silhouette mismatches visible |
| MU-X likeness | FAIL | Would still require a model label; not ready for panel/detail pass |
| Reflection quality | FAIL | Not automotive-quality coherent reflection flow |

## Three-view and reflection evidence
Front, side, rear and both three-quarter views were inspected rather than approving one attractive view. Initial grey volume images are under `renders/authored-v01/checkpoint-a-*.png`. Current study views are `study-{front,left,right,rear,front-three-quarter,rear-three-quarter}.png`.

Actual rectangular-light evaluations were rendered at X=+1.8, 0, -1.8m. The first two use the front-quarter camera; the third uses the rear-quarter camera. These are real moved-light snapshots, not painted stripe graphics. Neutral silver roughness .24 exposes the wave beneath rear side glass and arch/closure transitions. No final PBR material work, textures, bloom or badge conceals the defects.

## Requested outputs
- Source: **`source/authored/isuzu-mux-authored-v01.blend`**
- Comparison: **`renders/authored-reference-comparison-v01.jpg`**
- Silhouette: **`renders/authored-silhouette-overlay-v01.jpg`**
- Surface diagnostics: **`renders/authored-surface-diagnostics-v01.jpg`**

The red silhouette overlay is from a transparent model-only mask in the fitted canonical left camera. It retains the original reference photo, labels the uncertain fit and warns that open doors/bonnet/hatch extend beyond the closed-body target. It highlights front corner, roof-end and body-envelope differences rather than concealing them. It does not certify exact silhouette alignment.

## Remaining constraints / method decision
The tire anchors can be reconciled in one side view, but this does not reconcile the greenhouse, front corner/bonnet envelope, quarter-window/D-pillar, hatch and fascia across all views. Major sources of failure are incomplete manually authored surface control, unvalidated multi-view camera constraints and missing identity-specific fascia/quarter geometry. Photo occlusion is a limitation, but is not an excuse for the generic geometry.

The new scripted patch method still has not produced the requested likeness or automotive surface continuity. Reconsider the reconstruction method now: a genuine interactive region-by-region automotive surface-authoring and multi-view camera-matching workflow is needed, not another global deformation or denser generic SUV. This candidate should remain a low-density starting study; it is not the new accepted exterior master. No automatic next detail pass.

## Validation and protection
Blender 5.2.2 LTS, `/usr/bin/blender`. Current source reopened for independent renders; finite-coordinate checks, half-cage centerline check, topology census and geometry-signature validation of the rig-only update passed. Four relevant static protection tests in two files PASS. Old Pass 2 rollback hash checked unchanged. File/geometry checks do not replace the failed visual gates.

No application source changed; production build/TypeScript/lint/full test suite, web-loader/device-performance and responsive web checks were not repeated. No GLB exists for this candidate. Optional Blender thumbnail/shader/config cache warnings were nonfatal; sources and evidence saved successfully.

Website: UNCHANGED. Existing vehicle, Hero/three cars, corner pills, AI, enquiry flow and Titanium Bronze unchanged. Inside TOLI remains removed. Protected original and separate 3D projects: UNCHANGED (no writes). GLB: NOT EXPORTED. Deployment: NOT PERFORMED.

---

## Earlier progress reports (preserved)

# Pass 3 — stopped at the proportion gate

**OVERALL EXACT-CUT & FINISH GATE: FAIL.** This is a saved macro-proportion study, not a completed exact-cut reconstruction. The staged gate prevented advancing into identity/detail/finish work. Existing website vehicle remains active.

## Stage results
| Stage | Result | Meaning |
|---|---|---|
| 3A — Proportions | FAIL | Two macro adjustments did not establish a convincing canonical silhouette |
| 3B — MU-X identity | FAIL / NOT REACHED | No exact greenhouse/fascia reconstruction claimed; diagnostic three-quarter views are not a passed identity stage |
| 3C — Automotive finish | FAIL / NOT REACHED | No final moving-strip evaluation; deferred because the earlier gates failed |

No category is passed merely because an approximate guide is in the right place. No panel separation, interior, engine, final textures, GLB or website integration was performed.

## Canonical reference and landmarks
The existing reference audit was read and retained. Silver open-panel photographs 1–4 remain canonical. Pass 3 adds `references/pass3-landmarks.json` before editing the mesh, with manual image-coordinate guides and separate estimated world-space targets. Annotated source views: `renders/pass3a/landmarks-front.jpg`, `landmarks-side.jpg`, `landmarks-rear.jpg`. Numeric point labels correspond to the ordered JSON entries. These are uncertain visual guides, not calibrated exact contours.

Front guides cover centerline, raised bonnet center/edges, grille top/bottom/edges, four headlight corners, bumper corners, lower intake and wheel centers. Side guides cover both wheels, bumper tips, cowl/windscreen ends, roof peak, belt/shoulder/rocker, arch apices and A/B/C/D pillars. Rear guides cover centerline, aperture/tailgate edges, raised-hatch glass/spoiler, tail-lamp boundaries, shoulders, bumper and rear wheels. The JSON explicitly flags occlusion and open-panel ambiguity. An open bonnet does not establish its closed contour; an open hatch does not establish closed rear glass geometry. No distorted photographed edge was treated as an exact blueprint.

A non-rendering `PASS3_LANDMARK_GUIDES — estimates` collection in the saved Blender candidate contains corresponding world guide empties, including fascia and tailgate targets. These are guide objects, not completed vehicle parts. The existing packed canonical reference planes remain.

## Changes and incremental saves
Started by loading `source/milestones/isuzu-mux-body-pass2.blend`, which remains byte-for-byte unchanged against the recorded rollback hash (`source/milestones/pass2-rollback.sha256`). No unrelated generic model was imported.

First macro study (`source/pass3a-proportions.py`): retained axle/tire anchors and mirror/subdivision settings; shortened front overhang coordinates beyond X=1.425 by 20%, rear beyond X=-1.425 by 16%; lowered the high shoulder/belt region up to .075m with a broad vertical falloff while preserving the roof crown; reduced inflated shoulder width up to .020m. These are local cage-coordinate changes, not a scale applied to the whole vehicle. The wheelbase remains an estimated 2.85m, tire radius .39m and axle Z=.39m. No manufacturer dimensional accuracy is claimed. The revised deformation initially crossed the mirror centerline; the final version explicitly preserves Y=0 and asserts that the half-cage never crosses it. Final evaluated count matches Pass 2 after the correction.

Second macro study (`source/pass3a-refine.py`): reduced the square rear upper-quarter/roof-end volume with up to .045m local vertical/longitudinal correction, narrowed the upper-quarter cage up to .018m and adjusted the cowl transition up to .035m. Core roof crown and tire anchors retained. The upper cabin remains boxy and the body still lacks the canonical volume transitions.

Incremental sources:
- `source/milestones/isuzu-mux-body-pass3a.blend` — first macro checkpoint
- `source/milestones/isuzu-mux-body-pass3a-refined.blend` — revised macro checkpoint
- **`source/milestones/isuzu-mux-body-pass3.blend`** — final failed-gate candidate

The main master remains the earlier Pass 2 source; the failed Pass 3 candidate is deliberately separate. Pass 2 rollback is untouched.

## What was NOT completed
No exact windscreen/window aperture, A-pillar, grille, lamp, arch, tailgate or bumper cuts were made after the proportion gate failed. Their existing Pass 2 geometry remains an unresolved study. The requested front/rear structured closure retopology was not reached; radial cap topology remains. No functional panel or production material work. Do not read a dark region, guide empty or generated Blender file as a completed identity feature.

## Comparison and diagnostics
First gate renders: `renders/pass3a/proportions-front.png`, `proportions-left.png`, `proportions-rear.png` (neutral grey). Revised six views: `renders/body-v04-{front,left,right,rear,front-three-quarter,rear-three-quarter}.png`.

Comparison sheet: **`renders/reference-comparison-v04.jpg`**. Six neutral-grey diagnostic views sit next to canonical photographs for principal views and compatible secondary photographs for three-quarter views. These three-quarter views document the failed study; they do not imply that Stage 3B was executed successfully. A camera inheritance mismatch was found and corrected before the final batch: final comparisons use the intended 65mm perspective setup. Camera heights/framing remain approximate, not calibrated to photographic lens metadata.

Close-up sheet: **`renders/body-diagnostics-v04.jpg`**. Shows windscreen/A-pillar, front fender/fascia, rear arch/quarter and tailgate. The moving side-reflection-strip tile is explicitly marked DEFERRED, not fabricated, because Stage 3C may only follow sufficiently improved 3A/3B. Neutral-grey views already expose inherited closure pinching, but this is not a final glossy finish test.

## Category gate
All results below mean NOT ACCEPTABLE / NOT VERIFIED against the canonical contours, not a claim that every unperformed test ran.

| Category | Result | Remaining defect |
|---|---|---|
| Windscreen | FAIL | Perimeter and corners remain approximate; no exact cut |
| A-pillars | FAIL | Broad painted wedge and incorrect front window boundary |
| Greenhouse | FAIL | Rectangular window cells, wrong quarter-glass/D-pillar geometry |
| Front fascia | FAIL | Generic cap/marker; correct grille/headlight/fog envelopes not authored |
| Bonnet | FAIL | Broad inflated transition lacks reference-specific crown/falloff |
| Front fenders | FAIL | Bulged generic surface and pinched arch supports |
| Front wheel arches | FAIL | Inherited circular profile, not an exact shaped opening |
| Rear wheel arches | FAIL | Inherited circular profile; insufficient distinct rear treatment |
| Rear quarters | FAIL | Too square/van-like despite reduced volume |
| Tailgate/rear | FAIL | Rounded generic closure; no accurate glass/lamp/hatch contours |
| Side curvature | FAIL | Still slab-like rather than reference-specific sculpted panels |
| Reflection continuity | FAIL / NOT VALIDATED | Known cap/arch concentration; final strip sweep not reached |
| MU-X likeness | FAIL | The silhouette still needs a model label to establish identity |

## Root cause and stop decision
The primary blockers are **B — proportion mismatch, C — control-cage topology, D — insufficient manual surface modeling, E — fascia geometry and F — greenhouse geometry**. A — reference-camera mismatch contributes uncertainty but cannot explain the obvious generic volumes. Simple cage deformations and further subdivision cannot produce the required likeness. This approach has not reached the required shape. Stop here, preserve the candidate, and do not automatically proceed to Pass 4 detailing.

A future attempt needs genuinely authored perimeter/section topology for the greenhouse and shaped front/rear volumes rather than another global loft/deformation pass. The current guide estimates should be reviewed, not described as a successful proportion lock. No request for additional assets is being used to excuse the current geometry failure.

## Geometry and checks
Topology was not increased: **29,312 evaluated vehicle triangles / 15,149 vertices**, including the existing four tire envelopes and four rim studies. Mirror and one subdivision level retained. Production textures: zero. No draw-call, FPS, web-export or device performance claim. `source/pass3-statistics.json` records the evaluated result and finite-coordinate check.

Blender: 5.2.2 LTS, `/usr/bin/blender`. Sources saved locally; optional thumbnail cache permission warnings were nonfatal. Two protection test files / four tests PASS. The Pass 2 rollback hash was checked unchanged. No application code changed, so production build/TypeScript/lint/full suite, browser regression and device performance checks were not repeated.

Website, active vehicle, Hero/three cars, corner pills, Titanium Bronze theme, AI, enquiry flow and navigation: UNCHANGED. Inside TOLI remains removed. Original project and independent 3D project: UNCHANGED (no writes). Deployment: NOT PERFORMED. GLB: NOT EXPORTED.

---

## Previous progress reports (historical)

# Exterior Body Reconstruction Pass 2 — FAIL

The Pass 2 exterior milestone is saved. It remains a development candidate, not an acceptable MU-X. Stopped before detailing, panel rigging, GLB export and website integration, as required by the failed body gate.

## Blender
Blender 5.2.2 LTS; executable `/usr/bin/blender`. Existing source reopened, not replaced with an unrelated asset. Canonical decision retained: silver open-panel photographs 1–4. Other photographs used only as compatible secondary silhouette comparisons. Reference audit retained unchanged.

## Existing and new geometry
| Evaluated vehicle (including tire/rim envelopes) | Triangles | Vertices |
|---|---:|---:|
| Pass 1 | 9,908 | 5,726 |
| Pass 2 | 29,312 | 15,149 |

Pass 2 has nine vehicle mesh objects. Its body is a single connected half-cage with 1,676 control vertices, Y-axis Mirror with centerline merging, and one subdivision level. The half-cage has 242 boundary edges: centerline and intentionally open lower/underbody boundary. It is not a claimed watertight finished production shell. Finite evaluated vertex values and single connected body component asserted. Production textures: zero. Study materials and four packed canonical photos retained.

Retained geometry: four tire envelopes and four separate rim studies at their previous approximate axle locations. Metric convention +X front, +Y vehicle left, +Z up; wheelbase 2.85m, tire radius .39m, axle Z=.39m. These remain photo-based scale estimates, not verified engineering dimensions.

## Rebuilt areas
Removed the separate side patches, arch ribbons, overlapping roof/windscreen/window sheets, bonnet patch and detached front/rear masks. Replaced them with one shared-vertex surface lattice. Seventeen deliberate longitudinal sections cover bumper/fascia, front axle/fender, bonnet/cowl, windscreen/A-pillar, front door, B-pillar, rear door/axle, quarter/hatch and rear bumper. Intermediate samples and arch support points follow those design sections.

Side sections introduce a recessed rocker, door-skin belly, fender flare, shoulder roll, tumblehome and crowned roof. Front/rear contour rings share the side/roof boundary vertices, removing detached masks. An early cap test had an unacceptable V-shaped front lower edge; corrected the bottom-center boundary before final renders.

Windscreen and side/rear glass areas are now part of the connected shell, with no floating overlapping sheets. These are opaque study-material regions, not final window openings or glazing. The dark front area is an inadequate blockout marker, not an accurate grille/headlight assembly. No detailed badges, lamps, engine, cabin, doors or rigging added.

## Inspection and comparisons
Inspected old and new candidates in solid, wireframe, reflective matcap and Cycles studio lighting. Diagnostic images: `renders/pass2-inspection/pass1-{solid,wireframe,matcap,studio}.png` and `pass2-{solid,wireframe,matcap}.png`. Final studio reflection view: `renders/body-v03-front-three-quarter.png`.

Broad rectangular lights and silver roughness .24 expose surface problems. Reflections flow more continuously across formerly disconnected patches, but still kink at arch supports and concentrate around radial front/rear cap poles. These defects were not hidden with high roughness or post-processing.

Final comparison sheet: **`renders/reference-comparison-v03.jpg`**.

Six final renders: `renders/body-v03-front.png`, `body-v03-left.png`, `body-v03-right.png`, `body-v03-rear.png`, `body-v03-front-three-quarter.png`, `body-v03-rear-three-quarter.png`.

Comparison cameras use 65mm perspective, approximate principal-view heights 1.55–1.65m and three-quarter height 3.1m. These are approximate photographic matches, not calibrated photogrammetry. Open reference panels, perspective and different crops prevent a trustworthy pixel overlay; a side-by-side sheet is used instead. Canonical references are labeled separately from secondary closed three-quarter views.

## Pass 2 quality gate
| Criterion | Result | Finding |
|---|---|---|
| Front connectivity | PASS | Shared-vertex closure; its shape still fails |
| Rear connectivity | PASS | Shared-vertex quarter/roof closure; its shape still fails |
| Windscreen | FAIL | Overlap removed; frame/cowl contour and corner radii insufficiently matched |
| A-pillars | FAIL | Excessively broad wedge; rectangular window region does not follow correct rake |
| Roof | PASS | Connected longitudinal/transverse crown; does not establish full vehicle accuracy |
| Side-body curvature | FAIL | Less planar, but still too slab-like and boxy |
| Fender volume | FAIL | Added volume, inflated shoulder and pinched arch flow |
| Wheel-arch placement | PASS | Approximate prior axle centers and tire-clearance anchors retained |
| MU-X stance/proportions | FAIL | Reads as an elongated generic SUV, not canonical MU-X |
| Reflection continuity | FAIL | Major arch/closure kinks and cap-pole curvature concentration |
| Overall exterior body gate | **FAIL** | Not ready for detailing / functional panels |

## Focused Pass 3
Rebuild the front side-window and A-pillar with diagonal perimeter topology instead of rectangular material cells. Match the rear quarter-window/D-pillar contour and cabin/body relationship. Replace radial closure poles with structured front-fascia and hatch grids. Sculpt reference-specific bonnet, fender and bumper volumes and major lamp/grille/fog regions without fine detailing. Rebalance overhangs and stance against the canonical set and compatible closed profiles. Repeat the six-view and reflection checks. Do not begin functional panels, interior, engine, production materials, export or integration until those defects pass.

## Saved source
- Master: `source/isuzu-mux-master.blend`
- Pre-rebuild backup: `source/milestones/isuzu-mux-body-pass1.blend`
- Pass 2 milestone: `source/milestones/isuzu-mux-body-pass2.blend`
- Current pass script: `source/exterior-pass2.py` (loads Pass 1 backup; older scripts remain historical studies)
- Mesh statistics: `source/pass2-statistics.json`
- Old topology inspection: `source/pass1-topology-inspection.json`
- Independent reopen/save comparison: `source/pass2-save-validation.json`

Master and milestone were independently reopened and their body vertices/faces/material assignments matched. Binary file hashes differ because Blender embeds the save-file path; byte identity is not claimed.

## Protection and checks
Website: UNCHANGED. Existing vehicle, Hero/three cars, compact corner pills, Titanium Bronze theme, 01–06 navigation, AI and enquiry flow unchanged. Inside TOLI remains removed. Protected original and independent 3D projects: UNCHANGED (no writes). Deployment: NOT PERFORMED. No GLB exported.

Two relevant protection test files / four tests PASS. Blender finite-geometry and connected-component assertions passed; both saved sources reopened. Full application build/TypeScript/lint/suite, browser matrix and physical-device/performance checks were not repeated because no application code or web model was changed. Thumbnail-cache permission warnings were nonfatal; source and render files saved. The first render batch was stopped before the corrected batch, which supplies the final comparisons. No FPS or draw-call claims.

---

## Previous report — historical

# MU-X body reconstruction — saved candidate, not approved

## Runtime and files
Blender 5.2.2 LTS, executable `/usr/bin/blender` (also resolved path). `blender --version` executed successfully.

- Editable master: `source/isuzu-mux-master.blend`
- Previous milestone: `source/isuzu-mux-body-v01.blend`
- Current reconstruction script: `source/build-body-candidate.py`
- Initial cage script: `source/build-body-v01.py`
- Standalone render/mesh check: `source/render-candidate.py`
- Comparison renders: `renders/body-v01-*.png` and `renders/body-v02-*.png`
- Web GLB: NOT EXPORTED. Intended path remains `public/models/vehicles/isuzu-mux/isuzu-mux-web.glb`.

## Reference decision
Existing audit retained, not restarted. Silver open-panel images 1–4 remain canonical. Their four image planes are packed in the Blender file in the hidden `REFERENCE_PLANES — canonical only` collection. Enable that collection in the viewport to inspect them. Other photographs are secondary comparison evidence, not authority for conflicting fascia/trim. No external model or branding was downloaded or reused.

## Saved modeling milestones
1. Estimated metric scale, canonical reference empties, cross-section body cage, open wheel-arch boundaries, cabin/roof/bonnet studies and four separate tire envelopes.
2. Window-surround correction and three side-window areas per side; six comparison camera views. No interior, engine, badges or small mechanical components detailed because the exterior gate has not passed.

Coordinates: +X front, +Y vehicle left, +Z up. Floor Z=0. Axle centers X=±1.425m, Z=.39m; tire-envelope radius .39m. Estimated body envelope length 4.84m, body width 1.86m, roof approximately 1.87m including crown. These are authoring estimates, not verified manufacturer dimensions. Orthographic front/profile/rear and elevated three-quarter views expose shape without perspective camouflage. Reference planes remain perspective photographs; no false orthographic calibration is claimed.

## Visual gate: FAIL
This is an early candidate, not a recognizable production-quality MU-X.

- Side: wheelbase/cabin envelope now reads as a long SUV, but body panels are excessively flat and slab-like; shoulder/fender transitions are not the canonical MU-X surfaces. Rear-quarter roof transition needs more controlled topology.
- Front: unresolved windscreen/roof overlap causes bright inconsistent surfaces; fascia closure is a plain study surface, not an MU-X grille or bumper. Front shoulder edges show pinching/curling from the open patch topology.
- Rear: closure lacks the correct shaped hatch/bumper volume; D-pillar and upper hatch transitions remain an approximation.
- Three-quarter: disconnected surface patches and coarse closure volumes do not form clean continuous automotive reflections.

The section-loft approach has reached its useful limit for this candidate. It needs a manual connected-surface topology pass, rather than more procedural badges, lights or interior detail. Another pass must resolve the A/D pillars and windscreen, connected front/rear closure curvature, shoulder/fender flow and accurate window/door contours. Only then repeat silhouette review, followed by the identifying exterior features. Do not mistake the saved file or successful mesh checks for a passed visual gate.

## Geometry and materials
Evaluated vehicle-only candidate: 9,908 triangles; 5,726 vertices; 28 meshes. Four vehicle study materials (silver, window-area study, rubber, rim), six Blender material datablocks total including unused/default and review floor. Production textures: zero. Four packed reference photos: 819×595, 1060×522, 1060×522 and 1148×492. Render Result and Viewer Node are Blender image datablocks, not vehicle textures. No export size, draw-call or FPS result exists.

## Functional state
Four wheel-envelope objects are separate and centered at their intended axle pivots; separate rim studies are not yet parented into functional wheel assemblies. Bonnet is an editable cage patch, not a completed hinged part. Four doors, tailgate, mirrors, lights, interior and engine bay: NOT COMPLETED. Mathematical tire-envelope contact is Z=0 for all four, asserted by the checker; full production grounding/loaded suspension validation has NOT passed. Studio floor receives ray-traced contact shadows; these are review lighting, not an optimized web shadow solution.

## Checks and protection
Blender master reopened successfully for independent render/mesh inspection. Finite vertex values and four tire-origin heights asserted. Candidate comparison renders generated locally. Two relevant protection test files / four tests PASS (retained asset hashes, removed section/navigation and Hero lineup). No website source, manifests, Hero assets, bronze styling or protected projects changed. Inside TOLI remains removed. Existing website vehicle remains active. Website integration: DEFERRED.

No production build/TypeScript/lint/full browser matrix repeated: no executable website code was changed and no GLB integration exists. No physical-device or web performance test. No deployment. Blender reported an optional thumbnail cache permission warning; master saved and reopened. A render batch terminated early and the remaining views were resumed from the saved master with two CPU threads.

## Acceptance status
Reference audit retained / canonical set used / editable source saved / local progress saved: PASS.
Body recognizability / clean surfaces / exterior quality gate: FAIL.
Functional parts / interior / engine / GLB / web export / browser model controls / production grounding / device responsiveness / performance: NOT READY, DEFERRED.
Hero and protected projects: UNCHANGED. Deployment: NOT PERFORMED.
