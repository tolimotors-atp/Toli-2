# Generated ISUZU MU-X — saved candidate, not production-approved

## Status
Visual quality gate: **NEEDS WORK**. Website integration **NOT PERFORMED**. GLB **NOT YET EXPORTED**; independent GLB reimport **NOT REACHED**. No deployment or commit. External vehicle assets and paid assets: **NONE**. This is a fresh reference-based subdivision candidate, not recovered CAD.

Blender: 5.2.2 LTS, `/usr/bin/blender` (executed successfully).
Master: `tools/3d/isuzu-mux/source/production/isuzu-mux-generated-master.blend`.
Reference folder: `/home/thunder/shared/tolimotors-main1/Isuzu MU-X` (18 images). The canonical silver/open-panel body family remains authoritative; other supplied paint colors do not change geometry authority. Prior audits/failed geometry remain historical research only and were not imported.

## Work saved
Fresh half-body control cage with Y mirror and subdivision; new curved windscreen, roof, rear glass, separate side windows, wheel arches, wheels, fascia, trim and panel apertures. Hard-point, blockout, components and studio milestones are retained. The first component candidate before the broad-shape refinements is also retained. The constructor and inspection scripts reproduce the current candidate; they do not import past reconstructed geometry.

Broad-shape iterations lowered the bonnet/fender mass, reduced the lamp proportions, revised rear waist/glass height and pillars, repaired window shading, and adjusted wheel-spoke spacing. Subsequent clearance refinement moved door hinges outward and widened the engine opening. These improvements are not a claim that the resulting styling is acceptable.

## Practical gates
|Gate|Result|Evidence / remaining issue|
|---|---|---|
|Proportions|NEEDS WORK|Dimensional hard points established; too straight-sided and slab-like, fender/bonnet/cabin volumes still need sculpting.|
|Greenhouse|NEEDS WORK|Rake and window sequence present; frames look attached, visible perimeter gaps and overly planar glazing.|
|Front identity|NEEDS WORK|Double bars and projector concept present; bumper, chrome and lamps still blocky and insufficiently integrated.|
|Side identity|NEEDS WORK|Tall SUV stance/steps/rails present; wheel arches, shoulder and lower-door shaping insufficiently MU-X-like.|
|Rear identity|NEEDS WORK|Separate hatch/glass and split lamps present; lamp wrap and rear-quarter transition too rudimentary.|
|Surface quality|NEEDS WORK|Finite coordinates; broad reflection views reveal geometric discontinuities and flat transitions.|
|Functional components|PARTIAL|Six animated controllers and sampled shell clearance checks pass; full all-part swept clearance remains unverified.|
|Overall recognition|NEEDS WORK|Recognizable SUV cues are not yet a convincingly recognizable MU-X reproduction.|

### Five largest defects for the next modeling pass
1. Rebuild the front fascia into continuous fender/bumper surfaces and properly recessed angular lamp envelopes; current mounted-looking boxes and thin chrome bars fail front identity.
2. Reconcile A/B/C/D pillar and door-frame topology into continuous roof/belt interfaces. Close the visible lower-window gaps and reduce the detached-frame appearance.
3. Shape the front/rear fender bulges, shoulder and lower-door sculpting; the current broad side panels are too slab-like.
4. Integrate the tailgate surround, broad split wraparound lamps and rear bumper; current rear modules are too small and angular.
5. Refine bonnet/fender continuity, wheel-arch lips and shading transitions under reflection strips before adding any finer badges or mechanical detail.

## Functional structure and inspection
Separate DOOR_FL, DOOR_FR, DOOR_RL, DOOR_RR, BONNET and TAILGATE controllers. Frame 1 closed; frame 50 doors 55 degrees, bonnet 58 degrees and hatch 82 degrees. Intermediate frames 15 and 30 inspected numerically. Four wheel controls and separate left/right mirrors exist. Headlight housing, lens and emissive components are separate objects/materials; no website controls were added.

Latest painted-panel versus fixed-shell diagnostic reports **zero triangle-overlap pairs at frames 1, 15, 30, 50** for all six panels. This covers only the painted panels against the fixed main body, not all trim, glass, seals, interior components or the continuous swept volume. Tailgate/light-strip parenting and complete trim clearances still need a dedicated functional pass. No full functional PASS claimed.

Simplified right-hand-drive interior: dashboard, steering wheel, instrument mass, center stack/console, six seat masses, door cards, floor/sills/jambs and cargo continuity. Simplified engine bay: cover, intake/airbox, battery, reservoirs and structural masses. These exist but remain economical placeholders rather than finished interior/engine reproductions.

All four actual tire meshes have minimum world Z 0.000 m. Finite-coordinate checks pass. Production master reopening and controller checks are recorded separately in `source/production/generated/reopen-validation.json`.

## Geometry
- Authored mesh base vertices: 8,670.
- Evaluated vehicle vertices: 25,193.
- Evaluated vehicle triangles: 48,582.
- Mesh/curve objects: 241.
- Vehicle materials: 12.
- Image textures: 0; resolution not applicable (procedural PBR materials).
- Web vertices/triangles/file size: not available; export gate not passed.

Counts include evaluated mesh and curve vehicle parts, exclude cutters/studio/cameras. Base vertices omit curve control-point counts. Counts do not imply acceptable visual quality.

## Evidence classification
**Reference-supported arrangement:** tall SUV silhouette, upright cabin and quarter glass, four doors, bonnet and roof-hinged tailgate, double-bar grille, angular projectors, broad split rear-lamp concept, steps, rails, RHD dashboard and visible engine-bay component arrangement. These are supported features, not a claim that current modeled outlines match precisely.

**Approximated:** cross-sections, curvature, glazing crown, panel thicknesses, hinge coordinates, lamp depth, bumper transitions and unseen structure. Tire radius 0.382 m/width 0.255 m are modeling estimates.

**Simplified:** tire tread, wheel recesses, optics, chrome details, interior upholstery, seat construction, engine plumbing, fasteners and underbody. No detailed hidden mechanical systems invented.

Dimensional family guide: official India MU-X brochure, https://www.isuzu.in/images/Brochure/pdf_area/ISUZU%20mu-X%20brochure.pdf — length 4825 mm, width 1860 mm, height 1860 mm, wheelbase 2845 mm, front/rear overhangs 905/1075 mm and track 1570 mm. Exact photographed year/trim is unverified; these guide family scale rather than establish exact reference dimensions. X forward is negative, Y left positive, Z up; ground Z=0.

## Diagnostic files
All paths below are under `tools/3d/isuzu-mux/renders/`:
- `generated-blockout-v01.jpg`
- `generated-greenhouse-v01.jpg`
- `generated-front-v01.jpg`
- `generated-side-v01.jpg`
- `generated-rear-v01.jpg`
- `generated-surface-v01.jpg`
- `generated-final-comparison-v01.jpg`
Individual orthographic/profile, front/rear/three-quarter neutral views and PBR closed/open renders are retained beside the sheets. Comparisons are visual side-by-side studies, not calibrated overlays. The greenhouse sheet shows the current completed assembly, not a fabricated intermediate milestone.

## Protection and scope
Only new generated research/source/render files were saved inside this project's MU-X tools directory. The website vehicle remains active and unchanged. Hero, Titanium Bronze, Inside TOLI removal, booking and other website behavior are untouched. Protected 3D/original projects and pre-existing research are checked against the preservation manifest. See `source/production/generated/preservation-check.json` for the exact coverage/result.

Website build, TypeScript, lint and browser regression checks were not run because no application source or public model was changed. Blender scripts, finite geometry, grounding, sampled panel clearance, reopened source and visual renders were checked instead. Known risk: this is an unfinished modeling candidate with significant identity/surface defects and incomplete all-part motion clearance; it must not be activated on the website.
