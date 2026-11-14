# RECONSTRUCTION FROZEN — 2026-11-08

**DO NOT START ANOTHER PROCEDURAL BODY / CURVE / PATCH ITERATION WITHOUT NEW GEOMETRIC EVIDENCE.**

Authoritative status: [RECONSTRUCTION_STATUS.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/RECONSTRUCTION_STATUS.md). Module classifications and reusable data: [REUSABLE_RECONSTRUCTION_DATA.md](/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/REUSABLE_RECONSTRUCTION_DATA.md). No current MU-X exterior is approved for production or website replacement. Retain all code and masters; do not run historical generation/export commands as a continuation.

The following is preserved historical documentation and is superseded by the freeze above.

# TOLI MU-X — reference-traced cage

Current stage: reference-traced 3D curve cage, Decision B with unresolved 3D joins/depth. No approved surfaces, detailing or export. Full report: `tools/3d/isuzu-mux/REFERENCE_CURVE_CAGE_REPORT.md`.

Load the package in Blender by adding `tools/blender-addons` to Python's path, importing `toli_mux_generator` and calling `register()`. In the TOLI MU-X sidebar use Generate Reference-Traced Cage and Curve Cage Only. References link local originals, without embedding. Diagnostic colors are not website materials. Hiding legacy bodies is reversible.

Pixel measurements/inferred depth: `traced_data.py`. Curve engine: `geometry/reference_cage.py`. Any accepted adjustment must be made there, not only edited in Blender. Current default runner calls `run_cage.py`; it resets a separate background scene. It saves `isuzu-mux-reference-curve-cage-v01.blend`. Use `render_cage_gates.py` then `boards_cage.py` for source-filtered gate images and native annotations. Test the cage with `check_cage.py`.

`test_topology_cage.py` validates the repaired *previous* body generator: Preview/Quality degenerates and non-manifold edges are zero. The old blend is intentionally preserved unchanged. The root fix is exact arch-edge bevel weights in `geometry/rounded.py`.

Prior add-on preserved in `code-generator/soft-v01-addon/`; previous masters remain unchanged. Later runs should use new versioned outputs. Surface generation remains blocked until the cage passes; production GLB, website, controlled capture and protected projects remain untouched. No Fal uploads or generation jobs were made; its recommendation tool was unavailable, and the brief forbids paid/cloud reconstruction.
