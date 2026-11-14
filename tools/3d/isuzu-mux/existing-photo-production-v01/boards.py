from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
P=Path(__file__).resolve().parents[4];B=P/'tools/3d/isuzu-mux';R=B/'code-generator/renders/existing-photo-production-v01';REF=P.parent/'Isuzu MU-X'
F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',23);S=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',16)
def canvas(cols,rows,w=900,h=650):return Image.new('RGB',(cols*w,rows*h),'#191d24')
def panel(out,im,col,row,label,w=900,h=650):
 pic=ImageOps.contain(im.convert('RGB'),(w-24,h-80));x=col*w;y=row*h;out.paste(pic,(x+(w-pic.width)//2,y+54+(h-80-pic.height)//2));ImageDraw.Draw(out).text((x+12,y+12),label,font=F,fill='white')
views=['front','front34','side','rear34','rear']
times={'front':'18-17-10','front34':'18-17-27','side':'18-17-14','rear34':'18-17-31','rear':'18-17-18'}
photo_crops={'front':(330,100,730,495),'front34':(140,130,885,500),'side':(120,105,950,485),'rear34':(250,100,885,505),'rear':(330,110,720,495)}
render_crops={'front':(310,160,690,540),'rear':(310,160,690,540),'side':(60,170,940,560),'front34':(60,100,940,580),'rear34':(60,100,940,580)}
combined=canvas(3,5)
for i,v in enumerate(views):
 out=canvas(3,1);photo=Image.open(REF/f'Screenshot From 2026-11-06 {times[v]}.png').crop(photo_crops[v])
 for j,(im,label) in enumerate([(photo,'REFERENCE'),(Image.open(R/f'previous-clay-{v}.png').crop(render_crops[v]),'PREVIOUS V04 / FAILED'),(Image.open(R/f'clay-{v}.png').crop(render_crops[v]),'NEW MILESTONE 1 / UNAPPROVED')]):
  panel(out,im,j,0,v.upper()+' / '+label);panel(combined,im,j,i,v.upper()+' / '+label)
 ImageDraw.Draw(out).text((15,625),'Same model camera/studio; photographs uncalibrated. Comparator has historical identity details; new candidate is primary surfaces only.',font=S,fill='#bec9d5');out.save(R/f'comparison-{v}.jpg',quality=95)
combined.save(R/'reference-previous-new-comparison.jpg',quality=95)
for mode in ['clay','reflection','zebra','wire']:
 out=canvas(3,2)
 for i,v in enumerate(views):panel(out,Image.open(R/f'{mode}-{v}.png'),i%3,i//3,mode.upper()+' / '+v.upper())
 ImageDraw.Draw(out).text((1820,1000),'Milestone 1 only\nNo badges or detail camouflage\nNot production approved',font=F,fill='white');out.save(R/f'{mode}-five-view.jpg',quality=95)
close=[('bonnet-fender','18-17-27',(140,240,510,470)),('cowl-a-root','18-17-27',(300,150,570,330)),('d-pillar','18-17-31',(470,120,730,315)),('rear-quarter','18-17-31',(400,240,680,480)),('rear-corner','18-17-31',(600,260,900,490))]
out=canvas(3,5)
for i,(feature,time,crop) in enumerate(close):
 photo=Image.open(REF/f'Screenshot From 2026-11-06 {time}.png').crop(crop)
 for j,(im,label) in enumerate([(photo,'REFERENCE'),(Image.open(R/f'clay-{feature}.png'),'NEW CLAY'),(Image.open(R/f'reflection-{feature}.png'),'NEW REFLECTION')]):panel(out,im,j,i,feature.upper()+' / '+label)
out.save(R/'primary-surface-closeups.jpg',quality=95)
print('Five reference comparisons, five-view clay/reflection/zebra/wire and primary close-ups saved')
