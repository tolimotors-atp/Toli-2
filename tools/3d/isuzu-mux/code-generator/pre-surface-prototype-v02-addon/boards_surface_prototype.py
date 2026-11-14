from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json
P=Path(__file__).resolve().parents[3];r=P/'tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v01';src=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');font=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',24);small=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',16)
def panel(canvas,im,box,label):
 x,y,w,h=box;im=ImageOps.contain(im.convert('RGB'),(w-24,h-62));canvas.paste(im,(x+(w-im.width)//2,y+48+(h-62-im.height)//2));d=ImageDraw.Draw(canvas);d.text((x+14,y+10),label,font=font,fill='white')
refs={'a':('18-17-27',(145,150,650,465)),'b':('18-17-31',(505,115,875,350)),'c':('18-17-31',(420,220,900,495))};names={'a':'BONNET / FENDER / COWL','b':'ROOF / D-PILLAR / GLASS','c':'QUARTER / LAMP / BUMPER'}
combined=Image.new('RGB',(3000,3*800),'#191d24')
for i,z in enumerate(['a','b','c']):
 t,crop=refs[z];photo=Image.open(src/f'Screenshot From 2026-11-06 {t}.png').crop(crop);primary='front34' if z=='a' else 'rear34';out=Image.new('RGB',(3000,800),'#191d24')
 for j,(im,label) in enumerate([(photo,'REFERENCE'),(Image.open(r/('zone-'+z)/'cage.png'),'V04 CAGE'),(Image.open(r/('zone-'+z)/('clay-'+primary+'.png')),'SURFACE PROTOTYPE')]):panel(out,im,(j*1000,0,1000,760),'ZONE '+z.upper()+' / '+label)
 ImageDraw.Draw(out).text((18,772),'Independent construction zone / '+names[z]+' / source cameras are uncalibrated',font=small,fill='#c6cbd4');out.save(r/('comparison-zone-'+z+'.jpg'),quality=95);combined.paste(out,(0,i*800))
combined.save(r/'reference-comparison.jpg',quality=95)
clay=Image.new('RGB',(3200,3*600),'#191d24');reflection=Image.new('RGB',(2400,3*820),'#191d24');control=Image.new('RGB',(2400,3*820),'#191d24')
for i,z in enumerate(['a','b','c']):
 views=['front','front34','side','close'] if z=='a' else ['side','rear34','rear','close']
 for j,v in enumerate(views):panel(clay,Image.open(r/('zone-'+z)/('clay-'+v+'.png')),(j*800,i*600,800,600),'ZONE '+z.upper()+' / '+v.upper())
 for j,n in enumerate(['reflection','zebra']):panel(reflection,Image.open(r/('zone-'+z)/(n+'.png')),(j*1200,i*820,1200,820),'ZONE '+z.upper()+' / '+n.upper())
 for j,n in enumerate(['base-control','control-sections']):panel(control,Image.open(r/('zone-'+z)/(n+'.png')),(j*1200,i*820,1200,820),'ZONE '+z.upper()+' / '+n.upper())
clay.save(r/'clay-diagnostics.jpg',quality=95);reflection.save(r/'reflection-zebra-diagnostics.jpg',quality=95);control.save(r/'control-net-sections.jpg',quality=95)
print('Prototype comparison, clay, reflection/zebra and control-net boards saved')
