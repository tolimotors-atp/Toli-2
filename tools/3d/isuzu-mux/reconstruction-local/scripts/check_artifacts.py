from pathlib import Path
import json,hashlib,numpy as np
from PIL import Image
r=Path(__file__).resolve().parents[1]
def sha(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1024*1024),b''):h.update(b)
 return h.hexdigest()
man=json.loads((r/'input/manifest.json').read_text());assert len(man['originals'])==18
for entry in man['originals']:
 p=Path(entry['original']);assert sha(p)==entry['original_sha256']
 for d in entry['derived']:
  a=Image.open(p).convert('RGB').crop(d['crop_xyxy']);b=Image.open(r/d['path']).convert('RGB');assert np.array_equal(np.asarray(a),np.asarray(b))
  if 'mask' in d:assert Image.open(r/d['mask']).size==b.size
for t in ['18-17-10','18-17-27','18-17-14','18-17-35','18-17-18']:
 d=np.load(r/'calibration/depth'/f'{t}-inverse-depth.npy');assert d.shape==(256,256) and np.isfinite(d).all() and d.max()>d.min()
summary=json.loads((r/'logs/summary.json').read_text());assert summary['images_submitted']==8 and summary['images_registered']==0 and summary['sparse_points']==0
before=json.loads((r/'logs/preservation-before.json').read_text());changed=[p for p,h in before.items() if not Path(p).is_file() or sha(Path(p))!=h]
result={'protected_files_checked':len(before),'changed':changed,'originals_checked':18,'lossless_derivatives_checked':13,'depth_maps_checked':5,'comparison_board_exists':(r/'comparisons/five-view-reference-depth-v04.jpg').is_file(),'status':'PASS' if not changed else 'FAIL'}
(r/'logs/validation.json').write_text(json.dumps(result,indent=2));assert not changed,changed
print(json.dumps(result,indent=2))
