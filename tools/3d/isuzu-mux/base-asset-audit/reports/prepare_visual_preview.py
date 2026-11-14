from pathlib import Path
import json,hashlib,shutil
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';W=B/'base-asset-audit';R=W/'renders/warehouse-2018-mux'
assert not R.exists(),'Do not overwrite an existing visual inspection'
for n in ['warehouse-2018-mux-viewer-contact-sheet.jpg','warehouse-2018-mux-reference-comparison.jpg','reference-manual-warehouse-comparison.jpg']:assert not (W/'comparisons'/n).exists()
R.mkdir(parents=True)
old=json.loads((W/'metadata/preservation-before.json').read_text());paths={Path(p) for p in old}
paths.update(p for p in B.rglob('*') if p.is_file() and R not in p.parents and '__pycache__' not in p.parts)
rows={str(p):hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(paths) if p.is_file()}
(W/'metadata/warehouse-preview-preservation-before.json').write_text(json.dumps(rows))
shutil.copy2(B/'FREE_BASE_ASSET_AUDIT.md',W/'reports/FREE_BASE_ASSET_AUDIT-before-visual-preview.md')
print('Protected baseline saved:',len(rows),'files')
