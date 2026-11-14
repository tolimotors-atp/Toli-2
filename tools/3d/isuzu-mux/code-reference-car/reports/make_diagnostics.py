"""Assemble actual Three.js browser captures; uniform scaling only, no image warping."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,shutil
ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'renders/v01';OUT.mkdir(parents=True,exist_ok=True)
SOURCE=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X')
for p in Path('/tmp').glob('mux-v01-*.jpg'):shutil.copy2(p,OUT/p.name)
shutil.copy2('/tmp/mux-v01-render-measurements.json',ROOT/'reports/render-measurements.json')
FIVE=['front','front-left','left','rear-left','rear'];EIGHT=['front','front-left','left','rear-left','rear','rear-right','right','front-right']
def tile(path,label,w=640,h=380):
 out=Image.new('RGB',(w,h),'#e8e8e8');im=Image.open(path).convert('RGB');im=ImageOps.contain(im,(w-12,h-40));out.paste(im,((w-im.width)//2,36+(h-40-im.height)//2));ImageDraw.Draw(out).text((14,10),label,fill='#252525');return out
def sheet(mode,views,name,cols):
 w,h=640,380;rows=(len(views)+cols-1)//cols;board=Image.new('RGB',(w*cols,h*rows+45),'#d9d9d9');d=ImageDraw.Draw(board);d.text((15,13),'MU-X CODED REFERENCE CAR V01 / '+mode.upper()+' / UNAPPROVED PRIMARY BODY',fill='#222')
 for i,v in enumerate(views):board.paste(tile(OUT/f'mux-v01-{mode}-{v}.jpg',v),(i%cols*w,45+i//cols*h))
 board.save(OUT/name,quality=94)
for mode in ['clay','reflection','wireframe']:sheet(mode,FIVE,mode+'-five-view.jpg',3)
sheet('reflection',FIVE,'coded-five-view.jpg',3);sheet('clay',EIGHT,'coded-eight-view.jpg',4)
for src,dest in [('close-front-left','front-34-closeup'),('close-rear-left','rear-34-closeup'),('close-left','greenhouse-closeup'),('cross-sections','cross-sections'),('zebra-front-left','zebra-front-34')]:shutil.copy2(OUT/f'mux-v01-{src}.jpg',OUT/f'{dest}.jpg')
refs=[('front','Screenshot From 2026-11-06 18-17-10.png'),('front-left','Screenshot From 2026-11-06 18-17-27.png'),('left','Screenshot From 2026-11-06 18-17-14.png'),('rear-left','Screenshot From 2026-11-06 18-17-31.png'),('rear','Screenshot From 2026-11-06 18-17-18.png')]
board=Image.new('RGB',(1280,5*380+70),'#d9d9d9');d=ImageDraw.Draw(board);d.text((15,10),'SUPPLIED REFERENCE | CODED CLAY V01 — BADGELESS MODEL',fill='#222');d.text((15,32),'Uniform fits of unwarped images. Perspectives/crops differ; closest facing side selected; NOT calibrated overlays.',fill='#444')
for i,(v,name) in enumerate(refs):
 board.paste(tile(SOURCE/name,v+' / supplied reference'),(0,70+i*380));camera={'front-left':'front-right','left':'right','rear-left':'rear-right'}.get(v,v);board.paste(tile(OUT/f'mux-v01-clay-{camera}.jpg',v+' comparison / coded camera: '+camera),(640,70+i*380))
board.save(OUT/'reference-coded-comparison.jpg',quality=95);shutil.copy2(OUT/'reference-coded-comparison.jpg',ROOT/'comparisons/reference-coded-comparison.jpg')
(ROOT/'reference-data/README.md').write_text('Central editable source: /home/thunder/shared/tolimotors-main1/toli-static-website/src/components/three/mux/MuxReferenceData.ts\n\nContains the supplied dimension framework, normalized image landmarks, 19 nonuniform normalized body stations, longitudinal/window/front/rear curves and fixed camera names. These are authored visual interpretations, not calibrated coordinates. No previous mesh or cage data is imported. See ../analysis/DESIGN_MAP.md for evidence and confidence.\n')
print('Saved',len(list(OUT.glob('*.jpg'))),'diagnostic images in',OUT)
