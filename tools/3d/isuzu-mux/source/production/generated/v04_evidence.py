from pathlib import Path
import os,json
from PIL import Image,ImageOps,ImageDraw,ImageFont
O=Path(os.environ.get('MUX_V04_OUTPUT',Path(__file__).resolve().parents[3]));R=O/'renders/v04';BASE=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux')
REF=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',21);H=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',26)
views=[('front','18-17-10'),('front_34','18-17-27'),('side','18-17-14'),('rear_34','18-17-35'),('rear','18-17-18')]
reference_crop={'front':(335,100,740,500),'front_34':(125,100,900,505),'side':(125,105,950,475),'rear_34':(105,110,920,510),'rear':(325,115,730,495)}
model_crop={'front':(190,40,775,625),'rear':(190,40,775,625),'side':(70,155,890,495),'front_34':(100,140,865,570),'rear_34':(100,140,865,570)}
def photo(t):return REF/('Screenshot From 2026-11-06 '+t+'.png')
def image(path,view,reference=False):return Image.open(path).convert('RGB').crop((reference_crop if reference else model_crop)[view])
def sheet(path,title,rows):
 cw=570;ch=460;out=Image.new('RGB',(cw*max(len(row) for row in rows),75+ch*len(rows)),(27,29,32));draw=ImageDraw.Draw(out);draw.text((20,18),title,fill='white',font=H)
 for i,row in enumerate(rows):
  for j,(label,im) in enumerate(row):
   im=ImageOps.contain(im,(cw-16,ch-50));x=j*cw;y=75+i*ch;out.paste(im,(x+(cw-im.width)//2,y+42+(ch-50-im.height)//2));draw.text((x+10,y+5),label,fill='white',font=F)
 out.save(path,quality=93)
def comparison(keys):
 return [[('Reference / '+n,image(photo(t),n,True)),('V02 / '+n,image(BASE/'renders/refinement-v02'/('v02-'+n+'.png'),n)),('V03 / '+n,image(BASE/'renders/v03'/('v03-identity-'+n+'.png'),n)),('V04 / '+n,image(R/('v04-final-'+n+'.png'),n))] for n,t in views if n in keys]
sheet(R/'v04-front-gate.jpg','Front gate: V04 better than both earlier versions = YES',comparison(['front','front_34']))
sheet(R/'v04-side-gate.jpg','Side gate: clear MU-X identity improvement = NO',comparison(['front_34','side','rear_34']))
sheet(R/'v04-rear-gate.jpg','Rear gate: clear improvement over both baselines = NO',comparison(['rear_34','rear']))
items=[(n.upper(),image(R/('v04-final-'+n+'.png'),n)) for n,t in views];sheet(R/'v04-turnaround.jpg','V04 neutral turnaround / PARTIAL IMPROVEMENT — stop before detailing',[items[0:2],items[2:4],items[4:5]])
image(R/'v04-final-front_34.png','front_34').save(R/'v04-badgeless-recognition.jpg',quality=95)
(O/'source/production/generated/v04-evidence-crops.json').write_text(json.dumps({'reference_files_by_view':dict(views),'reference_crop_pixels':reference_crop,'same_crop_for_all_model_versions':model_crop,'method':'Manual vehicle-framing crops, aspect ratio preserved with contain. Same fixed camera pixels for V02/V03/V04; photos approximately framed/scaled for visual comparison only. Not photogrammetric registration.'},indent=2));print('V04 required gate sheets, turnaround and uncaptioned badgeless image saved')
