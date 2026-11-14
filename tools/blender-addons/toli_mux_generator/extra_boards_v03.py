from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json
P=Path(__file__).resolve().parents[3];R=P/'tools/3d/isuzu-mux/code-generator/renders/crossview-surface-prototype-v03';V2=R.parent/'crossview-surface-prototype-v02'
F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',24);S=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',16)
features={
 'a':[('COWL / ROOT','close',(700,35,985,270)),('BONNET ROLL','close',(100,240,690,510)),('ARCH TERMINATION','close',(410,390,950,690))],
 'b':[('QUARTER APERTURE','close',(130,150,590,620)),('D-PILLAR','close',(430,90,730,640)),('REAR-GLASS BOUNDARY','rear',(80,150,920,560)),('ROOF JUNCTION','close',(240,10,700,280))],
 'c':[('UPPER LAMP BRIDGE','close',(300,120,780,360)),('APERTURE RETURN','close',(330,260,800,470)),('LOWER CORNER','lower',(0,0,1000,700))]}
for z,items in features.items():
 im=Image.new('RGB',(2800,len(items)*610),'#191d24');d=ImageDraw.Draw(im)
 for row,(label,view,crop) in enumerate(items):
  for col,(folder,version,state) in enumerate([(V2,'V02','base'),(V2,'V02','clay'),(R,'V03','base'),(R,'V03','clay')]):
   if view=='lower':path=R/f'zone-{z}/{"v02-" if version=="V02" else ""}lower-{state}.png'
   else:path=folder/f'zone-{z}/{state}-{view}.png'
   pic=ImageOps.contain(Image.open(path).convert('RGB').crop(crop),(676,538));x=col*700;y=row*610
   im.paste(pic,(x+(700-pic.width)//2,y+56+(538-pic.height)//2));d.text((x+12,y+10),f'{label} / {version} {state.upper()}',font=F,fill='white')
 im.save(R/f'closeups-zone-{z}.jpg',quality=95)

data=json.loads((R/'root-and-pillar-sections.json').read_text());colors={'V02':'#91b9cf','V03':'#ff6c79'}
for zone,title in [('A','COWL / ROOT SECTION'),('B','D-PILLAR SECTION')]:
 n=len(data['V03'][zone]);im=Image.new('RGB',(n*600,780),'#191d24');d=ImageDraw.Draw(im)
 for i,row in enumerate(data['V03'][zone]):
  x=i*600+65;y=80;w=490;h=535
  d.text((x-35,15),f'{title} {row["position"]:.3f}',font=F,fill='white')
  xmin,xmax,ymin,ymax=(.55,1.,1.1 if i else .5,1.55) if zone=='A' else (1.85,2.40,.55,.95)
  def screen(v):
   a,b=(-v[1],v[2]) if zone=='A' else (v[0],-v[1]);return (x+(a-xmin)/(xmax-xmin)*w,y+(ymax-b)/(ymax-ymin)*h)
  d.rectangle((x,y,x+w,y+h),outline='#53606d',width=1)
  d.text((x,y+h-24),f'{xmin:.2f}',font=S,fill='#b7c2cc');d.text((x+w-48,y+h-24),f'{xmax:.2f}',font=S,fill='#b7c2cc')
  d.text((x+5,y+5),f'{ymax:.2f}',font=S,fill='#b7c2cc');d.text((x+5,y+h-48),f'{ymin:.2f}',font=S,fill='#b7c2cc')
  for ver in ['V02','V03']:
   for state in ['base','evaluated']:
    for a,b in data[ver][zone][i][state]:
     if all(xmin<=((-v[1]) if zone=='A' else v[0])<=xmax and ymin<=(v[2] if zone=='A' else -v[1])<=ymax for v in [a,b]):
      d.line([screen(a),screen(b)],fill=colors[ver] if state=='evaluated' else '#66717d',width=4 if state=='evaluated' else 1)
  d.text((x,y+h+15),'Glass-side <   > Outer body' if zone=='A' else 'X rear depth > / lateral width up',font=S,fill='white')
 d.text((30,700),'V02 evaluated blue | V03 evaluated red | base grey. Actual skin-plane cuts; construction boundaries remain open.',font=S,fill='white')
 d.text((30,735),'Nominal coordinates, not calibrated dimensions. Cross-section shape alone does not approve reference fidelity.',font=S,fill='#b7c2cc')
 im.save(R/('root-sections.png' if zone=='A' else 'd-pillar-sections.png'))
print('Defect close-ups and root/pillar section boards saved')

im=Image.new('RGB',(2000,760),'#191d24');d=ImageDraw.Draw(im)
for i,version in enumerate(['V02','V03']):
 pic=Image.open(R/f'zone-c/{"v02-" if version=="V02" else ""}lower-reflection.png');im.paste(pic,(i*1000,60));d.text((i*1000+20,15),version+' / LOWER CORNER REFLECTION',font=F,fill='white')
im.save(R/'lower-corner-reflection.jpg',quality=95)
