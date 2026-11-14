# ISUZU MU-X — phone capture guide

**One physical vehicle. One phone. One 1× main rear lens. Park once; you walk around it.**

Take about **36 normal-height + 18 elevated photos**. Add **12 low photos** only if comfortable. This is preparation for reconstruction, not a guarantee of a usable model.

## Before you start — quick checklist

- [ ] Same physical MU-X throughout; no mixed vehicles, generations, body kits, wheelbases or geometry-changing trims.
- [ ] All four doors, bonnet and tailgate closed; windows preferably closed. Mirrors stay in the same position. Do not change configuration during exterior orbits.
- [ ] Vehicle parked safely and completely stationary for every primary photo. No turntable; no repositioning between rings.
- [ ] Enough clear space to walk a complete circle and see the whole vehicle from every direction.
- [ ] Bright overcast daylight or an evenly lit workshop. Avoid darkness, harsh glare, changing sun and headlights shining into the camera.
- [ ] Stable textured surroundings: paving, parking lines, wall features, buildings or workshop structure. Avoid a blank white studio. Keep people and moving vehicles out of the sequence where practical.
- [ ] Clean phone lens. Normal rear camera at **1×**, no digital zoom, no switching to 0.5×/2× or another lens.
- [ ] Same app, resolution, orientation and aspect ratio throughout. Landscape is usually easiest for a complete vehicle.
- [ ] Normal photo mode: no portrait blur, beauty/art filters, AI replacement or optional strong HDR effects.
- [ ] Keep focus/exposure behavior consistent. Use a focus/exposure lock if the app supports it and the result remains sharp and correctly exposed; otherwise avoid changing settings deliberately.

## 1. Normal-height orbit — approximately 36 photos

1. Start straight in front. Record this as the start of the normal sequence.
2. Hold the phone around chest/upper-torso height, consistently, and aim toward the vehicle center.
3. Frame the **entire vehicle**, including roof, bumpers, all visible wheels and mirrors, with background margin. Do not crop a part to fill the frame.
4. Walk slowly in one direction around the car. Stop for each photograph; do not shoot while walking.
5. Take one photo about every **10°**, roughly 36 around the full circle. No need to measure angles precisely. Neighboring photos must share most of the visible vehicle and surroundings; add extra transition shots if the view changes abruptly.
6. Keep roughly the same distance, enough to fit the complete vehicle. Do not jump front → side → rear. Continue progressively through the corners.
7. End close to the starting viewpoint so the orbit closes.

Check these eight clear views are included, but **do not take only these eight**:

**Front → front-left ¾ → left side → rear-left ¾ → rear → rear-right ¾ → right side → front-right ¾.**

Left/right means the vehicle's left/right when seated facing forward. The orbit can run either way; record which direction you chose. Add an exact key view between orbit shots if needed, without removing the overlap shots.

## 2. Elevated orbit — approximately 18 photos

- Keep the car and configuration unchanged. Start at front again.
- Use a moderately higher viewpoint, safely reachable from the ground or a stable approved platform. Never climb on unstable objects or the vehicle.
- Take about one photo every **20°**, approximately 18 around the full orbit. Keep the complete vehicle visible; aim slightly down to show bonnet, roof and upper body.
- Include overlapping views with the normal-height ring. If the jump between shots is too large, take extras.
- If a safe higher viewpoint is unavailable, do not improvise an unsafe one. Record the limitation; normal-height completeness matters more.

## 3. Optional low orbit — approximately 12 photos

Only if comfortable and safe: take one photograph about every **30°** at a consistent lower height, with the complete vehicle still visible. This helps bumpers, sills, arches and lower body. No crawling beneath the vehicle or entering traffic/work areas.

## 4. Before changing anything, review the closed-body sequence

- [ ] Complete circle, no missing side or inaccessible corner.
- [ ] Continuous overlapping photographs, not just eight showcase angles.
- [ ] Full vehicle in every primary image; no clipped mirrors/roof/bumpers/wheels.
- [ ] At full zoom, body edges and wheel features are sharp; no motion blur.
- [ ] No blown-out glare hiding major panels or very dark unseen surfaces.
- [ ] Same phone/lens/orientation; no accidental zoom or portrait mode.
- [ ] Car did not move and doors/bonnet/tailgate/mirrors did not change.

Retake bad shots while the setup is unchanged. Keep the originals, including retakes, and record which are replacements. If the car or lighting changed materially, label a separate session; do not silently merge it.

## 5. Separate later sequences — never mix into primary exterior calibration

Only **after both closed-body rings are finished**:

| Folder / sequence | Photograph |
|---|---|
| `detail` | Headlights, grille, front bumper/fenders, wheels, mirrors, handles, side steps, tail lamps, rear bumper, roof rails and badges. Detail close-ups are for later validation, not the primary full-car sequence. |
| `open-panel` | Four doors, bonnet and tailgate open, including hinge/seam views where accessible. Label which part is open. |
| `interior` | Dashboard, steering wheel, center console, front/rear seats, door panels and cargo area. |
| `engine` | Several overlapping engine-bay views; no disassembly required. |

These remain useful alongside the existing 18 detail references. Keep older references separate from this controlled session. Do not recolor or alter photos to match the existing reference paint.

## 6. Optional scale notes

If convenient and safe, record tire sidewall size, wheel diameter, distance between wheel centers and overall width. Record units, method, uncertainty and whether width includes mirrors. Wheel size on a tire label is rim diameter, not outside tire diameter. Use official dimensions only for the matching generation/variant and record the source; do not substitute an unrelated specification. No crawling under the vehicle or unsafe measurements.

Fill `metadata/session-notes.md`. Approximate camera heights and starting direction help; exact angle measurement is unnecessary.

## 7. Preserve and transfer originals

**Do not resize, screenshot, crop, filter, erase backgrounds or intentionally strip metadata.** Avoid messaging-app compression. Copy original camera files by cable or an original-quality file transfer. Keep a backup on the phone.

Project root:

`/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/controlled-capture/`

Copy files without renaming originals into these empty incoming subfolders:

- `incoming/normal/`
- `incoming/elevated/`
- `incoming/low/` (optional)
- `incoming/detail/`
- `incoming/open-panel/`
- `incoming/interior/`
- `incoming/engine/`

Do not put the old 18 reference images here. Use one capture session per workspace; preserve another session separately rather than mixing it in. If you cannot identify a sequence, leave it directly in `incoming/`; the checker flags it for assignment.

JPEG originals are straightforward to inspect locally. If the phone produces HEIC/HEIF or RAW, preserve those originals too. The checker may flag formats without a local decoder; that is not proof the photo is bad. A later supported, metadata-preserving conversion must be made separately.

## 8. Run the local photo checker — not reconstruction

From the project root:

```sh
/home/thunder/Documents/Codex/mux-reconstruction-env/bin/python tools/3d/isuzu-mux/controlled-capture/validate_capture.py
```

The existing local environment has Pillow and NumPy; no network, paid service or GPU is used. The checker:

- Reads originals and records filenames, SHA-256, dimensions, time, camera/lens, focal length, exposure, EXIF/display orientation, sequence and working filename where available.
- Flags low resolution, missing metadata, changes of camera/lens/focal length/resolution/orientation, exact duplicate files and possible severe blur.
- Detects numbering gaps only when originals already have names such as `normal_001.jpg`. Camera-native names cannot prove full orbit continuity: manually inspect the order and session notes.
- Creates **byte-identical copies**, systematically named, under `accepted/` or `rejected/`; it never deletes or moves originals.
- Writes `metadata/capture-manifest.json` atomically. `accepted` means automatic checks passed, **not approval for reconstruction**. `rejected` contains review copies, not a deletion list.

Working names resemble `normal_001_<hash>.jpg`, `elevated_001_<hash>.jpg` or `detail_001_<hash>.jpg`. Annotate detail subjects in session notes, e.g. `detail_front_headlight_left_001`. Original names and metadata remain intact.

Blur scores are advisory and affected by texture, noise and sharpening. Missing EXIF alone does not reject a photo. The checker cannot establish same physical vehicle, full coverage, true overlap, reliable focus everywhere or unchanged panels. **A person must review these.**

Reruns preserve prior working copies; use **only the latest manifest's listed files**, not every file found in `accepted/`. Fix classifications in the incoming sequence folders without editing the image bytes, then rerun. Old unlisted copies are not the active dataset. Symlinks are not imported. Unknown/corrupt/unsupported files are retained for review. No automatic COLMAP step exists.

## 9. Future reconstruction — only after new photos and review

1. **Validate photos:** review the manifest and full-resolution images; verify one stationary closed vehicle and continuous orbit coverage. Keep details/interior/engine/open panels out.
2. **Extract features** on the reviewed primary working images.
3. **Match** sequentially with loop closure and cross-ring links; use spatial matching only with trustworthy location information. Capture order must be checked, not inferred from arbitrary renamed files.
4. **Recover cameras and sparse points.**
5. **Inspect camera distribution** and correspondence quality before proceeding.
6. **Attempt dense reconstruction only after the camera gate passes.**
7. **Compare** the result in front, side, rear and both three-quarter views against the photos, V04 and matching official/measured dimensions.
8. Use only validated geometry as evidence for a clean production mesh. No automatic replacement/shrinkwrap of V04.

### Camera gate

Report total/registered images, registration percentage, registered images per ring/sector, orbit coverage, sparse-point count, mean/median and outlier reprojection errors, suspect focal estimates and missing sectors. Seek registration of nearly all sharp primary photos; a high percentage alone is insufficient.

**Stop before dense reconstruction if any entire side/major sector is missing, poses cluster or collapse, cameras face implausible directions, or sparse points mostly describe background/repeated wheels instead of consistent body features.** Inspect at least all eight key-view sectors and the links between them. Explain any excluded views and numerical error distribution rather than declaring success because several cameras registered. Background aids camera recovery; it is not vehicle geometry.

V04 stays available for its front work, proportions, greenhouse layout, hard points and 113 internal components. Existing reference audits and all experiments/depth maps remain preserved. No V05, GLB, website change, integration, deployment or commit is authorized by this preparation task.
