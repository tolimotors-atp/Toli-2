from pathlib import Path
import json,math,collections
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'source/reconstruction/calibration-v02';PROJECT=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');BASE=PROJECT/'tools/3d/isuzu-mux';OLD=BASE/'source/reconstruction'
S=json.loads((OUT/'v02-solution.json').read_text());V=json.loads((OUT/'validation-summary-v02.json').read_text());E=json.loads((OUT/'intrinsic-and-pose-sensitivity.json').read_text());C=json.loads((OUT/'blender-projection-check-v02.json').read_text());A=json.loads((OUT/'all-observations-v02.json').read_text());L=json.loads((OUT/'per-landmark-v02.json').read_text());W=json.loads((OUT/'worst-residual-diagnosis.json').read_text());V1=json.loads((OLD/'joint-solution.json').read_text())
backup=BASE/'MULTIVIEW_RECONSTRUCTION_V01.md';prior=(backup if backup.exists() else BASE/'MULTIVIEW_RECONSTRUCTION.md').read_text();(ROOT/'MULTIVIEW_RECONSTRUCTION_V01.md').write_text(prior)
core=S['core_cameras'];train=S['training'];held=S['heldout'];allcore=S['all'];worst=V['core_worst'];counts=V['observation_status_counts'];classcounts=V['observation_confidence_counts'];low_good=sum(o['confidence']=='C' and o['error_pixels']<5 for o in A)
text='''# ISUZU MU-X calibration recovery / outlier rejection — V02

## Calibration gate: FAIL
**CALIBRATION FAILED — CAMERA PARAMETERS UNDERCONSTRAINED**

This is a practical pose/depth recoverability failure at the requested accuracy, not a claim of an algebraically rank-deficient system or proof of incompatible vehicles. Residual annotation uncertainty remains a secondary contributor. The joint data-only Jacobian has full numerical rank at the selected threshold; rank alone does not certify predictive geometric accuracy. No new photos are requested: different trims or a need for additional controlled captures have not been established. Existing landmarks need stronger physical identification and camera/depth validation before geometry work.

No contours, surfaces, SUV cage, fascia, greenhouse mesh, retopology or GLB created. V01 source/results remain untouched. V02 is a separate calibration-only candidate and must not construct body surfaces.

## Original V01 versus V02
These are different datasets: V01 used 198 observations with 176 training/22 held out; V02 deliberately uses a documented structural subset. Lower V02 training error is not an apples-to-apples proof of recovery.

| Measurement | V01 | V02 selected structural core |
|---|---:|---:|
'''
text+=f"| Training RMS | {V1['training_rms_pixels']:.2f}px | {train['rms']:.2f}px ({train['n']} points) |\n| Held-out RMS | {V1['heldout_rms_pixels']:.2f}px | {held['rms']:.2f}px ({held['n']} points) |\n| Training median | not the original headline | {train['median']:.2f}px |\n| Core all-points median | not comparable | {allcore['median']:.2f}px |\n| Core all-points RMS | not comparable | {allcore['rms']:.2f}px |\n| Worst observation | {V1['max_error_pixels']:.2f}px | {allcore['max']:.2f}px (held-out) |\n"
text+=f"\nGeometry leave-one-view-out V02 RMS: **{S['lovo_aggregate']['rms']:.2f}px**, worst **{S['lovo_aggregate']['max']:.2f}px**. These are independent structural test projections after the omitted camera's pose is fitted only to separate anchor points. They are not folded into the smaller core training RMS. Worst external-view current residual is **{max(o['error_v02'] for o in S['rows'] if o['camera'] not in core):.2f}px**. No poor camera or validation regime is hidden in a global average.\n"
text+='''
## Complete residual and landmark audit
All 198 original observations are retained in `calibration-v02/v01-residual-audit.csv` and JSON, sorted by descending V01 residual. Every row includes image/camera, landmark, category, observed/predicted X/Y, signed X/Y residual, Euclidean residual, confidence and visibility/identity reasoning. `all-observations-v02.csv` and JSON retain the same 198 rows with V02 status and predictions where genuinely fitted/projected, sorted by descending available V02 error; excluded points have empty V02 error fields, never fabricated zero error. Observations with no V02 projection remain visible as grey marks in the diagnostics.

All 48 V01 named landmarks are individually audited in `v01-landmark-audit.json`; per-landmark V02 JSON/CSV reports counts, RMS/max, confidence and inclusion. There is no residual-based automatic point purge.

### The exact 26.83px V01 failure
'''
text+=f"**Camera/image {W['camera']}, `{W['landmark']}` (`{W['category']}`): {W['residual_pixels']:.2f}px.** Observed {W['observed']}, predicted {[round(x,3) for x in W['projected']]}. The magnified evidence is `renders/v01-worst-residual-review-v02.jpg`.\n"
text+='''
The observed point is a rounded, oblique far-side black-glazing border. No unique sharp physical corner was established as the same 3D point in every view. Supported primary causes: **H — incorrect shared-landmark assumption**, **E — perspective/tangency ambiguity**. An uncertain annotation definition (A) and pose/depth uncertainty (F) can contribute. This is a closed-panel image: open tailgate displacement (C) is not the cause. No direct evidence supports different trim (B) or lens distortion (G) as the explanation. The same visibility/identity rule excludes analogous far rounded glazing picks even when their old residual was small.

### Confidence/identity decisions
| Class | Original observations | V02 treatment |
|---|---:|---|
'''
text+=f"""| A high confidence | {classcounts['A']} | Visible hubs, finite-width tire contacts, clear fixed body lamp corners, clear closed windscreen intersections; initial structural solve |
| B medium | {classcounts['B']} | Grazing windscreen, grille/bumper/arch/rounded glass transitions; only six/eight stable windshield ties admitted after A initialization, others remain references |
| C low confidence | {classcounts['C']} | Documented current fixed-point assumption rejected; retained as visual/detail information |
"""
text+=f"\nOf the 50 rejected Class C observations, **{low_good} previously had residual below 5px**. They were rejected for physical identity/visibility, not simply because errors were large. Tire-top silhouette tangencies and oblique arch apexes are not assured identical physical 3D surface points across camera directions. Rounded quarter-glass and hatch-seam apparent corners also lack verified point identity. This removes those assumptions instead of deleting only the worst numeric outlier.\n"
text+='''
Open-panel audit: moving door glass/edges, raised bonnet/hatch contours and moving hatch-lamp segments were already excluded from V01 picks and remain excluded. No moving-panel observation is fitted to the V02 closed-body frame. Rejected closed hatch-seam picks are a point-definition issue, not falsely labeled open-panel contamination. No unjustified inverse hinge transform is applied.

## Core set, exclusions and roles
'''
text+=f"Selected **core8**: {', '.join(map(str,core))}. These are the closed-panel front, both sides, rear and both front/rear quarter directions. They retain the visually compatible canonical silver body/trim. The documented initial core6 is also solved and fully reported. The selected core has **20 active structural landmarks**, **68 observations**: **60 Class A / 8 Class B**, divided into **60 training / 8 held out**. Eight medium-confidence windscreen ties enter after the high-confidence initialization, not as an unconstrained all-feature first solve.\n"
text+=f"\nFinal observation dispositions: {counts}. Thus 50 Class C observations are rejected as current fixed-point identities, 52 medium/detail picks are not fitted, and all remaining 96 structural projections across core and external views remain reported. Twenty-eight of the original 48 named landmark IDs are not active structural landmarks; this does not mean all 28 are invalid—many remain detail references.\n"
text+='''
| Image(s) | Final role | Reason |
|---|---|---|
| 6, 7, 8, 9, 10, 11, 12, 13 | CALIBRATION + DETAIL | Matching closed configuration and six view classes; both quarter directions improve depth support |
| 2, 4 | CALIBRATION ONLY — external pose/validation | Useful fixed structural points but open panels; no shared-geometry fitting |
| 1, 3 | DETAIL ONLY — weak diagnostic pose | Frontal/rear hubs occluded and open-panel occlusion; limited independent pose anchors |
| 5 | EXCLUDED | Interior panorama has no stable exterior ties |

No exterior photo is declared to be a different trim just because it fits poorly. Four open-panel cameras are excluded from shared-geometry fitting, not erased from visual diagnostics. CAM_01 has only two pose anchors and numerical pose rank four: it is explicitly underconstrained, not presented as a recovered camera. CAM_03 is also a weak external diagnostic.

### Six-camera versus eight-camera comparison
| Candidate | Train RMS | Held-out RMS | Geometry-LOVO RMS | Max LOVO | Targets passed |
|---|---:|---:|---:|---:|---|
'''
for r in S['other_runs']:text+=f"| {r['name']} | {r['training']['rms']:.2f}px | {r['heldout']['rms']:.2f}px | {r['lovo']['rms']:.2f}px | {r['lovo']['max']:.2f}px | {r['numeric_targets_pass']} |\n"
text+='''
Neither candidate passed. The eight-camera failed candidate is preserved because the predeclared selection score (held-out plus geometry-LOVO RMS) is lower; this is not an acceptance decision. Both candidate files and every fold remain available. Choosing a lower training RMS core6 would conceal its worse view-withholding behavior.

## Staged solving
Every full/fold solve starts from the same sparse estimate and generic camera-class initialization, not V01 fitted geometry or omitted-view pixels. Normalized wheelbase=1, ground Z=0 and symmetry Y=0 define the gauge; absolute manufacturer dimensions are not invented.

A: fit track/radius relationships from wheel/contact measurements with the gauge fixed.

B/C: refine orientations, then positions using Class A, with a second orientation/position stabilization.

D: refine one shared constrained focal length; zero per-camera principal shifts.

E: refine shared landmark coordinates/depths; admit the documented stable medium-confidence windshield ties.

F: robust joint bundle only after those stages. Logs include active unknowns, fit counts and errors at each step. Loss is Soft-L1 via IRLS, with declared weak geometric/yaw/roll/focal priors. No observation is automatically dropped for residual size.

## Intrinsics, metadata and distortion
All 13 supplied files are PNG screenshots without reliable camera EXIF/focal metadata. The base model constrains a common closed-set focal, initialized at 70mm under a 36mm horizontal-sensor convention, bounded 50–100mm, with a log-focal prior. This is a projection convention, not recovered EXIF. Camera position/orientation vary; no independent principal shifts are allowed.
'''
text+=f"\nSelected equivalent focal: **{S['focal_36mm']:.3f}mm**. Geometry-LOVO fold values range **{min(x['focal_from_other_views'] for x in S['lovo']):.2f}–{max(x['focal_from_other_views'] for x in S['lovo']):.2f}mm**. Bounded numerical plausibility: **PASS**, but actual physical intrinsics are not verified. Camera/depth generalization still fails.\n"
text+=f"\nA restrained ablation allowed only cameras 7/9/10/11 focal offsets (±12%, 5% prior), with fixed principal centers. Held-out RMS changed **{E['baseline_heldout']['rms']:.3f} → {E['flex_heldout']['rms']:.3f}px**, still far above 5px; not promoted. The fitted focal equivalents are {E['camera_focal_mm']}. Extra flexibility is not used to force acceptance.\n"
text+='''
Distortion investigation: image inspection and the residual screen do not establish one consistent radial pattern. Per-camera radial-error/radius-squared correlations have mixed signs and very few samples. There are no independent straight-line lens controls, screenshot cropping and uncertain feature definitions confound interpretation, and the original worst error is an ambiguous glazing boundary. Interior panorama image 5 is excluded. No distortion coefficient is fitted merely to absorb errors. This is not proof of zero optical distortion.

## Leave-one-view-out validation
For each selected core view:
1. Remove every observation from that view from the shared-geometry solve.
2. Re-run stages A–F on the remaining cameras, retaining the same original priors/holdout policy.
3. Fit only the omitted camera's six-DOF pose using a predefined separate Class A anchor subset. Focal and shared geometry remain fixed from other views.
4. Measure the other structural points, which never fit that pose or geometry.

A completely unseen camera cannot be projected without some pose information. This protocol makes that necessary anchor use explicit; it is **geometry-LOVO with disjoint pose anchors and validation points**, not a zero-information camera prediction. Test points never choose the pose. Only one independent test point exists for rear-quarter folds 12/13, so those folds cannot receive a strong PASS even if the single residual is small. All folds require at least two independent tests, full local pose rank, RMS ≤5px and max ≤10px.

| Omitted camera | Pose anchors | Anchor RMS | Independent tests | Independent RMS | Max | Rank | Result |
|---|---:|---:|---:|---:|---:|---:|---|
'''
for f in S['lovo']:text+=f"| {f['omitted_camera']} | {f['pose_anchor_result']['n']} | {f['pose_anchor_result']['rms']:.2f}px | {f['independent_projection']['n']} | {f['independent_projection']['rms']:.2f}px | {f['independent_projection']['max']:.2f}px | {f['pose_rank']} | {'PASS' if f['pass'] else 'FAIL'} |\n"
best=E['image9_pose_multistart']['selected'];delta=V['fold9_landmark_motion'][0]
text+=f"\nNine anchor-only starting poses for omitted image 9 converge to the same anchor solution. It fits anchors at **{best['anchor_result']['rms']:.2f}px RMS**, but independent projections are **{best['independent_test']['rms']:.2f}px RMS / {best['independent_test']['max']:.2f}px max**. Pose selection used anchor loss and priors only. This failure is not fixed by selecting the most flattering test result. Removing image 9 also moves `{delta['landmark']}` by **{delta['delta_wheelbase_units']:.3f} wheelbase units** relative to the full solution, evidence of poor practical depth stability.\n"
text+=f"\nThe full structural data-only normalized Jacobian is rank **{V['data_only_normalized_rank']}/{V['unknowns']}**, condition number approximately **{V['normalized_condition_number']:.1f}**. The classification is practical predictive underconstraint/instability, not a false assertion of exact rank deficiency. Remaining correspondence and camera-model uncertainty are not uniquely separable without stronger verified ties.\n"
text+='''
## Every camera — poor views retained
Positions are wheelbase units; yaw/pitch/roll are radians in JSON and degrees in CSV. All 12 camera poses are saved, but only eight fit shared geometry. Confidence remains globally unvalidated. Numerical plausibility is not geometric acceptance.

| Camera | Role | N | RMS | Median | Max | Held-out / independent | Focal equivalent |
|---|---|---:|---:|---:|---:|---:|---:|
'''
for i,c in sorted(S['per_camera'].items(),key=lambda x:int(x[0])):
 test=c['heldout']['rms'] if c['included'] else c['independent_projection']['rms'];text+=f"| {i} | {'CORE' if c['included'] else 'EXTERNAL pose only'} | {c['observations']} | {c['all']['rms']:.2f}px | {c['all']['median']:.2f}px | {c['all']['max']:.2f}px | {test:.2f}px | {c['focal_36mm']:.2f}mm |\n"
text+='\nFull positions, orientations, focal, confidence and inclusion are in `calibration-v02/per-camera-v02.csv` and `v02-solution.json`.\n\n## All 48 named landmarks\n\n| Landmark | V01 N | Classes | V01 RMS / max | V02 core N | V02 core RMS / max | Status |\n|---|---:|---|---:|---:|---:|---|\n'
for p in L:
 values='—' if p['v02_core_rms'] is None else f"{p['v02_core_rms']:.2f} / {p['v02_core_max']:.2f}px";text+=f"| `{p['landmark']}` | {p['observations']} | {'/'.join(p['confidence_classes'])} | {p['v01_rms']:.2f} / {p['v01_max']:.2f}px | {p['v02_included_core_observations']} | {values} | {'ACTIVE STRUCTURAL' if p['v02_included_core_observations'] else 'NOT FIT; reference/rejected assumption'} |\n"
text+='''
Per-observation exclusions and visibility reasons remain in the linked CSV/JSON; excluded landmarks are not assigned fake V02 zero residuals.

## View compatibility matrix
S = strongly compatible visible closed configuration; T = compatible for static structural calibration only (open versus closed); L = limited common visibility in open views. These are visual/configuration assessments, not a claim that calibration passed. No incompatible trim is established. Open-panel corners must never be equated to their closed positions.

| Image | 1 | 2 | 3 | 4 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
'''
ids=[1,2,3,4,6,7,8,9,10,11,12,13]
for i in ids:text+='| '+str(i)+' | '+' | '.join('—' if i==j else 'T' if (i<5)!=(j<5) else 'S' if i>=6 else 'L' for j in ids)+' |\n'
text+='''
Pair-specific reasons are recorded in `calibration-v02/view-compatibility.json`. The supplied view coverage is complete enough to continue investigating existing correspondences. New controlled captures are not requested because necessity has not been demonstrated.

## Current worst residual and visual gate
'''
text+=f"Core worst: image **{worst['camera']}**, `{worst['landmark']}`, **{worst['v02_residual']:.2f}px**, held out. It is a fixed body lamp point in a closed view; moving-panel contamination is not an explanation. Other strong observations can fit tightly while this untrained projection misses, exposing the pose/depth/generalization issue. It remains visible and counted. The worst external static-lamp residual is 24.98px; worst geometry-LOVO residual is 68.59px.\n"
text+='''
Manual inspection of all 12 projection panels and the landmark-sampled heatmap: **FAIL**. The withheld rear lamp projections visibly miss in images 12/13; external rear image 3 is also poor. Residual clustering shifted from the rejected ambiguous glazing/seam picks to structural rear-lamp and omitted-view windshield/depth errors. It is not mainly a wheel-center training error. Grey excluded markers remain visible; unobserved areas of the heatmap are not a dense surface-error estimate.

## Final acceptance
| Requested check | Result |
|---|---|
| Core training RMS ≤3px | PASS on the structural subset only |
| Held-out RMS ≤5px | FAIL |
| No unexplained >10px residual | FAIL — core held-out and LOVO misses retained |
| Camera parameter numeric plausibility | PASS — bounded common focal, locked principal centers; actual EXIF unknown |
| Open-panel contamination removed | PASS — no moving-panel coordinates in the active frame |
| Invalid shared assumptions removed | PASS for documented Class C rules; remaining A/B annotations still require validation |
| Robust optimization | Soft-L1 IRLS, staged then joint; no numeric-only deletion |
| Leave-one-view-out validation | FAIL |
| Structural projection visual check | FAIL |
| CALIBRATION GATE | **FAIL** |

**CALIBRATION FAILED — CAMERA PARAMETERS UNDERCONSTRAINED**

Do not construct contours from this rig. The practical evidence is low anchor/training errors with large independent prediction errors and view-withholding depth motion. This does not prove different body trims, zero annotation error, or that new photos are necessary. No unsupported D/additional-photo request is made.

## Files and limits
- `source/reconstruction/isuzu-mux-multiview-v02.blend` — separate failed calibration candidate, 20 active landmarks, 8 core and 4 external cameras, zero body mesh objects.
- `renders/multiview-camera-solve-v02.jpg` — all 12 views with projected/observed points, residual vectors, roles and errors.
- `renders/multiview-residual-heatmap-v02.jpg` — sampled current structural residuals, grey excluded picks.
- `renders/v01-worst-residual-review-v02.jpg` — exact old 26.83px case.
- `source/reconstruction/calibration-v02/` — full observation/landmark/camera audits, both candidate solves, staged logs, every LOVO fold, intrinsic/pose sensitivity, validation and reproducible scripts.
- `MULTIVIEW_RECONSTRUCTION_V01.md` — exact backup of the prior report; V01 Blender/JSON/diagnostics are not overwritten.

'''
text+=f"Blender/source checks: version 5.2.2 LTS, `/usr/bin/blender`; all {C['observations_checked']} current structural projections independently match the numeric solver in Blender to **{C['max_solver_blender_difference_pixels']:.6f}px** maximum. Body mesh count is zero. Frame/contact symmetry, finite values and all 48/198 audit coverage checks passed. These verify implementation consistency, not calibration accuracy.\n"
text+='''
Website: UNCHANGED. Hero/cars/current vehicle, navigation, Titanium Bronze, Services, Gallery, enquiry and AI unchanged. Inside TOLI remains removed. Protected original and separate 3D projects: UNCHANGED. GLB: NOT EXPORTED. Deployment: NOT PERFORMED. Production web/device tests are not rerun because no application/model integration changed. Read-only before/after source/config and static public/model hash verification is recorded separately in `calibration-v02/protection-verification-v02.json` after installation. V01 and previous milestones remain untouched.
'''
(ROOT/'MULTIVIEW_RECONSTRUCTION.md').write_text(text)
print('V02 report and exact V01 report backup prepared.')
