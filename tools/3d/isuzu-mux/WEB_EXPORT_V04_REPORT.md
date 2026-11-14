# ISUZU MU-X — V04 local website integration

Status: **SUCCESS — V04 PREVIEW / TEMPORARY PRODUCTION ASSET**. Date: 2026-11-07.

This is the existing reference-generated V04 candidate, not final geometry, factory CAD or a manufacturer-supplied asset. Its side/rear identity and surface limitations remain. Replace it after a better controlled-photo reconstruction; no website redesign is needed.

## Source and export

- Original, unchanged: `tools/3d/isuzu-mux/source/production/isuzu-mux-generated-v04.blend`.
- Export preparation copy: `tools/3d/isuzu-mux/source/production/export/isuzu-mux-web-v04.blend`.
- Web asset: `public/models/vehicles/isuzu-mux/isuzu-mux-web.glb`.
- Blender 5.2.2 LTS, `/usr/bin/blender`; original reopened successfully. All **113 retained components** were found before export. No V05 or new modeling.

The export selects 43 V04 exterior objects plus the 113 retained components and their genuine parent hierarchy. Existing modifier results are baked in the export copy **before** deleting diagnostic dependencies. An initial export exposed why this is necessary: deleting Boolean cutters first filled body openings. That rejected export was replaced; it is not the website asset. Exported content excludes guides, cutters, floor, cameras and Blender lights. No destructive optimization touched the original. Roughly 34k triangles and no textures made decimation unnecessary.

Original units and proportions are preserved. Blender Z-up converts through glTF to Three.js Y-up. The viewer rotates yaw by π to place the V04 front along its established +X presentation, centers the body, normalizes to 4.825 m length and grounds it using four actual wheel bounds. This is V04's scale, not a new claim of measured factory accuracy.

## Final GLB audit

| Item | Result |
|---|---:|
| File bytes | **1,056,516** (1.06 MB decimal / 1.01 MiB) |
| glTF triangles | **34,010** |
| Vertices after clean Blender import | **28,623** |
| Materials | **10** |
| Scene objects/nodes | **161** |
| Mesh objects | **156** |
| Texture count | **0** |
| Original-space length × width × height | **4.825 × 1.870 × 1.818 m** |
| Four wheel assemblies / glazing geometry | Present / present |
| Minimum tire/vehicle height | 0 m within tolerance |
| Normal coordinates | Finite |

**Reimport validation: PASS.** A clean Blender scene imported the final GLB, checked geometry, bounds, wheels, glass geometry, material presence and finite normals. Blender's importer yields 34,005 triangles, five fewer than glTF's 34,010 indexed triangles due to degenerate-face cleanup. The file audit and Three.js test use the actual glTF triangle count. Vertex growth over the authored mesh reflects export normal/material splits; it is not new body modeling.

Five clean-import views and a source comparison board were inspected: front, front three-quarter, side, rear three-quarter and rear. V04 body openings, silhouette, glazing and wheel positions survive. Neutral audit lighting differs from original render lighting, so the board is visual evidence, not a pixel-identical render test. Existing opaque graphite glazing and unfinished fascia/trim details are inherited from V04; no new transparent glass or finished mirror geometry was invented.

Evidence: `renders/web-export-v04/comparison-board.jpg`, `front.png`, `front_34.png`, `side.png`, `rear_34.png`, `rear.png`, `reimport.json`.

## Website integration

Inspection found no MU-X selector/entry in the active static site. The existing below-Hero viewer used the temporary sportback, while the registry's SUV slot was asset-required. The user explicitly chose **replace the below-Hero service vehicle with MU-X**.

- `src/lib/vehicle-model/mux.ts`: replaceable V04 asset manifest, static capability, exact inspected wheel paths under `MUX_ROOT`, scale/orientation/source/status.
- `src/lib/vehicle-model/contract.ts`: active below-fold model now MU-X; supports static-preview manifests without fabricated panel mappings.
- `src/lib/vehicle-model/static-preview.ts`: uses real exported geometry/materials, normalizes/grounds it, supplies four wheel assemblies and inert inspection commands. No doors/bonnet/tailgate are exposed or faked.
- `src/lib/vehicle-model/adapter.ts`: static-preview branch; existing articulated assets retain their old behavior and tests.
- `src/lib/vehicle-model/registry.ts`: SUV entry now **ISUZU MU-X**, preproduction; existing sedan asset and other classes remain unchanged.
- `src/components/journey/VehicleComponentView.tsx`: MU-X overview name.

Model URL uses the existing `vehicleAssetUrl` base-path helper: `/Toli-2/models/vehicles/isuzu-mux/isuzu-mux-web.glb` locally, not an absolute filesystem path or root-only `/models` URL.

The existing shared below-fold renderer, studio environment, actual-bounds camera fitting, reduced-motion behavior, near-section lazy loading, one-template-per-URL cache, resource cloning and disposal are reused. No new renderer/library or Hero loading was added. The existing generic illustration is **retained as fallback**, not used as a successful MU-X load. The original sedan GLB remains available; other assets were not overwritten. The shared scene may also use the model in its existing process/completion docks, as it already did for the sportback.

## Browser and responsive validation

Local development preview: `http://127.0.0.1:8194/Toli-2/`.
Production-build preview: **`http://127.0.0.1:8195/Toli-2/`**. Open the Vehicle / component exploration section below Hero.

Real headless Chromium with software graphics loaded the actual GLB, not a mocked scene. The request returned **HTTP 200** and the model reached ready. One model response was observed across the multi-size run: no repeated model download during resizing. The initial light desktop/mobile screenshots and dark mobile production screenshot were inspected; four wheels/body/materials and floor contact are visible. No new interaction lockups or page exceptions were observed. These checks are not a physical low-end Android benchmark or long-duration GPU memory profile.

| Viewport | Model / horizontal overflow |
|---|---|
| 320 × 568 | Ready / none |
| 360 × 800 | Ready / none |
| 390 × 844 | Ready / none |
| 412 × 915 | Ready / none |
| 768 × 1024 | Ready / none |
| 1024 × 768 | Ready / none; separately confirmed from a fresh production page |
| 1366 × 768 | Ready / none |
| 1440 × 900 | Ready / none |
| 1920 × 1080 | Ready / none |

The shared canvas can move to another active dock as sections overlap; the first resize run at 1024 recorded no canvas inside the old service dock. A fresh production-page check confirmed the correct service dock, full-car framing and no overflow (`tablet.json`, `website-1024.png`). This was a scroll-position issue in the check, not proof of a missing model.

Production follow-up: zero page exceptions and zero console errors on the successful-load page; TOLI AI answered a local services query; Book Service opened one request dialog. No form was submitted. A separate page intentionally aborted the GLB request: existing fallback activated without a page exception. `followup.json` records those results. Slow initialization retains the existing loading state; a synthetic network-throttle benchmark was not performed.

## Validation results

- **Production build: PASS.** Existing bundle-size advisory remains; no unrelated chunk restructuring.
- **TypeScript: PASS**, all three configured projects.
- **Lint: PASS.**
- **Unit tests: 51 files, 358 tests PASS.** Final log: `source/production/export/test-pass.log`. Non-failing React test warnings remain in the suite log; they are not production runtime errors.
- New actual-asset test validates final GLB triangles, scale, grounding of each wheel, material color, static panel behavior, registry and idempotent disposal.
- Intentionally updated old active-model/label tests; retained the original sedan tests by passing its manifest explicitly. Updated only the authorized VehicleComponentView hash in the static-protection fixture; all other fixture entries remain protected.

Changed tests: `src/test/isuzu-mux.test.ts` (new), `imported-vehicle.test.ts`, `preproduction-vehicle.test.ts`, `original-sportback-asset.test.ts`, `vehicle-registry.test.ts`, `phase2-services.test.tsx`, and `fixtures/separation-protected.json`.

## Preservation and local files

The preservation check covered **1,726 existing files**. Ten changed existing files are the intended integration source/tests listed above; the two new implementation files and new test are additions. No changed file was outside the target static project. The original V04, earlier milestones/audits/experiments, 113 retained parts (inside the unchanged source), controlled-capture workflow, Hero, navbar and all recorded protected-project files matched their pre-change hashes. Details: `source/production/export/preservation-result.json` and `preservation-before.json`.

All final assets, export preparation scripts/copy, validation logs, comparison renders and responsive screenshots were saved under the actual project. The original historical reports are not rewritten; their no-export status remains historical. This report records the newly authorized integration.

| Protected item | Status |
|---|---|
| Hero, navbar, Titanium Bronze, other website sections | **UNCHANGED** |
| TOLI AI | **WORKING** in production preview |
| Inside TOLI | **REMAINS REMOVED** |
| Controlled-capture workflow | **PRESERVED** |
| V04 original / previous milestones | **UNCHANGED** |
| 113 retained components | **UNCHANGED** in source |
| Separate `toli-3d-website` / `tolimotors-main` | **UNCHANGED** |
| Deployment / Git commit | **NOT PERFORMED** |

Remaining limitation: the site now displays the **unapproved V04 reference-generated MU-X preview**. Its geometry has not passed a factory-accuracy gate. Panels are static, source surface/trim limitations remain, and physical Android performance is untested. The controlled-photo workflow remains ready for a later replacement.
