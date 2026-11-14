# Inside TOLI removal and MU-X asset audit

## Result
Inside TOLI removed: YES. Static project only. No deployment or commit. No writes to the independent 3D website or original project.

The Gallery now follows SectionStack immediately. There is no replacement wrapper or section spacer. Browser DOM measurement found zero gap between the stack and Gallery. Removed workshop-specific JSX, CSS, runtime, debug UI, near-section observer/prewarming, renderer-lending branch, isolated workshop preview, both exclusive workshop model copies and six obsolete test files. Shared vehicle renderer, contact, gallery and booking remain.

## Navigation
Six intended numbered destinations remain: 01 Entry (hero), 02 Services, 03 Journey (process), 04 Toli Motors (trust), 05 Request (booking), 06 Contact (connect). Inside TOLI was never in this registry, so no renumbering was warranted. All six destinations exist. The dynamic registry, active tracking, popover, focus/hover styling and Titanium Bronze rail are unchanged. Gallery remains available through the menu and footer.

## ISUZU MU-X
**ISUZU MU-X INTEGRATION = BLOCKED — GENUINE/PROPERLY LICENSED 3D ASSET REQUIRED**

No genuine existing asset found. Source: unavailable. Audited model files and vehicle registry. Remaining models are public/models/toli-sportback/toli-atelier-sportback.glb and public/models/vehicles/toli-preproduction-sedan.glb. Neither is an MU-X. Active registry points to the original preproduction sedan (4,268,888 bytes, registry audit 192,105 triangles, 58 meshes, 12 materials, no textures). Its metadata is not an MU-X specification.

Supply an authentic, licensed GLB preferably at `public/models/vehicles/isuzu-mu-x.glb`, with associated license/provenance documentation. No downloads, fabricated badges, relabeling or purchases performed. MU-X format, file size, triangles and textures: unavailable. Camera, grounding, materials and responsive MU-X integration: not performed until a valid asset exists. Existing dedicated vehicle unchanged apart from removing the workshop-only renderer-lending code.

## Protection and validation
Hero artwork, cars, logo, grounding and typography untouched. The only change in mobile-responsive.css removes three obsolete facility rules; other rules preserved. Navbar and bronze chapter styles untouched. Historical docs and this regression test intentionally mention the removed section; no live section references remain.

- Production build: PASS (existing Tailwind ambiguity and large chunk warnings remain).
- TypeScript: PASS (app, node and QA projects).
- Lint: PASS.
- Tests: PASS — 50 files, 358 tests. Includes new absence/adjacency, valid navigation and retained-asset hash assertions. Obsolete section tests removed; protected fixture excludes deliberately removed assets and updates authorized shared-file hashes.
- Browser: ten sizes in both themes: 360×640, 390×844, 430×932, 600×960, 720×1024, 768×1024, 1024×768, 1366×768, 1440×900, 1920×1080. No horizontal overflow; removed section absent; all six dark-theme destinations checked; zero transition gap. Chapter click/scroll updated active state to 04 Toli Motors. Theme switching worked. Console warnings/errors: none in inspected production tab.
- No new performance audit or physical-device testing. Existing performance concern from prior report remains unresolved. MU-X-specific tests cannot run without its asset.

## Files
Modified:
- `src/pages/Index.tsx`
- `src/components/journey/JourneyProvider.tsx`
- `src/lib/vehicle-scene.ts`
- `src/mobile-responsive.css`
- `src/workshop-surfaces.css`
- `src/test/fixtures/separation-protected.json`
- `src/test/inside-removal.test.ts` (added)

Removed:
- `src/components/workshop/Facility.tsx`
- `src/components/workshop/facility.css`
- `src/lib/workshop/preview.ts`
- `src/lib/workshop/debug.ts`
- `src/lib/workshop/drag.ts`
- `src/lib/workshop/readiness.ts`
- `src/lib/workshop/production.ts`
- `src/lib/workshop/lifecycle.ts`
- `src/lib/workshop/asset.ts`
- `src/lib/workshop/scene.ts`
- `src/test/workshop-visibility.test.ts`
- `src/test/workshop.test.ts`
- `src/test/workshop-preview.test.ts`
- `src/test/workshop-drag.test.ts`
- `src/test/workshop-production.test.tsx`
- `src/test/workshop-touch.test.ts`
- `tools/3d/toli-workshop/exports/toli-workshop-web-v2.glb`
- `tools/3d/workshop-preview.html`
- `public/models/toli-workshop-web-v2.glb`

## Acceptance
| Criterion | Status |
|---|---|
| Inside TOLI removed | PASS |
| No empty section gap | PASS |
| Navigation mapping valid | PASS — six existing destinations retained |
| Number indicators updated | PASS — existing count already correct |
| Titanium Bronze preserved | PASS |
| Genuine MU-X verified | BLOCKED |
| MU-X integrated | BLOCKED |
| MU-X grounded | BLOCKED |
| MU-X responsive | BLOCKED |
| MU-X 3D performance acceptable | BLOCKED |
| Hero preserved | PASS |
| Local files updated | PASS |
| Protected projects unchanged | PASS — no writes |
| Deployment | NOT PERFORMED |

Preview: http://127.0.0.1:8200/Toli-2/
Responsive evidence: [JSON](inside-removal-evidence/responsive.json).
