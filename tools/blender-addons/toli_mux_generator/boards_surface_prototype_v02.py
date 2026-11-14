from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json

P=Path(__file__).resolve().parents[3]
R=P/'tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v02'
V1=R.parent/'crossview-surface-prototype-v01'
REF=P.parent/'Isuzu MU-X'
FONT=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',23)
SMALL=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',16)

def board(cols,rows,w=900,h=650):return Image.new('RGB',(cols*w,rows*h),'#191d24')
def panel(canvas,im,col,row,label,w=900,h=650):
 im=ImageOps.contain(im.convert('RGB'),(w-24,h-72));x=col*w;y=row*h
 canvas.paste(im,(x+(w-im.width)//2,y+52+(h-72-im.height)//2))
 ImageDraw.Draw(canvas).text((x+14,y+10),label,font=FONT,fill='white')

refs={
 'a': [('front','18-17-10',(320,100,720,490)),('front34','18-17-27',(145,150,650,465)),('side','18-17-14',(130,145,485,460))],
 'b': [('side','18-17-14',(560,120,935,330)),('rear34','18-17-31',(490,110,880,305)),('rear','18-17-18',(340,125,705,320))],
 'c': [('side','18-17-14',(650,230,935,460)),('rear34','18-17-31',(420,220,900,495)),('rear','18-17-18',(340,240,705,490))]}
combined=board(3,3)
for row,(z,views) in enumerate(refs.items()):
 out=board(3,3)
 for i,(view,t,crop) in enumerate(views):
  photo=Image.open(REF/f'Screenshot From 2026-11-06 {t}.png').crop(crop)
  for j,(im,label) in enumerate([(photo,'REFERENCE'),(Image.open(V1/f'zone-{z}/clay-{view}.png'),'V01'),(Image.open(R/f'zone-{z}/clay-{view}.png'),'V02')]):
   panel(out,im,j,i,f'ZONE {z.upper()} / {view.upper()} / {label}')
   if i==1:panel(combined,im,j,row,f'ZONE {z.upper()} / {label}')
 ImageDraw.Draw(out).text((18,out.height-22),'Same V01/V02 camera + studio. Photos are uncalibrated; crops identify the corresponding region.',font=SMALL,fill='#b8c1cd')
 out.save(R/f'comparison-zone-{z}.jpg',quality=95)
combined.save(R/'reference-comparison.jpg',quality=95)

clay=board(4,3,w=800,h=600);reflection=board(4,3,w=800,h=600);control=board(4,3,w=800,h=600)
sections=board(2,3,w=1000,h=730)
for i,z in enumerate('abc'):
 views=['front','front34','side','close'] if z=='a' else ['side','rear34','rear','close'];primary=views[1]
 for j,v in enumerate(views):panel(clay,Image.open(R/f'zone-{z}/clay-{v}.png'),j,i,f'{z.upper()} / {v.upper()}',800,600)
 for j,(folder,name) in enumerate([(V1,'reflection'),(V1,'zebra'),(R,'reflection'),(R,'zebra')]):panel(reflection,Image.open(folder/f'zone-{z}/{name}.png'),j,i,f'{z.upper()} / {"V01" if folder==V1 else "V02"} / {name}',800,600)
 for j,(name,label) in enumerate([(f'base-{primary}','BASE'),(f'clay-{primary}','LEVEL 2'),('base-close','BASE CLOSE'),('clay-close','LEVEL 2 CLOSE')]):panel(control,Image.open(R/f'zone-{z}/{name}.png'),j,i,f'{z.upper()} / {label}',800,600)
 for j,name in enumerate(['control-sections',f'clay-{primary}']):panel(sections,Image.open(R/f'zone-{z}/{name}.png'),j,i,f'{z.upper()} / {name.upper()}',1000,730)
for name,im in [('clay-diagnostics.jpg',clay),('reflection-zebra-diagnostics.jpg',reflection),('control-net-evaluation.jpg',control),('control-net-sections.jpg',sections)]:im.save(R/name,quality=95)

data=json.loads((R/'bonnet-edge-roll-sections.json').read_text());im=Image.new('RGB',(2400,1150),'#191d24');d=ImageDraw.Draw(im)
colors={'V01': '#8db5cd','V02':'#ff6974'}
for col in range(5):
 x0=col*480+55;y0=85;w=390;h=850
 d.text((x0-25,15),['LEADING','25%','50%','75%','COWL'][col],font=FONT,fill='white')
 for z in [.4,.6,.8,1.,1.2,1.4]:
  y=y0+h*(1.5-z)/1.2;d.line((x0,y,x0+w,y),fill='#353b44');d.text((x0-40,y-10),str(z),font=SMALL,fill='#aab3c0')
 for ver in ['V01','V02']:
  for state in ['base','evaluated']:
   for a,b in data[ver][col][state]:
    xy=[(x0+v[0]*w,y0+(1.5-v[1])/1.2*h) for v in [a,b]]
    d.line(xy,fill=colors[ver] if state=='evaluated' else '#65717c',width=4 if state=='evaluated' else 1)
 d.text((x0,970),f'X = {data["V02"][col]["x"]:.4f}',font=SMALL,fill='white')
d.text((55,1040),'V01 evaluated: blue | V02 evaluated: red | base nets: thin grey. Actual Y/Z mesh-plane intersections.',font=FONT,fill='white')
d.text((55,1085),'Identical axes. Cowl root is an open construction cut, not a completed A-pillar. Units are uncalibrated model coordinates.',font=SMALL,fill='#b8c1cd')
im.save(R/'bonnet-edge-roll-sections.png')
assert all(len(data[v])==5 and all(row['base'] and row['evaluated'] for row in data[v]) for v in ['V01','V02'])
print('Matched comparisons, cross-sections and diagnostic boards saved')
