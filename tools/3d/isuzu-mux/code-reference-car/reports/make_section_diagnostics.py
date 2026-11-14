"""Assemble actual browser renders and preserved-site regression screenshots, without warping."""
from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageChops,ImageStat
import json,shutil
W=Path(__file__).resolve().parents[1];O=W/'renders/section-03-05';O.mkdir(exist_ok=True,parents=True)
for p in Path('/tmp').glob('mux-0305-*.jpg'):shutil.copy2(p,O/p.name.replace('mux-0305-',''))
for name in ['responsive','render-stats','settled-checks']:shutil.copy2('/tmp/mux-0305-'+name+'.json',W/'analysis/section-03-05'/(name+'.json'))
def tile(path,label,w=640,h=380):
 im=Image.open(path).convert('RGB');im=ImageOps.contain(im,(w-12,h-36));out=Image.new('RGB',(w,h),'#dedede');out.paste(im,((w-im.width)//2,32+(h-36-im.height)//2));ImageDraw.Draw(out).text((12,9),label,fill='#222');return out
five=['front','front-left','left','rear-left','rear'];eight=['front','front-left','left','rear-left','rear','rear-right','right','front-right']
def board(mode,views,name,cols):
 out=Image.new('RGB',(640*cols,40+380*((len(views)+cols-1)//cols)),'#d2d2d2');ImageDraw.Draw(out).text((15,12),'SECTION 03/05 CODED CANDIDATE — ISOLATED, NOT ACTIVE / '+mode.upper(),fill='#222')
 for i,v in enumerate(views):out.paste(tile(O/f'{mode}-{v}.jpg',v),(i%cols*640,40+i//cols*380))
 out.save(O/name,quality=94)
board('clay',five,'coded-mux-five-view.jpg',3);board('clay',eight,'coded-mux-eight-view.jpg',4)
for mode in ['clay','reflection','wireframe']:board(mode,five,'coded-mux-'+mode+'.jpg',3)
for src,dest in [('close-front-left.jpg','front-34-closeup.jpg'),('close-rear-left.jpg','rear-34-closeup.jpg'),('close-left.jpg','greenhouse-closeup.jpg'),('section-03-1000.jpg','section-03-desktop.jpg'),('section-05-1000.jpg','section-05-desktop.jpg'),('section-03-390.jpg','section-03-mobile.jpg'),('section-05-390.jpg','section-05-mobile.jpg')]:shutil.copy2(O/src,O/dest)
source=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X')
rows=[('front','front','18-17-10'),('front 3/4','front-right','18-17-27'),('side','right','18-17-14'),('rear 3/4','rear-right','18-17-31'),('rear','rear','18-17-18')]
out=Image.new('RGB',(1280,40+380*5),'#d2d2d2');ImageDraw.Draw(out).text((12,12),'REFERENCE | CODED CLAY — independent uniform fit, not a calibrated overlay',fill='#222')
for i,(label,v,suffix) in enumerate(rows):
 out.paste(tile(source/f'Screenshot From 2026-11-06 {suffix}.png',label+' / supplied reference'),(0,40+i*380));out.paste(tile(O/f'clay-{v}.jpg',label+' / coded, badges absent'),(640,40+i*380))
out.save(O/'reference-coded-comparison.jpg',quality=94)
metrics={}
for name in ['hero','navigation']:
 a=Image.open(O/f'before-{name}.jpg').convert('RGB');b=Image.open(O/f'after-{name}.jpg').convert('RGB');assert a.size==b.size,(name,a.size,b.size)
 diff=ImageChops.difference(a,b);metrics[name]={'size':a.size,'meanAbsoluteRGB':sum(ImageStat.Stat(diff).mean)/3,'pixelsWithAnyChannelDifferenceOver10':sum(max(p)>10 for p in diff.getdata()),'pixels':a.width*a.height}
 pane=Image.new('RGB',(a.width*2,a.height+35),'#ddd');pane.paste(a,(0,35));pane.paste(b,(a.width,35));d=ImageDraw.Draw(pane);d.text((12,10),'BEFORE / protected '+name,fill='#222');d.text((a.width+12,10),'AFTER / source unchanged',fill='#222');pane.save(O/(name+'-regression.jpg'),quality=94)
(W/'analysis/section-03-05/regression-image-metrics.json').write_text(json.dumps(metrics,indent=2))
checks=json.loads((W/'analysis/section-03-05/responsive.json').read_text());out=Image.new('RGB',(1280,40+420*6),'#ddd');ImageDraw.Draw(out).text((12,12),'EXISTING VEHICLES PRESERVED / 03 LEFT | 05 RIGHT / RESPONSIVE QA',fill='#222')
for i,width in enumerate([320,360,390,412,768,1440]):
 for j,section in enumerate(['03','05']):out.paste(tile(O/f'section-{section}-{width}.jpg',f'{section} / {width}px — old vehicle',640,420),(j*640,40+i*420))
out.save(O/'responsive-contact-sheet.jpg',quality=92)
print(json.dumps(metrics));print('Saved diagnostics:',len(list(O.glob('*.jpg'))))
