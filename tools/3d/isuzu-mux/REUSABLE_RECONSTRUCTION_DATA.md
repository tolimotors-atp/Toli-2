# Reusable MU-X reconstruction data

**FROZEN RESEARCH DATA — NO PRODUCTION BODY APPROVED**

Current authority: [RECONSTRUCTION_STATUS.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/RECONSTRUCTION_STATUS.md). Reuse evidence and tooling; do not rerun a frozen body generator.

## Centralized nominal dimensions and fixed anchors

Code authority: [parameters.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/parameters.py) (`BASE`). This checkpoint does not copy dimensions into another code/config module. The values below are documentation read from that source. They are the frozen nominal project framework, not newly measured factory dimensions or proof of photo calibration.

| Parameter | Nominal metres |
|---|---:|
| length | 4.8250 |
| width | 1.8600 |
| height | 1.8600 |
| wheelbase | 2.8450 |
| track | 1.5700 |
| tire_diameter | 0.7640 |

Coordinates: front is negative X, rear positive X, Z up, ground Z=0; Y signs identify lateral sides. Historical modules use differing side-label conventions, so verify a part’s coordinate convention before assigning driver/left/right names.

Wheel centres are derived from the centralized wheelbase/track/tire values: X=±wheelbase/2, Y=±track/2, Z=tire_diameter/2. No new independent wheel constants are introduced.

| Anchor | X | Y | Z |
|---|---:|---:|---:|
| Front, negative Y | -1.4225 | -0.7850 | 0.3820 |
| Front, positive Y | -1.4225 | 0.7850 | 0.3820 |
| Rear, negative Y | 1.4225 | -0.7850 | 0.3820 |
| Rear, positive Y | 1.4225 | 0.7850 | 0.3820 |

Anchor implementation: [cage_ui.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/cage_ui.py) (`support`) and preserved V04 master. V03 checks confirm wheel transforms unchanged. Wheel cylinders are construction anchors, not accurate wheel/tire assets.

## Reference inventory and strongest views

Authoritative originals: [Isuzu MU-X](</home/thunder/shared/tolimotors-main1/Isuzu MU-X>). Existing reconciled inventory contains **18 originals**: [inventory.json](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/references/authoritative-folder/inventory.json). Prior historical/clipboard library: [inventory.json](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/references/complete-library/inventory.json). Do not confuse its 34 historical entries with the 18 originals in the corrected authoritative folder.

Preserve [REFERENCE_AUDIT.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/REFERENCE_AUDIT.md) and [REFERENCE_FOLDER_RECONCILIATION.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/REFERENCE_FOLDER_RECONCILIATION.md). The canonical silver open-panel body family remains the identity authority; compatible closed-panel views support closed contours. Ignore paint color, exclude incompatible generation/body families, and never trace displaced open panels as closed body geometry. Exact year/trim remains unverified. Original images are not renamed, edited or overwritten.

| View | Existing primary |
|---|---|
| Front | [Screenshot From 2026-11-06 18-17-10.png](</home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-10.png>) |
| Front three-quarter | [Screenshot From 2026-11-06 18-17-27.png](</home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-27.png>) |
| Side | [Screenshot From 2026-11-06 18-17-14.png](</home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-14.png>) |
| Rear three-quarter | [Screenshot From 2026-11-06 18-17-31.png](</home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-31.png>) |
| Rear | [Screenshot From 2026-11-06 18-17-18.png](</home/thunder/shared/tolimotors-main1/Isuzu MU-X/Screenshot From 2026-11-06 18-17-18.png>) |

Rear 3Q 18-17-31 is the orientation used by V02/V03 comparison crops. The existing 18-17-35 image is an opposite-side alternative used by some older helpers; do not silently swap comparison orientations. Open-panel front/side/rear views support panel relationships and identity; interior/engine images do not calibrate exterior depth.

## Image-space proportion maps

**IMAGE-SPACE REFERENCE RATIOS — NOT CALIBRATED PHYSICAL DIMENSIONS**

Source: [reference-proportions.json](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04/reference-proportions.json). Values are hand-read visible feature width divided by visible body width excluding mirrors; perspective and landmark uncertainty remain. Read `reference_ratio`, not `fit_target` or `v04_render_ratio`, when recovering the photograph measurement.

| Feature | Approximate photograph ratio |
|---|---:|
| front: Lower windscreen width | 0.771 |
| front: Grille surround width | 0.588 |
| front: Lower opening width | 0.529 |
| rear: Rear glass lower width | 0.857 |
| rear: Upper bumper width | 0.958 |
| rear: Lower bumper width | 0.857 |

Maps: [front-proportion-map.jpg](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04/front-proportion-map.jpg); [rear-proportion-map.jpg](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04/rear-proportion-map.jpg). Width stations and internal guide depth remain inferred; these maps must not be promoted to measured body sections.

## Window boundary information

V04 `TRACE_QUARTER_GLASS`, `TRACE_REAR_GLASS`, windscreen/A-pillar and roof-edge traces are reusable visual constraints, not exact factory glazing geometry. Preserve [traced_data.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/traced_data.py), [convergence_data.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/convergence_data.py) and the V04 master. Preserve the boundary measurement implementation and [boundary-deviations.json](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/boundary-deviations.json). Quarter shape/drift must be assessed separately; rear Y/Z improvements do not solve rear-glass X depth or D-pillar form.

## Fixed validation cameras

Keep front, front 3Q, side, rear 3Q and rear definitions in [operators.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/operators.py) (`VIEWS`, `cameras`). These are orthographic comparison cameras, not recovered photographic intrinsics. Exact zone camera transforms/framing used for V01/V02/V03 comparisons: [fixed-v01-cameras.json](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/fixed-v01-cameras.json). Keep [surface_diagnostics.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/surface_diagnostics.py) for the same neutral clay, strip-reflection and zebra setup; do not change lighting to conceal defects.

## Known visual characteristics

- Tall/upright older MU-X body family; swept angular projector headlamp envelopes and two heavy chrome grille bars.
- Polygonal fog-light surrounds, substantial fender/arch mass and roof rails/side steps where visible.
- Upright rear quarter-glass character; broad split wraparound rear lamps; horizontal tailgate garnish and recessed central plate area.
- RHD interior evidence is useful for a later approved base, not for reconstructing invisible exterior surfaces.
- Exact trim, hidden sections, lens calibration and physical depth are not established.

## Uncertain geometry — never assume solved

- Bonnet/fender compound depth
- Cowl/A-pillar root
- Front fender volume
- Roof/D-pillar transition
- Rear-quarter volume
- Lamp/quarter relationship
- Rear bumper corner
- Rear-body/D-pillar composition

## Generator module classification

All modules are retained. KEEP means reusable infrastructure or diagnostic pattern, not permission to execute a stage-specific runner. KEEP AS EXPERIMENTAL means retained constraints/experiments. DO NOT USE AS PRODUCTION GEOMETRY means preserve the failed geometry logic as research only. Mixed modules are classified at function level in the notes. Nothing is deleted, relocated or rewritten.

| Module | Classification | Retained purpose / restriction |
|---|---|---|
| [__init__.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/__init__.py) | KEEP | Dimensions/registration/UI or technical diagnostics; stage-specific controls remain frozen and technical PASS is not visual approval. |
| [audit_surface_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/audit_surface_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_cage.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_cage.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_cage_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_cage_v02.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_cage_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_cage_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_cage_v04.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_cage_v04.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_curve.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_curve.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_rounded.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_rounded.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_soft.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_soft.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_surface_prototype.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_surface_prototype.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_surface_prototype_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_surface_prototype_v02.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_surface_prototype_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_surface_prototype_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [boards_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/boards_v02.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [cage_ui.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/cage_ui.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [check_cage.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_cage.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_cage_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_cage_v02.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_cage_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_cage_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_cage_v04.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_cage_v04.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_curve.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_curve.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_milestone.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_milestone.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_rounded.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_rounded.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_soft.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_soft.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_surface_prototype.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_surface_prototype.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_surface_prototype_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_surface_prototype_v02.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_surface_prototype_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_surface_prototype_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [check_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/check_v02.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [convergence_data.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/convergence_data.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [curve_ui.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/curve_ui.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [diagnose_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/diagnose_v02.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [diagnostics_cage_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/diagnostics_cage_v02.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [diagnostics_cage_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/diagnostics_cage_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [diagnostics_cage_v04.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/diagnostics_cage_v04.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [extra_boards_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/extra_boards_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [geometry/__init__.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/__init__.py) | DO NOT USE AS PRODUCTION GEOMETRY — MIXED | Keep generic material/mesh/symmetry helpers; generate/body_sections/cabin_sections/cut_arch/windows produced unapproved bodies. |
| [geometry/continuity.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/continuity.py) | KEEP | Dimensions/registration/UI or technical diagnostics; stage-specific controls remain frozen and technical PASS is not visual approval. |
| [geometry/converged_cage.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/converged_cage.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [geometry/curves.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/curves.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [geometry/depth_cage.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/depth_cage.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [geometry/flow_cage.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/flow_cage.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [geometry/reference_cage.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/reference_cage.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [geometry/rounded.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/rounded.py) | DO NOT USE AS PRODUCTION GEOMETRY | Frozen body/surface construction logic. Shared-net/boundary-class ideas remain research, not approved MU-X shape. |
| [geometry/section_network.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/section_network.py) | DO NOT USE AS PRODUCTION GEOMETRY | Frozen body/surface construction logic. Shared-net/boundary-class ideas remain research, not approved MU-X shape. |
| [geometry/soft_body.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/soft_body.py) | DO NOT USE AS PRODUCTION GEOMETRY | Frozen body/surface construction logic. Shared-net/boundary-class ideas remain research, not approved MU-X shape. |
| [geometry/surface_patch.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/geometry/surface_patch.py) | DO NOT USE AS PRODUCTION GEOMETRY | Frozen body/surface construction logic. Shared-net/boundary-class ideas remain research, not approved MU-X shape. |
| [join_debug.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/join_debug.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [join_evidence_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/join_evidence_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [join_evidence_v04.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/join_evidence_v04.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [measure_proportions_v04.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/measure_proportions_v04.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [mux_curve_data.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/mux_curve_data.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [mux_shape_data.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/mux_shape_data.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [operators.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/operators.py) | KEEP — MIXED | Keep cameras, validation/render/export framework. Generate/Regenerate/Reset remain experimental; Export is retained but must not be run on current candidates. |
| [overlay_soft.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/overlay_soft.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [panels.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/panels.py) | KEEP | Dimensions/registration/UI or technical diagnostics; stage-specific controls remain frozen and technical PASS is not visual approval. |
| [parameters.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/parameters.py) | KEEP | Dimensions/registration/UI or technical diagnostics; stage-specific controls remain frozen and technical PASS is not visual approval. |
| [reference_data.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/reference_data.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [render_cage_gates.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/render_cage_gates.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [render_combs_v04.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/render_combs_v04.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [render_joins_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/render_joins_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [render_joins_v04.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/render_joins_v04.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [render_surface_prototype.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/render_surface_prototype.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [render_surface_prototype_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/render_surface_prototype_v02.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [render_surface_prototype_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/render_surface_prototype_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [rounded_ui.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/rounded_ui.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_cage.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_cage.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_cage_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_cage_v02.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_cage_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_cage_v03.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_cage_v04.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_cage_v04.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_curve.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_curve.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_milestone.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_milestone.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_rounded.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_rounded.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_soft.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_soft.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_surface_prototype.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_surface_prototype.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_surface_prototype_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_surface_prototype_v02.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_surface_prototype_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_surface_prototype_v03.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [run_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/run_v02.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [sections_surface_v02.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/sections_surface_v02.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [sections_surface_v03.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/sections_surface_v03.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [surface_diagnostics.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/surface_diagnostics.py) | KEEP | Dimensions/registration/UI or technical diagnostics; stage-specific controls remain frozen and technical PASS is not visual approval. |
| [surface_ui.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/surface_ui.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [surfaces.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/surfaces.py) | DO NOT USE AS PRODUCTION GEOMETRY — MIXED | Keep generic material/mesh/symmetry helpers; generate/body_sections/cabin_sections/cut_arch/windows produced unapproved bodies. |
| [test_topology_cage.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/test_topology_cage.py) | KEEP | Validation, reproducibility, measurements, section or render diagnostic tooling; model-specific assumptions/paths need review for a future approved input. Do not invoke generators during freeze. |
| [traced_data.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/traced_data.py) | KEEP AS EXPERIMENTAL | MU-X-specific traces, inferred shape/depth, generator runner or construction UI; preserve historical decisions and do not regenerate without new evidence. |
| [validation.py](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons/toli_mux_generator/validation.py) | KEEP | Dimensions/registration/UI or technical diagnostics; stage-specific controls remain frozen and technical PASS is not visual approval. |

## Restart inputs and restrictions

Preferred: new controlled photos using [CONTROLLED_CAPTURE_GUIDE.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/controlled-capture/instructions/CONTROLLED_CAPTURE_GUIDE.md). Alternatives: suitable verified free legally usable MU-X base, user-provided BLEND/FBX/OBJ/GLB/GLTF, better calibrated views or reliable body-section dimensions. Audit generation, scale, topology, provenance/license and accuracy first. No paid asset. No current search/download/integration. Do not generate another guide or repeat the completed audit without changed evidence.
