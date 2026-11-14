# C — V05 REGRESSED

Date: 2026-11-09. Project: `/home/thunder/shared/tolimotors-main1/toli-static-website`.

**V04 remains active in Sections 03 and 05. V05 was not activated. Geometry work stopped after the close-up review exposed regressions.** V05 is preserved separately as **MU-X CODED PRODUCTION V05 — DEVELOPMENT CANDIDATE**.

The initial wide-view assessment suggested some improvements. The subsequent closeups changed the decision to C: the new rear-bumper valance intersects the body, leaving visible white cutout artifacts across the black surface, and the lamp's side/rear continuation is discontinuous. These fail the explicit “no major new surface defects” gate. Passing tests and producing renders did not override that result.

## References inspected before modeling

Authoritative directory: `/home/thunder/shared/tolimotors-main1/Isuzu MU-X`.

The original silver same-generation studio references were reopened and inspected before changes:

- `Screenshot From 2026-11-06 18-17-10.png` — front, bonnet, grille, lamps and front bumper.
- `Screenshot From 2026-11-06 18-17-14.png` — side proportions, windows, D-pillar, mirrors, doors and handles.
- `Screenshot From 2026-11-06 18-17-27.png` — front three-quarter and bonnet/fender relationships.
- `Screenshot From 2026-11-06 18-17-31.png` — rear quarter, lamp wrap, tailgate and bumper.
- `Screenshot From 2026-11-06 18-17-18.png` — rear glass, tailgate, lamp and bumper arrangement.

No later-generation grille, greenhouse or rear-light design was mixed into the candidate. Inter-view depth remains estimated; no calibrated photogrammetry or factory-CAD accuracy is claimed.

## V04 → reference error map

This map was saved before authoring V05 at `tools/3d/isuzu-mux/production-v05/v04-reference-error-map.json`.

| Region | V04 result | Principal error |
|---|---|---|
| Overall stance | NEEDS WORK | Dimensional framework exists; cabin and nose read too generic. |
| Bonnet | FAIL | Ramp/slab appearance instead of the reference crown and rolled nose. |
| Front fascia | FAIL | Missing reference chrome/fog-pocket relationships. |
| Headlights | FAIL | Undetailed dark apertures; outline/integration inaccurate. |
| Grille | FAIL | Plain slots instead of interlocking trapezoids and chrome. |
| Front fenders | FAIL | Abrupt bonnet, lamp and arch transitions. |
| Wheel arches | NEEDS WORK | Lip and panel transitions remain unnatural. |
| Windscreen | NEEDS WORK | Rake exists; cowl/corner softness remains inaccurate. |
| Greenhouse | NEEDS WORK | Window architecture and quarter-glass termination too generic. |
| Mirrors | NEEDS WORK | Housing too rounded compared with the photographs. |
| Doors | NEEDS WORK | Four definitions exist; boundary relationships approximate. |
| Handles | NEEDS WORK | Projection and placement approximate. |
| Side body | NEEDS WORK | Weak shoulder, sill and door-volume relationships. |
| Rear fenders | FAIL | Arch crown and shoulder do not flow convincingly. |
| D-pillar | FAIL | Inclination and quarter-window termination inaccurate. |
| Rear glass | NEEDS WORK | Corners and pillar relationship inaccurate. |
| Tail lamps | FAIL | No red/clear internals or convincing side continuation. |
| Tailgate | FAIL | Flat appearance and inaccurate plate-region depth. |
| Rear bumper | FAIL | Missing valance, reflector pockets and corner depth. |
| Wheels | NEEDS WORK | Correct tire size; rim/spoke/brake distinction insufficient. |

## V05 candidate changes

The website integration was not restarted. V05 has its own factory, patches, exterior-detail variant and new production-detail module under `src/components/three/mux/v05/`. It reuses the unchanged V04 reference data, general geometry helpers and wheel assembly rather than duplicating those foundations.

- Raised/revised the swept headlamp envelope and related front-fascia boundaries.
- Added modest bonnet crown and front-fender volume. Updated the fender's leading-edge anchor calculation to use its new shared fascia boundary; an endpoint-continuity test covers this change.
- Revised upper/lower grille opening proportions, adding chrome rims, lower slats and separate fog pockets.
- Added physical headlamp cover, projector ring/depth, upper light guide and lower reflector return. These remain visible with emission disabled.
- Added rear red lenses, upper clear band, reflector/light-guide structure and a tessellated side continuation.
- Added shallow tailgate surface depth, chrome brow, lower graphite valance and reflector pockets. The valance/body intersection is a **new rejected defect**, not an acceptable production finish.
- Made mirror shells less oval, reduced handle projection/length and narrowed the door-cut ribbons while retaining four definitions and four handles.
- Added economical dark cabin/underfloor forms behind tinted glass. The shapes remain visibly simplified; glazing/cabin presentation is not approved.
- Added restrained metallic/clearcoat paint and glass/lamp materials. These did not resolve or conceal the failed geometry gate.
- Preserved both physical `TOLI MOTORS` plates, tire diameter, axle positions and nominal dimensional framework.

Windscreen architecture, main side-body framework, D-pillar/quarter-glass arrangement, roof and wheels were largely retained. They were not reported as successfully reconstructed merely because other details were added.

## Visual assessment and activation gate

| Gate | Result |
|---|---|
| Front | Some detail improvement; still inaccurate as an overall fascia. |
| Front three-quarter | Lamp/fog structure is more visible, but fender/bonnet flow still needs work. |
| Headlights | Internal geometry exists; envelope and grille integration remain unapproved. |
| Fenders | Leading-edge continuity improved numerically; arch and shoulder transitions remain inaccurate. |
| Greenhouse | Underlying architecture largely unchanged; still too generic. |
| Side | Primary proportions retained; panel/arch reflection quality remains insufficient. |
| D-pillar / rear quarter | Not sufficiently improved; broad surface flow remains a primary failure. |
| Rear three-quarter | **REGRESSED**: new valance intersection and discontinuous lamp wrap. |
| Rear lamps | More internal structure, but side/rear integration fails. |
| Tailgate / rear bumper | **REGRESSED**: visible clipping/cutout artifacts and inadequate corner flow. |
| Surface quality | **FAIL**: broad normals/joins and new attached-detail intersections remain visible. |
| No major new defects | **FAIL**. |
| Section 03 | Retains active V04; V05 rejected before switching. |
| Section 05 | Retains active V04; V05 rejected before switching. |

**Decision: C — V05 REGRESSED.** No further geometry iteration was performed after this decision.

## Reference / V04 / V05 comparisons

Evidence directory: `tools/3d/isuzu-mux/production-v05/renders/`.

- `reference-v04-v05-five-view.jpg` — complete three-column comparison.
- `reference-v04-v05-front.jpg`
- `reference-v04-v05-front-right.jpg`
- `reference-v04-v05-right.jpg`
- `reference-v04-v05-rear-right.jpg`
- `reference-v04-v05-rear.jpg`
- `v04-v05-clay-five-view.jpg`
- `rejection-evidence.jpg` — closeup clearly showing the rejected rear-bumper/lamp condition.

V04 and V05 use identical diagnostic cameras, lighting, floor and canvas size. Assembly uses the same union crop for the two coded versions and uniform scaling without distortion. Reference-camera calibration was not established; these are visual comparisons, not registered overlays or silhouette-IoU measurements. Original full canvas captures remain in `renders/raw/`.

## Detail closeups

All requested features have dedicated camera captures:

`headlight-closeup.jpg`, `front-fender-closeup.jpg`, `mirror-closeup.jpg`, `doors-handles-closeup.jpg`, `greenhouse-closeup.jpg`, `D-pillar-closeup.jpg`, `rear-quarter-closeup.jpg`, `rear-light-closeup.jpg`, `rear-bumper-closeup.jpg`, `front-plate-closeup.jpg`, `rear-plate-closeup.jpg`.

The seven diagnostic modes are implemented and were exercised: final, clay, wireframe, reflection, lights off, lights on and body only. Front/rear three-quarter captures for reflection, wireframe, lights off/on and body only are in `renders/raw/`. Diagnostic console: zero warnings/errors observed (`diagnostic-console.json`).

## Geometry and performance

| Measurement | V04 | V05 |
|---|---:|---:|
| Position entries, including instances | 71,115 | 77,762 |
| Triangles | 96,194 | 105,294 |
| Mesh instances | 86 | 132 |
| Materials | 7 | 12 |
| Diagnostic draw calls, including floor | 87 | 133 |
| Invalid coordinates | 0 | 0 |
| Degenerate triangles | 0 | 0 |

V05 adds 9,100 triangles (approximately 9.5%) and 46 draw calls (approximately 53%). The additional lamp/cabin detail has a measurable cost; material/mesh consolidation would be needed before any future release consideration. No real-device FPS or GPU timings were measured. Since V05 was not activated, this cost is **not added to the website**.

Both candidates retain approximately 2.20 m overall mirror width and 1.86 m height. V05 full length including detail offsets is approximately 4.84457 m. Tire diameter remains approximately 0.764 m; minimum tire Z remains effectively zero. The diagnostic floor is common to both versions and does not provide production contact-shadow validation. The website's existing contact-shadow, DPR, low-quality, pause and reduced-motion controls remain untouched.

Statistics and deterministic hashes: `geometry-statistics.json`. V05 hash: `6912bfb42dfa39ee2e66c3f280a52dd0c62bcb41c6dbf564e66b50a96e22375f`. Position/hash counting follows the new test's visible-mesh measurement and is not compared with differently scoped historical hash algorithms.

## Technical validation

All results are from this V05 task, after the final geometry changes:

- All TypeScript configurations (app/node/qa): **PASS**, command chain exited 0.
- Lint: **PASS**, exit 0.
- Production website build: **PASS**, 25.40 seconds.
- Isolated V05 diagnostic build: **PASS**, 7.50 seconds.
- Full test suite: **54 files / 371 tests PASS**, 172.66 seconds.
- V05 tests cover scale/grounding, finite geometry, degenerate-triangle rejection, deterministic generation, geometry budget, plate text, lamp visibility with emission off and leading-edge endpoint continuity.

Both builds retain the existing greater-than-500-kB chunk advisory. Technical checks do not certify MU-X resemblance, broad surface quality or absence of all visual intersections; the new valance defect demonstrates this limitation.

Logs are preserved beside the candidate as `mux-v05-tests.log`, `mux-v05-lint.log`, `mux-v05-types.log`, `mux-v05-build.log` and `mux-v05-diagnostic-build.log`. The types log contains the separate app check; the later app/node/qa command chain also completed with exit 0.

## Website and protected elements

The current source/public baseline audit checked **369 existing files: zero changed, zero missing** (`website-protection.json`). Original V04 source hashes also match (`v04-source-hashes.json`). In particular, neither `src/lib/vehicle-scene.ts` nor `src/lib/mux-presentation.ts` was edited or switched to V05.

**Hero: UNCHANGED. Navbar: UNCHANGED. Section 02: UNCHANGED. Section 03/05 content and layout: UNCHANGED. Protected projects and reference originals: UNCHANGED.** All writes were to the requested project or temporary evidence files; no protected-project source or original reference was edited.

Fresh live browser checks at the user's current 407 × 684 viewport confirmed both target sections report `coded-mux-v04-exterior-details`, 87 draw calls and the existing fitted camera. Screenshots: `renders/raw/live-section03-still-v04.jpg` and `live-section05-still-v04.jpg`.

TOLI AI opened, accepted input and returned the expected local service-category response. A hit test confirmed its dialog was above the canvas; closing worked. Evidence: `ai-protection.json` and `live-ai-unchanged.jpg`. No live website errors were observed (`site-errors.json`).

## Responsive result

**Post-activation V05 checks: NOT RUN — activation was rejected.** V05 was not substituted into the actual site at any viewport. It would be misleading to claim a V05 seven-size responsive PASS. The unchanged active V04 camera/routing tests remain part of the freshly passing full suite, but this is not new physical-device validation.

## Exact new files

No existing production source or V04 diagnostic file was changed.

New source:

- `src/components/three/mux/v05/MuxVehicle.ts`
- `src/components/three/mux/v05/MuxReferencePatches.ts`
- `src/components/three/mux/v05/MuxExteriorDetails.ts`
- `src/components/three/mux/v05/MuxProductionDetails.ts`
- `src/components/three/mux/v05/validation.ts`
- `src/test/mux-v05.test.ts`

New diagnostic/evidence folder: `tools/3d/isuzu-mux/production-v05/` (HTML, standalone Vite config, error map, source hashes, protection audit, statistics, decision, logs, build output and renders). Report: this file.

Isolated review URL: `http://127.0.0.1:8190/Toli-2/tools/3d/isuzu-mux/production-v05/index.html`.

**Deployment: NOT PERFORMED. Git commit: NOT PERFORMED. Active website vehicle: V04.**
