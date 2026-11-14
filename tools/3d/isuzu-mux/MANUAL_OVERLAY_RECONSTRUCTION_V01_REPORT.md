# MU-X Manual Overlay Reconstruction V01

**Decision C — STILL GENERIC / INCORRECT. STOP.**

**Badgeless MU-X recognition: FAIL. No approval for detail, GLB export or website integration.**

## Method and scope

New hand-authored explicit low-density half-body control vertices and quad connectivity, serialized into Blender using Python. This is code-assisted manual control-net authoring, not an interactive artist-retopology session and not a recovered 3D surface. The vertex data is saved independently in source/authored-control-net.json. No old body is imported, fitted or used as geometric truth. No photogrammetry, PyCOLMAP, curve-cage V05, surface-prototype V04, existing-photo V02, automatic remesh, parameter-only exterior or mathematical depth recovery. Only the nominal framework and existing neutral diagnostic studio helper are reused.

354 authored surface control vertices in five patches, exact Y symmetry, level-2 subdivision. Main side/fender/quarter cage, compound bonnet, continuous cowl/A/roof/D shell and broad front/rear volumes only. Glass is a diagnostic face-material assignment on the shared shell, not detailed production glazing. Region-specific curvature is in the authored controls; a finite 0.6 boundary crease retains open patch envelopes, but does NOT establish joined/G1 surfaces. No global body bevel.

## References

43 files / 39 distinct visual references reviewed on the full audit contact board, with the selected canonical and intermediate views inspected at larger size. 13 active primary references; 26 distinct secondary references. Four redundant crop/scale copies excluded. More precisely: 31 distinct G2 images minus 13 selected G2 = 18 secondary G2; eight secondary G1 = 26. The four G0 files are excluded, not additional distinct references.

Silver open-panel body family remains canonical for identity; compatible closed silver views control closed contours. Red viewer-series intermediates inform appearance only. Paint color ignored. Exact year/trim, real camera and same-physical-vehicle provenance remain unknown. Open panels cannot define the closed envelope. Roof-only 043 unverified and LOW confidence. No incompatible facelift details were merged or averaged.

| ID | Filename | View / approximate azimuth | Visibility confidence | Why / supported regions |
|---|---|---|---|---|
| MUX-011 | Screenshot From 2026-11-06 18-17-10.png | Front / 0° | HIGH | Canonical closed body; symmetric face envelope; Bonnet, windscreen, fender width |
| MUX-016 | Screenshot From 2026-11-06 18-17-27.png | Front-left 3Q / 45° | HIGH | Canonical compatible silver three-quarter; Bonnet, fender, cowl, greenhouse |
| MUX-030 | Screenshot 2026-11-08 213441.png | Left-front intermediate / 65° | MEDIUM | Closer transition angle; cropped screenshot; Bonnet side falloff, A root, arch |
| MUX-012 | Screenshot From 2026-11-06 18-17-14.png | Left side / 90° | HIGH | Canonical closed side with full vehicle; Wheel relation, roof, side opening |
| MUX-022 | Screenshot (3).png | Left-rear intermediate / 115° | MEDIUM | Intermediate rear wrap visible; Quarter mass, D pillar, rear wrap |
| MUX-017 | Screenshot From 2026-11-06 18-17-31.png | Rear-left 3Q / 135° | HIGH | Canonical rear quarter, compatible silver; D pillar, rear glass, quarter |
| MUX-013 | Screenshot From 2026-11-06 18-17-18.png | Rear / 180° | HIGH | Canonical closed rear full envelope; Rear glass, D pillars, taper, bumper |
| MUX-035 | Screenshot 2026-11-08 213507.png | Rear-right 3Q / 225° | MEDIUM | New opposite-side corner support; Quarter, D pillar, bumper corner |
| MUX-014 | Screenshot From 2026-11-06 18-17-21.png | Right side / 270° | HIGH | Canonical opposite side full contour; Roof, arches, opposite side |
| MUX-015 | Screenshot From 2026-11-06 18-17-25.png | Front-right 3Q / 315° | HIGH | Canonical opposite front three-quarter; Bonnet, windscreen, fender wrap |
| MUX-043 | images.jpg | Overhead / None° | LOW | Only roof reference; family unconfirmed; Roof/bonnet plan only |
| MUX-020 | Screenshot (1).png | Front-left 3Q support / 45° | MEDIUM | Larger image shows compound surfaces; Bonnet crown, arch, cowl |
| MUX-027 | Screenshot 2026-11-08 213402.png | Front support / 0° | MEDIUM | Red series near frontal envelope; Bonnet plan, A pillars, face width |

All other file roles are individually recorded in references/secondary-and-excluded.json. 001/003/004/006–010 are detail/composite/open-panel evidence, not active closed-body planes. 032/033/041/042 are redundant. The remaining compatible exterior alternatives are secondary cross-checks. Conflicts are retained, not silently averaged: red viewer tyre/fascia appearance versus canonical silver, changing crop/resolution, unknown focal length, unknown source vehicle and isolated roof reference. No trim detail is modeled in this pass.

## Reference-fit cameras

13 cameras (12 perspective, 1 roof-plan orthographic), never calibrated. 2 side fits HIGH; 11 remaining fits LOW. Uniform image normalization to 800×520, aspect ratio preserved, no vehicle warping or non-uniform scaling. Original images unchanged; copies and derivatives saved. Perspective anchor RMS ranges roughly 4–24 px. Roof points are estimated envelopes and some anchors uncertain/occluded; no physical focal or pose claim. Detailed camera positions/rotations/lens and per-view limitations: reports/REFERENCE_CAMERA_FITS.md and cameras/reference-fits.json.

The Blender reference workflow is embedded as overlay_tools.py. Run that text once, open Camera View > N > MU-X Overlay, choose a scene camera, then Reference only / Model only / 50% / Silhouette / Wire. No automatic script execution is required. Background operator checks pass; an interactive Blender viewport was not user-tested. Reference images are packed into the .blend.

## Primary exterior visual gate

| Region/view | Assessment | Observed reference mismatch |
|---|---|---|
| Overall proportions | NEEDS WORK | Nominal wheel framework preserved; cabin/body mass and roof/shoulder placement still generic. |
| Front | FAIL | Plain front wrap is bulbous/featureless; bonnet nose and corner volume do not match the angular MU-X envelope. |
| Front 3/4 | FAIL | Bonnet/fender seam and flattened character; wide featureless flank; windscreen/A-root relationship wrong. |
| Side | FAIL | Wheelbase anchored, but window opening and quarter glass rectangular; D pillar too broad; fender/shoulder mass too weak. |
| Rear 3/4 | FAIL | Wrong D-pillar/glass depth, quarter too plain, tailgate/bumper patch corner seam visible. |
| Rear | FAIL | Blank wrap lacks the broad inset/shoulder and correct rear-glass/bumper mass relationship. |
| Overhead | NEEDS WORK | Plan diagnostic exists; low-confidence independent roof view cannot approve taper/crown. |
| Bonnet | FAIL | Compound crown is present, but falls off incorrectly and has a discontinuous fender transition. |
| Front fenders | FAIL | Anchored arches remain approximately located; crown/support and corner wrap are insufficient. |
| Cowl / A-pillar | NEEDS WORK | One continuous shell avoids old isolated root tabs; it does not deliver the correct muscular cowl/A/fender flow. |
| Greenhouse | FAIL | Not recognizable canonical window/quarter-glass design; material-only glazing is a coarse diagnostic representation. |
| D-pillar | FAIL | Overwide and incorrectly tapered, with generic side-window termination. |
| Rear quarter | FAIL | Weak shoulder, incorrect compound section and rear connection. |
| Rear bumper corner | FAIL | Independent broad patch has visible wrap/continuity break. |
| Surface quality | FAIL | No zero-area faces, but visible gaps/highlight breaks and broad flat flank; numerical mesh checks do not approve surfaces. |

## Diagnostic observations

Clay: FAIL. Generic massing, wrong window/D outlines, discontinuous broad wrap. Reflection: FAIL. Hood/fender highlight breaks, little controlled shoulder/fender definition; rear patch return discontinuity. Zebra: FAIL. Abrupt reflection bands at joins, inflated/flat transition regions; synthetic reflection-normal stripes are diagnostics, not measured automotive surface continuity. Rounded edges: soft, but softness does not match reference sections. Character lines: insufficient; none added to camouflage failed massing.

Silhouette overlays use orange actual rendered alpha edges versus cyan coarse hand-read reference traces. Internal-boundary overlays use cyan approximate windscreen/window/quarter/bonnet guides and the actual model cage. These are diagnostic guides, not precise masks or calibrated correspondences. No pixel IoU or accuracy claim. Camera error, omitted mirrors/rails/steps and traced-outline uncertainty remain distinct from body defects.

## Comparison against Existing-photo V01

| View | Result |
|---|---|
| Front | SIMILAR failure: generic blank fascia; no recognizable primary front form |
| Front 3/4 | WORSE: conspicuous bonnet/fender seam and featureless flank |
| Side | WORSE greenhouse: rectangular material windows and broad D pillar; anchored wheels do not rescue shape |
| Rear 3/4 | SIMILAR / WORSE: wrong D/quarter and visible return seam |
| Rear | SIMILAR failure: broad blank wrap, incorrect inset relationships |
| Overall | WORSE; no meaningful fidelity improvement demonstrated |

The same new reference-fit cameras are used for both candidates in reference-previous-new-comparison.jpg, so no flattering framing change is used to claim improvement. Earlier model remains failed research.

## Geometry and dimensions

| Measure | Base | Evaluated |
|---|---:|---:|
| vertices | 2146 | 11022 |
| triangles | 4114 | 21040 |
| quads | 1937 | 10400 |
| n_gons | 8 | 8 |
| degenerate_faces | 0 | 0 |
| nonmanifold_edges | 152 | 976 |
| boundary_edges | 152 | 976 |
| interior_nonmanifold_edges | 0 | 0 |

Counts include primary surfaces and eight wheel/rim proxy meshes, exclude studio/reference objects. Base surfaces alone: 354 vertices. The eight n-gons are flat cylinder caps on the four plain rim proxies; the primary body cage itself has only quads. Open patch boundaries are intentional research state, not acceptable finished body sealing. No claim of joined watertightness or zero inter-patch intersections.

| Dimension | Nominal m | Evaluated m |
|---|---:|---:|
| length | 4.825000 | 4.823334 |
| width | 1.860000 | 1.865365 |
| height | 1.860000 | 1.858333 |
| wheelbase | 2.845000 | 2.845000 |
| tyre diameter | 0.764000 | 0.764000 |

Evaluated bounds: {'min': [-2.4116668701171875, -0.9326823353767395, 0.0], 'max': [2.4116668701171875, 0.9326823353767395, 1.8583333492279053]}. Ground contact all four tyre meshes checked within 1e-6 m. Symmetry maximum nearest reflected evaluated-vertex discrepancy: 7.15255737305e-07 m. Global dimension differences from subdivision/open-panel construction are reported above, not silently normalized. Nominal 1.860 m height includes a full vehicle framework; rails are omitted here. No production dimensional conformity claimed.

## Saved artifacts

- Blender executable: /usr/bin/blender; Blender 5.2.2 LTS.
- Master: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-manual-overlay-v01.blend
- Initial immutable milestone: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/milestones/isuzu-mux-manual-overlay-primary-body-v01.blend
- Final immutable failed-gate milestone: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/milestones/isuzu-mux-manual-overlay-v01-gated.blend
- Control net: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/source/authored-control-net.json
- Reference board: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/diagnostics/selected-reference-board.jpg
- Cameras: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/reports/REFERENCE_CAMERA_FITS.md
- Inference map: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/reports/DEPTH_INFERENCE_MAP.md
- Geometry: /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/diagnostics/geometry-validation.json

Diagnostic renders under /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/renders/v01:

- /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/renders/v01/reference-overlay-six-view.jpg
- /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/renders/v01/clay-six-view.jpg
- /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/renders/v01/reflection-six-view.jpg
- /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/renders/v01/wire-six-view.jpg
- /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/renders/v01/zebra-six-view.jpg
- /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/renders/v01/silhouette-five-view.jpg
- /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/renders/v01/internal-boundary-five-view.jpg
- /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/renders/v01/reference-previous-new-comparison.jpg
- /home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/manual-overlay-reconstruction/renders/v01/primary-surface-closeups.jpg

Individual descriptive PNGs: front, front34, side, rear34, rear, overhead for clay/reflection/wire/zebra; all 13 reference-fit model/50% overlays; five silhouette and five internal-wire overlays; seven region closeups. All actual source/render/log files stay in this branch. Overhead camera orientation was corrected after the first diagnostic batch; final images use the corrected horizontal plan. No geometry was changed during that correction.

## Stop decision and exact remaining work

Decision C. The new approach has not delivered sufficient MU-X fidelity. STOP, preserve candidate and diagnostics. Do not start another branch or details automatically. Primary fixes that a future separately authorized pass would need: genuinely traced continuous window/quarter-glass topology; correct A/cowl/fender section; cohesive bonnet/fender and broad fascia envelopes; muscular shoulder/arch volumes; correct D/quarter depth; joined rear tailgate/bumper wrap. Existing references remain visual guidance, not a resolved cross-section.

Exterior identity/deep detail/functional panels/interior/engine: NOT STARTED. GLB: NOT EXPORTED. Website, Hero, navigation, TOLI AI, current public model and controlled-capture workspace: UNCHANGED/PRESERVED. Protected original/3D projects: UNCHANGED. No build/lint/site regression tests were run because no website code or public asset changed; reconstruction-specific checks and preservation hashes were used. No deployment or commit. Cost ₹0/$0.

See diagnostics/preservation-validation.json for historical/source image/production protection verification. Technical checks passing must not be presented as visual approval.
