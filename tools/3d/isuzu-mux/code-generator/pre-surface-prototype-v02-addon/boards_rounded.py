from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');r=P/'tools/3d/isuzu-mux/code-generator/renders/curve-rounded-v01';src=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');f=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',16);b=Image.new('RGB',(1500,1550),'#222327');d=ImageDraw.Draw(b)
for i,(view,t) in enumerate([('front','18-17-10'),('front34','18-17-27'),('side','18-17-14'),('rear34','18-17-35'),('rear','18-17-18')]):
 imgs=[Image.open(src/f'Screenshot From 2026-11-06 {t}.png').crop((5,65,1033,530)),Image.open(P/f'tools/3d/isuzu-mux/code-generator/renders/v02/{view}.png'),Image.open(r/f'clay-{view}.png')]
 for j,im in enumerate(imgs):
  im=ImageOps.contain(im.convert('RGB'),(490,275));b.paste(im,(j*500+(500-im.width)//2,i*310+30));d.text((j*500+5,i*310+5),['REFERENCE','CODED V02','ROUNDED CURVES'][j]+' / '+view,font=f,fill='white')
b.save(r/'reference-previous-rounded.jpg',quality=93)
