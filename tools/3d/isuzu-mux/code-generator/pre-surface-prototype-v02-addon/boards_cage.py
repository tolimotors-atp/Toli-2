from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import runpy
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');a=P/'tools/blender-addons/toli_mux_generator';r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v01';src=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');data=runpy.run_path(str(a/'traced_data.py'));f=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',14)
for source,filename in data['SOURCES'].items():
 im=Image.open(src/filename).convert('RGB');d=ImageDraw.Draw(im)
 for name,(s,pts,depth,closed) in data['TRACES'].items():
  if s!=source:continue
  extended=pts+[pts[0]] if closed else pts
  d.line(extended,fill=(0,215,255),width=2)
  for u,v in pts:d.ellipse((u-2,v-2,u+2,v+2),fill=(255,90,40))
 d.text((10,10),'Native hand-picked pixel landmarks / polygon guides; not a camera solve',font=f,fill='red');im.save(r/f'native-traces-{source}.jpg',quality=94)
views=[('front','18-17-10','front'),('front34','18-17-27','front_34'),('side','18-17-14','side'),('rear34','18-17-35','rear_34'),('rear','18-17-18','rear')];b=Image.new('RGB',(1800,1550),'#222327');d=ImageDraw.Draw(b)
for i,(v,t,old) in enumerate(views):
 images=[Image.open(src/f'Screenshot From 2026-11-06 {t}.png').crop((5,65,1033,530)),Image.open(P/f'tools/3d/isuzu-mux/renders/v04/v04-final-{old}.png'),Image.open(P/f'tools/3d/isuzu-mux/code-generator/renders/deep-detail-v01/clay-{v}.png'),Image.open(r/f'{v}.png')]
 for j,im in enumerate(images):
  if im.mode=='RGBA':bg=Image.new('RGBA',im.size,(20,20,24,255));bg.alpha_composite(im);im=bg.convert('RGB')
  im=ImageOps.contain(im.convert('RGB'),(440,275));b.paste(im,(450*j+(450-im.width)//2,310*i+30));d.text((450*j+5,310*i+5),['REFERENCE','V04','SOFT V01','NEW CAGE / NO BODY'][j]+' / '+v,font=f,fill='white')
b.save(r/'four-state-comparison.jpg',quality=94)
