from pathlib import Path
import hashlib,json
from PIL import Image
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';W=B/'base-asset-audit';R=W/'renders/warehouse-2018-mux';main=B/'FREE_BASE_ASSET_AUDIT.md'
base=json.loads((W/'metadata/warehouse-preview-preservation-before.json').read_text());changes=[]
for p,sha in base.items():
 path=Path(p)
 if path==main:continue
 if not path.is_file() or hashlib.sha256(path.read_bytes()).hexdigest()!=sha:changes.append(p)
assert not changes,changes
before=(W/'reports/FREE_BASE_ASSET_AUDIT-before-visual-preview.md').read_bytes();assert hashlib.sha256(before).hexdigest()==base[str(main)];assert main.read_bytes().startswith(before)
meta=json.loads((W/'metadata/warehouse-2018-mux-visual-preview.json').read_text());assert sum(meta['captured_views'].values())==1 and not meta['model_downloaded']
for name,sha in meta['screenshot_sha256'].items():assert hashlib.sha256((R/name).read_bytes()).hexdigest()==sha
for p in list(R.glob('*.jpg'))+list((W/'comparisons').glob('*warehouse*.jpg')):
 with Image.open(p) as im:im.verify()
original=json.loads((B/'references/authoritative-folder/current-inventory.json').read_text())
for r in original['images']:assert hashlib.sha256((Path(original['source'])/r['relative_path']).read_bytes()).hexdigest()==r['sha256']
assert not any(p.suffix.lower() in {'.glb','.gltf','.blend','.obj','.fbx','.zip','.rar','.skp'} for p in R.rglob('*'))
assert not any(p.is_file() and p.name!='README.md' for p in (W/'downloads').rglob('*'))
result={'date':'2026-11-09','viewer_access':'PARTIAL','actual_angles_captured':1,'five_priority_views_completed':False,'reason':'Interactive 3D viewer requires sign-in; no bypass/login/model download attempted','baseline_files_verified_unchanged':len(base)-1,'authorized_change':'FREE_BASE_ASSET_AUDIT.md append only; original bytes preserved and verified','unexpected_changes':changes,'original_images_hash_verified':len(original['images']),'license_inventory_and_decision':'UNCHANGED — L2 / M3 provisional / BASE-X / NOT CLEARED','production_and_protected_projects':'UNCHANGED','preview_integrity_checks':'PASS','model_downloaded':False,'GLB_exported':False,'deployment_or_commit':False}
(W/'metadata/warehouse-preview-preservation-validation.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
