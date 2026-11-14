# Existing-photo MU-X production candidate V01

**Milestone: PRIMARY EXTERIOR BODY**

**Decision C — STILL GENERIC / INCORRECT. STOP.**

Overall badgeless recognition: **FAIL**. The independent authored-section candidate does not convincingly read as the supplied MU-X and does not demonstrate substantial overall reference-fidelity improvement. The production filename denotes a candidate branch, not approval. Do not advance to Milestone 2 or automatically start another reconstruction branch.

## Authorization and source limits

The user explicitly overrode the controlled-photo waiting condition for this branch, authorizing a visual reconstruction from the existing 18 images. No claim is made that these photographs are controlled, calibrated, metrological or capable of exact depth recovery. The branch did not rerun calibration, photogrammetry, Curve Cage V05 or Surface Prototype V04.

The pre-geometry region map covers all 24 requested regions: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/EXISTING_PHOTO_REGION_MAP.md. The previous freeze remains preserved at /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/existing-photo-production-v01/pre-authorization-status.md. Older candidates are research comparators only.

## Construction and milestone scope

The candidate was built in a new empty Blender scene. No old body mesh, patch net or internal curve-cage depth was imported. Half-body section coordinates, an independent compound bonnet and the continuous greenhouse/root structure were authored in the new branch. Code supplies mesh assembly, symmetry, fixed wheel repetition, nominal framework, cameras, clay materials and diagnostics. This is coordinate-authored construction through code, not an assertion of mouse-authored Blender work or recovered physical sections.

Named primary meshes: main body/front fenders/rear quarters; compound bonnet; greenhouse/roof/A- and D-structure; front/rear/quarter glazing envelopes. Tyres and plain wheel volumes are fixed placeholders, not identity-detail wheels. The bonnet perimeter and glazing are seated on the new candidate’s own host surfaces; those local projections are construction interfaces, not evidence-derived depth. The greenhouse has lower overlap with the body to avoid an unintended floating seam.

No lamp/grille internals, identity details, panel gaps, handles, mirrors, rails, steps, badges, functional panels, interior, engine or production materials were added. Existing images of those details inform the region map only.

## View assessments

| View | Assessment | Improvement / retained strength | Remaining difference |
|---|---|---|---|
| Front | FAIL | Fixed overall framework and a continuous broad front volume | Nose is too generic; bonnet/fender relationship and broad fascia contour do not establish the MU-X |
| Front three-quarter | FAIL | Continuous cowl/root volume replaces the isolated prototype tabs; bonnet no longer floats at its perimeter | Fender crown/arch mass, diffuse bonnet roll and A-root transition remain unconvincing; no substantial identity gain |
| Side | NEEDS WORK | Axle spacing, tyre diameter, overhang framework and continuous cabin silhouette are consistent | Window/quarter-glass shape, pillar proportions, shoulder and lower-body mass still read as a generic SUV |
| Rear three-quarter | FAIL | Continuous quarter volume and rear glazing are present | D-pillar/rear-quarter depth, hatch/glass relationship and bumper corner lack reference-specific form |
| Rear | FAIL | Symmetric broad rear volume and glass envelope | Roof/glass/body taper and broad rear fascia do not reproduce the supplied vehicle |

## Primary surfaces

- **Bonnet/fenders — NEEDS WORK:** independent compound panel and fixed arch positions are present, but broad fender mass and the bonnet edge transition remain too smooth/generic. A smoother blob is not a reference-quality automotive surface.
- **Cowl/A-pillar — NEEDS WORK:** continuous primary volume avoids the old isolated tab construction, but the visible root/pillar junction remains over-simplified.
- **Greenhouse — FAIL:** the three glazing envelopes and roof/rake are not sufficiently MU-X-specific. Host-seated glazing fixes construction placement, not photographic fidelity.
- **D-pillar — FAIL:** broad quarter-glass/roof/rear-glass relationships still lack convincing control of the original vehicle’s section.
- **Rear quarter — NEEDS WORK:** substantial continuous mass is preserved, but the volume remains too slab-like and the rear corner is generic.

## Surface-quality gate

Clay: **FAIL** for reference fidelity. Reflection flow: **NEEDS WORK**; long calm regions coexist with compression at window edges, fender/arch turns and corner transitions. Rounded-edge quality: **NEEDS WORK**; soft evaluation does not reproduce the intended variable physical rolls. Character-line quality: **FAIL**; the shoulder and regional cuts are too diffuse/absent at the primary-surface stage. Details would conceal rather than solve these problems, so they are blocked.

## Confidence

- **HIGH evidence confidence:** nominal framework as a fixed project constraint, axle/ground relationships, compatible side silhouette and major front/rear feature layout in image space. This is not high confidence in the candidate’s exterior accuracy.
- **MEDIUM:** greenhouse outline/rake, roof trajectory, bonnet envelope, wheel-arch placement, shoulder/lower-body silhouette and broad rear layout.
- **LOW:** bonnet/fender compound depth, cowl/A-root volume, D-pillar section, roof-to-quarter depth, lamp/quarter relationship and rear bumper corner. These remain inferred and visually unresolved.

## Geometry validation

| Metric | Base control geometry | Evaluated geometry |
|---|---:|---:|
| Vertices | 2615 | 20982 |
| Triangles | 5018 | 41904 |
| N-gons | 0 | 0 |
| Degenerate faces | 0 | 0 |
| Non-manifold edges | 180 | 0 |
| Boundary edges | 180 | 0 |

Base counts include the authored half-surfaces and wheel controls, before Mirror/Subdivision/Solidify. The 180 base non-manifold edges are intentional open half-surface/skin boundaries. Evaluated components have zero non-manifold/boundary edges. These per-component checks do not certify a joined watertight or intersection-free production shell. Plain wheel end caps use triangles; there are no n-gons.

## Dimensions, symmetry and wheel transforms

| Quantity | Nominal framework | Evaluated result |
|---|---:|---:|
| Length | 4.825 | 4.82500124 |
| Width | 1.860 | 1.85900182 |
| Height | 1.860 | 1.85650027 |
| Wheelbase | 2.845 | 2.84500000 |

Dimensions are nominal metre-coordinate model bounds, not physical accuracy claims. Subdivision changes the outer width/height slightly. Parameters are read from the centralized existing `parameters.py:BASE`; no camera fit changes the wheelbase.

Evaluated bilateral symmetry discrepancy: **0.0000211707 model units**. The explicit check tolerance is 0.0001; local surface seating produces a small numerical discrepancy, so it is not reported as zero. Ground minimum Z=0 and fixed wheel anchors PASS.

Wheel centres:

| Wheel | X | Y | Z |
|---|---:|---:|---:|
| ANCHOR_FRONT_NEGATIVE_Y_TIRE | -1.4225 | -0.7850 | 0.3820 |
| ANCHOR_FRONT_POSITIVE_Y_TIRE | -1.4225 | 0.7850 | 0.3820 |
| ANCHOR_REAR_NEGATIVE_Y_TIRE | 1.4225 | -0.7850 | 0.3820 |
| ANCHOR_REAR_POSITIVE_Y_TIRE | 1.4225 | 0.7850 | 0.3820 |

Wheel object location/rotation/scale are identity because positions are baked into mesh coordinates; the separately recorded centres are the physical placement in this scene. Full transforms, per-object counts and checks are in `geometry-validation.json`. No opening-panel or wheel-animation rig is claimed.

## Previous-candidate comparison

The preserved whole-body `source/production/isuzu-mux-generated-v04.blend` is the meaningful previous research comparator: its front identity was stronger than earlier generated versions, while its side/rear remained failed. It is never labeled approved. Old isolated Surface V01–V03 regions are not presented as a complete-body baseline.

Previous and new candidates are rendered with the same orthographic directions, 6.1 framing scale, studio lights and clay setup. Existing previous-object visibility is retained; badges are excluded. Body/glazing/tyre diagnostic tones are normalized. The previous model has historical identity details while the new candidate intentionally stops at primary surfaces; this stage difference is disclosed on comparison boards. No claim is made that the new candidate wins simply by omitting those details.

Photographs remain uncalibrated perspective views. Boards use documented image crops for readability, not fitted photographic camera solutions or metric overlays.

## Exact outputs

- Blender master: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-existing-photo-production-v01.blend
- Primary-surface milestone: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/milestones/isuzu-mux-existing-photo-primary-surfaces-v01.blend
- Region map: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/EXISTING_PHOTO_REGION_MAP.md
- Source/replay/check/render scripts: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/existing-photo-production-v01
- Five reference comparisons: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/existing-photo-production-v01/comparison-front.jpg, comparison-front34.jpg, comparison-side.jpg, comparison-rear34.jpg, comparison-rear.jpg
- Combined comparison: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/existing-photo-production-v01/reference-previous-new-comparison.jpg
- Five-view clay: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/existing-photo-production-v01/clay-five-view.jpg
- Five-view reflection / zebra: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/existing-photo-production-v01/reflection-five-view.jpg ; /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/existing-photo-production-v01/zebra-five-view.jpg
- Wire / control cage: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/existing-photo-production-v01/wire-five-view.jpg
- Bonnet/fender, cowl/A-root, D-pillar, quarter and corner close-ups: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/existing-photo-production-v01/primary-surface-closeups.jpg
- Measurements / decision / preservation: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/existing-photo-production-v01/geometry-validation.json, FINAL_GATE.json, preservation.json

## Commands actually used

Recorded commands, not authorization to restart after this C gate:

```sh
blender --version
blender -b -t 2 --python /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/existing-photo-production-v01/build.py
blender -b -t 2 --python /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/existing-photo-production-v01/check.py
M1_JOB=clay-front34 blender -b -t 8 --python /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/existing-photo-production-v01/render.py
M1_PREVIOUS=1 M1_JOB=clay-front34 blender -b -t 8 --python /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/existing-photo-production-v01/render.py
python /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/existing-photo-production-v01/boards.py
```

The renderer was invoked separately for clay/reflection/zebra/wire in all five views and clay/reflection for each named close-up. No export, calibration, SfM, cloud or paid tool was run. Blender 5.2.2 LTS at `/usr/bin/blender` was used locally.

## Stop and protection

Deep detailing, functional panels, interior and engine: **NOT STARTED**. GLB: **NOT EXPORTED**. Website, Hero, navigation and TOLI AI: **UNCHANGED**. Controlled capture: **PRESERVED**. Protected projects and all old candidates/reference images: **UNCHANGED**. Preservation check: 7397 pre-existing files matched, excluding the explicitly authorized status-document update.

Cost: **₹0 / $0**. Deployment/Git commit: **NOT PERFORMED**.

**NEXT STEP: STOP. Do not start another automatic reconstruction branch or advance to identity/detail work.**
