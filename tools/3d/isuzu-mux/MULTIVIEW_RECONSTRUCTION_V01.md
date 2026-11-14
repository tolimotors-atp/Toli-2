# Multi-view reconstruction recovery — 7 November 2026

## Result
**Reconstruction route: CALIBRATED MANUAL MULTI-VIEW — attempted joint calibration; overall gate FAIL.**

This branch contains a shared sparse landmark/camera candidate, not a body. No prior cage was loaded, deformed, shrinkwrapped or reconstructed again. Contour/surface/retopology stages are withheld because the common landmark framework has not passed validation. Existing authored-v01, Passes 1–3, reports, renders and website are preserved.

## Reference sufficiency
**SUFFICIENT for a six-class sparse manual calibration attempt; required full-body accuracy remains unproven.** All six requested exterior view classes are supplied. Reference insufficiency has not been demonstrated, so no duplicate front/profile/rear/quarter captures are requested. The present failure involves ambiguous manual corner definitions, imperfect joint fit and limited independent validation. It would be misleading to blame the images for every previous modeling failure or assert that another guessed body is justified.

Usable exterior candidates: **12** (images 1–4, 6–13). Excluded photograph: **1** (image 5, interior panorama without reliable common exterior points). No exterior photo was excluded as an incompatible trim: the visible body/fascia/lamp/roof/wheel signatures are compatible with the canonical silver vehicle. This is visual compatibility, not proof of identical physical vehicle/VIN. Image 5's exterior identity cannot be verified from its interior content.

## Geometry-specific audit of all 13 images
The original general audit remains unchanged. This audit addresses geometric constraints only; detailed visibility/occlusion fields are in `source/reconstruction/image-geometric-audit.json`.

| Image | Canonical exterior match | Exterior usable | View | Wheels / tires | Glass / fixed body features | Occlusion/configuration | Camera-solving suitability |
|---|---|---|---|---|---|---|---|
| 1 | YES — visually compatible | YES | Front, bonnet and four doors open; engine bay partial | Hub centers occluded; tire contact picks only; Partial front tire sides/contact edges | Blocked by bonnet in 1; visible in 6; Front lamp outlines visible; grille: Fixed grille corners visible | Raised bonnet hides windscreen; moving doors excluded | Joint candidate, planar/depth weakness |
| 2 | YES — visually compatible | YES | Left profile, doors/bonnet/tailgate open | Both near left hub centers; Both near tire silhouettes/ellipses | Fixed rear quarter glass; windshield partly obscured when open; Near fixed front/rear lamp corners; grille: Mostly edge-on; ambiguous corners not picked | Open panels cover door/hinge regions; moving door glass excluded | Joint candidate |
| 3 | YES — visually compatible | YES | Rear, tailgate and rear doors open; cargo aperture | Rear hubs occluded; tire contact picks only; Partial rear tire sides/contact edges | Moving raised hatch excluded in 3; closed rear glass in 8; Fixed outer body lamp segments; hatch-mounted segments excluded when open; grille: Not visible | Raised hatch and open doors exclude moving geometry | Weak candidate: six observations, no independent held-out view test |
| 4 | YES — visually compatible | YES | Right profile, doors/bonnet/tailgate open | Both near right hub centers; Both near tire silhouettes/ellipses | Fixed rear quarter glass; windshield partly obscured when open; Near fixed front/rear lamp corners; grille: Mostly edge-on; ambiguous corners not picked | Open panels cover door/hinge regions; moving door glass excluded | Joint candidate |
| 5 | NO — unverified from interior | NO | Right-hand-drive dashboard, steering, front cabin and door cards | No exterior wheel centers; No | Interior/panoramic only; No; grille: No | Cabin-only panorama; cannot link reliable exterior landmarks | EXCLUDED |
| 6 | YES — visually compatible | YES | Closed front | Hub centers occluded; tire contact picks only; Partial front tire sides/contact edges | Blocked by bonnet in 1; visible in 6; Front lamp outlines visible; grille: Fixed grille corners visible | Hubs hidden by frontal body; mirrors overlap edges | Joint candidate |
| 7 | YES — visually compatible | YES | Closed left profile | Both near left hub centers; Both near tire silhouettes/ellipses | Windscreen oblique, fixed quarter glass and door glass visible; Near fixed front/rear lamp corners; grille: Mostly edge-on; ambiguous corners not picked | Mirror hides some cowl; grazing glass edges and far side occluded | Joint candidate |
| 8 | YES — visually compatible | YES | Closed rear | Rear hubs occluded; tire contact picks only; Partial rear tire sides/contact edges | Moving raised hatch excluded in 3; closed rear glass in 8; Fixed outer body lamp segments; hatch-mounted segments excluded when open; grille: Not visible | Hubs hidden by bumper; rounded glazing corners uncertain | Joint candidate |
| 9 | YES — visually compatible | YES | Closed right profile | Both near right hub centers; Both near tire silhouettes/ellipses | Windscreen oblique, fixed quarter glass and door glass visible; Near fixed front/rear lamp corners; grille: Mostly edge-on; ambiguous corners not picked | Mirror hides some cowl; grazing glass edges and far side occluded | Joint candidate |
| 10 | YES — visually compatible | YES | Closed front three-quarter, right side | Both near-side hub centers; far hubs mostly occluded; Near front/rear ellipse silhouettes | Windscreen and small fixed quarter glass; Near headlight outline and grille boundaries; grille: Upper/lower broad corners visible | Mirror/cowl and far windshield corner ambiguities | Joint candidate; quarter fit currently FAIL |
| 11 | YES — visually compatible | YES | Closed front three-quarter, left side | Both near-side hub centers; far hubs mostly occluded; Near front/rear ellipse silhouettes | Windscreen and small fixed quarter glass; Near headlight outline and grille boundaries; grille: Upper/lower broad corners visible | Mirror/cowl and far windshield corner ambiguities | Joint candidate; quarter fit currently FAIL |
| 12 | YES — visually compatible | YES | Closed rear three-quarter, left side | Both near-side hub centers; far hubs mostly occluded; Near front/rear ellipse silhouettes | Rear and fixed quarter glass; Rear body lamp outlines; grille: Not visible | Far glass/hatch corners ambiguous; reflections and black ceramic borders | Joint candidate; quarter fit currently FAIL |
| 13 | YES — visually compatible | YES | Closed rear three-quarter, right side | Both near-side hub centers; far hubs mostly occluded; Near front/rear ellipse silhouettes | Rear and fixed quarter glass; Rear body lamp outlines; grille: Not visible | Far glass/hatch corners ambiguous; reflections and black ceramic borders | Joint candidate; quarter fit currently FAIL |

For every image the JSON also records native size, body-corner visibility, perspective distortion and open-panel state. Near-profile photographs are not orthographic blueprints. Open doors, bonnet, hatch, moving hatch-mounted lamp portions, hidden hubs, reflections, UI overlays and view-dependent extrema were excluded as rigid shared landmarks. The same vehicle-side label always means physical +Y left / -Y right.

## Photogrammetry viability and local tools
No COLMAP, Meshroom/AliceVision, OpenMVG/OpenMVS commands or corresponding binaries were found in the checked local executable directories. Python has NumPy and Pillow; SciPy, OpenCV and pycolmap were not available in the inspected Python environment. Blender is `/usr/bin/blender`, version 5.2.2 LTS. No binaries or packages downloaded, no software purchased.

No conventional feature-based SfM run was performed, and no photogrammetry success is claimed. The eight closed exterior screenshots might support a masked SfM experiment, but reliability at the requested precision is unestablished: silver paint/chrome/glass are reflective and weakly textured, background/UI features are not attached to the rotating vehicle, image coverage is sparse, and open-panel states must be handled separately. This is a route assessment, not a mathematical proof that SfM is impossible. The executed route is manual correspondences plus joint geometric optimization, with Blender used for the camera/landmark framework and independent projection verification.

## Shared landmarks and scale
One dimensionless vehicle configuration is fitted to all 12 cameras simultaneously. There are 48 named shared points: symmetric front/rear wheel centers, tire top/contact anchors, fixed lamp/grille/bumper corners, windscreen, fixed quarter glass, rear glass/hatch and arch points. Initial sparse coordinates are declared estimates; no vertex/shape data from failed body meshes is used.

Wheelbase is fixed to **one unit** as a scale gauge; front/rear axle X=±0.5, symmetry plane Y=0 and contact plane Z=0. Track and tire-radius ratios are jointly estimated. No 2.85m manufacturer claim or absolute metre conversion is used. Verified manufacturer dimensions are not required to attempt this up-to-scale sparse solve. Absolute production scale remains unresolved.

Each camera has rotation yaw/pitch/roll, 3D position, focal scale and principal-point shifts. Shared symmetry, tire/ground constraints and declared weak initializer/focal/shift/roll/yaw priors regularize the problem. The 36mm-sensor focal equivalents are a convention for expressing fitted focal scale, not recovered EXIF or verified actual lens data. Radial lens distortion is not solved from this sparse annotation set.

## Joint optimization and validation
NumPy-only joint Levenberg–Marquardt with finite-difference derivatives and an available Huber robust loss fits **164 unknowns**, including all camera parameters and shared point coordinates. This is not 12 independent best-camera fits. Parameters, all per-observation predictions/errors, split membership, priors and bounds are saved in machine-readable files.

There are **198 manual 2D observations**. **176** are used for training and **22** held out before optimization; the split is deterministic and unchanged between the initial and revised annotation runs. The weak six-point rear/open view has no held-out sample and therefore cannot receive a validation PASS just because its training residual is small. Initial annotations/fit are preserved as `observations-initial.json` and `joint-solution-initial.json`.

Magnified image review identified a real correspondence-definition error: some side windscreen picks lay on the side-window/A-pillar or roof trim. Rear-glass picks mixed clear-glass and outer black-border conventions. Nineteen corrections are explicitly logged in `annotation-revisions.json`, with original/revised pixels and reasons. They were based on image inspection; no points were silently moved to fitted predictions.

| Run | All-observation 2D RMS | Training RMS | Held-out RMS | Worst error |
|---|---:|---:|---:|---:|
| Initial annotation fit | 6.93px | 5.20px | 14.70px | 48.60px |
| Revised annotation fit | 5.46px | 4.34px | 10.84px | 26.83px |

All errors are unweighted 2D Euclidean pixel errors, including bad fits; they are not hidden by reporting only the best camera or optimizer loss. No observation was automatically dropped. Four current observations exceed 12px, including held-out far rear-glass/hatch and small quarter-glass corners. Final training points are within the normalized Huber cutoff, so no training residual is downweighted in the final revised solution. Held-out points do not affect the fit.

Local diagnostic thresholds were set in the solver: camera RMS <5px, maximum <12px, held-out RMS <8px, local camera rank 9 and no bound hit. The whole framework also requires all included cameras to pass and the data-Jacobian rank check. These thresholds are working project checks, not manufacturer accuracy standards. Local PASS below is not full reconstruction acceptance.

## Every fitted camera candidate
No accepted complete joint solution is claimed. The original approximately 0.88px side-only fit is historical evidence for its limited six-anchor calculation; it is not imported as full camera calibration. The left view is re-solved here together with all other views.

| Image / camera | Points | Training / held out | All RMS | Max | Held-out RMS | Local gate |
|---|---:|---|---:|---:|---:|---|
| CAM_01 | 12 | 10 / 2 | 3.63px | 5.48px | 5.19px | PASS |
| CAM_02 | 16 | 15 / 1 | 3.52px | 7.44px | 1.92px | PASS |
| CAM_03 | 6 | 6 / 0 | 3.41px | 5.24px | not available | FAIL |
| CAM_04 | 16 | 15 / 1 | 4.26px | 9.62px | 2.93px | PASS |
| CAM_06 | 16 | 14 / 2 | 3.88px | 7.99px | 5.37px | PASS |
| CAM_07 | 18 | 16 / 2 | 4.14px | 10.08px | 7.40px | PASS |
| CAM_08 | 12 | 10 / 2 | 4.87px | 9.34px | 6.62px | PASS |
| CAM_09 | 18 | 16 / 2 | 5.14px | 8.84px | 5.82px | FAIL |
| CAM_10 | 22 | 20 / 2 | 6.62px | 20.00px | 15.45px | FAIL |
| CAM_11 | 22 | 20 / 2 | 5.06px | 13.22px | 7.06px | FAIL |
| CAM_12 | 20 | 17 / 3 | 5.38px | 10.05px | 7.47px | FAIL |
| CAM_13 | 20 | 17 / 3 | 9.40px | 26.83px | 22.00px | FAIL |

Overall RMS: **5.46px**. Held-out RMS: **10.84px**. Worst: **26.83px**. Normalized data Jacobian rank at the declared relative threshold: 164/164; smallest normalized singular value 0.000403. All fitted landmarks are in front of their cameras. A full numerical rank does not prove accurate corners, a unique physical lens, or a visually acceptable vehicle.

All camera positions, yaw/pitch/roll, focal values and crop shifts are in `joint-solution.json`. No bound was hit. Example view-class coverage: front CAM_06, left CAM_02/CAM_07, right CAM_04/CAM_09, rear CAM_08, front-quarter CAM_10/CAM_11, rear-quarter CAM_12/CAM_13. Quarter views and CAM_09 fail; CAM_03 lacks independent held-out validation. The common-landmark gate therefore fails.

### Current >12px residuals
- Image 13, `rw_base_L`: 26.83px, held out; retained in the report.
- Image 13, `hatch_low_L`: 26.27px, held out; retained in the report.
- Image 10, `q_fb_R`: 20.00px, held out; retained in the report.
- Image 11, `q_rb_L`: 13.22px, training; retained in the report.

Remaining corner ambiguity must be resolved with consistently defined physical correspondences, stronger ties in the existing views and validation of the lens/pose assumptions. These residuals are not proof that the photos show incompatible trims or that a new SUV should be guessed. No additional photograph angle is actually missing from the supplied set, so none is requested at this stage.

## Saved source and diagnostics
- `source/reconstruction/isuzu-mux-multiview-v01.blend`: 12 fitted camera candidates with packed backgrounds, 48 shared landmark empties and axle/wheelbase reference lines. Scene metadata prominently marks global FAIL. There are **zero body/surface mesh objects**. Per-camera native resolutions and errors are saved on the camera objects.
- `renders/multiview-camera-solve-v01.jpg`: all 12 current candidate projections on photographs, observed training picks, held-out picks, projected points and residual vectors, with every camera's RMS/max/held-out error. These are numerical point projections, not photogrammetric body renders.
- `source/reconstruction/shared-landmarks.json`: one common dimensionless point set.
- `source/reconstruction/joint-solution.json`: all parameters, residuals, holdouts, flags and errors.
- `source/reconstruction/observations.json`, `observations-initial.json`, `annotation-revisions.json`: inputs and revisions.
- `source/reconstruction/image-geometric-audit.json`: 13-image geometry audit.
- `source/reconstruction/stage-status.json`: gated/not-created outputs.
- Reproducible scripts: `observations.py`, `joint_solve.py`, `audit_and_scene.py`, `make_diagnostics.py`, `write_report.py`. Run them from this branch in that order; the staged installation helper is not needed for reconstruction.

Blender's camera projection was independently checked against the solver for all 198 observed points: maximum implementation difference **0.000534px**. This verifies the projection implementation and background framing, not the landmark solution's accuracy. The Blender file was saved successfully.

## Withheld later stages
The joint landmark gate did not pass, so no contour curves, reference-conforming surfaces, retopology or reflection/body checks were created. The following requested outputs are deliberately **not generated**, rather than filled with guessed geometry or misleading placeholders:

- `renders/multiview-contours-v01.jpg` — contour stage not reached.
- `renders/reconstructed-body-comparison-v01.jpg` — no body is allowed before contour acceptance.
- `renders/reconstructed-surface-diagnostics-v01.jpg` — no reconstructed surface exists to evaluate.

## Final gates
| Requested result | Status |
|---|---|
| Reconstruction route | CALIBRATED MANUAL MULTI-VIEW, attempted |
| Usable exterior candidates | 12; six view classes present |
| Excluded images | 1 interior panorama; no exterior trim-based exclusions |
| Cameras fitted | 12 candidates; full joint acceptance not achieved |
| Shared landmark solution | FAIL |
| Contour projection | FAIL / not reached |
| Greenhouse | FAIL / no accepted new surface |
| Front fascia | FAIL / no accepted new surface |
| Rear volume | FAIL / no accepted new surface |
| Fender/arch geometry | FAIL / no accepted new surface |
| Overall MU-X proportions | FAIL / not certified by the sparse fit |
| Reflection continuity | FAIL / no surface stage reached |
| MU-X likeness | FAIL / no new body built |
| Reference sufficiency | SUFFICIENT for sparse six-class calibration attempt; full target accuracy unproven |
| Overall reconstruction gate | **FAIL** |
| Website | UNCHANGED |
| Protected projects | UNCHANGED |
| GLB | NOT EXPORTED |
| Deployment | NOT PERFORMED |

## Validation and limits
Shared L/R symmetry and floor-contact gauge assertions passed. Projection checks passed. Numeric parameters are finite, and every point has positive camera depth. No conventional SfM, metric manufacturer validation, photogrammetric dense reconstruction, web build/browser/device test or performance measurement was claimed or performed. Website source did not change. This is an unresolved calibration milestone, not a reconstruction-ready master.
