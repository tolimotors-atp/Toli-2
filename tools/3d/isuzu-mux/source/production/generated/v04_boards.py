from pathlib import Path
import os,json
from PIL import Image,ImageOps,ImageDraw,ImageFont
O=Path(os.environ.get('MUX_V04_OUTPUT',Path(__file__).resolve().parents[3]));A=O/'source/production/generated';R=O/'renders/v04';REF=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');plan=json.loads((A/'v04-reference-plan.json').read_text());F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',22)
for region,d in plan['regions'].items():
 out=Image.new('RGB',(1800,510),(28,29,32));draw=ImageDraw.Draw(out)
 for i,t in enumerate([d['primary']]+d['secondary']):
  p=REF/('Screenshot From 2026-11-06 '+t+'.png');im=ImageOps.contain(Image.open(p).convert('RGB'),(590,440));out.paste(im,(i*600+(600-im.width)//2,60+(440-im.height)//2));draw.text((i*600+12,12),('PRIMARY' if i==0 else 'SECONDARY '+str(i))+' / '+t,fill='white',font=F)
 out.save(R/('reference-board-'+region+'.jpg'),quality=93)
# Pixel-grid annotations describe image ratios only, never real-world distances.
for region,t in [('front','18-17-10'),('rear','18-17-18')]:
 p=REF/('Screenshot From 2026-11-06 '+t+'.png');im=Image.open(p).convert('RGB');draw=ImageDraw.Draw(im);d=plan['normalized_measurements'][region];box=d['reference_bounds'];draw.rectangle(box,outline='#ff334b',width=2);draw.line(((box[0]+box[2])/2,box[1],(box[0]+box[2])/2,box[3]),fill='#ff334b',width=2);im.save(R/('normalized-'+region+'-grid.png'))
print('Five regional reference boards and normalized front/rear grids saved')
