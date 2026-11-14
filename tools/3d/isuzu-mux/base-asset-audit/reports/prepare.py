from pathlib import Path
import json,hashlib
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';W=B/'base-asset-audit'
assert not W.exists(),'Preserve an existing audit; do not overwrite'
assert not (B/'FREE_BASE_ASSET_AUDIT.md').exists()
for n in ['downloads','metadata','working','renders','comparisons','reports']:(W/n).mkdir(parents=True)
prior=json.loads((B/'manual-overlay-reconstruction/reports/before-hashes.json').read_text());paths={Path(p) for p in prior}
paths.update(p for p in B.rglob('*') if p.is_file() and W not in p.parents and '__pycache__' not in p.parts)
rows={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths) if p.is_file()}
(W/'metadata/preservation-before.json').write_text(json.dumps(rows))
print('Protected current-state baseline:',len(rows),'files')
