# TOLI MU-X Generator — current primary-body gate

Current runner: `run_soft.py` or `run_milestone.py`, in a separate background Blender process. It saves `isuzu-mux-curve-soft-detail-v01.blend`; this filename is an unapproved primary-body attempt, NOT a finished deep-detail vehicle. Decision C: clay/reference fidelity failed. No detail work or export.

Blender sidebar: Generate MU-X — Soft Body — Clay Gate. Earlier sources remain archived in `tools/3d/isuzu-mux/code-generator/rounded-v01-addon/` and preceding archives. Enable the add-on by adding `tools/blender-addons` to Python's module path, importing `toli_mux_generator`, and calling `register()`; use the TOLI MU-X sidebar. Never run the scene-resetting headless runner inside an unsaved interactive scene.

Profiles/classes: `geometry/soft_body.py`; shared sampled-Bezier engine: `geometry/rounded.py`; curve data: `mux_curve_data.py`. Accepted fixes must be in code. Preview and Quality share design intent with different sample densities. Parameters are experimental; changing them does not guarantee a valid surface.

Validation: `check_soft.py`. Silhouettes: `overlay_soft.py`. Comparisons: `boards_soft.py`. Diagnostics are under `renders/deep-detail-v01/`. Reset then Generate restores the baseline. Show Construction Curves controls viewport diagnostics; render helpers omit construction curves. Reference toggles link local originals without embedding them. No production export is enabled.

Full findings: `tools/3d/isuzu-mux/DEEP_DETAIL_V01_REPORT.md`, including six Preview degenerate faces and the failed visual gate. Preserve every existing milestone; use a new versioned filename for future approved changes. No manual mesh fixes, paid assets, cloud use, deployment or commit.
