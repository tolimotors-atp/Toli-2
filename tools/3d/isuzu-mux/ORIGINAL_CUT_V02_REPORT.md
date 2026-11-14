# TOLI MU-X — original-cut procedural V02

**Decision C — ORIGINAL MU-X CHARACTER NOT RECOVERED — STOP.** No production GLB export or website replacement. This is an engineering/shape experiment, not original-like finish approval.

## Code and preservation

New shape data: `tools/blender-addons/toli_mux_generator/mux_shape_data.py`. New surface functions: `surfaces.py`. Changed generator: `geometry/__init__.py`; versioned UI/output routing: `operators.py`, `panels.py`, `run_milestone.py`, `check_milestone.py`. Added `run_v02.py`, `diagnose_v02.py`, `boards_v02.py`, `check_v02.py`. The complete previous add-on is preserved in `tools/3d/isuzu-mux/code-generator/v01-addon/`. V01 blend/renders and original reports remain intact. Current runners/UI target V02 rather than silently overwriting V01.

Generated scene: `tools/3d/isuzu-mux/source/production/isuzu-mux-code-generated-v02.blend`. Entirely procedural; no manually pushed vertices or imported V04 control cage. V04 and its 113 components remain unchanged. No component reuse, interior, engine, handles, badges or lamp-internal work. No application source edits. Hero, navigation, TOLI AI, controlled-capture workflow and protected projects are unchanged; TOLI AI was not retested because the website was not modified. No paid assets/cloud/APIs; ₹0 / $0. No deployment or Git commit.

## Reference usage

The 18-authoritative-image atlas was inspected again. Shape evidence stays with the compatible older silver MU-X body family. Interior/engine photographs remain context, not exterior controls; open panels are not traced as the closed silhouette. Color differences alone do not define incompatible geometry.

- Front and bonnet: `Screenshot From 2026-11-06 18-17-10.png`, corroborated by `18-17-27.png` and the open-bonnet front only for structural context.
- Front fenders/side shoulder/arch: `18-17-14.png`, `18-17-21.png`, `18-17-25.png`, `18-17-27.png`.
- Windscreen, side-window boundaries and roof: side profiles and both front-three-quarter views; front controls upper/body width relationships.
- Quarter glass, D-pillar and rear taper: `18-17-14.png`, `18-17-18.png`, `18-17-31.png`, `18-17-35.png`.
- Rear massing: straight rear and both rear-three-quarter views together.

These are visual constraints with perspective, not calibrated blueprints. The metric stations in `mux_shape_data.py` are fitted **VISUAL APPROXIMATIONS**, not claimed exact image measurements or manufacturer CAD. Original screenshot readings remain in `reference_data.py`. No invented solved cameras or new official dimensions are claimed.

## What changed

The body has cubic-Hermite longitudinal interpolation through twelve named-by-position sections. Each section now has sill return, lower-door volume, mid-door convexity, shoulder, upper return and bonnet crown instead of a six-point rectangular extrusion. The bonnet height/crown evolves through front, middle and cowl stations. Cabin stations separately control lower/upper width, base and roof crown. Rear roof/cabin narrowing changes in three dimensions. Three side-window envelopes per side introduce separate pillar/quarter-glass relationships; these remain approximate thin volumes, not approved glass joins.

Wheel openings use an extruded longitudinal profile with different front/rear clearances, a crown and lower termination, based on the actual axle coordinates. They are actual cuts. Finished fender flare/arch transitions and front/rear fascia composition remain unachieved; no floating trim was added to simulate them.

The existing symmetry error came from independently evaluated Boolean/bevel results. The generator now bakes the evaluation, bisects at Y=0 and mirrors one half with centerline welding. This changes geometry rather than increasing validation tolerance. A pre-mirror degenerate-edge cleanup is included; it does **not** resolve every Quality-mode degeneracy (see below).

Inactive older sliders were removed from the current panel. Current shape tuning occurs in the data module; do not assume all old parameter fields still control V02. Dimensions, greenhouse width and wheel/track settings remain exposed. More intuitive region controls are not implemented yet.

## Engineering validation

Blender 5.2.2 LTS, `/usr/bin/blender`. All figures below are evaluated geometry, not a claim of visual acceptance.

| Metric | Preview | Quality |
|---|---:|---:|
| Vertices | 3,050 | 5,491 |
| Triangles | 6,036 | 10,918 |
| Objects / materials | 16 / 4 | 16 / 4 |
| Length | 4.8250 m | 4.8250 m |
| Width | 1.86047 m | 1.86052 m |
| Height | 1.86136 m | 1.86136 m |
| Wheelbase | 2.8450 m | 2.8450 m |
| Minimum ground Z | −5.25e−9 m | −5.25e−9 m |
| Symmetry max discrepancy | 5.96e−8 m | 5.96e−8 m |
| Non-manifold edges | 0 | 0 |
| Degenerate faces | 0 | **2 — FAIL** |

Symmetry: **PASS**, approximately **0.0000596 mm**, versus the prior 1.61 mm. The unchanged pass threshold is .0001 m (0.1 mm). Heights/widths remain within about 1.4 mm of the user-supplied approximate guidance; cubic interpolation creates a small overshoot.

Finite coordinates: PASS; negative signed-volume objects: zero. Neither proves all local normals/intersections are valid. Body/cabin/window volumes are individually closed but overlap; this is not a watertight continuous production exterior. Quality topology still fails. The two remaining degenerate faces are reported, not hidden by changing the area threshold.

The initial V02 runner proved delete-and-regenerate equality. `check_v02.py` additionally checks the final current code twice and compares it to the reopened saved scene; `final-check.json` records the exact result. `validation.json` and `quality-validation.json` retain mode-specific checks. Arbitrary parameter combinations are not certified.

## Visual gate

Five neutral renders, five clay views, three reflection-strip views, five silhouette overlays and seven enlarged region comparisons are under:

`tools/3d/isuzu-mux/code-generator/renders/v02/`

Key evidence: `code-vs-v04.jpg`, `front.png`, `front34.png`, `side.png`, `rear34.png`, `rear.png`, `clay-*.png`, `strips-front34.png`, `strips-side.png`, `strips-rear34.png`, `overlay-*.jpg`, `region-*.jpg`.

Overlays use the rendered alpha silhouette fitted into a manually chosen photographic vehicle rectangle, preserving aspect ratio. **They are uncalibrated 2D box-fit diagnostics**, not solved camera alignment, and must not be used to claim numerical silhouette agreement. Region crops likewise are approximate visual comparisons. Their preparation code is saved in the add-on.

Inspection finds more curvature than V01 but insufficient MU-X recognition. The long body is still too plain. Bonnet/fender/door curvature is overly uniform, the cowl has a dark seam/overlap, windscreen and rear glass are still not properly separated, roof/cabin returns pinch, quarter-glass geometry does not reproduce the source, and front/rear compositions are missing. Reflection strips show discontinuities and inconsistent highlight flow at cabin joins. Neutral clay exposes those defects without paint or text.

| Region | Gate |
|---|---|
| Bonnet cut | NEEDS WORK |
| Front fender cut | NEEDS WORK |
| Front identity | NEEDS WORK — grille/lamp/bumper envelopes not reached |
| Windscreen / A-pillar | NEEDS WORK |
| Greenhouse | NEEDS WORK |
| Side body cut | NEEDS WORK |
| Quarter glass / D-pillar | NEEDS WORK |
| Rear-cabin taper | NEEDS WORK |
| Rear quarter | NEEDS WORK |
| Rear identity | NEEDS WORK — lamp/tailgate composition not reached |
| Clay / reflection strips / continuity | NEEDS WORK / NEEDS WORK / NEEDS WORK |
| Badgeless recognition | NEEDS WORK |

Relative to V04: **front WORSE; front-three-quarter WORSE; side WORSE; rear-three-quarter WORSE; rear WORSE; overall WORSE**. Curvature improvement over V01 does not establish improvement over V04 or recovery of original MU-X character.

## Stop / next requirement

Decision **C** applies. Stop at this failed body-character gate. Do not add badges, shinier paint, grille microdetail or interior to conceal the failed silhouette and joins. Further work would need redesigned cross-section and cabin boundary data, a continuous cowl/roof/quarter connection, validated arch/shoulder transitions and resolution of Quality-mode degeneracies, followed by a new versioned comparison. The current result is not ready for detailing or website use.

Production GLB: **NOT EXPORTED**. Website MU-X: **NOT UPDATED**; its V04 preview stays active. Unrelated website build/tests were not rerun because there was no website modification. No deployment or commit.
