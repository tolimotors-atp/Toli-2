from pathlib import Path
import json, hashlib
p=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');w=p/'tools/3d/isuzu-mux/code-reference-car';a=w/'analysis/identity-v02'
for source,target in [(w/'reports/preservation-before.json','protected-after.json'),(a/'source-before.json','source-after.json')]:
 baseline=json.loads(source.read_text());changed=[];missing=[]
 for name,h in baseline.items():
  f=Path(name)
  if not f.is_file():missing.append(name)
  elif hashlib.file_digest(f.open('rb'),'sha256').hexdigest()!=h:changed.append(name)
 (a/target).write_text(json.dumps({'checked':len(baseline),'changed':changed,'missing':missing},indent=2));print(target,len(baseline),'changed',len(changed),'missing',len(missing),flush=True)
