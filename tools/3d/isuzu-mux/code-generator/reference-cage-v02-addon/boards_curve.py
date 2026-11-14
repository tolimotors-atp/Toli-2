from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');r=P/'tools/3d/isuzu-mux/code-generator/renders/curve-validation';src=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');f=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',16)
views=[('front','18-17-10','front',(340,110,740,505)),('front34','18-17-27','front_34',(145,105,890,505)),('side','18-17-14','side',(130,110,950,480)),('rear34','18-17-35','rear_34',(120,110,895,495)),('rear','18-17-18','rear',(340,120,730,505))]
b=Image.new('RGB',(1500,1550),'#222327');d=ImageDraw.Draw(b)
for i,(view,t,old,box) in enumerate(views):
 ref=Image.open(src/f'Screenshot From 2026-11-06 {t}.png').convert('RGB');net=Image.open(r/f'{view}.png').convert('RGBA');dark=Image.new('RGBA',net.size,(25,25,29,255));dark.alpha_composite(net)
 for j,(label,im) in enumerate([('REFERENCE',ref.crop((5,65,1033,530))),('V04',Image.open(P/f'tools/3d/isuzu-mux/renders/v04/v04-final-{old}.png')),('CURVES ONLY / gate pending',dark.convert('RGB'))]):
  pic=ImageOps.contain(im,(490,275));b.paste(pic,(j*500+(500-pic.width)//2,i*310+30));d.text((j*500+5,i*310+5),label+' / '+view,font=f,fill='white')
 alpha=net.getchannel('A');mask=ImageOps.contain(alpha.crop(alpha.getbbox()),(box[2]-box[0],box[3]-box[1]));canvas=Image.new('L',ref.size);canvas.paste(mask,(box[0]+(box[2]-box[0]-mask.width)//2,box[1]+(box[3]-box[1]-mask.height)//2));ref.paste((0,210,240),mask=canvas);ImageDraw.Draw(ref).text((8,10),'Approximate 2D box-fit; NOT a solved photo camera',font=f,fill='red');ref.save(r/f'overlay-{view}.jpg',quality=93)
b.save(r/'reference-v04-curves.jpg',quality=93)
