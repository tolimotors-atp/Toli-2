# Reference-traced curve cage — v01

**B — CURVE CAGE IS A CLEAR IMPROVEMENT BUT SPECIFIC REGIONS STILL REQUIRE TUNING.** This is improvement in auditable tracing and boundary layout, not an approved surfaced vehicle or a claim that it beats V04 as a complete model. Front/rear depth registration and shared joins remain unapproved. **No new body was lofted; no deep detailing or web export.**

## Fal selection and cost

The user selected Fal. Its tools were discovered and the media guidance read. A read-only recommendation was attempted with a $0 request ceiling and explicit no-cloud/no-upload constraints; it returned `Unknown tool ({name: fal.recommend_model})`. No generation job was submitted, no images were uploaded and no paid endpoint was used. Work continued locally under the brief's no-cloud-reconstruction rule. There is no Fal request ID or generated media URL to report. Cost: **₹0 / $0**.

## 1. Preview topology fixed first

The preserved soft-detail source remains unchanged. The **generator logic** that produced its six threshold-degenerate Preview faces was investigated, rather than editing the saved mesh or increasing tolerance.

`degenerate-source-before.json` records the exact object, coordinates and areas. All six were on `MUX_CURVE_SURFACE_PATCHES`: paired microscopic slivers near front X≈−2.3265 m / Z≈1.0454 m and rear X≈2.3113 m / Z≈1.0893 m, with areas roughly 3.7e−11 to 9.4e−11 m². The existing threshold stays **1e−10 m²**.

The global angle-limited bevel was operating on dense fascia-cap intersections. A trial vertex-group restriction was rejected because it affected incident edges too broadly. The final fix assigns Blender `bevel_weight_edge` only to **sharp actual arch-boundary edges**, selected using the sampled Bezier arch and face angle. No manual face deletion or tolerance relaxation. The operation is not disabled: **86 weighted arch edges in Preview, 294 in Quality**.

`topology-fix.json` proves the regenerated **previous body algorithm** now has:

| Regression result | Preview | Quality |
|---|---:|---:|
| Degenerate faces | **0** | **0** |
| Non-manifold edges | **0** | **0** |
| Negative-volume objects | 0 | 0 |
| Symmetry discrepancy | 5.96e−8 m | 5.96e−8 m |
| Vertices | 5,166 | 12,638 |
| Triangles | 10,296 | 25,240 |

Both topology gates **PASS**. Symmetry remains approximately **0.0000596 mm**, at the unchanged .0001 m threshold. Dimensions stay approximately 4.825 × 1.860 × 1.860 m, wheelbase 2.845 m. These are regression measurements of the repaired previous generator, **not a newly surfaced curve-cage vehicle**. The historical soft-detail blend intentionally still contains the old result because it was required to remain preserved.

## 2. New source and architecture

New scene: `tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v01.blend`.

New code under `tools/blender-addons/toli_mux_generator/`:

- `traced_data.py`: hand-picked native screenshot pixel coordinates, source filenames, anchors and explicit inferred depth bands.
- `geometry/reference_cage.py`: conversion into 3D curves, mirrored construction, explicit FREE handles and diagnostic colors.
- `cage_ui.py`: Generate Reference-Traced Cage, Curve Cage Only, wheel/ground support and reversible body hiding.
- `run_cage.py`, `check_cage.py`, `boards_cage.py`, `render_cage_gates.py`: scene generation, tests, annotations/comparisons and source-filtered gate renders.
- `test_topology_cage.py`: strict previous-generator regression.

Changed `geometry/rounded.py`, `parameters.py`, `__init__.py`, `panels.py` and default runner routing. The pre-pass add-on is archived at `tools/3d/isuzu-mux/code-generator/soft-v01-addon/`. Earlier masters, coded versions and audits were not overwritten.

The scene contains wheels, ground, centerline, axles, linked image references and the cage. **No new body panels or finished body surface.** Image references remain unpacked originals. Curve Cage Only hides legacy body collections and restores recorded visibility when disabled; support objects and references are shown. Colors distinguish silhouette, character, greenhouse, front, rear and transverse links. Diagnostic tubes are not exported geometry.

## 3. Tracing and reference provenance

Primary side: `Screenshot From 2026-11-06 18-17-14.png`, corroborated by 18-17-21, front-three-quarter 18-17-27 / 25, and rear-three-quarter 18-17-35 / 31. Primary front: 18-17-10. Primary rear: 18-17-18. All paths resolve within the authoritative `Isuzu MU-X` folder. The existing 18-image audit still controls compatible-body selection; open-panel/interior/engine views are contextual, not used as closed-body outlines.

The new data retains **pixel coordinates**, rather than representing every boundary only as an untraceable normalized approximation. Native-image annotation overlays revealed errors in the first readings. Windscreen lower points were moved from approximately V271–280 to V242–249, and the rear glass, tail lamps, tailgate and bumper readings were corrected against the originals. Before/after annotations are saved. These are manually selected landmarks with approximate 5–10 pixel uncertainty, **not exact automatic segmentation**. Some side/fender readings still need adjustment.

Side X registration uses piecewise anchors at front tip, front axle, rear axle and rear tip to preserve length/wheelbase. Side Z is scaled between ground and roof. Front/rear use roof/cowl-or-glass/ground height anchors, and width/centerline anchors. These are **inferred registration maps**, not recovered camera intrinsics/extrinsics. The photographs have perspective; direct pixel ratios cannot all be imposed as metric dimensions. Depth bands are explicitly labeled inferred, guided by the three-quarter views; they still need tuning.

The cage has **78 traced/link curves, 360 traced/link control points**, plus three centerline/axle guides. It includes side silhouette and sill, bonnet center/edges, shoulder/belt, windscreen, roof center/edge, front/rear side-window and quarter-glass loops, B/C/D pillar lines, front/rear arch/crown/returns, headlight/grille/bumper envelopes and rear-glass/lamp/tailgate/bumper boundaries. All are mirrored from one side; no independent asymmetric fitting. Not every requested interior/transverse cage constraint is complete: the bonnet lattice, windscreen transverse sections and rear quarter section network remain incomplete.

FREE handles are chord-derived and explicit, including cyclic neighbors for closed loops. They are reproducible, but **not all artist-tuned or tangent-matched at shared joins**. Endpoint coincidence and G1 continuity are not solved merely by having traced the curves.

## 4. Curve gates

The reference-labeled side windows, quarter glass and frontal/rear boundaries are a clear improvement in *traceability and contour intent* over the broad prior approximations. This does not constitute a full gate PASS.

| Gate | Status / remaining issue |
|---|---|
| Front | NEEDS WORK — native boundaries improved, depth/height registration and connected front composition unresolved |
| Front three-quarter | NEEDS WORK — fender/bonnet/headlamp return depth and join placement |
| Side | NEEDS WORK — good source-linked window layout, but overhang registration, arch/sill and body shoulder still approximate |
| Greenhouse | NEEDS WORK — new traced window/pillar boundaries; shared cowl/roof/glass junctions not established |
| Rear three-quarter | NEEDS WORK — independent quarter/glass/lamp depth bands do not yet make compatible patch boundaries |
| Rear | NEEDS WORK — corrected native glass/lamp/bumper readings still require coherent 3D seating |

Bonnet, front fenders, front identity, windscreen/A-pillar, roof, side windows, quarter glass, D-pillar, shoulder, rear quarter and rear identity all remain **NEEDS WORK** as 3D surface constraints. The native overlays make specific errors visible rather than hiding them in a generated body. **Do not surface this failed/incomplete cage.**

## 5. Four-state comparisons

`four-state-comparison.jpg` shows REFERENCE | V04 | SOFT-DETAIL V01 | NEW CAGE, for all five views. New cage images are explicitly labeled **NO BODY**. Front/rear gate layers omit opposing identity curves to avoid wire-through clutter; three-quarter views show the full cage. Native pixel overlays are actual annotations in source coordinates, **not 3D projections or camera calibration**.

For **line/boundary evidence only** (not surface quality):

| View | New vs V04 | New vs soft-detail V01 |
|---|---|---|
| Front | WORSE — V04 retains a more integrated front composition | BETTER — named source-traced lamp/grille boundaries replace blank body mass |
| Front three-quarter | WORSE — depth and returns remain unresolved | BETTER in boundary/layout evidence, not validated volume |
| Side | BETTER in explicit source-linked window/quarter boundaries; surface shape not evaluable | BETTER in silhouette/window evidence |
| Rear three-quarter | WORSE — new depth seating still unresolved | BETTER in explicit quarter/glass/lamp evidence, not validated volume |
| Rear | WORSE — V04 has an assembled rear, though inaccurate | BETTER in traced boundary evidence |

These mixed-stage comparisons **do not establish that a new complete model beats V04**. Badgeless recognition: NEEDS WORK. The cage is unbranded, but a recognition PASS is not justified yet.

## 6. Reproducibility and geometry scope

Cage control-point symmetry: **0 m reported discrepancy, PASS**. This measures the mirrored control network; the previous-generator surface regression independently retains its ≈0.00006 mm result. No new surfaced-body symmetry result is invented.

Registered cage generation, repeated deletion/recreation including handles, Curve Cage Only toggling, four wheels/ground and linked references: **PASS** (`addon-tests.json`). Curves: PASS. New surfaces: **NOT REACHED**. Overall curves-plus-surfaces: **NOT REACHED**, despite the desired final PASS requirement. It would be misleading to claim a surface test when the curve gate has not passed.

New cage body Preview/Quality vertices/triangles and non-manifold/degenerate surface statistics: **N/A**. Only support wheels/ground and rendered curve tubes exist. The regression body numbers above must not be presented as new cage surfaces.

Clay gate / reflection gate: **NOT REACHED**, not PASS; new surfaces were deliberately blocked. No new clay/reflection body renders were fabricated. Existing soft-detail/V04 clay views appear only in the labeled comparison columns. Deep detailing **NOT STARTED**.

## Diagnostics and use

Directory: `tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v01/`.

Contains: `topology-fix.json`, `degenerate-source-before.json`, `cage-validation.json`, `addon-tests.json`, five curve gate renders, `native-traces-front.jpg`, `native-traces-side.jpg`, `native-traces-rear.jpg`, corresponding `*-before.jpg`, `four-state-comparison.jpg`, logs and gate notes.

Run locally from project root:

```sh
blender -b --threads 2 --python-exit-code 1 --python tools/blender-addons/toli_mux_generator/test_topology_cage.py
blender -b --threads 2 --python-exit-code 1 --python tools/blender-addons/toli_mux_generator/run_cage.py
blender -b --threads 2 --python-exit-code 1 --python tools/blender-addons/toli_mux_generator/render_cage_gates.py
python tools/blender-addons/toli_mux_generator/boards_cage.py
```

The runner resets a separate background scene; never run it inside an unsaved interactive scene. Use a new versioned output for later tuning rather than overwriting preserved milestones. The current run was tuned within its newly created v01 candidate; older milestones were preserved.

## Final decision / protection

**B — CURVE CAGE IS A CLEAR IMPROVEMENT BUT SPECIFIC REGIONS STILL REQUIRE TUNING.** Improved image evidence and fixed Preview topology are real progress; no completed surface/model quality is claimed. Continue only with coherent depth/shared boundary tuning before surfacing. The brief's curve gate prevents advancing to clay/deep details now.

GLB NOT EXPORTED. Website NOT UPDATED. Hero/navigation/TOLI AI/theme unchanged; controlled capture preserved; protected projects unchanged. The old soft-detail master and V04/113 components remain unchanged. No paid assets, uploads, cloud reconstruction, deployment or Git commit. Website suites were not rerun because no website source or production asset changed.
