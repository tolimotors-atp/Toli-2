# Existing-photo Milestone 1 completed — Decision C

**PRIMARY BODY REMAINS GENERIC / INCORRECT — NO PRODUCTION APPROVAL. STOP.**

The user-authorized existing-photo branch has completed Milestone 1. Do not automatically advance to identity/details or create another reconstruction branch. Report: [EXISTING_PHOTO_PRODUCTION_V01_REPORT.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/EXISTING_PHOTO_PRODUCTION_V01_REPORT.md). Old models, the controlled-capture workspace and website assets remain preserved. No GLB export.

The authorization and prior freeze below are retained as history; they do not reopen this failed milestone.

# Scoped authorization — existing-photo visual reconstruction

The user explicitly authorized a new, separate **existing-photo production-candidate V01, Milestone 1 only** branch on 2026-11-08. This overrides the controlled-photo waiting requirement for that branch, without describing the existing photos as controlled/calibrated or conferring production approval.

Old curve-cage, patch, calibration and photogrammetry routes remain frozen. Preserve all earlier models. No website replacement or GLB export is authorized. Stop after the Milestone 1 body review even if it passes. See [EXISTING_PHOTO_REGION_MAP.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/EXISTING_PHOTO_REGION_MAP.md).

The prior authoritative freeze is preserved below and in `existing-photo-production-v01/pre-authorization-status.md`.

# MU-X reconstruction status

**PROCEDURAL RECONSTRUCTION FROZEN**

**FROZEN — WAITING FOR NEW GEOMETRIC EVIDENCE**

Authoritative current checkpoint: 2026-11-08. This status supersedes older continuation instructions and approval implications in historical reports, filenames, runners and UI labels. Historical reports and artifacts are preserved, not rewritten.

## Reason

Existing uncontrolled photographs do not constrain compound exterior depth sufficiently for the current procedural reconstruction methods to meet the visual fidelity gate. Surface Prototype V03 ended in **Decision C**. Engineering correctness and improved boundary metrics do not override the failed visual comparison. This is the outcome of the attempted implementations, not proof that every possible reconstruction method is useless.

## Approval and export

- Production model: **NONE APPROVED**. Production exterior: **NOT APPROVED**.
- Website model: **NONE APPROVED FOR REPLACEMENT**.
- GLB: **NOT EXPORTED in this checkpoint**. No new production export is permitted from current candidates.
- An older website asset may exist at [isuzu-mux-web.glb](/home/thunder/shared/tolimotors-main1/toli-static-website/public/models/vehicles/isuzu-mux/isuzu-mux-web.glb). It is unchanged. Historical export or activation is not current visual approval and does not authorize another replacement.

## Do not restart

**DO NOT START ANOTHER PROCEDURAL BODY / CURVE / PATCH ITERATION WITHOUT NEW GEOMETRIC EVIDENCE.**

No Surface Prototype V04, Curve Cage V05, manual curve pass, topology-density pass, full exterior, deep detailing or production GLB. Do not run regeneration/export entry points merely because they remain available. No reconstruction from the controlled-capture workspace until new controlled photographs actually arrive.

## Preserved classifications

| Class | Material | Permitted interpretation |
|---|---|---|
| REUSABLE | Nominal dimensions, fixed axles/wheel anchors, image-space measurements, reference inventory, camera definitions, diagnostics, validation and generator infrastructure | Reuse as documented constraints/tooling, with their uncertainty retained |
| EXPERIMENTAL | V04 curve cage | **REFERENCE / PROPORTION FRAMEWORK — NOT PRODUCTION BODY** |
| EXPERIMENTAL | Surface V01/V02/V03 | **SURFACE-CONSTRUCTION EXPERIMENTS — NOT PRODUCTION BODY** |
| REJECTED AS PRODUCTION GEOMETRY | All current and earlier exterior-body candidates | Research history only; do not integrate, delete, promote or export |

Protected masters:

- [isuzu-mux-reference-curve-cage-v04.blend](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v04.blend)
- [isuzu-mux-crossview-surface-prototype-v01.blend](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v01.blend)
- [isuzu-mux-crossview-surface-prototype-v02.blend](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v02.blend)
- [isuzu-mux-crossview-surface-prototype-v03.blend](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v03.blend)

All other masters, backups and diagnostics under [source](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source) and [renders](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders) remain in place. Directory names such as `production`, `master`, `generated` or `export` do not confer approval. Earlier procedural/body-pass, authored, multi-view, reference-constrained, greenhouse, generated/code-generated, rounded/soft and curve-derived body candidates are all unapproved.

## V03 engineering successes

- 593 base vertices; 8,252 evaluated vertices; 15,680 evaluated triangles; all base faces quads.
- Independent-zone cracks 0; base/evaluated degenerates 0; unintended interior non-manifold edges 0; non-adjacent evaluated overlaps 0.
- Strict base-control symmetry discrepancy 0.0.
- Delete/regenerate PASS; crease/subdivision reproducibility PASS; dimension locks PASS; fixed wheel transforms PASS.
- These checks concern the independent construction zones, not a watertight full vehicle or calibrated shape accuracy.

## V03 visual failure and retained passes

| Zone | Unresolved visual problems | Retained successful information |
|---|---|---|
| A | Tab-like cowl/A-pillar root; diffuse bonnet edge roll; compressed arch-end reflections | Structural cross-section and technical diagnostics remain useful |
| B | Quarter-aperture shape; inflated D-pillar; concentrated frame-junction reflections; roof flow | Quarter and rear-glass boundary numerical improvements |
| C | Over-rolled upper lamp bridge; compressed aperture returns; pinched lower-corner reflections | Rear-quarter mass and compound bumper-wrap preservation |

No zone passed shape, cross-view agreement, soft finish, reflection and reference fidelity together. These are major remaining failures.

## Boundary metrics

**MODEL-SPACE DIAGNOSTIC DISTANCES — NOT VEHICLE ACCURACY**

| Boundary / state | V01 mean / maximum | V02 mean / maximum | V03 mean / maximum |
|---|---:|---:|---:|
| quarter_glass / base | 0.00444347 / 0.01489262 | 0.00212054 / 0.01533179 | 0.00212054 / 0.01533179 |
| quarter_glass / evaluated | 0.01385265 / 0.03944359 | 0.01176544 / 0.02738808 | 0.00565251 / 0.02249335 |
| rear_glass / base | 0.00492820 / 0.02117570 | 0.00492820 / 0.02117570 | 0.00492820 / 0.02117570 |
| rear_glass / evaluated | 0.00905456 / 0.02916746 | 0.00911923 / 0.02931030 | 0.00699804 / 0.02457996 |

Quarter measurements use 192 fixed-reference samples against interface edge segments in 3D; rear uses 264 samples in Y/Z because X depth is inferred. These are approximate, one-directional reference-to-boundary distances. Base and evaluated edge sampling differ. Numerical improvement does not establish matching surfaces or physical vehicle accuracy. Source: [boundary-deviations.json](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/boundary-deviations.json).

## Attempted routes and final limitations

| Route | Why it did not produce production-approved geometry | Preserved value / record |
|---|---|---|
| 1. Procedural body modeling | Generic massing and surface cuts failed MU-X silhouette/identity; technical completion was insufficient | Body-pass masters and [REFERENCE_AUDIT.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/REFERENCE_AUDIT.md) |
| 2. Control-cage refinement | Refinement/exact-cut passes did not lock cross-view proportions or clean automotive surfaces | [milestones](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/milestones) |
| 3. Clean authored body | Basic volume, greenhouse, fender, fascia and continuity gates failed | [RECONSTRUCTION_PROGRESS.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/RECONSTRUCTION_PROGRESS.md); authored masters/landmarks |
| 4. Multi-view calibration | Camera parameters/depth remained underconstrained; inconsistent projections did not establish a reliable body | [MULTIVIEW_RECONSTRUCTION_V01.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/MULTIVIEW_RECONSTRUCTION_V01.md) |
| 5. Robust calibration | Identity/outlier audit improved rigor, but neither tested core subset passed independent validation/conditioning | [MULTIVIEW_RECONSTRUCTION.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/MULTIVIEW_RECONSTRUCTION.md); retained observations/residuals |
| 6. Reference-constrained reconstruction | Manual constraints improved traceability but did not determine correct compound surfaces | [visual-gate.json](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/reconstruction/reference-constrained-v01/visual-gate.json) |
| 7. Greenhouse reconstruction | Glazing, pillar, roof and cross-view surface gates remained failed after precision/surface-method trials | [GREENHOUSE_PRECISION_V02.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/GREENHOUSE_PRECISION_V02.md); greenhouse diagnostics |
| 8. Local photogrammetry/depth experiment | Tested CPU SfM did not register a sparse model; relative neural depth did not materially recover missing geometry | [LOCAL_RECONSTRUCTION_REPORT.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/LOCAL_RECONSTRUCTION_REPORT.md); tool/license logs and maps |
| 9. Code-generated body | V04 improved the front, but side/rear identity and cross-view fidelity remained insufficient | [GENERATED_MODEL_REPORT.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/GENERATED_MODEL_REPORT.md) and [CODE_GENERATED_MODEL_REPORT.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/CODE_GENERATED_MODEL_REPORT.md) |
| 10. Curve-cage reconstruction | V04 improved image-space proportions but did not solve trustworthy 3D joins/depth or automotive surfaces | [REFERENCE_CURVE_CAGE_V04_REPORT.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/REFERENCE_CURVE_CAGE_V04_REPORT.md) |
| 11. Cross-view surface patches | V03 topology improved drift and technical structure but left major cowl/fender/D-pillar/lamp reflection failures | [CROSSVIEW_SURFACE_PROTOTYPE_V03_REPORT.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/CROSSVIEW_SURFACE_PROTOTYPE_V03_REPORT.md) |

**METHOD FAILED TO REACH PRODUCTION VISUAL QUALITY** does not mean **METHOD PRODUCED NO VALUE**. Preserve the measurements, negative results and validation infrastructure. No repeat audit of the same photos is warranted without new source material.

## Acceptable future evidence

1. **Preferred zero-cost route: NEW CONTROLLED PHOTO CAPTURE.** Reuse [CONTROLLED_CAPTURE_GUIDE.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/controlled-capture/instructions/CONTROLLED_CAPTURE_GUIDE.md). Do not make another guide or start a reconstruction now. Capture must remain safely accessible: no climbing, crawling under vehicles, entering traffic or unsafe workshop positioning.
2. **VERIFIED FREE / LEGALLY USABLE BASE ASSET.** Correct MU-X generation/body family; free with no purchase; license permits intended website use and modification; actual geometry is a usable legitimate base. No searching, downloading or integration in this checkpoint. **NO PAID ASSET** remains mandatory.
3. **USER-PROVIDED BASE:** BLEND, FBX, OBJ, GLB or GLTF. Audit generation/body match, scale, topology, provenance/license, exterior accuracy and practical usefulness before modifying it.
4. Better calibrated multi-view imagery or reliable dimensional/body-section data may also justify a new assessment.

## Known unsolved depth

- Bonnet/fender compound depth
- Cowl/A-pillar root
- Front fender volume
- Roof/D-pillar transition
- Rear-quarter volume
- Lamp/quarter relationship
- Rear bumper corner
- Rear-body/D-pillar composition

These regions must not be treated as solved by a later script.

## Consolidated records and checkpoint validation

- [REUSABLE_RECONSTRUCTION_DATA.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/REUSABLE_RECONSTRUCTION_DATA.md)
- [BEST_EVIDENCE_INDEX.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/BEST_EVIDENCE_INDEX.md)
- [FREEZE_VALIDATION.json](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/FREEZE_VALIDATION.json)
- [FREEZE_PRESERVATION_MANIFEST.json](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/FREEZE_PRESERVATION_MANIFEST.json)

Zero new vehicle geometry. Website/Hero/navigation/TOLI AI unchanged. Controlled capture and protected projects preserved. No GLB export, download, deployment or Git commit. Cost ₹0 / $0. Website browser tests are not required for this documentation-only checkpoint.

**DO NOT START ANOTHER PROCEDURAL RECONSTRUCTION PASS UNTIL NEW GEOMETRIC EVIDENCE IS AVAILABLE.**
