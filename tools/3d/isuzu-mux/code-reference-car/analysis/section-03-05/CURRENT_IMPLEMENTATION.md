# Section 03 / 05 rendering audit — BEFORE source corrections

## Exact rendering path

`src/pages/Index.tsx` renders `HowItWorks` inside `SectionStack` for **03 / SERVICE JOURNEY**, id `process`. This is not `ComponentExperience` (the service/component explorer associated with section 02).

`src/pages/Index.tsx` renders `CtaBanner` for **05 / SERVICE REQUEST**, id `booking`.

03: `src/components/HowItWorks.tsx` → `JourneyDock mode="process"`.
05: `src/components/CtaBanner.tsx` → `JourneyDock mode="completion"`.
Both: `JourneyDock.tsx` → `[data-scene-dock]` inline host → `JourneyProvider.tsx` → `observeJourney` in `src/lib/journey-timeline.ts` → `loadVehicleScene` → `src/lib/vehicle-scene.ts`.

One renderer/canvas is moved between visible docks. The **same renderer/model also serves the Section 02 service/component explorer**. A global model URL/loader replacement would exceed this task's scope.

Current solid: `src/lib/vehicle-model/contract.ts` selects `muxVehicleManifest` from `mux.ts`, using existing `public/models/vehicles/isuzu-mux/isuzu-mux-web.glb` (historical V04 temporary preview). `load.ts` caches one template per URL and clones disposable geometry/materials for each renderer. `vehicle-scene.ts` loads that model into the shared car group; its original procedural sedan shell and separate service components are also constructed, with the imported solid controlling the displayed overview. This is the PRE-EXISTING implementation, not a new external asset introduced by this task.

## Camera / lighting

`journey.ts` maps process mode to inspection/pickup/service/ready and completion mode to completion. Both use scale 1, target Y .78 and camera height 1.65 (renderer Y-up convention), with differing damped yaw/dolly/scan/clean states.

The perspective camera uses 34° FOV, near .1, far 60. The imported non-Hero solid uses rotated bounding-box fitting with target (0,.75,0), direction normalized (7.4,1.3,4.3), padding 1.13, adjusting distance to aspect ratio. This framing supersedes much of the legacy free camera path.

Shared light/environment code: coded studio radiance + PMREM, directional key, hemisphere fill, point accent and desktop rim. Theme strengths come from `src/lib/vehicle-theme.ts`. Contact/tire shadows and a lightweight selected-mesh reflection approximation ground the vehicle. No new lighting or camera is active in 03/05 during isolated geometry evaluation.

## Animation / controls / mobile / failure

Process step buttons call `chooseStep`; chapter state controls damped turn/distance/scan/clean. Completion is a composed final request pose. Rendering is demand-based, paused offscreen/hidden/behind enquiry/AI dialogs. Scroll and pointer inputs feed the shared timeline; reduced-motion snaps/dampens travel and interrupts drive/drag inertia without removing the live model.

`vehicle-policy.ts` picks desktop/tablet; tablet includes phones, save-data and weak hardware. DPR caps 1.5/1. Geometry/lighting can downgrade after measured frame intervals. Context-loss/restoration is handled by the renderer. On actual failure the provider switches to `VehicleIllustration` in `JourneyDock`; text/buttons remain outside the canvas.

Layout is in `journey/experience.css` and associated existing journey styles. Desktop process grid 1.15fr/1fr with dock min-height 480; booking grid 1.1fr/1fr with dock min-height 440. Tablet dock min-height 350; narrow layouts stack with min-height 300. These layouts/CSS must not be edited. Live rendering uses alpha and does not paint a replacement section background.

## Scope and quality gate

Hero and navigation assets, CSS, modules and markup are hard-locked. 03/05 React layouts, timeline, loader, fallback and styling are unchanged while the failed V01 primary geometry is corrected in isolation.

If recognition passes, integration would need a scoped model-presentation branch for process/completion, preserving the existing service dock's solid and shared renderer/resource lifecycle. No such branch is activated before the gate. No second independently modeled vehicle is permitted.
