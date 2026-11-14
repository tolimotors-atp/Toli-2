from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,hashlib,shutil
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';W=B/'manual-overlay-reconstruction'
assert not W.exists(), 'Do not overwrite an existing branch'
for n in ['references','normalized','cameras','source','milestones','renders/v01','diagnostics','reports']: (W/n).mkdir(parents=True)
inv=json.loads((B/'references/authoritative-folder/current-inventory.json').read_text());by={int(x['id'][-3:]):x for x in inv['images']}
# Pixel anchors are visually read, with uncertainty; never treated as measured physical sections.
# World names: f/r axle, +/-Y; roof endpoints are broad inferred envelope anchors.
A={'fn':[-1.4225,-.785,.382],'fp':[-1.4225,.785,.382],'rn':[1.4225,-.785,.382],'rp':[1.4225,.785,.382], 'rf':[-.45,-.69,1.80],'rr':[1.76,-.70,1.80], 'rfo':[-.45,.69,1.80],'rro':[1.76,.70,1.80]}
# azimuth uses front(-X)=0; canonical image left profile is negative Y.
selection=[
(11,'Front',0,'HIGH','Canonical closed body; symmetric face envelope','Bonnet, windscreen, fender width',{'fn':[389,432],'fp':[685,432],'rf':[438,146],'rfo':[611,146]}),
(16,'Front-left 3Q',45,'HIGH','Canonical compatible silver three-quarter','Bonnet, fender, cowl, greenhouse',{'fn':[362,403],'rn':[768,340],'fp':[230,350],'rf':[457,133],'rr':[740,144]}),
(30,'Left-front intermediate',65,'MEDIUM','Closer transition angle; cropped screenshot','Bonnet side falloff, A root, arch',{'fn':[333,390],'rn':[853,332],'rf':[511,85],'rr':[851,86]}),
(12,'Left side',90,'HIGH','Canonical closed side with full vehicle','Wheel relation, roof, side opening',{'fn':[239,390],'rn':[752,389],'rf':[438,154],'rr':[840,153]}),
(22,'Left-rear intermediate',115,'MEDIUM','Intermediate rear wrap visible','Quarter mass, D pillar, rear wrap',{'fn':[251,391],'rn':[750,440],'rf':[500,129],'rr':[872,127]}),
(17,'Rear-left 3Q',135,'HIGH','Canonical rear quarter, compatible silver','D pillar, rear glass, quarter',{'fn':[391,345],'rn':[674,405],'rp':[823,351],'rf':[468,144],'rr':[676,140]}),
(13,'Rear',180,'HIGH','Canonical closed rear full envelope','Rear glass, D pillars, taper, bumper',{'rn':[388,432],'rp':[650,432],'rr':[433,151],'rro':[606,151]}),
(35,'Rear-right 3Q',225,'MEDIUM','New opposite-side corner support','Quarter, D pillar, bumper corner',{'rp':[400,377],'fp':[760,285],'rn':[160,333],'rro':[291,64],'rfo':[595,84]}),
(14,'Right side',270,'HIGH','Canonical opposite side full contour','Roof, arches, opposite side',{'rp':[292,399],'fp':[802,400],'rfo':[618,157],'rro':[212,158]}),
(15,'Front-right 3Q',315,'HIGH','Canonical opposite front three-quarter','Bonnet, windscreen, fender wrap',{'fp':[692,410],'rp':[384,342],'fn':[831,350],'rfo':[582,137],'rro':[393,142]}),
(43,'Overhead',None,'LOW','Only roof reference; family unconfirmed','Roof/bonnet plan only',{}),
(20,'Front-left 3Q support',45,'MEDIUM','Larger image shows compound surfaces','Bonnet crown, arch, cowl',{'fn':[439,450],'rn':[865,385],'rf':[636,153],'rr':[889,140]}),
(27,'Front support',0,'MEDIUM','Red series near frontal envelope','Bonnet plan, A pillars, face width',{'fn':[373,466],'fp':[734,466],'rf':[459,132],'rfo':[651,132]})]
rows=[]
for num,view,az,conf,why,regions,anchors in selection:
 r=by[num];src=Path(inv['source'])/r['relative_path'];assert hashlib.sha256(src.read_bytes()).hexdigest()==r['sha256'];shutil.copy2(src,W/'references'/src.name)
 im=ImageOps.exif_transpose(Image.open(src)).convert('RGB');scale=min(800/im.width,520/im.height);wh=(round(im.width*scale),round(im.height*scale));off=((800-wh[0])//2,(520-wh[1])//2);out=Image.new('RGB',(800,520),'white');out.paste(im.resize(wh,Image.Resampling.LANCZOS),off);out.save(W/'normalized'/f'{num:03}.png')
 row={**r,'selected_view':view,'confidence':conf,'why_selected':why,'regions':regions,'normalization':{'scale':scale,'offset':off,'canvas':[800,520]},'anchors':[{'name':n,'world':A[n],'pixel_original':xy,'pixel':[xy[0]*scale+off[0],xy[1]*scale+off[1]],'uncertainty_px_original':8 if n[0] in 'fr' and len(n)==2 else 14} for n,xy in anchors.items()]};rows.append(row)
 guide=out.copy();dr=ImageDraw.Draw(guide)
 for a in row['anchors']:
  x,y=a['pixel'];dr.ellipse((x-5,y-5,x+5,y+5),outline='#e92549',width=2);dr.text((x+7,y-7),a['name'],fill='#e92549')
 guide.save(W/'diagnostics'/f'anchor-readings-{num:03}.png')
(W/'references/selection.json').write_text(json.dumps(rows,indent=2))
font=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',17)
board=Image.new('RGB',(1600,5*340),'#191e25');d=ImageDraw.Draw(board)
for i,r in enumerate(rows):
 x=(i%3)*533;y=(i//3)*340;im=Image.open(W/'normalized'/f"{int(r['id'][-3:]):03}.png");im.thumbnail((520,260));board.paste(im,(x+(533-im.width)//2,y+32));d.text((x+8,y+5),f"{r['id']} / {r['selected_view']} / {r['confidence']}",font=font,fill='white');d.text((x+8,y+294),r['regions'],font=font,fill='#dcc58c')
board.save(W/'diagnostics/selected-reference-board.jpg',quality=94)
excluded=[]
ids={r['id'] for r in rows}
for r in inv['images']:
 if r['id'] in ids:continue
 reason='Secondary compatible angle; no extra active plane required'
 if r['geometric_class']=='G1':reason='Detail/composite/open panels; closed exterior not directly traced'
 if r['geometric_class']=='G0':reason='Redundant crop/scale variant of '+str(r['near_duplicate_of'])
 excluded.append({'id':r['id'],'filename':r['filename'],'role':reason})
(W/'references/secondary-and-excluded.json').write_text(json.dumps(excluded,indent=2))
shutil.copy2(B/'RECONSTRUCTION_STATUS.md',W/'reports/pre-branch-status.md')
# Snapshot all historical reconstruction files and protected production trees before new files are built.
old=json.loads((B/'FREEZE_PRESERVATION_MANIFEST.json').read_text())['files'];baseline={}
for k,v in old.items():
 p=Path(k);p=p if p.is_absolute() else P/p
 if p.is_file():baseline[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
for p in B.rglob('*'):
 if p.is_file() and W not in p.parents and '__pycache__' not in p.parts:baseline[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
(W/'reports/before-hashes.json').write_text(json.dumps(baseline))
print('Prepared',len(rows),'primary views; protected baseline',len(baseline))
