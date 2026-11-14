# MU-X reference / soft-surface / deep-detail pass — v01

**C — MODEL STILL DOES NOT REPRODUCE THE SUPPLIED MU-X WELL ENOUGH.**

The primary body failed the silhouette and neutral-clay gates. Deep detailing was therefore **not started**. The requested filename and diagnostic directory contain an unapproved **primary-surface attempt**, not a finished deep-detail model. No web export or replacement.

## Saved source and changes

Master: `tools/3d/isuzu-mux/source/production/isuzu-mux-curve-soft-detail-v01.blend`.

Diagnostics: `tools/3d/isuzu-mux/code-generator/renders/deep-detail-v01/`.

New add-on modules: `geometry/soft_body.py`, `run_soft.py`, `check_soft.py`, `overlay_soft.py`, `boards_soft.py`. `geometry/rounded.py` now accepts an optional profile callback; the previous default profile is retained. `rounded_ui.py` and the default runner expose the new soft-body attempt. The pre-pass add-on was preserved in `tools/3d/isuzu-mux/code-generator/rounded-v01-addon/`. Earlier code, curve, rounded and V04 milestones are not overwritten. No manual vertex edits or downloaded geometry.

## Reference review

All 18 authoritative originals were inspected at their supplied resolutions in this pass. They are screenshots, not original calibrated full-resolution camera captures. Original files remain unchanged. The compatible silver open/closed-panel family remains canonical; color is not itself a geometry criterion. The existing audit/inventory remains valid.

Full filenames share `Screenshot From 2026-11-06 ` and `.png`:

| Image time | Visible evidence / use |
|---|---|
| 18-05-01 | Collage: broad side/rear mass, quarter glass, tailgate/bumper. Different wheels/trim; secondary, not averaged into canonical curves. |
| 18-05-23 | Promotional front-three-quarter: fender crown, chrome grille, body reflection. Secondary; lighting is not a panel groove. |
| 18-05-58 | Engine cover, battery/airbox/reservoir arrangement. Later engine context only, no exterior geometry inferred from it. |
| 18-06-24 | Interior collage: RHD dashboard, center controls, seating/door-card mass. Deferred until exterior approval. |
| 18-08-46 | Frontal composition: lamp envelope, grille surround, fog recess, bumper depth. Promotional secondary, not calibration. |
| 18-09-21 | Open bonnet/doors: front housing/grille relationship and engine access. Open configuration excluded from closed-body silhouette. |
| 18-09-40 | Open left side: door shell/seat/side-step relationships and pillar context. No open-door silhouette imposed on closed body. |
| 18-09-48 | Open tailgate/rear doors: rear opening, dark cargo depth, bumper/lamp context. Deferred functional structure. |
| 18-10-06 | Opposite open side: arch/body/step relationships, door interior context. Secondary. |
| 18-11-39 | RHD cockpit: steering/dashboard/console and headliner. Interior deferred. |
| 18-17-10 | Primary frontal bonnet, windscreen, lamp/grille/bumper envelopes. |
| 18-17-14 | Primary left profile: bonnet/cowl/rake, window envelope, arch and sill. |
| 18-17-18 | Primary rear: glass/tailgate taper, lamp split, bumper returns. |
| 18-17-21 | Opposite profile checks rear-quarter mass, arch/step and cabin relationships. |
| 18-17-25 | Front-three-quarter checks front-corner wrap and fender-to-door transition. |
| 18-17-27 | Primary front-three-quarter: bonnet crown, fender volume, A-pillar and grille depth. |
| 18-17-31 | Rear-three-quarter: D-pillar, rear-glass seating and bumper mass. |
| 18-17-35 | Primary rear-three-quarter: quarter volume, lamp wrap, rear taper. |

## Region evidence and limits

| Region | Primary / secondary | Supported shape/finish and what remains unbuilt |
|---|---|---|
| Bonnet/front fender | 18-17-27 / 10,14,25 | Broad crown, narrower edge falloff, substantial arch crown. Highlights imply curvature, not extra seams. New code attempts these, but does not match accurately. |
| Door side/shoulder/sill | 18-17-14 / 21,27,35 | Convex door skin, modest shoulder transition, stronger lower sill/step. Handle/panel gaps are separate defined features, not deep character grooves. Not yet reconstructed faithfully. |
| Windscreen/roof | 18-17-10 / 14,27 | Rake, width change, gentle roof crown and supported rails. Current blank shell is not finished glass, pillars or rails. |
| Quarter glass/D-pillar | 18-17-35 / 14,18,31 | Distinct tapered quarter aperture and thick pillar with depth; dark seal/surround. Current shell lacks these boundaries. |
| Front lighting/grille | 18-17-10 / 27,09-21 | Projector/reflector housing, lens, DRL-like upper guide, bright double-bar grille, recessed backing. None added because body gate failed. |
| Mirrors/handles/steps | 18-17-14 / 21,27,09-40 | Chrome-like handle/mirror surfaces, black mounting/step surfaces. Supported visible positions; hidden mounts are not measured. Deferred. |
| Rear lamps/tailgate/bumper | 18-17-18 / 35,31,09-48 | Split wraparound red/clear lenses, garnish, handle recess, curved bumper/lower trim. Hidden optical/mechanism details unsupported; all deferred. |
| Wheels/tires | 18-17-14 / 27,35 | Multiple split spokes, hub, sidewall and rounded shoulder. Current cylinders/rim discs remain placeholders, not a detailed wheel. |
| Interior/engine | 18-11-39 / 06-24; 05-58 / 09-21 | Visible dashboard/seat/console and engine-bay massing only; no unseen mechanical CAD inferred. Deferred. |

No photograph provides exact 3D depth, lens calibration, glass thickness, edge radius or hidden assembly geometry. Existing curve coordinates, cross-car depth, arch clearances, scale/tire guidance, closure patches and all numeric blend distances remain documented conservative approximations. No exact/factory-accuracy claim.

## New primary-surface work

`SURFACE_CLASSES` explicitly distinguishes:

- **A — SOFT:** broad bonnet, door, roof and quarter ribbons with monotone cubic interpolation.
- **B — CONTROLLED:** fender returns, shoulder and corner transitions using closer support rails and localized influence.
- **C — DEFINED:** glass, lamp/grille and panel boundaries; retained as construction intent, not built as details before body approval.

The new profile callback removes the old abrupt bonnet/windscreen/roof switches, blends a common centerline through cowl and rear roof, and uses front/rear fender-crown curves to vary cross-car volume around axles. Door skin has broad convexity instead of repeating a flat maximum-width span. The joined sampled-curve body, rounded closures, arch cuts and small edge bevel remain from the rounded engine. This is a sampled procedural surface, not a solved reconstruction or certified G1/Class-A CAD surface. Existing closure layout and simplified cross-sections remain limiting factors.

Deep details were deliberately not added. More sparkle, badges, glass overlays or detailed lenses would not make the current clay silhouette acceptable.

## Engineering checks

Blender 5.2.2 LTS at `/usr/bin/blender`.

| Metric | Preview | Quality |
|---|---:|---:|
| Vertices | 6,556 | 14,398 |
| Triangles | 13,076 | 28,760 |
| Objects / materials | 9 / 3 | 9 / 3 |
| Length | 4.82500 m | 4.82500 m |
| Width | 1.86000 m | 1.86000 m |
| Height | 1.85994 m | 1.86000 m |
| Wheelbase | 2.845 m | 2.845 m |
| Symmetry max discrepancy | 5.96e−8 m | 5.96e−8 m |
| Non-manifold edges | 0 | 0 |
| Degenerate faces | **6 — FAIL** | 0 |
| Negative-volume objects | 0 | 0 |

Symmetry **PASS**, about **0.0000596 mm**, unchanged .0001 m test threshold. Ground height approximately floating-point zero. Finite coordinates PASS. Preview's six degenerate faces remain unresolved; they are not hidden by a tolerance adjustment. No local curvature, self-intersection or G1 certification.

Reproducibility **PASS for the generated curves/body**: explicit deletion, regeneration, saved-scene match, repeated generation, UI action and construction-curve visibility were checked. Deep-detail reproducibility is **NOT REACHED**, because no details exist. The two modes use the same profile intent at different sampling; numeric success does not imply visual approval.

## Visual gate and stop

Five clay views, three reflection-strip views and the reference comparisons were inspected. The smoother cowl is a local change, not a substantial reference-fidelity gain. The front still reads as a square blank fascia; door/shoulder proportions and wheel/body relationships are wrong; the greenhouse lacks the original openings and pillars; the rear mass/closures remain generic and pinched. Reflection flow remains uneven at the corners and rear. The body does not resemble the source MU-X sufficiently without details or badges.

Reference fidelity: **NEEDS WORK in all five principal views**. Soft finish: bonnet, fenders, body sides, shoulder, roof, rear quarters and bumpers **NEEDS WORK**. Original cuts: bonnet, arches, shoulder, greenhouse, quarter glass, D-pillar and rear **NEEDS WORK**. Clay, strips, edge radii and continuity **NEEDS WORK**. Badgeless recognition **NEEDS WORK**.

Deep-detail status: headlights, grille, mirrors, seated/thick glass, window trim, door separation, handles, wheel spokes/tire finish, tail lamps, detailed tailgate/bumper, underbody and visible interior **NOT REACHED / NOT BUILT**. Basic tire/rim placeholders and primary body mass are present. This pass does not deliver the requested deep detailing.

Compared with V04: **front WORSE; front-three-quarter WORSE; side WORSE; rear-three-quarter WORSE; rear WORSE; overall WORSE**. Current blank clay and the more developed V04 are different development stages; nevertheless the comparison cannot justify replacement.

**C — MODEL STILL DOES NOT REPRODUCE THE SUPPLIED MU-X WELL ENOUGH.** Stop at the failed clay gate as instructed. The next required work is reference-faithful macro/cabin/fascia surface reconstruction, not details applied over this body.

## Diagnostic package

`tools/3d/isuzu-mux/code-generator/renders/deep-detail-v01/` contains:

- `reference-v04-new.jpg`, five principal clay views and three `strips-*.png` views.
- Five `overlay-*.jpg` silhouettes, with raw `alpha-*.png` renders.
- Enlarged `region-bonnet.jpg`, `region-front-fender.jpg`, `region-headlight-grille.jpg`, `region-greenhouse.jpg`, `region-side-body.jpg`, `region-quarter-glass-d-pillar.jpg`, `region-rear-quarter.jpg`, `region-tail-lamp-rear.jpg`.
- Validation, add-on tests and logs.

Region images show the **unapproved primary body**, not completed lamps/glass/details. Overlays are manually box-fitted with preserved aspect ratio and explicitly labeled **not calibrated alignment**. They are qualitative diagnostics, not exact silhouette-error measurements.

## Protection

V04, its 113 components, prior code/curve/rounded milestones, original references and controlled-capture workflow remain preserved. No Hero, navigation, services, gallery, enquiry, TOLI AI, theme or responsive-source changes. Protected projects unchanged. Existing website GLB remains byte-identical. No web export, integration, deployment or commit. No paid models/cloud/API. **₹0 / $0**. Website tests were not rerun because nothing was integrated; Blender checks were run instead.
