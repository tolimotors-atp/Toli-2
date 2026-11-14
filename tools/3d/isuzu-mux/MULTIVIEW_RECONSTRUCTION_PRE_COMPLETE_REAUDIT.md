# ISUZU MU-X calibration recovery / outlier rejection — V02

## Calibration gate: FAIL
**CALIBRATION FAILED — CAMERA PARAMETERS UNDERCONSTRAINED**

This is a practical pose/depth recoverability failure at the requested accuracy, not a claim of an algebraically rank-deficient system or proof of incompatible vehicles. Residual annotation uncertainty remains a secondary contributor. The joint data-only Jacobian has full numerical rank at the selected threshold; rank alone does not certify predictive geometric accuracy. No new photos are requested: different trims or a need for additional controlled captures have not been established. Existing landmarks need stronger physical identification and camera/depth validation before geometry work.

No contours, surfaces, SUV cage, fascia, greenhouse mesh, retopology or GLB created. V01 source/results remain untouched. V02 is a separate calibration-only candidate and must not construct body surfaces.

## Original V01 versus V02
These are different datasets: V01 used 198 observations with 176 training/22 held out; V02 deliberately uses a documented structural subset. Lower V02 training error is not an apples-to-apples proof of recovery.

| Measurement | V01 | V02 selected structural core |
|---|---:|---:|
| Training RMS | 4.34px | 2.29px (60 points) |
| Held-out RMS | 10.84px | 9.39px (8 points) |
| Training median | not the original headline | 1.56px |
| Core all-points median | not comparable | 1.70px |
| Core all-points RMS | not comparable | 3.87px |
| Worst observation | 26.83px | 18.64px (held-out) |

Geometry leave-one-view-out V02 RMS: **17.02px**, worst **68.59px**. These are independent structural test projections after the omitted camera's pose is fitted only to separate anchor points. They are not folded into the smaller core training RMS. Worst external-view current residual is **24.98px**. No poor camera or validation regime is hidden in a global average.

## Complete residual and landmark audit
All 198 original observations are retained in `calibration-v02/v01-residual-audit.csv` and JSON, sorted by descending V01 residual. Every row includes image/camera, landmark, category, observed/predicted X/Y, signed X/Y residual, Euclidean residual, confidence and visibility/identity reasoning. `all-observations-v02.csv` and JSON retain the same 198 rows with V02 status and predictions where genuinely fitted/projected, sorted by descending available V02 error; excluded points have empty V02 error fields, never fabricated zero error. Observations with no V02 projection remain visible as grey marks in the diagnostics.

All 48 V01 named landmarks are individually audited in `v01-landmark-audit.json`; per-landmark V02 JSON/CSV reports counts, RMS/max, confidence and inclusion. There is no residual-based automatic point purge.

### The exact 26.83px V01 failure
**Camera/image 13, `rw_base_L` (`rw_base`): 26.83px.** Observed [159, 233], predicted [185.173, 227.116]. The magnified evidence is `renders/v01-worst-residual-review-v02.jpg`.

The observed point is a rounded, oblique far-side black-glazing border. No unique sharp physical corner was established as the same 3D point in every view. Supported primary causes: **H — incorrect shared-landmark assumption**, **E — perspective/tangency ambiguity**. An uncertain annotation definition (A) and pose/depth uncertainty (F) can contribute. This is a closed-panel image: open tailgate displacement (C) is not the cause. No direct evidence supports different trim (B) or lens distortion (G) as the explanation. The same visibility/identity rule excludes analogous far rounded glazing picks even when their old residual was small.

### Confidence/identity decisions
| Class | Original observations | V02 treatment |
|---|---:|---|
| A high confidence | 88 | Visible hubs, finite-width tire contacts, clear fixed body lamp corners, clear closed windscreen intersections; initial structural solve |
| B medium | 60 | Grazing windscreen, grille/bumper/arch/rounded glass transitions; only six/eight stable windshield ties admitted after A initialization, others remain references |
| C low confidence | 50 | Documented current fixed-point assumption rejected; retained as visual/detail information |

Of the 50 rejected Class C observations, **28 previously had residual below 5px**. They were rejected for physical identity/visibility, not simply because errors were large. Tire-top silhouette tangencies and oblique arch apexes are not assured identical physical 3D surface points across camera directions. Rounded quarter-glass and hatch-seam apparent corners also lack verified point identity. This removes those assumptions instead of deleting only the worst numeric outlier.

Open-panel audit: moving door glass/edges, raised bonnet/hatch contours and moving hatch-lamp segments were already excluded from V01 picks and remain excluded. No moving-panel observation is fitted to the V02 closed-body frame. Rejected closed hatch-seam picks are a point-definition issue, not falsely labeled open-panel contamination. No unjustified inverse hinge transform is applied.

## Core set, exclusions and roles
Selected **core8**: 6, 7, 9, 8, 10, 11, 12, 13. These are the closed-panel front, both sides, rear and both front/rear quarter directions. They retain the visually compatible canonical silver body/trim. The documented initial core6 is also solved and fully reported. The selected core has **20 active structural landmarks**, **68 observations**: **60 Class A / 8 Class B**, divided into **60 training / 8 held out**. Eight medium-confidence windscreen ties enter after the high-confidence initialization, not as an unconstrained all-feature first solve.

Final observation dispositions: {'EXTERNAL VALIDATION': 12, 'CORE HELD-OUT': 8, 'CORE TRAINING': 60, 'EXTERNAL POSE ANCHOR': 16, 'REJECTED FIXED-POINT OBSERVATION': 50, 'DETAIL/VALIDATION REFERENCE ONLY': 52}. Thus 50 Class C observations are rejected as current fixed-point identities, 52 medium/detail picks are not fitted, and all remaining 96 structural projections across core and external views remain reported. Twenty-eight of the original 48 named landmark IDs are not active structural landmarks; this does not mean all 28 are invalid—many remain detail references.

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
| core6 | 1.87px | 8.35px | 21.97px | 86.28px | False |
| core8 | 2.29px | 9.39px | 17.02px | 68.59px | False |

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

Selected equivalent focal: **78.629mm**. Geometry-LOVO fold values range **72.70–81.25mm**. Bounded numerical plausibility: **PASS**, but actual physical intrinsics are not verified. Camera/depth generalization still fails.

A restrained ablation allowed only cameras 7/9/10/11 focal offsets (±12%, 5% prior), with fixed principal centers. Held-out RMS changed **9.393 → 9.387px**, still far above 5px; not promoted. The fitted focal equivalents are {'7': 78.51324941701701, '9': 78.62356477121628, '10': 78.21696239623509, '11': 79.31485736989549}. Extra flexibility is not used to force acceptance.

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
| 6 | 5 | 5.81px | 5 | 14.54px | 19.54px | 6 | FAIL |
| 7 | 5 | 1.88px | 5 | 7.70px | 11.35px | 6 | FAIL |
| 9 | 5 | 1.11px | 5 | 31.34px | 68.59px | 6 | FAIL |
| 8 | 4 | 5.60px | 2 | 15.07px | 16.01px | 6 | FAIL |
| 10 | 5 | 2.82px | 5 | 7.72px | 14.46px | 6 | FAIL |
| 11 | 5 | 1.11px | 5 | 14.25px | 16.82px | 6 | FAIL |
| 12 | 5 | 3.35px | 1 | 4.05px | 4.05px | 6 | FAIL |
| 13 | 5 | 1.70px | 1 | 18.81px | 18.81px | 6 | FAIL |

Nine anchor-only starting poses for omitted image 9 converge to the same anchor solution. It fits anchors at **1.11px RMS**, but independent projections are **31.34px RMS / 68.59px max**. Pose selection used anchor loss and priors only. This failure is not fixed by selecting the most flattering test result. Removing image 9 also moves `tl_top_L` by **0.142 wheelbase units** relative to the full solution, evidence of poor practical depth stability.

The full structural data-only normalized Jacobian is rank **69/69**, condition number approximately **705.8**. The classification is practical predictive underconstraint/instability, not a false assertion of exact rank deficiency. Remaining correspondence and camera-model uncertainty are not uniquely separable without stronger verified ties.

## Every camera — poor views retained
Positions are wheelbase units; yaw/pitch/roll are radians in JSON and degrees in CSV. All 12 camera poses are saved, but only eight fit shared geometry. Confidence remains globally unvalidated. Numerical plausibility is not geometric acceptance.

| Camera | Role | N | RMS | Median | Max | Held-out / independent | Focal equivalent |
|---|---|---:|---:|---:|---:|---:|---:|
| 1 | EXTERNAL pose only | 6 | 6.04px | 6.48px | 8.73px | 7.40px | 78.63mm |
| 2 | EXTERNAL pose only | 8 | 4.24px | 3.77px | 6.97px | 5.51px | 78.63mm |
| 3 | EXTERNAL pose only | 6 | 10.57px | 0.32px | 24.98px | 18.31px | 78.63mm |
| 4 | EXTERNAL pose only | 8 | 9.03px | 3.53px | 19.35px | 14.33px | 78.63mm |
| 6 | CORE | 10 | 1.92px | 1.58px | 4.14px | 4.14px | 78.63mm |
| 7 | CORE | 10 | 3.24px | 1.64px | 6.69px | 6.62px | 78.63mm |
| 8 | CORE | 6 | 1.37px | 0.89px | 2.69px | 2.69px | 78.63mm |
| 9 | CORE | 10 | 2.29px | 1.45px | 3.68px | 3.68px | 78.63mm |
| 10 | CORE | 10 | 3.53px | 2.95px | 6.78px | 3.87px | 78.63mm |
| 11 | CORE | 10 | 3.36px | 2.63px | 7.64px | 7.64px | 78.63mm |
| 12 | CORE | 6 | 5.97px | 1.65px | 14.26px | 14.26px | 78.63mm |
| 13 | CORE | 6 | 7.79px | 1.92px | 18.64px | 18.64px | 78.63mm |

Full positions, orientations, focal, confidence and inclusion are in `calibration-v02/per-camera-v02.csv` and `v02-solution.json`.

## All 48 named landmarks

| Landmark | V01 N | Classes | V01 RMS / max | V02 core N | V02 core RMS / max | Status |
|---|---:|---|---:|---:|---:|---|
| `h_out_L` | 5 | A | 5.28 / 6.74px | 3 | 2.92 / 4.14px | ACTIVE STRUCTURAL |
| `h_out_R` | 5 | A | 2.83 / 4.85px | 3 | 2.77 / 3.68px | ACTIVE STRUCTURAL |
| `h_in_L` | 5 | A | 4.21 / 5.79px | 3 | 1.99 / 3.33px | ACTIVE STRUCTURAL |
| `h_in_R` | 5 | A | 3.30 / 4.50px | 3 | 1.15 / 1.37px | ACTIVE STRUCTURAL |
| `g_top_L` | 4 | B | 4.00 / 5.83px | 0 | — | NOT FIT; reference/rejected assumption |
| `g_top_R` | 4 | B | 3.30 / 5.95px | 0 | — | NOT FIT; reference/rejected assumption |
| `g_low_L` | 4 | B | 7.63 / 9.81px | 0 | — | NOT FIT; reference/rejected assumption |
| `g_low_R` | 4 | B | 3.06 / 4.49px | 0 | — | NOT FIT; reference/rejected assumption |
| `bumper_L` | 2 | B | 6.20 / 7.99px | 0 | — | NOT FIT; reference/rejected assumption |
| `bumper_R` | 2 | B | 3.90 / 5.09px | 0 | — | NOT FIT; reference/rejected assumption |
| `ws_base_L` | 4 | A/B | 5.83 / 10.08px | 4 | 5.06 / 6.78px | ACTIVE STRUCTURAL |
| `ws_base_R` | 4 | A/B | 4.72 / 7.50px | 4 | 3.50 / 4.98px | ACTIVE STRUCTURAL |
| `ws_top_L` | 4 | A/B | 4.55 / 6.90px | 4 | 4.30 / 7.64px | ACTIVE STRUCTURAL |
| `ws_top_R` | 4 | A/B | 5.48 / 8.81px | 4 | 2.70 / 3.87px | ACTIVE STRUCTURAL |
| `q_ft_L` | 4 | B | 4.98 / 7.61px | 0 | — | NOT FIT; reference/rejected assumption |
| `q_ft_R` | 4 | B | 5.25 / 7.05px | 0 | — | NOT FIT; reference/rejected assumption |
| `q_fb_L` | 4 | B | 4.41 / 7.44px | 0 | — | NOT FIT; reference/rejected assumption |
| `q_fb_R` | 4 | B | 10.98 / 20.00px | 0 | — | NOT FIT; reference/rejected assumption |
| `q_rt_L` | 4 | C | 4.09 / 6.11px | 0 | — | NOT FIT; reference/rejected assumption |
| `q_rt_R` | 4 | C | 6.86 / 8.84px | 0 | — | NOT FIT; reference/rejected assumption |
| `q_rb_L` | 4 | C | 8.25 / 13.22px | 0 | — | NOT FIT; reference/rejected assumption |
| `q_rb_R` | 4 | C | 7.71 / 9.06px | 0 | — | NOT FIT; reference/rejected assumption |
| `tl_top_L` | 5 | A | 5.07 / 8.83px | 3 | 9.11 / 14.26px | ACTIVE STRUCTURAL |
| `tl_top_R` | 5 | A | 5.36 / 9.34px | 3 | 10.78 / 18.64px | ACTIVE STRUCTURAL |
| `tl_low_L` | 5 | A | 4.75 / 8.73px | 3 | 1.51 / 1.85px | ACTIVE STRUCTURAL |
| `tl_low_R` | 5 | A | 5.77 / 9.62px | 3 | 2.72 / 3.31px | ACTIVE STRUCTURAL |
| `rw_top_L` | 3 | B/C | 4.03 / 5.97px | 0 | — | NOT FIT; reference/rejected assumption |
| `rw_top_R` | 3 | B/C | 5.48 / 6.56px | 0 | — | NOT FIT; reference/rejected assumption |
| `rw_base_L` | 3 | B/C | 16.21 / 26.83px | 0 | — | NOT FIT; reference/rejected assumption |
| `rw_base_R` | 3 | B/C | 3.25 / 3.87px | 0 | — | NOT FIT; reference/rejected assumption |
| `hatch_low_L` | 3 | C | 16.32 / 26.27px | 0 | — | NOT FIT; reference/rejected assumption |
| `hatch_low_R` | 3 | C | 6.97 / 9.23px | 0 | — | NOT FIT; reference/rejected assumption |
| `arch_F_L` | 4 | B/C | 2.97 / 4.52px | 0 | — | NOT FIT; reference/rejected assumption |
| `arch_F_R` | 4 | B/C | 1.48 / 2.00px | 0 | — | NOT FIT; reference/rejected assumption |
| `arch_R_L` | 4 | B/C | 3.69 / 4.61px | 0 | — | NOT FIT; reference/rejected assumption |
| `arch_R_R` | 4 | B/C | 5.05 / 6.58px | 0 | — | NOT FIT; reference/rejected assumption |
| `wc_F_L` | 4 | A | 1.34 / 1.56px | 3 | 1.32 / 1.94px | ACTIVE STRUCTURAL |
| `contact_F_L` | 6 | A | 2.28 / 3.36px | 4 | 2.09 / 2.55px | ACTIVE STRUCTURAL |
| `tiretop_F_L` | 4 | C | 3.71 / 5.80px | 0 | — | NOT FIT; reference/rejected assumption |
| `wc_F_R` | 4 | A | 1.93 / 3.32px | 3 | 2.18 / 3.59px | ACTIVE STRUCTURAL |
| `contact_F_R` | 6 | A | 2.53 / 5.64px | 4 | 1.80 / 2.79px | ACTIVE STRUCTURAL |
| `tiretop_F_R` | 4 | C | 4.14 / 7.18px | 0 | — | NOT FIT; reference/rejected assumption |
| `wc_R_L` | 4 | A | 1.83 / 3.18px | 3 | 1.37 / 2.03px | ACTIVE STRUCTURAL |
| `contact_R_L` | 6 | A | 2.18 / 2.54px | 4 | 1.16 / 1.58px | ACTIVE STRUCTURAL |
| `tiretop_R_L` | 4 | C | 3.47 / 4.72px | 0 | — | NOT FIT; reference/rejected assumption |
| `wc_R_R` | 4 | A | 1.81 / 2.93px | 3 | 1.53 / 1.85px | ACTIVE STRUCTURAL |
| `contact_R_R` | 6 | A | 2.69 / 3.58px | 4 | 1.32 / 2.20px | ACTIVE STRUCTURAL |
| `tiretop_R_R` | 4 | C | 5.34 / 8.16px | 0 | — | NOT FIT; reference/rejected assumption |

Per-observation exclusions and visibility reasons remain in the linked CSV/JSON; excluded landmarks are not assigned fake V02 zero residuals.

## View compatibility matrix
S = strongly compatible visible closed configuration; T = compatible for static structural calibration only (open versus closed); L = limited common visibility in open views. These are visual/configuration assessments, not a claim that calibration passed. No incompatible trim is established. Open-panel corners must never be equated to their closed positions.

| Image | 1 | 2 | 3 | 4 | 6 | 7 | 8 | 9 | 10 | 11 | 12 | 13 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | — | L | L | L | T | T | T | T | T | T | T | T |
| 2 | L | — | L | L | T | T | T | T | T | T | T | T |
| 3 | L | L | — | L | T | T | T | T | T | T | T | T |
| 4 | L | L | L | — | T | T | T | T | T | T | T | T |
| 6 | T | T | T | T | — | S | S | S | S | S | S | S |
| 7 | T | T | T | T | S | — | S | S | S | S | S | S |
| 8 | T | T | T | T | S | S | — | S | S | S | S | S |
| 9 | T | T | T | T | S | S | S | — | S | S | S | S |
| 10 | T | T | T | T | S | S | S | S | — | S | S | S |
| 11 | T | T | T | T | S | S | S | S | S | — | S | S |
| 12 | T | T | T | T | S | S | S | S | S | S | — | S |
| 13 | T | T | T | T | S | S | S | S | S | S | S | — |

Pair-specific reasons are recorded in `calibration-v02/view-compatibility.json`. The supplied view coverage is complete enough to continue investigating existing correspondences. New controlled captures are not requested because necessity has not been demonstrated.

## Current worst residual and visual gate
Core worst: image **13**, `tl_top_R`, **18.64px**, held out. It is a fixed body lamp point in a closed view; moving-panel contamination is not an explanation. Other strong observations can fit tightly while this untrained projection misses, exposing the pose/depth/generalization issue. It remains visible and counted. The worst external static-lamp residual is 24.98px; worst geometry-LOVO residual is 68.59px.

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

Blender/source checks: version 5.2.2 LTS, `/usr/bin/blender`; all 96 current structural projections independently match the numeric solver in Blender to **0.000632px** maximum. Body mesh count is zero. Frame/contact symmetry, finite values and all 48/198 audit coverage checks passed. These verify implementation consistency, not calibration accuracy.

Website: UNCHANGED. Hero/cars/current vehicle, navigation, Titanium Bronze, Services, Gallery, enquiry and AI unchanged. Inside TOLI remains removed. Protected original and separate 3D projects: UNCHANGED. GLB: NOT EXPORTED. Deployment: NOT PERFORMED. Production web/device tests are not rerun because no application/model integration changed. Read-only before/after source/config and static public/model hash verification is recorded separately in `calibration-v02/protection-verification-v02.json` after installation. V01 and previous milestones remain untouched.
