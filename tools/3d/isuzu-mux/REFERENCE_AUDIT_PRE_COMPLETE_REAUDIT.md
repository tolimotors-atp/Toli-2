# MU-X reconstruction reference audit

Status: reference audit complete; modeling NOT started. No production model activated.

Canonical: silver open-door/open-bonnet/open-tailgate set (images 1–4). Closed images 6–13 are secondary, not authority for conflicting trim. No exact model year or dimensions inferred as fact. Body proportions must be established against canonical side/front/rear images before details.

| Image | Evidence |
|---|---|
| 1 | Front, bonnet and four doors open; engine bay partial |
| 2 | Left profile, doors/bonnet/tailgate open |
| 3 | Rear, tailgate and rear doors open; cargo aperture |
| 4 | Right profile, doors/bonnet/tailgate open |
| 5 | Right-hand-drive dashboard, steering, front cabin and door cards |
| 6 | Closed front |
| 7 | Closed left profile |
| 8 | Closed rear |
| 9 | Closed right profile |
| 10 | Closed front three-quarter, right side |
| 11 | Closed front three-quarter, left side |
| 12 | Closed rear three-quarter, left side |
| 13 | Closed rear three-quarter, right side |

## Supported and uncertain details
Directly supported: tall SUV roof/cabin, roof rails, side steps, four door apertures, bonnet and roof-hinged hatch opening direction, grille/light outlines, split-spoke wheels, dark interior and RHD dashboard.

Engine bay is visible only partially in image 1; battery/intake/hoses cannot be reconstructed accurately from it. Rear seating, underside, hinge hardware, hidden door surfaces and absolute dimensions lack sufficient evidence. Use simplified neutral hidden surfaces, not invented engineering. The interior panoramic view has perspective distortion and is not an orthographic blueprint. Open doors obscure portions of the primary side surfaces. Secondary closed profiles may guide compatible contours only.

## Next gate and tooling requirement
Blender executable was not found on PATH, in /opt or the checked /tmp runtime location. A Blender runtime is required for editable .blend source and comparison renders. No external software/model was downloaded. No .blend, candidate mesh, GLB or render exists yet. Do not interpret this audit as completion or a passed silhouette gate.

Next: set up canonical front/side/rear reference planes, author a clean body cage, then render front, profiles, rear and both three-quarter views for the silhouette gate. Only after that gate passes should fascia, opening parts and cabin be detailed. Keep existing production sedan unchanged until all model quality gates pass.

Target source: tools/3d/isuzu-mux/source/isuzu-mux-master.blend
Target web model: public/models/vehicles/isuzu-mux/isuzu-mux-web.glb
Target comparisons: tools/3d/isuzu-mux/renders/

## Protection
Only this audit and inventory were saved. Website source, Hero, bronze styling, removed Inside TOLI state, original project and independent 3D project unchanged. No deployment. Build/TS/lint/browser checks not repeated because no executable website source changed. No model statistics, performance or functional-part results available.
