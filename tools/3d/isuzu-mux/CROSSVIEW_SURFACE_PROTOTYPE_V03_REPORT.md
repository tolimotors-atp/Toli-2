# CROSS-VIEW SURFACE PROTOTYPE V03

C — TARGETED TOPOLOGY DID NOT SOLVE THE SURFACE PROBLEMS; STOP THIS APPROACH

This is the decisive local topology trial, not a production model. The numerical aperture goals improved, but the same major shape/reflection defects remain. They are not minor adjoining-patch issues. Stop this implementation here; no V04 prototype or full-body expansion is authorized or generated.

Blender: **5.2.2 LTS**, executable `/usr/bin/blender`. Master: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v03.blend`. V01, V02, the V04 curve cage and earlier masters are preserved. The pre-V03 generator is archived under `code-generator/pre-surface-prototype-v03-addon/`.

## Zone A

Root volume: **NEEDS WORK**. The four-column root is no longer a stretched two-column strip. It has an outer flank, crown and glass-side construction edge, verified by actual X-plane sections. It still reads as an upturned tab/ear in side and three-quarter views and does not convincingly reproduce the photographed cowl/windscreen/A-root relationship.

Bonnet edge roll: **NEEDS WORK**. One varying support rail per side separates the broad bonnet from its roll. The control net can vary radius longitudinally, but the evaluated surface still looks too diffuse and the highlight progression is not convincingly MU-X-like. No global bevel or extra subdivision level is used.

Arch termination: **NEEDS WORK**. The trailing construction row is dropped locally to release the previous upward hook; the full arch is not widened. Compression remains near the arch termination and the resulting silhouette is still not reference-converged.

Shape / cross-view / soft finish / reflection / reference fidelity: **NEEDS WORK** for each. Root and roll improvements do not justify a zone pass.

## Zone B

Quarter aperture: **NEEDS WORK** visually. One support ring controls subdivision contraction without stacking several packed loops. The forward outer frame is widened locally to prevent control-face folding; the authoritative aperture curve is unchanged.

Quarter drift: **PASS for the stated relative reduction**, not a physical-accuracy certification. Evaluated mean/max reduce from V02 0.011765/0.027388 to V03 0.005653/0.022493. Base quarter values are unchanged from V02.

D-pillar: **NEEDS WORK**. A three-band cross-pillar section replaces the two-band bridge and removes its arbitrary lateral bulge. It still reads locally inflated and the roof/window/glass junction remains optically concentrated.

Rear-glass drift: **PASS for the stated numerical gate**. Added edge columns, matching roof-return columns and a retained defined-but-finite boundary weight of 0.74 reduce evaluated mean/max below both V01 and V02.

Frame junctions / roof flow: **NEEDS WORK**. Support stays near roof edges rather than the broad centre. However, the pole audit still finds eight extraordinary vertices adjacent to reflection-sensitive B patches. The main junction poles were not successfully relocated out of the sensitive transition. Additional rows did not solve that graph-level problem.

Shape / cross-view / soft finish / reflection / reference fidelity: **NEEDS WORK** for each. The drift gains do not override the visible surface failures.

## Zone C

Lamp bridge: **NEEDS WORK**. A six-quad shoulder strip per side gives real surface area above the aperture, rather than only widening the old thin strip. Its silhouette is now substantial but still over-rolled and not naturally integrated with the reference shoulder/tailgate-side body.

Aperture return: **NEEDS WORK**. A new deeper ring separates return depth from the existing radius row. The return follows an inferred inward corner normal rather than a constant X extrusion; the latter was tested and rejected because it intersected the quarter. The aperture remains empty and its reference Y/Z cut is retained. Reflection compression persists around the upper/inner return.

Lower corner: **NEEDS WORK**. The V02 compound wrap and lower-row spacing are preserved; no unnecessary loop was added to the already tight arch/lower band. The dedicated lower-corner comparison still shows a concentrated vertical turn. It is not a minor seam that full-body assembly would automatically solve.

Quarter mass: **PASS for preservation**. Bumper wrap: **PASS for preservation**. The quarter-crown controls and compound `corner_x` function are unchanged. Neither pass approves the complete zone.

Shape / cross-view / soft finish / reflection / reference fidelity: **NEEDS WORK** for each.

## Boundary metrics

| Boundary / state | V01 mean / max | V02 mean / max | V03 mean / max |
|---|---:|---:|---:|
| quarter_glass / base | 0.00444347 / 0.01489262 | 0.00212054 / 0.01533179 | 0.00212054 / 0.01533179 |
| quarter_glass / evaluated | 0.01385265 / 0.03944359 | 0.01176544 / 0.02738808 | 0.00565251 / 0.02249335 |
| rear_glass / base | 0.00492820 / 0.02117570 | 0.00492820 / 0.02117570 | 0.00492820 / 0.02117570 |
| rear_glass / evaluated | 0.00905456 / 0.02916746 | 0.00911923 / 0.02931030 | 0.00699804 / 0.02457996 |

Approximate uncalibrated model coordinates. Quarter uses 192 dense fixed reference samples and actual patch-interface edge segments in 3D; rear glass uses 264 samples in Y/Z because depth X is inferred. Nearest segment distance is measured in the reference-to-boundary direction. V03 rear boundaries have 14 base / 56 evaluated segments after support columns; quarter remains 12 / 48. A lower one-way deviation does not prove complete boundary or visual agreement.

## Topology changes

### Zone A
Added **40**, removed **12**, net **+28**. Separate changing bonnet roll radius from the bonnet plane; give root a transverse crown and outer/glass-side control.

{"bonnet_roll_rail": 16, "replacement_four_column_root_sections": 24}. Removed: 12 vertices of the former two-column root strips.

### Zone B
Added **72**, removed **13**, net **+59**. Isolate aperture drift control from the D crown, provide a deliberate cross-pillar section and match shared return/roof edges without T-junctions.

{"quarter_aperture_support": 24, "new_D_intermediate_columns": 20, "new_roof_return_interior_nodes": 10, "rear_glass_edge_columns": 10, "outer_roof_matching_columns": 8}. Removed: 10 former D middle-column nodes plus 3 otherwise-unshared old roof-return middle nodes.

### Zone C
Added **36**, removed **0**, net **+36**. Separate return depth from edge radius; create a painted upper bridge with actual surface area. Preserve quarter-crown and compound bumper controls.

{"deeper_return_ring": 24, "upper_lamp_shoulder": 12}. Removed: None; existing return/bridge nodes are repositioned, not removed.

A flow: the bonnet rail follows the existing longitudinal grid; the cowl root shares a wider four-node foot with that grid. The two root boundary poles move to the wider foot endpoints, not the bonnet crown.

B flow: aperture support, three-band D sections, four-row roof return and seven-column glass/outer-roof sections share exact vertices. No T-junction is hidden by subdivision. The eight sensitive extraordinary vertices persist; this is a failed pole-placement goal, not a claimed fix.

C flow: the upper strip shares the old lamp outer boundary and shoulder bridge endpoint. The inner ring separates radius and depth. Extraordinary vertices reduce from eight to six, but four remain adjacent to sensitive quarter patches. No broad quarter flattening is used.

Every added element controls an edge radius, separates curvature regimes, constrains aperture drift or provides a physical return. No global density increase, sculpt, production detail or global bevel is introduced.

## Geometry

| Zone | V02 base → V03 base | V03 evaluated vertices | V03 evaluated triangles |
|---|---:|---:|---:|
| A | 132 → 160 | 2197 | 4160 |
| B | 124 → 183 | 2607 | 4992 |
| C | 214 → 250 | 3448 | 6528 |
| Total | 470 → 593 | 8,252 | 15,680 |

Base vertices increase 26.2%; no global doubling. All base faces remain quads. Evaluation remains Catmull-Clark level 2.

## Technical validation

Cracks: **0**. Degenerate faces: **0** base/evaluated. Unintended interior non-manifold edges: **0**. Non-adjacent triangle overlaps: **0** base/evaluated per independent zone. Intentional construction/aperture boundaries remain open. These checks do not certify a watertight assembled body or cross-zone joining.

Symmetry: **PASS**, actual base discrepancy **0.0** in all zones. Reproducibility: **PASS**, delete/regenerate through the add-on; repeated generation also checks crease and subdivision settings. Fixed dimensions, wheel transforms and V04 constraint curves are protected. V02 regeneration regression: **PASS**. Zone visibility, controls and cage-only toggles: **PASS**.

## Pole audit

| Zone | Extraordinary V02 → V03 | Adjacent to sensitive patches V02 → V03 |
|---|---:|---:|
| A | 4 → 4 | 0 → 0 |
| B | 8 → 8 | 8 → 8 |
| C | 8 → 6 | 4 → 4 |

The audit lists vertex ID, coordinates, edge valence, boundary state and all incident patch labels. Interior valence other than four and non-corner boundary valence other than three are flagged. Ordinary open-cut corners are distinguished. Sensitive classification is based on patch adjacency; it is not a substitute for the rendered reflection review.

## Diagnostics

- Reference | V02 | V03: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/reference-comparison.jpg`
- Full A cross-view comparison: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/comparison-zone-a.jpg`
- Full B cross-view comparison: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/comparison-zone-b.jpg`
- Full C cross-view comparison: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/comparison-zone-c.jpg`
- Clay: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/clay-diagnostics.jpg`
- Reflection/zebra, matched V02/V03: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/reflection-zebra-diagnostics.jpg`
- Base vs evaluated control nets: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/control-net-evaluation.jpg`
- Actual control sections: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/control-net-sections.jpg`
- Bonnet sections: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/bonnet-edge-roll-sections.png`
- Root sections: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/root-sections.png`
- D-pillar sections: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/d-pillar-sections.png`
- A defect close-ups: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/closeups-zone-a.jpg`
- B defect close-ups: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/closeups-zone-b.jpg`
- C defect close-ups including lower corner: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/closeups-zone-c.jpg`

Lower-corner reflection comparison: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03/lower-corner-reflection.jpg`.

Individual clay/base/reflection/zebra images are in `zone-a/`, `zone-b/`, `zone-c/`. The V02 lower-corner comparison is saved inside V03 diagnostics, never over V02 files. Studio lighting, camera transforms, framing, shaders and sample count match V02; the lower view uses the same explicit camera offset for both versions. Primary reference crops match V02. Photos remain uncalibrated.

Evidence: `geometry-validation.json`, `addon-tests.json`, `boundary-deviations.json`, `topology-changes.json`, `pole-audit.json`, `root-and-pillar-sections.json`, `constraint-departures.json`, `preservation.json`, `preservation-baseline.json`, `FINAL_GATE.json`.

## Final decision / next step

C — TARGETED TOPOLOGY DID NOT SOLVE THE SURFACE PROBLEMS; STOP THIS APPROACH

Stop local iteration and preserve all work. The aperture improvements are real, but major cowl/root, fender, D-junction and lamp-surround shape/reflection failures remain. Expanding these patterns into the complete exterior would propagate those defects. No V04 prototype is generated.

Full body: **NOT GENERATED**. Deep detailing: **NOT STARTED**. Website: **UNCHANGED**. GLB: **NOT EXPORTED**. Hero/navigation/TOLI AI: **UNCHANGED**. Controlled capture: **PRESERVED**. Protected projects: **UNCHANGED**. 1501 preserved file hashes match. Cost: **₹0 / $0**. Deployment/Git commit: **NOT PERFORMED**.

Website build/lint were not rerun because source/public files are unchanged. Remaining risk: the model still fails visual/reference fidelity, with depth inferred from uncontrolled photographs.
