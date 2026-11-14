import hashlib,json
from pathlib import Path
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';W=B/'manual-overlay-reconstruction';baseline=json.loads((W/'reports/before-hashes.json').read_text());changed=[];checked=0
for name,digest in baseline.items():
 p=Path(name)
 if p==B/'RECONSTRUCTION_STATUS.md':continue
 if not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=digest:changed.append(name)
 checked+=1
assert not changed,changed
inv=json.loads((B/'references/authoritative-folder/current-inventory.json').read_text());src=Path(inv['source'])
for r in inv['images']:assert hashlib.sha256((src/r['relative_path']).read_bytes()).hexdigest()==r['sha256']
master=B/'source/production/isuzu-mux-manual-overlay-v01.blend';mil=W/'milestones/isuzu-mux-manual-overlay-v01-gated.blend';assert master.read_bytes()==mil.read_bytes()
# Verify authored primary control-net counts and required diagnostic files, not only file creation.
net=json.loads((W/'source/authored-control-net.json').read_text());assert sum(len(p['vertices']) for p in net['patches'])==354
for p in net['patches']:
 assert all(len(f)==4 and len(set(f))==4 and all(0<=v<len(p['vertices']) for v in f) for f in p['faces'])
for name in ['clay-six-view.jpg','reflection-six-view.jpg','wire-six-view.jpg','zebra-six-view.jpg','reference-overlay-six-view.jpg','silhouette-five-view.jpg','internal-boundary-five-view.jpg','reference-previous-new-comparison.jpg','primary-surface-closeups.jpg']:assert (W/'renders/v01'/name).is_file()
result={'historical_baseline_files_unchanged':checked,'authorized_changed_baseline_files':[str(B/'RECONSTRUCTION_STATUS.md')],'unexpected_changes':changed,'original_images_hash_verified':len(inv['images']),'protected_sibling_baseline_counts':{n:sum('/'+n+'/' in k for k in baseline) for n in ['toli-3d-website','tolimotors-main']},'master_and_final_milestone_sha256':hashlib.sha256(master.read_bytes()).hexdigest(),'render_png_count':len(list((W/'renders/v01').glob('*.png'))),'master_bytes':master.stat().st_size,'website_assets':'UNCHANGED','no_glb_export':True,'no_deployment_or_commit':True,'visual_gate':'C — FAIL; technical self-checks are not recognition approval'}
(W/'diagnostics/preservation-validation.json').write_text(json.dumps(result,indent=2));(W/'diagnostics/FINAL_GATE.json').write_text(json.dumps({'decision':'C','badgeless_recognition':'FAIL','body_approval':False,'details':'NOT STARTED','GLB':'NOT EXPORTED','website':'UNCHANGED','automatic_continuation':'STOP'},indent=2));print(json.dumps(result,indent=2))
