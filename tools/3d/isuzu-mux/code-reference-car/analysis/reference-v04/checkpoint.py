from pathlib import Path
import json,sys,hashlib,shutil
p=Path(__file__).resolve().parents[6];w=p/'tools/3d/isuzu-mux/code-reference-car';n=int(sys.argv[1]);a=w/'analysis/reference-v04';d=w/f'source-snapshots/reference-v04/checkpoint-{n:02}';d.mkdir(parents=True,exist_ok=True)
for f in (p/'src/components/three/mux').glob('*.ts'):shutil.copy2(f,d/f.name)
shutil.copy2(p/'src/test/mux-coded-reference.test.ts',d/'mux-coded-reference.test.ts')
for f in ['candidate-geometry.json','candidate-controls.json']:
 if (a/f).exists():shutil.copy2(a/f,a/(f'checkpoint-{n:02}-'+f))
def camera(s):return '\n'.join(l for l in s.splitlines() if 'new T.PerspectiveCamera(' in l or 'const views:' in l or 'const right=new T.Vector3()' in l)
assert camera((d/'validation.ts').read_text())==camera((w/'source-snapshots/identity-v03/final/validation.ts').read_text())
(a/f'checkpoint-{n:02}-source.json').write_text(json.dumps({'cameraUnchanged':True,'files':{f.name:hashlib.file_digest(f.open('rb'),'sha256').hexdigest() for f in d.glob('*.ts')}},indent=2));print('Saved checkpoint',n)
