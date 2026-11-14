"""Preserve actual code/data per controlled correction; does not create vehicle geometry."""
from pathlib import Path
import sys,shutil,json,hashlib,re
P=Path(__file__).resolve().parents[6]
W=P/'tools/3d/isuzu-mux/code-reference-car';stage=int(sys.argv[1]);name=f'iteration-{stage:02d}'
D=W/'source-snapshots/identity-v02'/name;D.mkdir(parents=True,exist_ok=True)
for f in (P/'src/components/three/mux').glob('*.ts'):shutil.copy2(f,D/f.name)
shutil.copy2(P/'src/test/mux-coded-reference.test.ts',D/'mux-coded-reference.test.ts')
s=(P/'src/components/three/mux/validation.ts').read_text();old=(W/'source-snapshots/section-03-05/validation.ts').read_text()
def camera(t):return '\n'.join(line for line in t.splitlines() if 'new T.PerspectiveCamera(' in line or 'const views:' in line or 'const right=new T.Vector3()' in line)
assert camera(s)==camera(old),'Camera definition/framing changed'
meta={'iteration':stage,'cameraCodeSHA256':hashlib.sha256(camera(s).encode()).hexdigest(),'cameraUnchanged':True,'files':{f.name:hashlib.sha256(f.read_bytes()).hexdigest() for f in D.glob('*.ts')}}
(W/'analysis/identity-v02'/f'{name}-snapshot.json').write_text(json.dumps(meta,indent=2));print('Preserved',name,'with unchanged fixed cameras')
