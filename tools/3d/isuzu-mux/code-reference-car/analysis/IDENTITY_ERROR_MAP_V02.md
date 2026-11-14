# MU-X coded identity V02 — error map BEFORE geometry changes

2026-11-09. Compared the five-view Section 03/05 coded candidate against the full-resolution supplied front, front-left 3/4, side, rear-left 3/4 and rear images. Current body: 55,391 vertex instances / 85,740 triangles, failed badgeless recognition. This is a correction to that architecture, not a new generator.

Reference locks (all in `/home/thunder/shared/tolimotors-main1/Isuzu MU-X`):
- FRONT_REFERENCE: `Screenshot From 2026-11-06 18-17-10.png`
- FRONT_34_REFERENCE / BONNET_REFERENCE: `Screenshot From 2026-11-06 18-17-27.png`
- SIDE_REFERENCE / GREENHOUSE_REFERENCE: `Screenshot From 2026-11-06 18-17-14.png`
- REAR_34_REFERENCE / REAR_QUARTER_REFERENCE: `Screenshot From 2026-11-06 18-17-31.png`
- REAR_REFERENCE: `Screenshot From 2026-11-06 18-17-18.png`
- FRONT_FENDER_REFERENCE: `Screenshot 2026-11-08 213436.png` (compatible red intermediate, secondary to silver trim)

| Region | Reference characteristic | Current coded characteristic / difference | Responsible code/data | Controlled correction |
|---|---|---|---|---|
| Overall mass | Tall glazed cabin, moderate bonnet, four wheels embedded in full arches | Too much painted side height and shallow glass; reads as a long utility van | Cabin belt z~1.25, window bases 1.285/1.36; cowl x=-.83; body stations upper bands | Move cowl forward ~.17 m; lower door/window belt independently, keep dimension/wheel anchors fixed |
| Front 3/4 | Bonnet, fender and A-root form one continuous volume | Hood and fender end on different front curves; fin-like leading corner | `bonnet`, `fenderTop`, `fasciaPoint`; unmatched leading X/Z | Make bonnet/fender share the actual fascia top boundary, with local front-roll/Coons correction; no global scale |
| Bonnet | Longitudinal rise with restrained transverse crown and outboard falloff | Broad high central slab with inconsistent rolled nose | `bonnetCentre`, `bonnetSide`, exponent 2.4 and unshared front edge | Shorten rear extent with cowl move, use controlled crown/falloff; pin leading edge to nose |
| Front fenders | Distinct full arch crown blending into bonnet and door | Narrow top strip/crease, flat door-side transition | `fenderCrown`, station widths near front axle, `fenderTop` | Local upper-fender crown and max-width band changes only; preserve circular wheel anchor |
| Cowl/A-root | Inclined A-pillar rooted behind front axle, broad low cowl | Cabin starts too far rearward and sits separately from hood | `cabinOutline`, `windscreen`, bonnet rear endpoints | Share rear bonnet/cowl/windscreen boundary and move related points together |
| Windscreen | Broad rounded trapezoid; clear side/front agreement | Overly planar narrow dark trapezoid, wrong lower/root relation | `screen`, windscreen control points | Reposition lower corners with cowl; retain curvature without camera adjustment |
| Greenhouse | Taller side glazing; upper line follows gently crowned roof | Window band too shallow and almost rectangular | `greenhouseY`, roof-side / cabin outline / window bases | Lower bases and refine tapered upper trajectory together |
| Front window/B-pillar | Front glass tapers into A-pillar, tall and slightly rising belt | Flat-bottom simple quadrilateral | `frontWindow`, cabin shape rounding | Reference-traced polygon proportions with independent lower/upper vertices |
| Rear window | Lower line rises gently rearward and rounded descending rear corner | Squared block with wrong lower-rear corner | `rearWindow` control list | Lower base and reshape last quarter of outline; no added trim |
| Quarter glass/D-pillar | Rounded trapezoid of appreciable height, modest painted surround | Small shallow glass and generic surrounding mass | `quarterWindow`, `cabinOutline`, rear screen and roof edge | Enlarge glass vertically; coordinate D-pillar/roof/rear-screen boundaries; do not independently stretch one view |
| Side body | Shallow door crown/low concavity; controlled shoulder | Featureless flat slab with some remaining joins | `section`, widths by absolute height, belt stations | Retain interpolation improvement; refine width bands locally, not entire-station scaling |
| Rear quarter | Full rear arch shoulder tapering progressively into hatch | Side-to-hatch volume too narrow/flat at top and generic taper | Rear station bands, `rearShoulder`, terminal blend | Separate rear-fender and rear-corner influences; maintain shared end boundary |
| Rear 3/4 | Wide rear glass, short D border and rounded bumper corners | Rear glass/hatch appear as separate planar panels | `rearGlass`, `rearProfile`, `fascia(true)` | Reconcile common top/bottom boundaries, broaden upper hatch and refine depth hierarchy |
| Rear face | Glass, lamp level, recessed hatch and projecting bumper have distinct blended depths | Tall smooth tailgate with broad uncharacteristic blank plane | `fasciaSections.rear`, recess function, `tailLamp` envelope | Control upper hatch/recess/lower bumper depth independently; no badge/trim camouflage |
| Bumper wrap | Continuous side-to-rear corner; soft lower undercut | Joined positions but wrong corner shape/tangents | Terminal `section` blend / `fasciaPoint` corner exponent | Same corner influence for both surfaces, with local undercut reconciliation |
| Reflection flow | Broad continuous highlights | Reduced waves but seam/pinching remains | Independent patch normals/edges, width-band changes | Final pass only: remove accidental control kinks; no extra subdivision to hide identity errors |

## Fixed evaluation and iteration plan

Use the unchanged 34° FOV and existing nine camera directions. Primary five comparisons use front, the front-quarter facing the source, side, rear-quarter facing the source and rear. Geometry is identical in every camera. No per-camera deformation, FOV adjustment, yaw tuning or pixel warp is permitted. Overlay preparation is only a documented uniform scale/translation; perspective mismatch remains visible.

1. Overall mass + bonnet/fender/front-quarter boundary correction.
2. Greenhouse, window polygons and D-pillar.
3. Rear-quarter volume and rear-quarter/hatch relationship.
4. Front/rear face reconciliation with all other views checked.
5. Local surface-flow cleanup and best-candidate selection.

After each pass: same five camera renders, geometry stats, source/data snapshot and BETTER/SIMILAR/WORSE ledger. Keep previous sources and captures. No badges, interior, engine, sensors, handles or fine lamp/grille work. Current website 03/05 cars, Hero and navigation remain active and unchanged until all mandatory identity gates pass.

Manual image traces/landmarks are approximate visual measurements, not calibrated 3D constraints. They will be saved with original image dimensions and alignment transforms; no numerical overlap score will be presented as proof of same-car identity.
