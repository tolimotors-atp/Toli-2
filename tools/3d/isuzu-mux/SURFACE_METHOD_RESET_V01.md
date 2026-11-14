# MU-X greenhouse surface-method reset — G1 decision

**LOW-CONTROL AUTOMOTIVE SURFACE PATCHES**

**G1 = FAIL. OVERALL GREENHOUSE SURFACE GATE = FAIL.**

**MANUAL REFERENCE-CONSTRAINED RECONSTRUCTION HAS REACHED ITS RELIABLE LIMIT.**

This is the stopping decision for the current mixed screenshot library and attempted manual workflow. It is not a mathematical proof that NURBS, manual modeling, or MU-X reconstruction is impossible. No later construction is authorized by this failed method test.

## Source and preserved work
New editable candidate: `source/reconstruction/isuzu-mux-greenhouse-surface-v01.blend`.

V01/V02, previous bodies, calibration rigs, reports and diagnostics remain untouched. Loaded V02 only to retain the eight stance proxy meshes and three stance curves. All other scene objects were removed from the new scene. No V02 greenhouse polygon coordinates were read, duplicated, shrinkwrapped, deformed, smoothed or retopologized. New construction contains exactly one NURBS surface and no new mesh geometry.

Stance mesh coordinates and transforms were compared exactly after reopening. Ground/axle/centerline curves retained; no wheelbase, wheel center, ground or basic ride-height edits. Physical metre scale remains unverified.

## Narrow reference priority
- PRIMARY: O06 closed straight-front windscreen.
- SECONDARY: O07 closed side, for rake and cowl/header relationship; partly occluded and not an orthographic drawing.
- VALIDATION: O11 front-left three-quarter.
- Opposite front-right render is also inspected. O10 is shown as contextual comparison only, not an extra equally weighted fitting target.

No incompatible body-family images are used. Paint ignored. Canonical family unchanged. No new calibration or shared-camera solution claimed. No extra images requested or downloaded.

## G1 method and bounded test
Blender 5.2.2 LTS, `/usr/bin/blender`. A new 4×4 clamped bicubic NURBS surface, order 4 in U and V, unit weights, non-cyclic, symmetric about the centerline. Four meaningful rows control base/lower bow/upper bow/header; four columns control edges and transverse bow. The control cage remains a native `SURFACE`, not converted to a polygon mesh. No subdivision modifier, dense vertex correction, rounded-corner fan mesh or A-pillar hiding geometry.

The initial candidate is preserved as `source/reconstruction/surface-v01/initial-g1-4x4.blend`. One bounded control-row correction was made after front/side inspection, without adding controls or moving the diagnostic cameras:

|Parameter|Initial|Final|
|---|---:|---:|
|Base edge Z|0.424|0.438|
|Header edge Z|0.587|0.593|
|Header half-width|0.238|0.230|
|Base half-width|0.269|0.269|
|Control points|16|16|

Coordinates use wheelbase=1, not metres. Transverse bow uses edge/interior handle displacement; vertical bow uses the two middle rows. Initial controls/results and final controls/results are saved separately for review. There is no open-ended sequence of correction versions.

## Visual evidence and G1 decision
The corrected front outline is closer and broad curvature is smooth. The simple patch avoids V02's dense local waviness; these are positive results of the method reset.

Nevertheless, the four-sided perimeter is still too rectilinear around the corners and lower boundary compared with the glass reference. Side rake looks broadly plausible but does not establish the correct cowl/header endpoints and transverse corner falloff together. The front-3Q comparison still does not convincingly reproduce the reference perimeter/foreshortening. The opposite view is symmetric and clean, but symmetry alone is not likeness evidence.

Front and side orange overlays show the **actual evaluated NURBS boundary**. Their 2D similarity aligns approximate stance contacts; it does not solve focal length, pose or perspective. Camera/annotation uncertainty means these overlays are qualitative fault-finding evidence, not a calibrated pixel-RMS test or proof of incompatible photographs. Reference/model crops are independently contained without anisotropic stretching. No bounding-box crop is claimed as metric alignment.

The single-surface strip-reflection image tests broad windscreen curvature only. It does **not** claim G6 or windscreen/header/roof continuity: those surfaces were never constructed. Opaque neutral material, CPU Cycles 24 samples, broad white emitters hidden from the camera; not production glass or cinematic finishing.

G1 requires simultaneous convincing front/side/3Q agreement, not merely smooth tessellation or a close-looking front overlay. That standard was not met. No roof, A-pillar guides, side contours, quarter glass, rear glass or further mesh is constructed.

## Sequential gates
|Gate|Result|
|---|---|
|G1 Windscreen|**FAIL**|
|G2 Roof|NOT REACHED|
|G3 Side contour|NOT REACHED|
|G4 C/D pillars + quarter glass|NOT REACHED|
|G5 Three-dimensional cabin identity|NOT REACHED|
|G6 Reflection continuity|NOT REACHED|

**MANUAL RECONSTRUCTION LIMIT REACHED = YES**, scoped to the present evidence/workflow. Stop the entire manual reconstruction. Practical next inputs are controlled same-vehicle photographs suitable for reconstruction or accurate licensed MU-X base geometry. No acquisition, download or licensing claim made.

## Geometry — windscreen only
Control points: **16** (4×4).

Evaluated vertices: **2304**.

Evaluated triangles: **4418**.

Evaluated counts are Blender's temporary render tessellation, not base control density or exported production geometry. Stance meshes, curves, cameras and packed references are excluded. No GLB exists.

## Diagnostics actually generated
Required reached-gate sheet: `renders/surface-windscreen-v01.jpg`.

Supporting G1 outputs:
- `renders/g1-windscreen-close-front-left-surface-v01.png`
- `renders/g1-windscreen-close-front-right-surface-v01.png`
- `renders/g1-windscreen-close-front-surface-v01.png`
- `renders/g1-windscreen-close-side-surface-v01.png`
- `renders/g1-windscreen-curvature-surface-v01.png`
- `renders/g1-windscreen-front-left-surface-v01.png`
- `renders/g1-windscreen-front-overlay-surface-v01.jpg`
- `renders/g1-windscreen-front-right-surface-v01.png`
- `renders/g1-windscreen-front-surface-v01.png`
- `renders/g1-windscreen-side-overlay-surface-v01.jpg`
- `renders/g1-windscreen-side-surface-v01.png`

Initial G1 evidence is retained under `renders/g1-initial/`. No G2–G6 diagnostic filenames were created. Scripts, control arrays, camera projections, exact stance signatures, gate decision and reopen checks are in `source/reconstruction/surface-v01/`.

## Validation and protection
Editable source saved and reopened; exactly one native surface with 16 finite control points; exactly eight unchanged stance meshes; no other new mesh. Source scripts compile. Blender reports environment audio/cache and API-deprecation warnings; successful file/reopen checks do not imply a visual PASS.

Pre/post SHA256 verification covers all pre-existing MU-X research files, website src/public/config, and protected-project source/config. Full dependency trees and every protected binary asset are outside this coverage. No pre-existing report is overwritten; this is a new report.

Website unchanged; both protected projects unchanged within stated checks and no writes performed there. No body/detail work. No production GLB, integration, Git commit or deployment. Website build, TypeScript, lint, browser and device tests not repeated because no website source/public assets changed.
