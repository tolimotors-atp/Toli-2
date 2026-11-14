from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,os
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux');O=Path(os.environ.get('MUX_GREENHOUSE_OUTPUT',Path(__file__).resolve().parents[3]));A=O/'source/reconstruction/greenhouse-v02';R=O/'renders'
font=ImageFont.truetype('/usr/share/fonts/TTF/DejaVuSans.ttf',16) if Path('/usr/share/fonts/TTF/DejaVuSans.ttf').exists() else ImageFont.load_default(size=16)
crops={'O07':(325,123,900,252),'O09':(115,120,735,255),'O06':(350,115,705,262),'O08':(350,135,705,267),'O11':(315,112,855,262),'O10':(300,100,850,290),'O12':(300,90,900,290),'O13':(260,90,950,300),'O02':(235,60,955,275),'O04':(220,50,990,275),'S13':(120,65,485,200),'S21':(120,70,530,240),'S19':(130,35,525,175)}
roles=[('Windscreen','O06','O11','O10'),('A-pillar','O07','O06','O09'),('Roof','O07','O11','O12'),('Front side glass','O07','O09','O11'),('B-pillar','O07','O09','O11'),('Rear side glass','O07','O09','O12'),('C-pillar','O07','O12','O09'),('Quarter glass','O07','O12','S21'),('D-pillar','O12','O08','O13'),('Rear glass','O08','O12','S19')]
sheet=Image.new('RGB',(1500,2700),'#efefef');d=ImageDraw.Draw(sheet)
for row,(region,*ids) in enumerate(roles):
 y=row*270;d.text((12,y+6),region,fill='black',font=font)
 for col,(role,key) in enumerate(zip(['PRIMARY','SECONDARY','VALIDATION'],ids)):
  im=ImageOps.contain(Image.open(P/f'references/complete-library/{key}.png').crop(crops[key]).convert('RGB'),(490,220));sheet.paste(im,(col*500+(500-im.width)//2,y+46));d.text((col*500+10,y+27),role+' / '+key,fill='black',font=font)
sheet.save(R/'greenhouse-reference-board-v02.jpg',quality=94)
(A/'reference-assignments.json').write_text(json.dumps([dict(region=r,primary=p,secondary=s,validation=v) for r,p,s,v in roles],indent=2))
data=json.loads((A/'profile-projection.json').read_text());im=Image.open(P/'references/complete-library/O07.png').convert('RGB');d=ImageDraw.Draw(im)
for edge in data['edges']:d.line([tuple(a) for a in edge],fill=(255,100,0),width=2)
d.rectangle((4,4,1034,43),fill='white');d.text((10,10),'V02 orange: manually axle/floor aligned outline. Orthographic comparison; NOT calibration.',fill='black',font=font);im.save(R/'greenhouse-profile-overlay-v02.jpg',quality=96)
sheet=Image.new('RGB',(1500,2400),'#efefef');d=ImageDraw.Draw(sheet)
pairs=[('O07','side','Side profile'),('O06','front','Front depth'),('O08','rear','Rear depth'),('O11','front-left','Front 3Q'),('O12','rear-left','Rear 3Q'),('S13','neutral','Neutral perspective / supplementary reference')]
for i,(key,view,title) in enumerate(pairs):
 y=i*400;d.text((12,y+6),title+' — illustrative camera, not pixel-fitted',fill='black',font=font)
 for x,path in [(0,P/f'references/complete-library/{key}.png'),(750,R/f'greenhouse-{view}-v02.png')]:
  im=ImageOps.contain(Image.open(path).convert('RGB'),(740,360));sheet.paste(im,(x+(750-im.width)//2,y+35))
sheet.save(R/'region-greenhouse-v02.jpg',quality=94)
