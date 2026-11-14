# Current authoritative reference status — folder reconciliation

Authoritative image source: `/home/thunder/shared/tolimotors-main1/Isuzu MU-X`.

**18 files / 18 readable PNG images**: 13 exact matches to O01–O13; five previously missed files, including one visual re-crop duplicate of S12. No internal byte/pixel duplicates. 18 compatible/secondary-useful references (15 exterior, two interior, one engine); no incompatible body-family images in this folder. No EXIF or 3D assets.

Five additions improve engine/interior detail and corroborate existing exterior views, but do not resolve a missing exterior camera/G1 constraint. **A — EXISTING 34-IMAGE CONCLUSION CONFIRMED; DO NOT RESTART. MANUAL RECONSTRUCTION LIMIT REACHED = YES.** No new calibration or surface construction justified.

Full per-file metadata, compatibility, duplicate mapping, sequence investigation and reasoning: `REFERENCE_FOLDER_RECONCILIATION.md` and `references/authoritative-folder/inventory.json`. Derived contact sheet: `renders/reference-folder-contact-v01.jpg`. Original photographs remain untouched.

The prior 34-image audit below is retained as a **historical audit scope**, not a claim that the authoritative folder contains 34 images. Exact previous audit also preserved as `REFERENCE_AUDIT_PRE_FOLDER_RECONCILIATION.md`. Historical supplements remain archived and the eight incompatible ones remain excluded.

---

# ISUZU MU-X — complete reference re-audit and reconstruction decision

## Decision before modeling
- Total **34 distinct source images**, all visually reviewed; repeated uploads of O06–O13 are not counted twice.
- **26 usable for the canonical family**: 25 exterior/detail/open-panel/partial-engine images plus one interior image.
- **8 excluded from this reconstruction**: S02, S04–S10 show a different body/glazing/lamp family. Retained in the archive, never fitted into the canonical body.
- **ROUTE B — REFERENCE-CONSTRAINED MANUAL SURFACE RECONSTRUCTION.**
- No new sufficiently constrained multi-view calibration subset found. O06–O13 are the same eight previously failed core views. Field S14–S18 likely share a source vehicle (same visible red registration MH-43 / Z230A in S14, S16, S18; matching wheel/trim/environment in S15/S17), but only S14/S15 are full 3Q views. S16 crops the roof; S17/S18 are details. This is useful evidence, not a new complete, controlled orbit.
- Previous failed bodies and V01/V02 preserved. No V03 joint calibration invented. Website and protected projects unchanged.

## Geometry master
Canonical first-generation-style tall MU-X body family (visual identification; exact model year/market trim unverified): swept angular projector headlamp envelopes, two heavy chrome grille bars, polygonal fog-light recesses, high roof with upright rear quarter glass, rising side-glass lower edge, broad split wraparound rear lamps, horizontal chrome tailgate garnish and recessed central number plate. Canonical O01–O04 override conflicting trim; O06–O13 guide compatible closed-body contours. Paint color is ignored.

## Inventory scope and metadata
Original 13 paths from `references/inventory.json`, all 21 currently accessible user-supplied clipboard images in `/tmp`, project MU-X reference directories and named MU-X workspace files were checked. Generated Blender renders, diagnostics and contact sheets are outputs, not extra photographs. No further MU-X originals discovered in those sources. This is not an exhaustive scan of unrelated personal folders or inaccessible operating-system temporary directories.

Each original is now archived losslessly under `references/complete-library/Oxx.png` or `Sxx.png`; the JSON inventory retains original absolute path, SHA256, dimensions, roles and every available EXIF field. All 34 are PNGs with **no EXIF camera/lens/focal/capture-time/orientation data**. File modification time is not capture evidence. Matching 640×427 sizes support a common publishing source, not proof of fixed focal length. No physical measurements available; no invented metre dimensions.

Roles: A calibration **candidate**, not accepted calibration; B silhouette; C fascia; D side body; E rear; F detail; G functional open panels; H interior; I partial engine; J excluded. Open panel positions do not constrain closed contours. O01 only partly exposes the engine bay. O05 is interior-only and is not evidence for exterior dimensions.

## Compatibility groups
|Group|Evidence and limits|
|---|---|
|G1 canonical-compatible body family|O01–O13, S01, S03, S11–S13, S19–S21. Compatible roof/glazing, arches, angular lamp/chrome-bar fascia and broad tail-lamp/hatch family where visible. Not proof of exact same trim or physical vehicle. Promotional compositing, wheel variants and lighting do not supply metric calibration.|
|G2 same broad body, trim/source differences|S14–S18: comparable pillars/arches/headlight envelope; fog-surround/bumper finishes and wheel treatment require canonical cross-check. Do not transplant source-specific inserts or infer invisible rear details from a front closeup.|
|G3 incompatible body family|S02/S04/S05/S06/S07/S08/S09/S10: narrower lamps, larger grille variants, tapered rear quarter glazing, different pillars/shoulder and slimmer rear-light/tailgate family. Differences are geometry, not paint. Exact year/trim is not asserted.|

## Per-image classification
|ID|Dimensions|Group / roles|Visible evidence and permitted use|
|---|---|---|---|
|O01|819×595|G1 / BCFGI|Front, bonnet and four doors open; engine bay partial|
|O02|1060×522|G1 / BDG|Left profile, doors/bonnet/tailgate open|
|O03|1060×522|G1 / BEG|Rear, tailgate and rear doors open; cargo aperture|
|O04|1148×492|G1 / BDG|Right profile, doors/bonnet/tailgate open|
|O05|1038×587|G1 / H|Right-hand-drive dashboard, steering, front cabin and door cards|
|O06|1038×587|G1 / ABCF|Closed front|
|O07|1038×587|G1 / ABDF|Closed left profile|
|O08|1038×587|G1 / ABEF|Closed rear|
|O09|1038×587|G1 / ABDF|Closed right profile|
|O10|1038×587|G1 / ABCDF|Closed front three-quarter, right side|
|O11|1038×587|G1 / ABCDF|Closed front three-quarter, left side|
|O12|1038×587|G1 / ABDEF|Closed rear three-quarter, left side|
|O13|1038×587|G1 / ABDEF|Closed rear three-quarter, right side|
|S01|704×435|G1 / BCDF|red low front 3Q; compatible broad body; fascia detail must follow canonical|
|S02|678×452|G3 / J|different narrow lamps, large grille and side glazing|
|S03|700×438|G1 / BD|red side promotional; useful silhouette, composited context not metric|
|S04|640×479|G3 / J|different rear lamps/tailgate and glazing|
|S05|678×452|G3 / J|large honeycomb grille and narrow lamp envelope|
|S06|738×414|G3 / J|different tapered quarter glazing and shoulder|
|S07|414×226|G3 / J|different tapered quarter glazing; low resolution|
|S08|516×387|G3 / J|different slim rear lamps/tailgate|
|S09|515×388|G3 / J|different rear quarter/tailgate|
|S10|738×414|G3 / J|different quarter glazing and slim rear lamps|
|S11|678×452|G1 / BCDF|red front 3Q; chrome double-bar grille and angular projector envelope|
|S12|738×414|G1 / BCDF|blue front 3Q; same broad body; promotional perspective not calibrated|
|S13|640×427|G1 / BCDF|silver studio front 3Q; matching headlight/grille/window family|
|S14|640×427|G2 / BCDF|silver field front 3Q; fog surround/bumper finish varies; body compatible|
|S15|640×427|G2 / BDEF|silver field rear 3Q; same plate as field front; compatible rear family|
|S16|640×427|G2 / BCF|field straight front; roof cropped, bumper finish differs|
|S17|640×427|G2 / DF|field wheel/arch closeup; no scale or exact tire specification|
|S18|640×427|G2 / CF|field lamp/grille closeup; trim only where canonical agrees|
|S19|640×424|G1 / BEF|red straight rear; matches broad tail lamps, chrome bar and hatch family|
|S20|640×424|G1 / BDEF|red rear 3Q promotional; silhouette only, background not calibration|
|S21|640×424|G1 / BDEF|red rear 3Q studio; useful quarter glass and rear envelope|

## Consistent subsets and decision rationale
1. O01–O04 open-panel studio set: strong visual session coherence, but moving doors/bonnet/hatch and occlusion preclude treating panel edges as closed landmarks. O05 secondary interior.
2. O06–O13 closed studio views: same source-style dimensions/UI, visually coherent; already exhausted by V02. Training 2.29px, held-out 9.39px, geometry leave-one-view-out 17.02px RMS / 68.59px maximum. Merely reuploading does not add information.
3. S14–S18 field subset: likely one source vehicle, not verified by metadata. Two oblique overviews, cropped frontal view and two local details are insufficient to justify a new rigorous calibration branch, especially no full opposite-side/rear-principal coverage.
4. S19/S21 rear promotional/studio views and S01/S03/S11/S12 front/side views: useful anatomy/silhouette, different vehicles or unverified sources. Do not force a shared lens, wheel or trim model.

No numerical recovery is claimed. Route B uses independent visual comparisons and explicit estimated depth; it cannot establish exact dimensional fidelity. The user-authorized manual route supersedes the prior instruction to wait for a new controlled set, but does not turn failed V02 into geometry authority.

## Region reference assignments
|Region|Primary|Secondary|Validation|Resolved evidence / remaining uncertainty|
|---|---|---|---|---|
|Wheels / stance|O07/O09 axle/profile proportions|O06/O08 track appearance|S17, S03|Normalized wheelbase=1; radius 0.137 and track 0.572 are estimates, not measured specs; wheel details deferred.|
|Greenhouse|O07 side-window and roof outline|O02/O04 canonical pillars, O11 front3Q|O09 opposite profile, O12/O13, S13/S15/S21|New views constrain quarter glass/roof silhouette; cross-car depth, glass crown, exact pillar curvature remain estimated.|
|Bonnet / fenders|O06/O11|O10/S13|S14/S16|Height/crown and fender/lamp transitions visible; not constructed before greenhouse passes.|
|Front fascia|O01 canonical fixed fascia, O06|O10/O11/S13|S16/S18 plus S11|Grille and lamp envelopes well evidenced; source-specific lower inserts do not override canonical; deferred.|
|Side / arches|O07/O09|O02/O04/S03|S14/S17/S21|Shoulder and rocker visible across several views; deferred.|
|Rear / tailgate|O08/O03 fixed aperture|O12/O13/S19|S15/S21|Broad lamp, hatch and rear-glass boundaries evidenced; open hatch position not copied into closed body; deferred.|

## Route B milestone: regions 1 and 2 only
Blender **5.2.2 LTS**, executable `/usr/bin/blender`. Fresh empty scene; no previous body mesh, V02 landmark structure or failed cage imported/deformed. Authored roof/glass/frames from an explicit O07 side trace and front/rear visual depth estimates. Four economical cylinder wheel/tire proxies establish normalized axles and ground; not production wheels. Reference images are packed in the blend.

Source: `source/reconstruction/isuzu-mux-reference-constrained-v01.blend`.
Authoring script/checks: `source/reconstruction/reference-constrained-v01/`.
Diagnostics: `renders/region-greenhouse-v01.jpg` and five neutral `greenhouse-*-v01.png` views, plus `renders/greenhouse-profile-overlay-v01.jpg`. Profile overlay is only a manual wheelbase/ground alignment, **not a solved perspective projection**. Orthographic diagnostic views and illustrative 3Q camera poses are not calibrated reference cameras; no pixel RMS is claimed.

### Greenhouse gate — FAIL / STOP
The first profile study captures the raised cabin, sloping A-pillar, two door-glass regions and separate rear quarter glass. However:
- Windscreen/roof section transition remains too angular; glass crown and leading-edge curvature need a dedicated surface pass.
- Side-glass corners and quarter glass are too polygonal; C/D-pillar junctions and window seals are not integrated clean surfaces.
- Front/rear glass width, cross-car crown and hatch-glass wrapping are estimates and have not passed multi-view likeness.
- The manually aligned profile also places the roof edge too high. Roof-edge/frame separation and visible gaps in 3Q remain; profile similarity alone does not pass 3D identity.

Do not continue into bonnet/fenders, fascia, side body or rear surfaces. No interior, engine, badges, materials, cuts or hinges. The model is a partial failed study, not a complete MU-X or production candidate. `region-front-v01.jpg`, `region-side-v01.jpg`, `region-rear-v01.jpg` are intentionally not fabricated for unbuilt regions.

### Next modeling correction
Refine continuous windscreen/roof/rear-glass sections and the rounded quarter-glass/C/D-pillar framework, using O07 and O09 side constraints and O11/O12/S13/S21 depth evidence. Compare the same neutral views again. Only after the greenhouse gate passes can region 3 begin. No claim of an accuracy guarantee from this mixed library.

## Preservation / validation
All prior source models, V01/V02 rigs and diagnostic renders preserved. Old audit and V02 report backed up exactly before the two authorized report updates. Source image copies hash-checked. Blender source is saved and reopened for mesh/packed-reference/ground checks. Website src/public/config and protected-project source/config hash-checked; no protected-project writes. Full dependency trees and every protected binary asset are outside this verification scope.

No website build/TypeScript/lint/browser checks repeated because no website source or public asset changes. No GLB, integration, Git commit or deployment.
