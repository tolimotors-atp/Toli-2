# CROSS-VIEW SURFACE PROTOTYPE V02

B — METHOD REMAINS VALID, BUT ONE OR MORE LOCAL ZONES STILL REQUIRE REFINEMENT

Saved local refinement of the V01 shared-vertex quad patches. Blender 5.2.2 LTS, `/usr/bin/blender`. V01 is preserved byte-for-byte; the pre-V02 generator is archived at `code-generator/pre-surface-prototype-v02-addon/`. No zone is approved as production bodywork.

## Zone A

Root stubs: **NEEDS WORK**. Their transverse width increases from 0.070 to 0.150 and their longitudinal reach shortens from 0.180 to 0.135 nominal units. The cowl/root boundary becomes SOFT rather than DEFINED. The front/three-quarter views show broader feet, but the side view still exposes thin rising construction tabs: this is not a complete structural root.

Bonnet edge roll: **NEEDS WORK**. The existing fender-upper rail moves from edge Z −0.115 to −0.080; its neighboring side rail is redistributed. Clay is less corrugated, but the bonnet/fender blend remains too diffuse and its curvature evolution is not yet reference-converged.

Arch return: **NEEDS WORK**. Lip offset grows from 0.015 to 0.030, the inboard return grows from 0.014 to 0.025, and CONTROLLED weights reduce from 0.22 to 0.12. Zebra compression persists at the arch ends, especially the trailing return. Section spacing still needs local work.

Shape / cross-view agreement / soft finish / reflection flow / reference fidelity: **NEEDS WORK** for each. The five section plots compare actual mesh-plane intersections at leading edge, 25%, 50%, 75% and cowl; they do not substitute a smoothed illustrative profile.

## Zone B

Aperture shape: **NEEDS WORK**, with a measured local improvement. Existing cyclic controls receive bounded inverse subdivision compensation (45% of a solved correction). The guide itself is unchanged. Full compensation was tested and rejected because it folded the narrow forward frame; the bounded result passes overlap checks. It does not force rectangular corners.

D-pillar / frame junctions: **NEEDS WORK**. The bridge crown offset reduces from 0.010 to 0.003 while retaining the coupled V01 rear-depth solve. Star-like zebra concentration remains at the roof/D-pillar/window junction and the pillar still reads as inflated locally. No new pole or support loop is added.

Boundary drift: **NEEDS WORK**. Lower rear-glass crease weights were tested and rejected after a measurable drift increase. Final B weights retain V01 CONTROLLED 0.22 / DEFINED 0.65. Final rear-glass drift is still slightly higher, not an improvement.

| Boundary / state | V01 mean | V01 max | V02 mean | V02 max |
|---|---:|---:|---:|---:|
| quarter_glass / base | 0.00444347 | 0.01489262 | 0.00212054 | 0.01533179 |
| quarter_glass / evaluated | 0.01385265 | 0.03944359 | 0.01176544 | 0.02738808 |
| rear_glass / base | 0.00492820 | 0.02117570 | 0.00492820 | 0.02117570 |
| rear_glass / evaluated | 0.00905456 | 0.02916746 | 0.00911923 | 0.02931030 |

Distances are approximate uncalibrated model-space units, not measured vehicle accuracy. Quarter-glass uses 192 fixed-curve samples against the actual window-return/frame interface segments in 3D. Rear glass uses 264 fixed samples against its roof/D-pillar interface in Y/Z; X depth remains inferred. Base boundaries have 12 segments, evaluated boundaries 48. Nearest segment distance is used, not nearest vertex. The measure is one-directional reference-to-boundary and does not prove complete curve agreement. Quarter evaluated maximum improves about 30.6%, mean about 15.1%; its base maximum rises slightly. Rear evaluated mean/max also rise slightly.

Shape / cross-view agreement / soft finish / reflection flow / reference fidelity: **NEEDS WORK** for each. A lower drift number does not approve the visible pillar/frame form.

## Zone C

Upper lamp bridge: **NEEDS WORK**. Its free rail moves forward from X 1.94 to 1.88 and its rise is redistributed. This broadens the bridge footprint but the upper termination remains a thin stretched lip, especially in rear and side views.

Aperture returns: **NEEDS WORK** despite more breathing room. Return depth grows from 0.008 to 0.020; the support rail moves from 35% to 55% of the surround width; the surrounding Y/Z expansion grows from 1.12/1.14 to 1.24/1.28. The lamp outline itself is not scaled down. A smooth lateral cap replaces a hard clamp that initially collapsed adjacent lower rows. The aperture stays empty. The upper corner still concentrates reflections.

Lower corner: **NEEDS WORK**. Existing lower Z rails change from 0.68/0.46/0.325/0.30 to 0.73/0.51/0.35/0.30. The close lower rails are separated, but a tight vertical corner reflection remains.

Quarter mass: **PASS** for preservation. Bumper wrap: **PASS** for preservation of the V01 height-dependent compound wrap. These two passes do not approve Zone C.

Shape / cross-view agreement / soft finish / reflection flow / reference fidelity: **NEEDS WORK** for each.

## Geometry comparison

| Zone | Base vertices V01 → V02 | Evaluated vertices V01 → V02 | Evaluated triangles V01 → V02 |
|---|---:|---:|---:|
| A | 132 → 132 | 1773 → 1773 | 3328 → 3328 |
| B | 124 → 124 | 1699 → 1699 | 3200 → 3200 |
| C | 214 → 214 | 2872 → 2872 | 5376 → 5376 |

No topology added or removed. Total: 470 base vertices, 6,344 evaluated vertices, 11,904 evaluated triangles. All patches retain level-2 Catmull-Clark, shared boundary vertex IDs and the SOFT / CONTROLLED / DEFINED system. Local vertex and support-spacing changes were sufficient for a limited improvement, not a full quality pass.

## Technical validation

Unintended cracks: **0**. Degenerate faces: **0** in base and evaluation. Interior non-manifold edges: **0**. Non-adjacent triangle overlaps: **0** in base and evaluation. Base-control symmetry discrepancy: **0.0** for every zone. Open construction cuts and lamp/window apertures are intentional, not watertight bodywork.

Delete/regenerate through the registered operator: **PASS**. Repeated generation also preserves crease values and subdivision settings; every base face remains a quad. Default V01 generation regression: **PASS**. Fixed reference curves and all wheel transforms: **PASS**. Dimension-lock rejection preserves the candidate: **PASS**. Zone filtering, control-section visibility, cage-only mode and three-zone isolation: **PASS**.

## V04 departures

Authoritative V04 curve objects and wheel anchors are unchanged. A-root intermediate sections, fender roll/lip rails, B aperture control compensation/bridge crown and C surround/bridge/lower-corner rails are deliberately adjusted internal surface controls. Reference aperture guides remain fixed; subdivision compensation is a control-net departure, not a guide edit. C retains the reference lamp Y/Z outline and the V01 inferred compound X solution. Rear-glass Y/Z section samples remain preserved. Depth is still inferred.

Measured departures:

```json
{
  "bonnet_center_max_z_departure_nominal_m": 0.05260050296783447,
  "lamp_yz_control_anchors": "PRESERVED",
  "lamp_x_max_departure_nominal_m": 0.10081315040588379,
  "quarter_window_evaluated_boundary_proximity_max_m": 0.0236786101013422,
  "interpretation": "Nominal model coordinates only; nearest evaluated open-edge sample is a diagnostic, not physical reconstruction accuracy.",
  "rear_glass_yz_section_samples": "PRESERVED",
  "rear_glass_x_section_max_departure_m": 0.09935116767883301
}
```

## Saved outputs

- Master: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v02.blend`
- Clay: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02/clay-diagnostics.jpg`
- Reflection / zebra, V01 beside V02: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02/reflection-zebra-diagnostics.jpg`
- Matching base / evaluated views: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02/control-net-evaluation.jpg`
- Actual control sections: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02/control-net-sections.jpg`
- Five bonnet edge-roll sections: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02/bonnet-edge-roll-sections.png`
- Reference | V01 | V02: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02/reference-comparison.jpg`
- Full multi-view comparisons: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02/comparison-zone-a.jpg`, `comparison-zone-b.jpg`, `comparison-zone-c.jpg`
- Individual 1000×700 renders: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02/zone-a/`, `zone-b/`, `zone-c/` (12 per zone)
- Machine-readable evidence: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02/geometry-validation.json`, `addon-tests.json`, `boundary-deviations.json`, `constraint-departures.json`, `fixed-v01-cameras.json`, `preservation.json`, `FINAL_GATE.json`

V01 and V02 use the same baseline camera transforms, orthographic framing, 12-sample neutral studio and reflection/zebra shaders. Reference photographs remain uncalibrated perspective images. No production paint or detail camouflage is used.

## Final recommendation

Decision **B**. Remaining blockers only:
- **A:** side-view root tabs, overly diffuse bonnet/fender transition and arch-end reflection compression.
- **B:** residual aperture drift, inflated D-pillar and concentrated roof/frame junction reflections; slight rear boundary regression.
- **C:** thin upper lamp bridge and pinched aperture/vertical lower-corner reflection flow.

Stop at V02 review. No V03 or complete body generated. Deep detailing not started. GLB not exported. Website, Hero, navigation and TOLI AI unchanged. Controlled capture preserved. Protected projects unchanged. Preservation checked against 1443 file hashes. Cost ₹0 / $0. Deployment and Git commit not performed.

Website build/lint were not rerun because no website source or public asset changed. The remaining risk is visual fidelity and inferred depth, not a claimed production-ready vehicle.
