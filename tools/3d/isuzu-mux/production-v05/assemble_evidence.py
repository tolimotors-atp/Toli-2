from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageChops
import json,hashlib,shutil
p=Path.cwd();w=p/'tools/3d/isuzu-mux/production-v05';r=w/'renders';raw=r/'raw';raw.mkdir(parents=True,exist_ok=True)
for f in Path('/tmp/mux-v05-evidence').iterdir():
 if f.is_file():shutil.copy2(f,raw/f.name)
for f in Path('/tmp').glob('mux-v05-*.log'):shutil.copy2(f,w/f.name)
font=ImageFont.load_default(size=14)
small=ImageFont.load_default(size=11)
ref=p.parent/'Isuzu MU-X'
references={
 'front':('Screenshot From 2026-11-06 18-17-10.png',(338,110,716,490)),
 'front-right':('Screenshot From 2026-11-06 18-17-27.png',(145,118,880,497)),
 'right':('Screenshot From 2026-11-06 18-17-14.png',(132,115,945,466)),
 'rear-right':('Screenshot From 2026-11-06 18-17-31.png',(260,118,875,498)),
 'rear':('Screenshot From 2026-11-06 18-17-18.png',(345,126,720,492))}
def image(path):return Image.open(path).convert('RGB')
def fit(im,w,h):
 im=im.copy();im.thumbnail((w,h),Image.Resampling.LANCZOS);out=Image.new('RGB',(w,h),'#e5e5e5');out.paste(im,((w-im.width)//2,(h-im.height)//2));return out
# Union framing is identical for V04/V05. All untouched canvas captures remain in raw/.
def pair_boxes(view,mode):
 boxes=[]
 for version in ['v04','v05']:
  im=image(raw/f'{version}-{mode}-{view}.jpg');diff=ImageChops.difference(im,Image.new('RGB',im.size,(229,229,229))).convert('L');box=diff.point(lambda v:255 if v>42 else 0).getbbox();boxes.append(box)
 return (max(0,min(b[0] for b in boxes)-20),max(0,min(b[1] for b in boxes)-20),min(1000,max(b[2] for b in boxes)+20),min(520,max(b[3] for b in boxes)+20))
rows=[]
for view,(file,crop) in references.items():
 panels=[];box=pair_boxes(view,'final')
 for label,im in [('REFERENCE',image(ref/file).crop(crop)),('V04 / ACTIVE',image(raw/f'v04-final-{view}.jpg').crop(box)),('V05 / REJECTED',image(raw/f'v05-final-{view}.jpg').crop(box))]:
  panel=Image.new('RGB',(350,274),'#ececec');draw=ImageDraw.Draw(panel);draw.text((10,8),label+' / '+view,fill='#222',font=font);panel.paste(fit(im,338,230),(6,35));panels.append(panel)
 row=Image.new('RGB',(1050,274),'white')
 for n,panel in enumerate(panels):row.paste(panel,(350*n,0))
 row.save(r/f'reference-v04-v05-{view}.jpg',quality=94);rows.append(row)
board=Image.new('RGB',(1050,len(rows)*274+75),'#ececec');draw=ImageDraw.Draw(board);draw.text((12,12),'V05: C — REGRESSED / V04 REMAINS ACTIVE',fill='#222',font=font);draw.text((12,37),'Uncalibrated visual comparison; uniform scaling only. Original full canvas captures are preserved.',fill='#333',font=small)
for i,row in enumerate(rows):board.paste(row,(0,75+274*i))
board.save(r/'reference-v04-v05-five-view.jpg',quality=94)
for mode in ['clay']:
 board=Image.new('RGB',(1000,5*280+55),'#e5e5e5');draw=ImageDraw.Draw(board);draw.text((12,14),'V04 | V05 / CLAY — geometry remains unapproved',fill='#222',font=font)
 for i,view in enumerate(references):
  box=pair_boxes(view,mode)
  for j,version in enumerate(['v04','v05']):
   board.paste(fit(image(raw/f'{version}-{mode}-{view}.jpg').crop(box),488,245),(j*500+6,65+i*280));draw.text((j*500+12,50+i*280),version+' / '+view,fill='#222',font=small)
 board.save(r/'v04-v05-clay-five-view.jpg',quality=94)
# Closeups are actual camera captures, not generated or retouched vehicle artwork.
features=['headlight','front-fender','mirror','doors-handles','greenhouse','D-pillar','rear-quarter','rear-light','rear-bumper','front-plate','rear-plate']
for name in features:shutil.copy2(raw/f'v05-{name}-closeup.jpg',r/f'{name}-closeup.jpg')
proof=Image.new('RGB',(1000,565),'#e5e5e5');draw=ImageDraw.Draw(proof);draw.text((12,14),'V05 REAR BUMPER REGRESSION — NOT ACTIVATED',fill='#222',font=font);draw.text((12,38),'Black valance/body intersection and discontinuous lamp wrap remain visible. V04 stays active.',fill='#333',font=small);proof.paste(image(raw/'v05-rear-bumper-closeup.jpg'),(0,65));proof.save(r/'rejection-evidence.jpg',quality=94)
base=json.loads((w/'website-baseline.json').read_text());changed=[];missing=[]
for name,digest in base.items():
 f=p/name
 if not f.is_file():missing.append(name)
 elif hashlib.sha256(f.read_bytes()).hexdigest()!=digest:changed.append(name)
assert not changed and not missing,(changed,missing)
(w/'website-protection.json').write_text(json.dumps({'checked':len(base),'changed':changed,'missing':missing,'activeVersion':'V04 exterior details','V05activated':False},indent=2))
for name,digest in json.loads((w/'v04-source-hashes.json').read_text()).items():assert hashlib.sha256((p/name).read_bytes()).hexdigest()==digest,name
for f in r.rglob('*.jpg'):
 with Image.open(f) as im:im.verify()
(w/'decision.json').write_text(json.dumps({'decision':'C — V05 REGRESSED','activated':False,'activeVersion':'V04 exterior details','stoppedGeometryWork':True,'reason':['Rear bumper valance intersects the body surface, producing visible cutout artifacts.','Rear lamp side/face wrap is discontinuous.','Primary greenhouse/fender/rear-quarter identity errors remain.'],'responsiveAfterActivation':'NOT RUN — activation rejected'},indent=2))
shutil.copy2('/tmp/assemble_mux_v05_evidence.py',w/'assemble_evidence.py')
print('Saved five-view reference/V04/V05 comparisons, 11 closeups, rejection evidence and protection audit:',len(base),'existing source/public files unchanged.')
print('Live website evidence dimensions:',Image.open(raw/'live-section03-still-v04.jpg').size)
