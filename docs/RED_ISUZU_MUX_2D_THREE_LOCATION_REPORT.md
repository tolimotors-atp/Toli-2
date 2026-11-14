# Red Isuzu MU-X: supplied image in all three locations

Date: 2026-11-10  
Project: `/home/thunder/shared/tolimotors-main1/toli-static-website`  
Development preview: <http://127.0.0.1:8190/Toli-2/>

## Result

| Requirement | Result |
| --- | --- |
| Section 03 — HowItWorks | PASS: supplied red MU-X front three-quarter image |
| Explore Vehicle Components | PASS: same supplied image |
| Section 05 — CtaBanner | PASS: same supplied image |
| Shared production image | YES, one master with two responsive WebP sizes |
| Real alpha transparency | PASS |
| Old 3D presentation active in these slots | NO |
| 360° / DRAG TO ROTATE | ABSENT |
| Hero | UNCHANGED |
| Navbar | UNCHANGED |
| TOLI AI desktop/mobile | PASS |
| Responsive checks | PASS, 42 current cases |
| TypeScript / lint / build | PASS |
| Tests | 55 files / 373 tests PASS |
| Commit | NOT CREATED: target is not a Git checkout |
| Branch | UNAVAILABLE: no repository metadata |
| GitHub push | BLOCKED / NOT PERFORMED |
| Deployment | NOT PERFORMED |

## Source and render paths, verified before editing

Supplied image:

`/home/thunder/Downloads/Glossy Red Isuzu MU-X Studio Shot.png`

1536 × 1024 PNG. SHA-256:

`fc6520b1c31e5a35be0cd125af899d90d5d8857626a0dc1dae13f3bc304693b3`

An unchanged copy was saved first as:

`src/assets/vehicles/isuzu-mux/isuzu-mux-red-front-3q.png`

Its hash matches the supplied file. No different car was generated, downloaded or substituted. The vehicle's RGB detail, orientation, metallic red finish, ISUZU grille and MU-X display plate are from that file.

The exact paths were searched and recorded in [source.json](red-mux/source.json) before implementation:

1. `Index → HowItWorks → JourneyDock(process) → MuxPhotography`
2. `Index → ComponentExperience → VehicleComponentView → JourneyDock(services) → MuxPhotography`
3. `Index → CtaBanner → JourneyDock(completion) → MuxPhotography`

The heading “Explore vehicle components.” originates in ComponentExperience, while “ISUZU MU-X / OVERVIEW” and the component buttons originate in VehicleComponentView. All three paths already shared the same image component; this task changes that component to use the newly supplied source.

Production-route searches found no additional non-Hero/non-navbar active 3D car. Historical VehicleStudio/model/validation sources remain on disk and are not rendered by Index. No unrelated decorative effects or separate showroom project were modified.

## Transparency and production assets

The supplied PNG includes a dark studio glow and nonuniform alpha. A manually traced silhouette mask removes the surrounding studio/floor/glow. Foreground alpha is normalized before masking so the retained car, glass and tires remain opaque. The original RGB pixels are retained through masking; only proportional resizing and WebP encoding follow. No image-generation system was asked to create or redraw the car.

The roof contour was refined during inspection. The resulting cutout was checked on light and dark backgrounds for complete rails, both visible mirrors, glazing, lamps, bumpers, side step and tires. It has no opaque black/white/grey rectangle, no background floor, and no holes in the glazing/body. Bright reflections on chrome/rails remain part of the supplied artwork.

Generator: `tools/images/prepare_red_mux.mjs`  
Authored mask: `tools/images/mux-masks/red-front.svg`  
Alpha PNG master: `docs/red-mux/isuzu-mux-red-cutout-master.png`

Run `node tools/images/prepare_red_mux.mjs` from the project root to reproduce the assets from the project-local source PNG. The Downloads original is not modified or required at runtime.

| Imported production asset | Dimensions | Bytes |
| --- | --- | ---: |
| `src/assets/vehicles/isuzu-mux/isuzu-mux-red-front-3q-640.webp` | 640 × 384 | 51,552 |
| `src/assets/vehicles/isuzu-mux/isuzu-mux-red-front-3q.webp` | 1100 × 660 | 111,232 |

The component uses `srcset`/`sizes`; these are responsive variants of one shared master, not three duplicate vehicle assets. A browser can reuse the selected asset for all three locations. The unchanged original PNG is retained for provenance and is not imported by the app. Combined WebP storage is 162,784 bytes; browsers select a size rather than fetching both unconditionally.

Asset assertions verify RGBA, transparent outer corners, substantial transparent space and opaque foreground. The 1100 variant contains 313,612 fully transparent pixels and 404,275 fully opaque pixels. These checks supplement visual inspection. See [assets.json](red-mux/assets.json), [light edge preview](red-mux/edge-light.jpg) and [dark edge preview](red-mux/edge-dark.jpg).

## Presentation and useful controls

MuxPhotography imports the new red asset variants once. All three slots retain the same accessible front-view alt text, intrinsic dimensions, lazy loading, async decoding and contain sizing. The vehicle is not flipped, distorted, cropped to simulate another view or made to rotate.

Existing transparent slots and CSS contact/drop shadows remain. The contact-shadow angle was adjusted for the new orientation. The under-bonnet discussion label moved to the right side and is width-constrained on phones. No heading, section dimension, main layout, Hero/Nav selector, vehicle asset or theme system outside these slots changed.

Vehicle inspection, Wheel & brake illustration and Battery illustration remain working service-zone buttons. Production-browser interaction confirmed front-wheel focus and under-bonnet focus labels, and Vehicle inspection resets the focus. Existing text explicitly explains that internal battery/brake parts are not visible in the photograph. Service selection, request context and draft-preservation tests pass.

## 3D removal and runtime

The three image branches render no `data-scene-dock`, canvas, loading car, geometry or rotation control. Production inspection after visiting all three locations returned:

- Canvas count: 0.
- Scene-host count: 0.
- 360° / DRAG TO ROTATE in component content: absent.
- Three loaded images, all using the same hashed `isuzu-mux-red-front-3q` WebP.
- Console warnings/errors: 0 / 0.

No vehicle camera, lights, drag control or model animation is initialized by these slots. No FPS/battery/memory improvement percentage was measured or claimed.

The existing generic scene provider and historical renderer remain dormant because the production page supplies no scene hosts. An optional broader provider refactor was rejected by automatic approval review because it could affect protected Hero behavior. It was not applied or retried through a workaround. The final change remains scoped to the requested image presentation. The retained legacy dynamic scene chunk still causes the existing build size advisory; this is not a claim that all historical 3D code has been deleted.

## Current responsive, theme and interaction checks

All three locations were checked in both themes at:

320 × 568; 360 × 800; 390 × 844; 412 × 915; 768 × 1024; 1366 × 768; 1920 × 1080.

All 42 cases passed the current checks: correct new asset loaded, complete image framing, no horizontal overflow, no following-panel occlusion of the image center, transparent container background, zero canvases/scene hosts and no old rotation UI. The saved overview was also inspected visually for roof/mirror/tire framing and text/button separation. Some images include neighboring content from the existing scroll/stack composition; its layout was preserved.

Fresh production-preview checks confirmed working component-area buttons, TOLI AI launch/input/response on desktop, usable mobile AI dialog and the canonical Book Service dialog with its Name field. No customer request was submitted. The image layer has pointer events disabled and does not block these controls.

## Hero and navigation protection

A baseline comparison checked 390 existing source/public files. Exactly three existing files changed: the shared image component, its vehicle-only CSS and its source-name test. Hero, navbar, their assets, TOLI AI, shared provider and historical model source are unchanged. All 43 older MU-X reference hashes also remain unchanged. The supplied Downloads image and its project copy retain identical hashes.

See [protection.json](red-mux/protection.json).

## Fresh technical validation

| Check | Actual result |
| --- | --- |
| TypeScript app/node/qa | PASS |
| Lint | PASS |
| Final production build | PASS, 7.87 seconds |
| Full final test suite | PASS, 55 files / 373 tests, 115.71 seconds |
| Responsive/theme browser checks | PASS, 42 cases |
| Production console | 0 warnings / 0 errors |
| Alpha asset assertions | PASS |
| Source protection | PASS |

These checks were run for this task, not copied from an earlier report. The initial test run began before the new image variants were written and had one import-resolution collection failure; the full suite was rerun after final assets existed and passed. The final report uses the successful final run only. Logs are under `docs/red-mux/validation-*.log`; current browser records are under `docs/red-mux/screenshots/`.

## Screenshots

- [Section 03 desktop](red-mux/screenshots/section03-red-mux-desktop.jpg)
- [Vehicle Components desktop](red-mux/screenshots/vehicle-components-red-mux-desktop.jpg)
- [Section 05 desktop](red-mux/screenshots/section05-red-mux-desktop.jpg)
- [Section 03 mobile](red-mux/screenshots/section03-red-mux-mobile.jpg)
- [Vehicle Components mobile](red-mux/screenshots/vehicle-components-red-mux-mobile.jpg)
- [Section 05 mobile](red-mux/screenshots/section05-red-mux-mobile.jpg)
- [Hero regression](red-mux/screenshots/hero-regression-after-red-mux.jpg)
- [Navbar regression](red-mux/screenshots/navbar-regression-after-red-mux.jpg)
- [Three slots together](red-mux/screenshots/three-red-mux-presentations.jpg)
- [Responsive overview](red-mux/screenshots/overview.jpg)
- [TOLI AI desktop](red-mux/screenshots/toli-ai-desktop.jpg)
- [TOLI AI mobile](red-mux/screenshots/toli-ai-mobile.jpg)

## Changed files

Modified:

- `src/components/journey/MuxPhotography.tsx`
- `src/components/journey/mux-photography.css`
- `src/test/mux-photography.test.tsx`

Added:

- Original supplied PNG copy and two responsive WebPs listed above.
- `tools/images/prepare_red_mux.mjs`
- `tools/images/mux-masks/red-front.svg`
- This report.
- Provenance, mask master, edge previews, logs, audit metadata and screenshots under `docs/red-mux/`.

Previous image/model work remains available for rollback. No protected project was modified.

## Git commit and GitHub push blocker

After successful local validation, `git status --short --branch`, `git branch --show-current` and `git remote -v` were checked in the specified target. All returned exit 128 because this directory is not a Git repository. Exact status error:

```text
fatal: not a git repository (or any parent up to mount point /)
Stopping at filesystem boundary (GIT_DISCOVERY_ACROSS_FILESYSTEM not set).
```

Commit hash: **unavailable — no commit created**.  
Branch: **unavailable — no repository metadata**.  
Configured remote: **unavailable in this target**.  
GitHub push: **blocked / not attempted**.

No repository was initialized, no remote was guessed or changed, no unrelated files were staged, and no history was rewritten. The existing checkout path was requested while local work continued. It is required to complete the GitHub portion safely. See [git-status.json](red-mux/git-status.json).

No deployment was performed. Physical-device performance was not measured; responsive QA used browser viewport emulation.
