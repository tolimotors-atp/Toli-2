from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont,ImageFilter
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');r=P/'tools/3d/isuzu-mux/code-generator/renders/v02';src=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');font=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',16)
views=[('front','18-17-10','front',(340,110,740,505)),('front34','18-17-27','front_34',(145,105,890,505)),('side','18-17-14','side',(130,110,950,480)),('rear34','18-17-35','rear_34',(120,110,895,495)),('rear','18-17-18','rear',(340,120,730,505))]
b=Image.new('RGB',(1500,1550),'#222327');d=ImageDraw.Draw(b)
for i,(view,t,old,box) in enumerate(views):
 ref=Image.open(src/f'Screenshot From 2026-11-06 {t}.png').convert('RGB');new=Image.open(r/f'{view}.png').convert('RGB')
 for j,(label,im) in enumerate([('Reference',ref.crop((5,65,1033,530))),('V04',Image.open(P/f'tools/3d/isuzu-mux/renders/v04/v04-final-{old}.png')),('Code V02',new)]):
  pic=ImageOps.contain(im,(490,275));b.paste(pic,(j*500+(500-pic.width)//2,i*310+30));d.text((j*500+6,i*310+4),label+' / '+view,font=font,fill='white')
 alpha=Image.open(r/f'clay-{view}.png').getchannel('A');mask=alpha.crop(alpha.getbbox());mask=ImageOps.contain(mask,(box[2]-box[0],box[3]-box[1]));canvas=Image.new('L',ref.size);canvas.paste(mask,(box[0]+((box[2]-box[0])-mask.width)//2,box[1]+((box[3]-box[1])-mask.height)//2));edge=canvas.filter(ImageFilter.FIND_EDGES).point(lambda v:255 if v>35 else 0);ref.paste((0,235,255),mask=edge);ImageDraw.Draw(ref).text((10,12),'2D box-fit edge only — NOT calibrated camera alignment',font=font,fill='red');ref.save(r/f'overlay-{view}.jpg',quality=93)
b.save(r/'code-vs-v04.jpg',quality=93)
# Enlarged matched-view diagnostics; approximate normalized crops, not pixel-error scoring.
regions={'bonnet-front':('front34',(.02,.25,.70,.72)),'front-fender':('front34',(.04,.40,.56,.94)),'greenhouse':('side',(.13,.15,.90,.56)),'side-body':('side',(.13,.43,.90,.83)),'quarter-glass-d-pillar':('rear34',(.05,.15,.58,.58)),'rear-quarter':('rear34',(.04,.38,.70,.93)),'rear':('rear',(.12,.15,.88,.94))}
for name,(view,crop) in regions.items():
 t=next(t for v,t,_,_ in views if v==view);imgs=[Image.open(src/f'Screenshot From 2026-11-06 {t}.png').crop((5,65,1033,530)),Image.open(r/f'{view}.png')];board=Image.new('RGB',(1400,500),'#222327');draw=ImageDraw.Draw(board)
 for j,im in enumerate(imgs):
  im=ImageOps.fit(im.convert('RGB'),(1000,667));im=im.crop(tuple(int(c*(1000 if i%2==0 else 667)) for i,c in enumerate(crop)));im=ImageOps.contain(im,(690,460));board.paste(im,(j*700,35));draw.text((j*700+5,7),('REFERENCE' if j==0 else 'CODE V02')+' / '+name,font=font,fill='white')
 board.save(r/f'region-{name}.jpg',quality=93)
