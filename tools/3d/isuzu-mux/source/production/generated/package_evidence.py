from PIL import Image,ImageOps,ImageDraw,ImageFont
from pathlib import Path
import json,hashlib
O=Path(__file__).resolve().parents[3];R=O/'renders';A=O/'source/production/generated';ref=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X')
font=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',20) if Path('/usr/share/fonts/noto/NotoSans-Regular.ttf').exists() else ImageFont.load_default()
def reference(t):return ref/('Screenshot From 2026-11-06 '+t+'.png')
def sheet(name,title,items):
 w=1400;cw=700;ch=530;out=Image.new('RGB',(w,80+ch*((len(items)+1)//2)),(28,29,32));d=ImageDraw.Draw(out);d.text((24,22),title,fill='white',font=font)
 for i,(label,path) in enumerate(items):
  x=i%2*cw;y=80+i//2*ch;im=ImageOps.contain(Image.open(path).convert('RGB'),(cw-20,ch-55));out.paste(im,(x+(cw-im.width)//2,y+35+(ch-55-im.height)//2));d.text((x+14,y+4),label,fill='white',font=font)
 out.save(R/(name+'.jpg'),quality=93)
pairs=[('front','18-17-10'),('side','18-17-14'),('rear','18-17-18'),('front3q','18-17-25'),('rear3q','18-17-35')]
for kind,t in pairs[:3]:sheet('generated-'+kind+'-v01','MU-X generated candidate / '+kind+' / NEEDS WORK',[('Supplied reference',reference(t)),('Fresh authored candidate',R/('generated-closed-'+kind+'.png'))])
sheet('generated-greenhouse-v01','Greenhouse inspection / NEEDS WORK',[('Canonical side',reference('18-17-14')),('Candidate side',R/'generated-closed-side.png'),('Canonical rear three-quarter',reference('18-17-35')),('Candidate rear three-quarter',R/'generated-closed-rear3q.png')])
sheet('generated-blockout-v01','Fresh blockout / broad-shape study',[(k,R/('generated-blockout-'+k+'.png')) for k in ['front','side','rear','front3q']])
sheet('generated-surface-v01','Neutral PBR reflection and open-panel inspection / NEEDS WORK',[(k,R/(k+'.png')) for k in ['generated-studio-closed-front3q','generated-studio-closed-rear3q','generated-studio-open-front3q','generated-studio-open-rear3q']])
items=[]
for k,t in pairs:items.extend([('Reference / '+k,reference(t)),('Candidate / '+k,R/('generated-closed-'+k+'.png'))])
sheet('generated-final-comparison-v01','Reference comparison / generated candidate / NOT APPROVED',items)
print('Seven diagnostic JPGs created')
