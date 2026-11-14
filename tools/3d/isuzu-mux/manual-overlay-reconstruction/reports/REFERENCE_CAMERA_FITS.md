# Reference-fit cameras — NOT CALIBRATED

13 visual reference cameras: 12 perspective fits and one manually framed orthographic roof-plan camera. No recovered EXIF, physical focal length or real-world extrinsics are claimed. Front = negative X, Z up; canonical left-profile label corresponds to negative-Y camera here.

Perspective fit: fixed 12 m distance from (0,0,0.93), 36 mm assumed sensor width, bounded visual azimuth ±12°, elevation 0–26°, positive 18–160 mm equivalent Blender lens. Least-squares uniform projected scale and image-centre shift fit visually read wheel centres and broad inferred roof points. Body geometry/dimensions never fit or change during camera fitting. Roof anchors are approximate envelope points, not known physical homologues. Physical camera distance/focal tradeoff is not recovered.

Reference-image confidence describes visibility/design evidence; camera confidence separately includes anchor mismatch. HIGH reference confidence never means calibrated depth. No overhead wheel anchors exist.

| Image / view | Lens mm / type | Position XYZ m | Rotation XYZ rad | Anchor RMS px (800×520) | Fit confidence |
|---|---:|---|---|---:|---|
| MUX-011 / Front | 64.51 | -11.4599, 0.6006, 4.4385 | 1.27409, -0.00000, -1.62316 | 16.74 | LOW |
| MUX-016 / Front-left 3Q | 62.50 | -7.4784, -9.2350, 2.6001 | 1.43117, 0.00000, -0.68068 | 14.32 | LOW |
| MUX-030 / Left-front intermediate | 80.32 | -5.6028, -10.5373, 2.1843 | 1.46608, -0.00000, -0.48869 | 14.95 | LOW |
| MUX-012 / Left side | 71.59 | -0.0000, -10.7855, 6.1905 | 1.11701, -0.00000, -0.00000 | 8.82 | HIGH |
| MUX-022 / Left-rear intermediate | 72.68 | 5.7956, -10.4555, 1.9759 | 1.48353, -0.00000, 0.50615 | 24.39 | LOW |
| MUX-017 / Rear-left 3Q | 58.33 | 9.6805, -6.7784, 3.0138 | 1.39626, -0.00000, 0.95993 | 16.98 | LOW |
| MUX-013 / Rear | 63.02 | 11.7378, -2.4949, 0.9300 | 1.57080, -0.00000, 1.36136 | 23.05 | LOW |
| MUX-035 / Rear-right 3Q | 94.17 | 8.5677, 8.2738, 2.3924 | 1.44862, 0.00000, 2.33874 | 23.16 | LOW |
| MUX-014 / Right side | 71.35 | 0.0000, 10.9625, 5.8108 | 1.15192, -0.00000, -3.14159 | 4.17 | HIGH |
| MUX-015 / Front-right 3Q | 59.93 | -8.5258, 8.2333, 2.8072 | 1.41372, -0.00000, -2.33874 | 17.57 | LOW |
| MUX-043 / Overhead | ORTHO | 0.0000, 0.0000, 12.0000 | 0.00000, 0.00000, 0.00000 | None | LOW |
| MUX-020 / Front-left 3Q support | 67.73 | -7.4956, -9.2562, 2.3924 | 1.44862, 0.00000, -0.68068 | 14.62 | LOW |
| MUX-027 / Front support | 70.45 | -11.5911, 0.0000, 4.0358 | 1.30900, 0.00000, -1.57080 | 21.92 | LOW |

## Per-view anchors and limitations

### MUX-011 — Front
Anchors: fp, fn, rfo, rf. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-016 — Front-left 3Q
Anchors: fn, rn, rf, rr. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-030 — Left-front intermediate
Anchors: fn, rn, rf, rr. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-012 — Left side
Anchors: fn, rn, rf, rr. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-022 — Left-rear intermediate
Anchors: fn, rn, rf, rr. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-017 — Rear-left 3Q
Anchors: fn, rn, rf, rr. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-013 — Rear
Anchors: rn, rp, rr, rro. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-035 — Rear-right 3Q
Anchors: rp, fp, rn, rro, rfo. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-014 — Right side
Anchors: rp, fp, rfo, rro. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-015 — Front-right 3Q
Anchors: fp, rp, rfo, rro. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-043 — Overhead
Anchors: none; manual planform framing. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Unrelated roof-only reference; no wheel anchors. Manually framed planform only, not metric evidence.

### MUX-020 — Front-left 3Q support
Anchors: fn, rn, rf, rr. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

### MUX-027 — Front support
Anchors: fp, fn, rfo, rf. Full pixel readings, estimated 3D anchors, projected values and per-anchor errors: cameras/reference-fits.json.
Roof anchors are inferred envelope points, not known homologous 3D corners. Missing rails/mirrors/details are excluded. Width/roof depth remain uncertain; this is not calibration.

Wheel centres use the nominal hard framework. Roof points are inferred x=−0.45/+1.76, y≈±0.69/0.70, z=1.80 m. Unknown trim, missing roof rails, mirrors/steps and subjective anchor reading contribute to residuals. Left/right names follow the audit convention, not a recovered physical orbit.

The saved Blender camera projections were independently compared with every saved fitted anchor; see geometry-validation.json. Framework overlays are in cameras/framework-overlay-*.png. These show a dimensional box, not a claim that a car occupies its rectangular corners.

Overhead 043 has unverified family/source and no fitted depth: LOW confidence only. Camera view is aligned front-left in the image, with no non-uniform scaling.
