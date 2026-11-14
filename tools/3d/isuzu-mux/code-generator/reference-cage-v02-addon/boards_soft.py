from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');r=P/'tools/3d/isuzu-mux/code-generator/renders/deep-detail-v01';src=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');f=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',16)
views=[('front','18-17-10','front',(340,110,740,505)),('front34','18-17-27','front_34',(145,105,890,505)),('side','18-17-14','side',(130,110,950,480)),('rear34','18-17-35','rear_34',(120,110,895,495)),('rear','18-17-18','rear',(340,120,730,505))];board=Image.new('RGB',(1500,1550),'#222327');d=ImageDraw.Draw(board)
for i,(view,t,old,box) in enumerate(views):
 ref=Image.open(src/f'Screenshot From 2026-11-06 {t}.png').convert('RGB');generated=Image.open(r/f'clay-{view}.png')
 for j,(label,im) in enumerate([('REFERENCE',ref.crop((5,65,1033,530))),('V04',Image.open(P/f'tools/3d/isuzu-mux/renders/v04/v04-final-{old}.png')),('PRIMARY BODY / DETAILS GATED',generated)]):
  im=ImageOps.contain(im.convert('RGB'),(490,275));board.paste(im,(j*500+(500-im.width)//2,i*310+30));d.text((j*500+5,i*310+5),label+' / '+view,font=f,fill='white')
 alpha=Image.open(r/f'alpha-{view}.png').getchannel('A');mask=ImageOps.contain(alpha.crop(alpha.getbbox()),(box[2]-box[0],box[3]-box[1]));full=Image.new('L',ref.size);full.paste(mask,(box[0]+(box[2]-box[0]-mask.width)//2,box[1]+(box[3]-box[1]-mask.height)//2));ref=Image.blend(ref,Image.composite(Image.new('RGB',ref.size,(10,180,220)),ref,full),.35);ImageDraw.Draw(ref).text((8,10),'Approximate box-fit silhouette, NOT calibrated alignment',font=f,fill='red');ref.save(r/f'overlay-{view}.jpg',quality=93)
board.save(r/'reference-v04-new.jpg',quality=93)
regions={'bonnet':('front34',(.02,.22,.65,.63)),'front-fender':('front34',(.03,.40,.56,.95)),'headlight-grille':('front',(.18,.40,.82,.78)),'greenhouse':('side',(.15,.12,.91,.58)),'side-body':('side',(.15,.42,.90,.86)),'quarter-glass-d-pillar':('rear34',(.03,.14,.57,.60)),'rear-quarter':('rear34',(.03,.36,.67,.94)),'tail-lamp-rear':('rear',(.13,.32,.87,.94))}
for name,(view,crop) in regions.items():
 t=next(t for v,t,_,_ in views if v==view);im1=Image.open(src/f'Screenshot From 2026-11-06 {t}.png').crop((5,65,1033,530));im2=Image.open(r/f'clay-{view}.png');b=Image.new('RGB',(1400,500),'#222327');dr=ImageDraw.Draw(b)
 for j,im in enumerate([im1,im2]):
  im=ImageOps.fit(im.convert('RGB'),(1000,667));im=im.crop(tuple(int(c*(1000 if k%2==0 else 667)) for k,c in enumerate(crop)));im=ImageOps.contain(im,(690,460));b.paste(im,(j*700,35));dr.text((j*700+5,8),('REFERENCE' if j==0 else 'UNAPPROVED BODY / details not built')+' / '+name,font=f,fill='white')
 b.save(r/f'region-{name}.jpg',quality=93)
