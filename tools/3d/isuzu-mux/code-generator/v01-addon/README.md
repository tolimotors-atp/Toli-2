# TOLI MU-X Generator — 0.1.0

Experimental **Milestone 1 only**. The code is the source of truth; generated vertices must not be hand-edited. Current visual gate: **NEEDS WORK**, not better than V04. Website export is intentionally blocked.

## Installation / usage

Use Blender's Scripting workspace to run:

```python
import sys
sys.path.insert(0, '/home/thunder/shared/tolimotors-main1/toli-static-website/tools/blender-addons')
import toli_mux_generator
toli_mux_generator.register()
```

Alternatively zip the `toli_mux_generator` folder and use Blender's Install from Disk for legacy add-ons. Registration was tested in Blender 5.2.2; other versions are not tested.

Open View3D → sidebar → **TOLI MU-X**. Generate MU-X creates `TOLI_MUX_GENERATED`; Regenerate replaces that collection's objects, not unrelated scene objects. Do not put hand-authored work in that owned collection. Reset restores parameter defaults; press Regenerate afterward. Preview uses lower wheel sampling/bevel segments; Quality increases those settings, not model fidelity. Dimensions/body/greenhouse/fender/wheel parameters are in meters and centrally defined in `parameters.py`. Station profiles and image constraints live in `reference_data.py`; edit those rather than generated vertices.

Current generated parts: body loft, true axle-derived Boolean arches, bonnet-height profile, greenhouse/rear block, four tires and simple rims. No grille, lights, glass panes, spokes/hubs, panels, interior or engine yet. Those later modules/UI sections are deliberately not presented as completed features. Materials use Principled nodes. The dark greenhouse material denotes a review volume, not finished glazing.

Validate Geometry writes `tools/3d/isuzu-mux/code-generator/renders/validation.json`. Render Validation Views uses stable orthographic review cameras (not solved photo cameras), and renders there. Reference collection `TOLI_MUX_REFERENCES` contains only comparison cameras currently; no image binaries embedded. Lighting is scene-owned; the supplied headless milestone runner creates neutral review lighting.

Reproduce the baseline scene and five views from the project root:

```sh
blender -b --threads 2 --python tools/blender-addons/toli_mux_generator/run_milestone.py
```

This runner starts an empty scene: use a separate Blender process, not an unsaved interactive scene. It saves `tools/3d/isuzu-mux/source/production/isuzu-mux-code-generated-v01.blend`. The add-on UI does not reset the user's entire scene. The runner compares geometry fingerprints before/after deletion and regeneration.

Export operator is blocked pending exterior approval. No GLB or website replacement is produced. Keep V04 and the controlled-photo workflow intact. Future controlled measurements can update the parameter/station data. No paid assets, APIs or cloud processing.
