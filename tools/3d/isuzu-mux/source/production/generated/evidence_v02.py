from PIL import Image,ImageOps,ImageDraw,ImageFont
from pathlib import Path
import os
O=Path(os.environ.get('MUX_V02_OUTPUT',Path(__file__).resolve().parents[3]));R=O/'renders/refinement-v02';OUT=O/'renders';F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',22);H=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',27);refs=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X')
views=[('front','18-17-10'),('front_34','18-17-25'),('side','18-17-14'),('rear_34','18-17-35'),('rear','18-17-18')]
def ref(t):return refs/('Screenshot From 2026-11-06 '+t+'.png')
def sheet(path,title,rows):
 cols=max(len(row) for row in rows);cw=600;ch=460;out=Image.new('RGB',(cols*cw,80+ch*len(rows)),(27,29,32));d=ImageDraw.Draw(out);d.text((22,20),title,fill='white',font=H)
 for i,row in enumerate(rows):
  for j,(label,p) in enumerate(row):
   x=j*cw;y=80+i*ch;im=ImageOps.contain(Image.open(p).convert('RGB'),(cw-16,ch-48));out.paste(im,(x+(cw-im.width)//2,y+42+(ch-48-im.height)//2));d.text((x+12,y+5),label,fill='#eeeeee',font=F)
 out.save(path,quality=93)
sheet(R/'baseline-v01.jpg','V01 baseline / fixed neutral comparison cameras',[[('V01 '+n,R/('baseline-'+n+'.png'))] for n,t in views])
def comparisons(keys):return [[('Reference / '+n,ref(t)),('V01 / '+n,R/('baseline-'+n+'.png')),('V02 / '+n,R/('v02-'+n+'.png'))] for n,t in views if n in keys]
sheet(R/'front-v02.jpg','Front identity / reference, V01, V02',comparisons(['front','front_34']))
sheet(R/'greenhouse-v02.jpg','Greenhouse / same before-and-after cameras',comparisons(['front_34','side','rear_34']))
sheet(R/'fenders-v02.jpg','Fender volume / same before-and-after cameras',comparisons(['front_34','side','rear_34']))
sheet(R/'rear-v02.jpg','Rear identity / reference, V01, V02',comparisons(['rear_34','rear']))
sheet(OUT/'generated-final-comparison-v02.jpg','MU-X exterior refinement V02 / not production-approved',comparisons([n for n,t in views]))
sheet(OUT/'generated-surface-v02.jpg','Neutral studio reflection inspection / V01 versus V02',[[('V01 '+n,R/('baseline-'+n+'.png')),('V02 '+n,R/('v02-'+n+'.png'))] for n in ['front_34','side','rear_34']])
if (R/'motion-100-front_34.png').exists():sheet(R/'motion-v02.jpg','V02 motion poses / discrete angular samples, clearance not certified',[[('Opening '+str(f)+'% / front',R/('motion-'+str(f)+'-front_34.png')),('Opening '+str(f)+'% / rear',R/('motion-'+str(f)+'-rear_34.png'))] for f in [0,25,50,75,100]])
print('V02 diagnostic sheets saved')
