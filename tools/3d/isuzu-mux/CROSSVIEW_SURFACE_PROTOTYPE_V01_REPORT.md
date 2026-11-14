# Cross-view surface prototype V01

## Decision B

**SURFACE-PATCH METHOD SHOWS PROMISE, BUT SPECIFIC ZONES REQUIRE ANOTHER LOCAL SURFACE ITERATION.**

Three independent test zones were constructed, inspected as low-density base nets and evaluated clay surfaces, and reviewed with reflection strips, synthetic zebra and reference comparisons. The method now creates connected compound forms instead of merely converting every internal cage curve into a loft. It also resolved a real patch overlap by coupling rear depth sections to the side silhouette. That is promising construction evidence, not an accepted MU-X reconstruction.

**No zone receives final shape/reference approval. Do not proceed to the full primary body.** No second prototype iteration was started. V04 remains an unapproved reference cage; this experiment does not retroactively approve it or create V05.

Blender **5.2.2 LTS**, `/usr/bin/blender`. All work local; no paid assets, cloud reconstruction or uploads.

## Zone A — bonnet / fender / cowl

|Criterion|Result|
|---|---|
|Shape|NEEDS WORK|
|Cross-view agreement|NEEDS WORK|
|Soft finish|NEEDS WORK|
|Reflection flow|NEEDS WORK|
|Reference fidelity|NEEDS WORK|

**Main improvement:** the bonnet crown, outer roll, front-fender mass, arch opening and cowl are a connected control surface. The root stubs attach through shared edges rather than floating as independent outlines. The fixed wheel/arch relationship remains available in front, side and three-quarter views.

**Remaining problem:** the cowl-root stubs are too thin and abrupt, and the arch/return band shows concentrated curvature. Reflection strips reveal uneven flow along the bonnet/fender band; zebra lines bunch at the root and arch return. The current result is more informative than the cage but still too generic and insufficiently faithful to the reference. The root ends are construction cuts, not a finished A-pillar.

Required images: `zone-a/clay-front.png`, `clay-front34.png`, `clay-side.png`, `clay-close.png`. `base-control.png` was inspected without subdivision; `control-sections.png` shows actual control sections.

## Zone B — roof / D-pillar / rear glass

|Criterion|Result|
|---|---|
|Shape|NEEDS WORK|
|Cross-view agreement|NEEDS WORK|
|Soft finish|NEEDS WORK|
|Reflection flow|NEEDS WORK|
|Reference fidelity|NEEDS WORK|

**Main improvement:** a rear-roof surface, returned quarter-window frame, D-pillar band and neutral-clay rear-glass surface now form one connected patch network. The glass and D-frame have shared boundary vertices. Coupled depth sections put the rear glass behind the side-window frame while preserving its sampled rear-view Y/Z outline and bounding its X positions by the side silhouette.

The first construction had **136 non-adjacent evaluated triangle-overlap pairs**, mainly between rear glass, the quarter frame and the D strip. These were located explicitly and corrected. Final base/evaluated overlap checks return **0** in all zones. This technical correction does not prove reference fidelity.

**Remaining problem:** the D-frame and quarter-window corners are too rounded/irregular, the evaluated aperture departs from its reference boundary, and reflection/zebra lines still concentrate around the upper/lower frame junctions. The roof/glass connection is now coherent but not suitably finished or reference-converged.

Required images: `zone-b/clay-side.png`, `clay-rear34.png`, `clay-rear.png`, `clay-close.png`. All Zone B diagnostics were rerendered after the depth correction.

## Zone C — rear quarter / lamp / bumper

|Criterion|Result|
|---|---|
|Shape|NEEDS WORK|
|Cross-view agreement|NEEDS WORK|
|Soft finish|NEEDS WORK|
|Reflection flow|NEEDS WORK|
|Reference fidelity|NEEDS WORK|

**Main improvement:** asymmetric wheel-area sections develop into a height-dependent corner wrap and lower bumper return. The empty lamp aperture is integrated through a painted quarter bridge and shared lower-frame edges; it is not a separate lens or a detailed lamp. Side-to-rear depth changes continuously rather than sitting on one rear plane.

**Remaining problem:** the upper lamp bridge rises too abruptly, the aperture return is too tight, and lower-corner reflections show concentrated curvature. Reference-specific quarter mass, lamp orientation and bumper section still need localized changes. The left/right corner test pieces intentionally do not connect across a complete rear body.

Required images: `zone-c/clay-side.png`, `clay-rear34.png`, `clay-rear.png`, `clay-close.png`.

## V04 constraints

**Preserved as reference data:** the entire V04 curve collection, section diagnostics, strong side outline, front/rear image-space measurement data, main glass/window reference curves, roof placement, width-station definitions, family dimensions, wheel locations/rotation/scale and tire geometry. V04 control coordinates/handles remain unchanged in memory during prototype generation and its master file remains byte-identical on disk. V01–V03 are likewise preserved.

**Surface adherence is not exact.** Retaining the authoritative curves in the scene does not mean the evaluated Catmull-Clark limit passes through every curve. The quarter-window aperture deviation below is explicitly a remaining failure, not silently accepted preservation.

**Adjusted/demoted internal constraints:**

- Zone A follows the stronger side cap where the old bonnet-centre guide would rise above it. Maximum centre-Z departure: **0.052601** nominal model units. Outer sections receive new crown/edge-roll/fender information rather than inheriting incompatible internal contours.
- Zone C retains sampled lamp Y/Z control anchors. Lamp X comes from a coupled height-dependent corner profile, with maximum departure **0.092813** nominal units. This supplies one wrapping corner surface instead of separate front/rear planes.
- Zone B preserves the rear-glass side-section Y/Z samples, while reconstructing X behind the D-frame and limiting it with the side cap. Maximum sampled side-section X departure: **0.099351** nominal units. The invented outer frame rail is constrained ahead of the glass; it is lower authority than the reference aperture and side silhouette.
- Maximum nearest evaluated open-edge distance for the sampled quarter-window reference: **0.041704** nominal units. This diagnostic combines Catmull-Clark approximation, returned lip offset and discrete sampling. It is not a calibrated physical error and is not a reference-fidelity PASS.

All these values use nominal family-scale model coordinates. The source photographs remain uncalibrated; no physically exact depth is claimed.

## Surface construction

**Patch method:** shared-vertex quad control networks with anatomical boundaries: bonnet centre/outer/roll, fender crown/arch return, cowl/root; rear roof, quarter-window annulus, D strip, roof return and rear glass; rear-quarter crown, lamp aperture/frame, upper bridge and bumper corner/return. The entire V04 cage was never lofted. Doors, grille, detailed tailgate, complete body and mechanisms were not built.

**Control-net strategy:** low-density sections establish the form before evaluation. Five approximate bonnet stations receive additional fixed-wheel and cowl sections. Rear-quarter sections use different fore/aft influence lengths around the axle. Window/lamp annuli and rear-perimeter strips follow actual feature boundaries rather than one arbitrary rectangular grid. Base views are saved separately; subdivision does not create the initial shape from a generic block.

**Continuity strategy:** every shared boundary between named patches declares **SOFT**, **CONTROLLED** or **DEFINED** in `patch-manifest.json`. Shared vertices provide exact positional closure. Subdivision and local crease weights (0 / 0.22 / 0.65) distinguish broad transitions from tighter rolls and intentional breaks. This is not a claim of G2 continuity. Base-normal-angle diagnostics are provided, and visual strip flow remains authoritative.

**Edges:** arch/window/lamp returns use local narrow geometry bands, approximately 0.008–0.018 nominal units, rather than a global bevel. Exterior rolls and interior return edges are distinct. Open experiment cut boundaries are unfinished and are not presented as finished physical panel edges. No final shell thickness is claimed.

**Evaluation/materials:** Catmull-Clark level 2 after base-net validity checks; neutral clay only. Rear-glass information uses a second neutral clay value for readability, not transparent production glass. Reflection clay is a temporary neutral glossy diagnostic. No final paint, chrome, badges, detailed optics, interior, engine or opening panels exist.

## Geometry

|Zone|Base control vertices|Evaluated vertices|Evaluated triangles|
|---|---:|---:|---:|
|A|132|1773|3328|
|B|124|1699|3200|
|C|214|2872|5376|
|Total|470|6344|11904|

Totals exclude V04 diagnostic curves, wheel-anchor cylinders, studio floor, cameras and lights. The three zones remain independent construction tests, not a full vehicle.

## Technical validation

|Zone|Base/evaluated degenerates|Interior non-manifold edges|Base/evaluated open edges|Shared-boundary cracks|
|---|---:|---:|---:|---:|
|A|0 / 0|0|54 / 216|0|
|B|0 / 0|0|50 / 200|0|
|C|0 / 0|0|92 / 368|0|

- Unintended boundary cracks / unwelded base T-junctions: **0**.
- Maximum positional gap at declared shared boundaries: **0** (shared control vertex IDs).
- Non-adjacent evaluated triangle-overlap pairs: **0** after the Zone B correction. The BVH diagnostic excludes triangles sharing a vertex; it is not a formal proof against every possible local fold.
- Base-control left/right symmetry discrepancy: **0**.
- Fixed dimension bounds: **PASS** at numerical precision; wheel anchors: **PASS**.
- Registered generator, delete/regenerate fingerprint, constraint preservation and invalid-dimension rejection without destroying the candidate: **PASS**.
- Zone isolation, actual-control-section toggles and Curve Cage Only mode: **PASS**.
- Python source parsing: **PASS**.

Open edges are reported separately. These are open construction surfaces with window/lamp apertures, not watertight body solids; “0 interior non-manifold edges” must not be read as “0 open edges.” No clean-topology result is used to approve visual shape.

## Reproducibility

**PASS.** Generated surfaces are deleted and rebuilt entirely from add-on code. Fingerprints cover base coordinates/faces/patch labels. The invalid-dimension guard runs before deleting the candidate. V04 constraints and fixed wheel transforms were checked before/after. Zones A/C were unchanged by the final B-only correction; their final images were retained based on matching control-geometry fingerprints and unchanged render setup. Zone B was fully rerendered. See `addon-tests.json`, `zone-render-cache-validation.json`, `constraint-departures.json`, `geometry-validation.json` and `self-intersection-diagnostic.json`.

## Source and diagnostics

Source: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/production/isuzu-mux-crossview-surface-prototype-v01.blend`

Clay overview: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/clay-diagnostics.jpg`

- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-a/clay-front.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-a/clay-front34.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-a/clay-side.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-a/clay-close.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-b/clay-side.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-b/clay-rear34.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-b/clay-rear.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-b/clay-close.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-c/clay-side.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-c/clay-rear34.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-c/clay-rear.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-c/clay-close.png`

Reflection/zebra overview: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/reflection-zebra-diagnostics.jpg`

- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-a/reflection.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-a/zebra.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-b/reflection.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-b/zebra.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-c/reflection.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-c/zebra.png`

Reference comparison: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/reference-comparison.jpg`

- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/comparison-zone-a.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/comparison-zone-b.jpg`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/comparison-zone-c.jpg`

Control-net/section overview: `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/control-net-sections.jpg`

- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-a/constraints-overlay.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-b/constraints-overlay.png`
- `/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01/zone-c/constraints-overlay.png`

The reflection images use actual area-light strip reflections. Zebra images use a high-contrast reflection-vector shader for shape diagnosis, not a calibrated curvature measurement or production material. Reflection pinching remains visible in the delivered files. V04 boundaries are available in each `constraints-overlay.png`; `cage.png` is the corresponding V04-only comparison with the same diagnostic camera. Photographic reference crops are uncalibrated, not registered reprojections.

## Reproduction

From the static project:

```
blender -b --python tools/blender-addons/toli_mux_generator/run_surface_prototype.py
blender -b --python tools/blender-addons/toli_mux_generator/check_surface_prototype.py
MUX_SURFACE_ZONE=A blender -b --python tools/blender-addons/toli_mux_generator/render_surface_prototype.py
MUX_SURFACE_ZONE=B blender -b --python tools/blender-addons/toli_mux_generator/render_surface_prototype.py
MUX_SURFACE_ZONE=C blender -b --python tools/blender-addons/toli_mux_generator/render_surface_prototype.py
python tools/blender-addons/toli_mux_generator/boards_surface_prototype.py
```

For short jobs, add for example `MUX_SURFACE_JOBS=reflection` or `MUX_SURFACE_JOBS=clay-side,clay-rear34`. The Blender sidebar exposes the experimental generator, zone isolation, V04 authoritative constraints and actual control sections; existing V04 section/comb tools remain available.

## Files and protection

Existing add-on files updated: `__init__.py`, `parameters.py`, `panels.py`, `cage_ui.py` for the prototype action and visibility. New modules: `geometry/section_network.py`, `geometry/surface_patch.py`, `geometry/continuity.py`, `surface_ui.py`, `surface_diagnostics.py`, plus generation/check/render/board scripts. The pre-experiment add-on is archived under `tools/3d/isuzu-mux/code-generator/pre-surface-prototype-addon/`.

Before/after hashes verify **544 unchanged earlier files**, covering static source/public, controlled capture, V01–V04 sources and all prior cage diagnostics. Old cage geometry generators/reference data also match the archived add-on. See `preservation.json`.

Original photographs were read only. The static frontend and public assets, including the existing website vehicle, were not changed. Protected sibling projects received no writes. No model was uploaded, published or integrated.

## Stop state

Decision **B** permits consideration of a localized second surface iteration, not automatic full-body construction. Priorities: A cowl-foot/arch-return flow; B aperture retention and D/glass corner flow; C upper-lamp bridge and lower-corner return. This run stops for review.

**Full body: NOT GENERATED. Deep detailing: NOT STARTED. GLB: NOT EXPORTED. Website: UNCHANGED. Hero: UNCHANGED. Navigation: UNCHANGED. TOLI AI: UNCHANGED. Controlled capture: PRESERVED. Protected projects: UNCHANGED. Cost: ₹0 / $0. Deployment: NOT PERFORMED. Git commit: NOT PERFORMED.**

Website build/browser checks were not run because website files were untouched. Visual/reflection issues and uncalibrated depth remain material limitations; the prototype is not approved for website integration.
