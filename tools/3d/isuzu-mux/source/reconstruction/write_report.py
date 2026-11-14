from pathlib import Path
import json
R=Path(__file__).resolve().parents[2];B=R/'source/reconstruction';S=json.loads((B/'joint-solution.json').read_text());I=json.loads((B/'joint-solution-initial.json').read_text());A=json.loads((B/'image-geometric-audit.json').read_text());C=json.loads((B/'blender-projection-check.json').read_text())
text='''# Multi-view reconstruction recovery — 7 November 2026

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
'''
for a in A:
 match='NO — unverified from interior' if a['image']==5 else 'YES — visually compatible'
 text+=f"| {a['image']} | {match} | {'YES' if a['exterior_usable'] else 'NO'} | {a['camera_position_class']} | {a['wheel_centers']}; {a['tire_ellipse']} | {a['glass_corners']}; {a['lamp_corners']}; grille: {a['grille_landmarks']} | {a['occlusions']} | {a['camera_solve_suitability']} |\n"
text+='''
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
'''
for label,r in [('Initial annotation fit',I),('Revised annotation fit',S)]:text+=f"| {label} | {r['overall_rms_pixels']:.2f}px | {r['training_rms_pixels']:.2f}px | {r['heldout_rms_pixels']:.2f}px | {r['max_error_pixels']:.2f}px |\n"
text+='''
All errors are unweighted 2D Euclidean pixel errors, including bad fits; they are not hidden by reporting only the best camera or optimizer loss. No observation was automatically dropped. Four current observations exceed 12px, including held-out far rear-glass/hatch and small quarter-glass corners. Final training points are within the normalized Huber cutoff, so no training residual is downweighted in the final revised solution. Held-out points do not affect the fit.

Local diagnostic thresholds were set in the solver: camera RMS <5px, maximum <12px, held-out RMS <8px, local camera rank 9 and no bound hit. The whole framework also requires all included cameras to pass and the data-Jacobian rank check. These thresholds are working project checks, not manufacturer accuracy standards. Local PASS below is not full reconstruction acceptance.

## Every fitted camera candidate
No accepted complete joint solution is claimed. The original approximately 0.88px side-only fit is historical evidence for its limited six-anchor calculation; it is not imported as full camera calibration. The left view is re-solved here together with all other views.

| Image / camera | Points | Training / held out | All RMS | Max | Held-out RMS | Local gate |
|---|---:|---|---:|---:|---:|---|
'''
for k,e in S['per_camera'].items():
 held='not available' if e['heldout_rms_pixels'] is None else f"{e['heldout_rms_pixels']:.2f}px"
 text+=f"| CAM_{int(k):02d} | {e['observations']} | {e['training']} / {e['heldout']} | {e['rms_pixels']:.2f}px | {e['max_pixels']:.2f}px | {held} | {e['landmark_gate']} |\n"
text+=f"\nOverall RMS: **{S['overall_rms_pixels']:.2f}px**. Held-out RMS: **{S['heldout_rms_pixels']:.2f}px**. Worst: **{S['max_error_pixels']:.2f}px**. Normalized data Jacobian rank at the declared relative threshold: {S['data_jacobian_rank_1e4']}/{S['unknown_count']}; smallest normalized singular value {S['normalized_jacobian_smallest_singular']:.6f}. All fitted landmarks are in front of their cameras. A full numerical rank does not prove accurate corners, a unique physical lens, or a visually acceptable vehicle.\n"
text+='''
All camera positions, yaw/pitch/roll, focal values and crop shifts are in `joint-solution.json`. No bound was hit. Example view-class coverage: front CAM_06, left CAM_02/CAM_07, right CAM_04/CAM_09, rear CAM_08, front-quarter CAM_10/CAM_11, rear-quarter CAM_12/CAM_13. Quarter views and CAM_09 fail; CAM_03 lacks independent held-out validation. The common-landmark gate therefore fails.

### Current >12px residuals
'''
for o in sorted((o for o in S['observations'] if o['outlier_over_12px']),key=lambda o:o['error_pixels'],reverse=True):text+=f"- Image {o['camera']}, `{o['landmark']}`: {o['error_pixels']:.2f}px, {'held out' if o['heldout'] else 'training'}; retained in the report.\n"
text+='''
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

'''
text+=f"Blender's camera projection was independently checked against the solver for all {C['checked_observations']} observed points: maximum implementation difference **{C['max_solver_blender_difference_pixels']:.6f}px**. This verifies the projection implementation and background framing, not the landmark solution's accuracy. The Blender file was saved successfully.\n"
text+='''
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
'''
(R/'MULTIVIEW_RECONSTRUCTION.md').write_text(text)
print('Report saved; gate FAIL, later geometry not created.')
