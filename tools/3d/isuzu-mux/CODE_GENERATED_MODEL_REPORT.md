# TOLI MU-X Generator — coded milestone 1

2026-11-07. **Milestone 1: NEEDS WORK. Milestones 2–4: NOT REACHED. Website NOT UPDATED.**

The newer add-on brief supersedes manual image-redesign modeling. This pass creates a new procedural source; it neither deforms V04 nor loads its vertices into the generator. The older brief's image-driven constraints remain relevant, but a separate manual redesign master was not created. No reconstruction algorithm was rerun.

## Delivered

Add-on: `tools/blender-addons/toli_mux_generator/`, name **TOLI MU-X Generator**, View3D sidebar **TOLI MU-X**. Files: `__init__.py`, `parameters.py`, `reference_data.py`, `operators.py`, `panels.py`, `geometry/__init__.py`, `validation.py`, `run_milestone.py`, `README.md`, `check_milestone.py`.

Architecture: central property defaults and UI; reference/station data; shared quad loft and wheel generation; Blender operators; validation. Eight implementation modules plus two headless checks/docs. Geometry remains one compact module for Milestone 1 rather than empty front/rear/interior placeholders. Those later systems are not implemented. The full finished-vehicle add-on is **not complete**.

Generate/Regenerate/Reset: implemented and exercised. Generated collection is replaced predictably without retaining duplicate vehicles. Reset restores parameters; regeneration is explicit. Preview: lower wheel tessellation and bevel segments. Quality: higher wheel tessellation/bevel, tested at 3,664 triangles versus 1,944 preview. It does not make the shape approved. Export is explicitly blocked while the silhouette gate fails.

## References / parameters

18 originals remain unchanged in the authoritative `Isuzu MU-X` folder; their existing inventory/audit was reused, not repeated as a photogrammetry experiment. All are indexed in the reference atlas. Primary closed-body screenshot times: front **18-17-10**, front three-quarter **18-17-27**, side **18-17-14**, rear three-quarter **18-17-35**, rear **18-17-18**; all dated 2026-11-06. Open-panel/interior/engine images are not used to define the closed-body cage. No incompatible newer-generation references or downloaded geometry were used.

`reference_data.py` records approximate hand-read screenshot landmarks and ratios with exact source filenames. Example: side axle separation 489 px / visible length 782 px; frontal roof width 248 px / body width 331 px. These are **IMAGE-DERIVED visual constraints with perspective**, not calibrated measurements. Stations, heights, curvature and taper are **VISUAL APPROXIMATIONS**. Length 4.825 m, width/height 1.860 m, wheelbase 2.845 m and tire diameter .764 m are **user-supplied family-scale guidance**, not newly verified OFFICIAL DIMENSION claims. The photographic wheelbase ratio differs from the physical guidance; it is not blindly imposed as metric geometry.

Photographs inform bonnet-to-cowl placement, narrow upper cabin, wheel/body relationships and rear taper. They have **not yet yielded a satisfactory coded exterior**. The front/side/rear section definitions are only coarse controls; no claim that every reference ratio has been solved. There are no solved photographic camera poses, image-plane alignment, calibrated overlays or quantified silhouette fit. Fixed orthographic cameras are stable review views only. No embedded image binaries.

## Geometry and tests

Coordinate convention X length (front negative), Y width, Z up, ground Z=0. Axles ±wheelbase/2; tire centers at radius above ground. Body uses symmetric half-width stations connected as quads, outward face recalculation, real axle-derived Boolean arch cuts and restrained bevel. Greenhouse is a separate closed review volume, not finished windows. Wheels are cylinders with tire/rim layers; proper spokes/hubs are deferred. No existing 113 components were reused.

Saved output: `source/production/isuzu-mux-code-generated-v01.blend`. Reopened in Blender 5.2.2 LTS at `/usr/bin/blender`. The code remains source of truth; the blend contains no manual vertex fixes.

Actual preview: **992 evaluated vertices; 1,944 triangles; 10 objects; 4 materials**. Dimensions **4.825 × 1.860 × 1.860 m**, wheelbase **2.845 m**. Ground minimum approximately −5.25e−9 m (floating-point zero).

- Delete generated geometry + regenerate fingerprint: **PASS**, identical baseline geometry.
- Reset and Quality mode checks: **PASS**. Saved scene reopen: **PASS**.
- Finite vertex coordinates: PASS.
- Non-manifold edges: **0**, per evaluated closed object.
- Degenerate faces: **0**.
- Negative signed-volume objects: **0**; outward winding check, not exhaustive local normal/intersection verification.
- Symmetry: **NEEDS WORK**. Largest reflected-nearest-vertex discrepancy **0.001610 m**, failing the strict .0001 m tolerance. Boolean/bevel results need investigation; mathematical station symmetry alone is not sufficient.
- Assembly continuity: **NEEDS WORK**. Body and greenhouse are separate closed blockout volumes; a watertight, tangent-continuous assembled exterior is not established. Separate tires/rims are intentional, not a connectivity PASS for the exterior.
- Duplicate-vertex/seam classification and exhaustive inverted-face/intersection testing: not completed. No production topology approval.

Full machine-readable results: `code-generator/renders/validation.json`. Parameters outside defaults are not guaranteed to produce valid geometry across every combination; the generator is experimental.

## Mandatory visual gate — reviewed and failed

`code-generator/renders/code-vs-v04.jpg`: reference | V04 | coded M1, for front, front three-quarter, side, rear three-quarter and rear. `reference-atlas.jpg` indexes the 18 originals. Individual five-view renders are saved alongside them. Different framing and lighting mean these are qualitative comparisons, not pixel-error measurements.

**All five silhouette gates: NEEDS WORK.** The new body is too rectangular; shoulder/lower-body volume lacks character; windscreen/roof transitions are crude; the single greenhouse block lacks MU-X quarter-glass/D-pillar relationships. Wheel hard points meet dimensional guidance, but their body integration and arch shoulders are not yet convincing. Frontal detail is intentionally absent, yet even the macro silhouette is insufficient. Rear taper and massing remain generic.

Against V04: overall **WORSE**; front **WORSE**; greenhouse **WORSE**; fenders **WORSE**; side **WORSE**; rear cabin **WORSE**; rear **WORSE**. This compares an early blockout against a more developed candidate; it is still enough to reject website replacement. Badgeless recognition: **NEEDS WORK**. No badges, paint tricks or extra detail were used to conceal the failure.

**C — REDESIGN FAILED TO IMPROVE THE VEHICLE; WEBSITE ASSET NOT REPLACED.**

Stop before Milestone 2 fender/shoulder sculpting and all Milestone 3 identity details. The next permitted shape pass must change section/profile code: curved lower-body cross-sections, a controlled shoulder, a genuinely raked/crowned greenhouse and reference-specific rear-cabin boundaries. It must also resolve the measured symmetry discrepancy. No manual Blender fixes, panel work, interior/engine work or web export should precede the macro gate. This pass establishes a reusable experimental generator, not an accurate MU-X.

## Preservation

V04, its 113 retained components, previous milestones/audits, local reconstruction outputs, current V04 website GLB and controlled-capture workspace remain unchanged. Hero/navbar/TOLI AI/application sources were not edited. Protected projects were not modified. Website suites were not rerun because there was no website integration. Add-on checks and Blender renders were run instead.

GLB: **NOT EXPORTED**. Website MU-X: **NOT UPDATED** (V04 stays active). External paid assets: **NONE**. Cloud/API: **NONE**. Cost **₹0 / $0**. Deployment and Git commit: **NOT PERFORMED**.
