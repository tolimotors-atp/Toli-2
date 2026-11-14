# Curves + rounded body — v01

**C — RESULT REMAINS TOO BOXY OR HAS BECOME OVER-ROUNDED.** This attempt does not establish original MU-X cuts or automotive finish. Website NOT UPDATED; production GLB NOT EXPORTED.

## Saved work

Source: `tools/3d/isuzu-mux/source/production/isuzu-mux-curve-rounded-v01.blend`.

Add-on: `tools/blender-addons/toli_mux_generator/`. New modules: `geometry/rounded.py`, `rounded_ui.py`, `run_rounded.py`, `check_rounded.py`, `boards_rounded.py`. Changed: `geometry/curves.py` (bounded roof/side-master handle tangents), `__init__.py`, `panels.py`, `run_milestone.py`. The prior curve-first add-on is archived at `tools/3d/isuzu-mux/code-generator/curve-first-addon/`. Prior V01/V02/curve-only scenes and evidence are preserved. The generic runner now delegates to the rounded attempt; old runners remain separately available.

Generate MU-X — Rounded Curves and Render Rounded Validation Views are registered UI actions. Construction curves can be shown above the body via the existing toggle. No manually edited vertices are part of the solution. Export remains blocked.

## Construction method

The generator first creates actual Blender Bezier datablocks from the reference-informed curve data. It samples those datablocks (including their handles), then builds body ribbons constrained by bonnet center, side master, roof center, shoulder, belt, lower body and sill. Transverse interpolation supplies broad lateral curvature; it is no longer the V01 rectangular six-point body extrusion. Wheel openings are cut from sampled Bezier arch profiles, not perfect circular cutters.

The ribbons share vertex rows in a joined body/cabin mesh. Front/rear closures use progressively inset shared rings, with longitudinal corner depth, instead of planar n-gon caps. This is controlled mesh generation between sampled curves, not a Blender NURBS surface. Separate independent region patches with certified G1 continuity are not implemented. The first patch joins still produce visible problems.

Curve-derived crown/door/sill/shoulder profiles supply the primary curvature. A small angle-limited 12 mm bevel rounds hard cut edges; it is not a large global bevel. It can also affect other high-angle edges, not exclusively the arch. `RADII` contains body/arch/bumper/shoulder/sill controls; some are profile-blend distances rather than measured geometric radii. No panel-edge parameter was added because panels are not separated.

A first attempt overshot body width by about 55 mm. Monotone cubic tangents replaced overshooting transverse Catmull-Rom tangents. Roof and side-master Bezier handles were also bounded in component slope, preventing roof-height overshoot. Closed-body outward winding is explicitly recalculated after evaluating the mirror. No tolerance was enlarged to conceal errors.

The arch lip/fender blend is not visually finished. Dedicated fender-crown construction curves exist, but not all of their constraints are enforced by the current body ribbon algorithm. This is a limitation, not proof of reference-accurate fenders.

## References

The 18-image authoritative inventory/atlas and compatible older silver MU-X decision remain in use. Front/bonnet controls come from 2026-11-06 screenshots **18-17-10 / 18-17-27**; side/shoulder/arches from **18-17-14 / 18-17-21 / 18-17-25 / 18-17-27**; rear cabin/quarter/taper from **18-17-18 / 18-17-31 / 18-17-35**. Open-panel photographs remain contextual rather than closed-body silhouette constraints; interior/engine views were not used to justify exterior geometry.

Curve positions/depths remain visual approximations, not solved photogrammetry or original factory surface data. No new images, downloaded vehicle geometry, paid models, API or cloud service. No claim that all the reference constraints are satisfied.

## Actual checks

Blender 5.2.2 LTS at `/usr/bin/blender`.

| Metric | Preview | Quality |
|---|---:|---:|
| Vertices | **5,684** | **12,453** |
| Triangles | **11,332** | **24,870** |
| Objects / materials | 9 / 3 | 9 / 3 |
| Length | 4.82504 m | 4.82500 m |
| Width | 1.86000 m | 1.86000 m |
| Height | 1.85994 m | 1.86000 m |
| Wheelbase | 2.845 m | 2.845 m |
| Minimum ground Z | −5.25e−9 m | −5.25e−9 m |
| Symmetry discrepancy | 5.96e−8 m | 5.96e−8 m |
| Non-manifold edges | 0 | 0 |
| Degenerate faces | 0 | 0 |
| Negative signed-volume objects | 0 | 0 |

Symmetry **PASS**, approximately **0.0000596 mm** versus historic 1.61 mm, with unchanged .0001 m threshold. Main geometry is mirrored from one half; no independent left/right surface fitting. Finite coordinates PASS. These checks do not certify self-intersection freedom, tangent continuity, uniform curvature or original MU-X resemblance.

Reproducibility **PASS**: reopened saved scene matches current code; explicitly deleting both construction curves and generated surfaces, then regenerating, gives the same fingerprint, including curve handles. Repeated generation, registered UI Generate action and construction visibility over the body were tested. See `addon-tests.json`. Preview and Quality use the same functions/rails with different sampling, not different intended designs. Quality geometry was measured; the saved five-view visual set is Preview, not a claim that Quality surfaces have passed finish review.

## Visual findings and decision

Five clay views and three long-area-light reflection views were generated and inspected. The broad side now has some convexity and the bonnet has crown. However:

- **Still unnaturally flat:** wide central fascia, long mid-door/side regions and the tailgate mass. The bumpers do not yet read as integrated original MU-X volumes.
- **Too soft / poorly controlled:** roof-to-cabin transitions and rear-cabin mass lose window-cut structure. The current blank clay greenhouse is not a finished windscreen, A/D pillar or glazing arrangement.
- **Pinching / waviness:** front corner seams, bonnet-to-cabin transition and rear closure rings show uneven highlights. Rear curvature changes too abruptly. Small bevels or more samples do not solve those structural errors.
- **Character:** the shoulder remains defined but its break is not convincingly the reference MU-X. Fender-to-door/bonnet transitions and arch lower terminations remain crude. Rounded does not mean recognizable.

| Region / finish | Status |
|---|---|
| Bonnet curvature | NEEDS WORK |
| Front fender curvature | NEEDS WORK |
| Wheel arches / lip | NEEDS WORK |
| Body-side curvature | NEEDS WORK |
| Shoulder / lower body | NEEDS WORK / NEEDS WORK |
| Roof / greenhouse | NEEDS WORK / NEEDS WORK |
| Rear fender / rear quarter | NEEDS WORK / NEEDS WORK |
| Front / rear bumper | NEEDS WORK / NEEDS WORK |
| Original MU-X cuts retained | NEEDS WORK |
| Clay surface / reflection flow | NEEDS WORK / NEEDS WORK |

Five-view comparison against **previous coded V02**: front **SIMILAR** (both lack convincing front identity); front-three-quarter **WORSE**; side **WORSE**; rear-three-quarter **WORSE**; rear **WORSE** as a complete visual representation. Individual broad curvature improves over early rectangular blockouts, but this is not a better MU-X. Missing earlier window guides and current shading/closure defects also limit direct comparison. It does not beat V04 either.

**Final C:** the attempted rounding is neither adequate original cut nor controlled finish. Stop before identity detailing. Grille mesh, lamp internals, badges, handles, wipers, interior, engine and moving doors were not added. Next work would require redesigning the fascia/rear patch layout and enforcing the fender/cabin boundaries rather than adding more bevel or subdivision. No automatic website replacement.

## Evidence

Directory: `tools/3d/isuzu-mux/code-generator/renders/curve-rounded-v01/`.

- `reference-previous-rounded.jpg`: reference | previous coded V02 | new rounded body, five views.
- `clay-front.png`, `clay-front34.png`, `clay-side.png`, `clay-rear34.png`, `clay-rear.png`.
- `strips-front34.png`, `strips-side.png`, `strips-rear34.png`.
- `validation.json`, `addon-tests.json`, generation and test logs.

The comparison is qualitative, not a calibrated overlay. No badge, metallic paint or fancy texture was used to conceal body shape. No new surface-quality PASS is claimed merely because numerical geometry tests pass.

## Protection

V04 source, its retained components, earlier coded/curve milestones, original reference images, controlled capture, Hero, navigation, TOLI AI and both protected projects remain unchanged. The active website V04 GLB remains byte-identical. No website source changes, so website tests were not rerun; Blender/add-on checks were run instead. Deployment/commit **NOT PERFORMED**. Cost **₹0 / $0**.
