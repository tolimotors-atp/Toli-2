from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import os,shutil
O=Path(os.environ.get('MUX_V03_OUTPUT',Path(__file__).resolve().parents[3]));R=O/'renders/v03';REF=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');V02=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/renders/refinement-v02');F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',21);H=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',27)
views=[('front','18-17-10'),('front_34','18-17-25'),('side','18-17-14'),('rear_34','18-17-35'),('rear','18-17-18')]
def photo(t):return REF/('Screenshot From 2026-11-06 '+t+'.png')
def sheet(path,title,rows):
 cw=600;ch=460;out=Image.new('RGB',(cw*max(len(r) for r in rows),80+ch*len(rows)),(27,29,32));d=ImageDraw.Draw(out);d.text((20,20),title,fill='white',font=H)
 for i,row in enumerate(rows):
  for j,(label,p) in enumerate(row):
   im=ImageOps.contain(Image.open(p).convert('RGB'),(cw-16,ch-50));x=j*cw;y=80+i*ch;out.paste(im,(x+(cw-im.width)//2,y+42+(ch-50-im.height)//2));d.text((x+10,y+4),label,fill='white',font=F)
 out.save(path,quality=93)
sheet(R/'v03-side-guide-gate.jpg','V03 normalized side guides / not calibrated photogrammetry',[[('Normalized guide overlay',R/'v03-side-guide-overlay.png'),('Blender side guide and fixed wheels',R/'v03-guide-side.png')]])
for stage,label in [('blockout','silhouette'),('greenhouse','greenhouse'),('identity','identity')]:sheet(R/('v03-'+label+'-gate.jpg'),'V03 '+label+' gate / broad forms, no badges',[[('Canonical reference / '+n,photo(t)),('V03 '+stage+' / '+n,R/('v03-'+stage+'-'+n+'.png'))] for n,t in views])
sheet(R/'v02-v03-comparison.jpg','Reference / V02 / V03 — identity improvement threshold NOT PASSED',[[('Reference / '+n,photo(t)),('V02 / '+n,V02/('v02-'+n+'.png')),('V03 / '+n,R/('v03-identity-'+n+'.png'))] for n,t in views])
shutil.copy2(R/'v03-identity-front_34.png',R/'v03-recognition-no-badges.png');print('V03 requested comparison sheets and unlabelled recognition render saved')
