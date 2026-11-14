from pathlib import Path
import hashlib,json
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';W=B/'base-asset-audit'
before=json.loads((W/'metadata/preservation-before.json').read_text());changed=[]
for name,sha in before.items():
 p=Path(name)
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=sha:changed.append(name)
assert not changed,changed
inv=json.loads((W/'metadata/candidate-inventory.json').read_text());assert inv['candidate_count']==len(inv['candidates'])==13;assert len({r['id'] for r in inv['candidates']})==13
assert sum(inv['license_counts'].values())==13 and inv['license_counts']['L3']==0
assert sum(inv['provisional_body_counts'].values())==13 and inv['downloaded_count']==0
assert all(r['asset_classification']=='BASE-X' and not r['downloaded'] and r['original_sha256'] is None and r['measured_geometry'] is None for r in inv['candidates'])
assert not any(p.is_file() and p.name!='README.md' for p in (W/'downloads').rglob('*'))
assert not list((W/'comparisons').glob('*.jpg'))
photos=json.loads((B/'references/authoritative-folder/current-inventory.json').read_text())
for r in photos['images']:assert hashlib.sha256((Path(photos['source'])/r['relative_path']).read_bytes()).hexdigest()==r['sha256']
for path in [B/'FREE_BASE_ASSET_AUDIT.md',W/'reports/LICENSE_AUDIT.md']:
 text=path.read_text();assert 'L3' in text and 'NOT' in text.upper()
res={'audit_date':'2026-11-09','baseline_files_verified_unchanged':len(before),'unexpected_changes':changed,'original_image_hashes_verified':len(photos['images']),'protected_project_baseline_counts':{n:sum('/'+n+'/' in p for p in before) for n in ['toli-3d-website','tolimotors-main']},'candidate_inventory_count_checks':'PASS','download_gate_check':'PASS — no L3, no asset downloads','new_blender_sources':0,'new_glb_exports':0,'production_and_historical_files':'UNCHANGED','report_paths':[str(B/'FREE_BASE_ASSET_AUDIT.md'),str(W/'reports/LICENSE_AUDIT.md'),str(W/'metadata/candidate-inventory.json')],'limitations':'No technical asset evaluation because no candidate cleared license/provenance gate. No website build or regression tests; site unchanged.'}
(W/'metadata/preservation-validation.json').write_text(json.dumps(res,indent=2)+'\n');print(json.dumps(res,indent=2))
