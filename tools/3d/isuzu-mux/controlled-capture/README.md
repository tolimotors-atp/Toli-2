# Controlled capture workspace

Status: **NOT STARTED — WAITING FOR CONTROLLED PHOTOS**. Empty capture folders are intentional. No existing reference photographs have been imported.

Read `instructions/CONTROLLED_CAPTURE_GUIDE.md` before photographing. Record the session in `metadata/session-notes.md`. Copy original new photos into `incoming/<sequence>/`, retaining the original filenames.

Run `validate_capture.py` using the existing local reconstruction Python environment. It only inspects and copies photos; it does not launch reconstruction. Read the latest `metadata/capture-manifest.json`; passing automatic checks does not approve calibration. Never feed an entire working folder blindly to reconstruction, because stale copies may remain after reclassification.

Folder purposes:

- `instructions/`: capture checklist and later camera gate.
- `incoming/`: untouched original new photographs, organized by sequence.
- `accepted/`: byte-identical automatically passing working copies, awaiting manual review.
- `rejected/`: review copies; not a deletion list.
- `metadata/`: original-to-working mappings, EXIF, hashes, notes and preparation checks.
- `calibration/`: future reviewed camera solution; empty now.
- `reconstruction/`: future geometry evidence; empty now.
- `comparisons/`: future reference/V04 comparisons; empty now.

No V04 changes, V05, retained-component edits, website changes, GLB, paid assets, integration, deployment or commit. All previous references, experiments and depth maps remain separate and preserved. Preparation cost: ₹0 / $0.
