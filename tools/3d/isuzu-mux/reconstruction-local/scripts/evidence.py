from pathlib import Path
from PIL import Image,ImageDraw,ImageFont,ImageOps
import json,sqlite3
r=Path(__file__).resolve().parents[1];project=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',19)
# Updated mask sheet shows the actual ROIs used by COLMAP.
board=Image.new('RGB',(1600,1040),'#191b20');dr=ImageDraw.Draw(board)
for i,p in enumerate(sorted((r/'input/primary').glob('*.png'))):
 im=Image.open(p).convert('RGB');ma=Image.open(r/'masks'/(p.name+'.png'));masked=Image.composite(im,im.point(lambda v:int(v*.18)),ma)
 for j,a in enumerate([im,masked]):
  x=(i%2)*800+j*400;y=(i//2)*260;pic=ImageOps.contain(a,(394,220));board.paste(pic,(x+(400-pic.width)//2,y+30));dr.text((x+5,y+3),p.stem+(' input' if j==0 else ' conservative ROI'),font=F,fill='white')
board.save(r/'comparisons/input-mask-contact.jpg',quality=93)
man=json.loads((r/'input/manifest.json').read_text())
for entry in man['originals']:
 for d in entry['derived']:
  if d['path'].endswith(('18-17-31.png','18-17-35.png')):d['mask_method']='conservative rectangular ROI after visual correction to retain roof/tires; rectangle recorded in scripts/run_sfm.py'
(r/'input/manifest.json').write_text(json.dumps(man,indent=2))
views=[('front','18-17-10'),('front_34','18-17-27'),('side','18-17-14'),('rear_34','18-17-35'),('rear','18-17-18')]
board=Image.new('RGB',(1500,5*330+85),'#191b20');dr=ImageDraw.Draw(board)
for j,label in enumerate(['USER REFERENCE','LOCAL MiDaS: relative inverse depth','V04: existing render, unchanged']):dr.text((j*500+10,8),label,font=F,fill='white')
dr.text((10,40),'Diagnostic comparison ONLY: no recovered cameras/mesh; columns are not calibrated or geometrically aligned.',font=F,fill='#ffbba5')
for i,(view,name) in enumerate(views):
 y=85+i*330
 for j,path in enumerate([r/'input/primary'/f'{name}.png',r/'calibration/depth'/f'{name}-preview.png',project/'tools/3d/isuzu-mux/renders/v04'/f'v04-final-{view}.png']):
  pic=ImageOps.contain(Image.open(path).convert('RGB'),(490,290));board.paste(pic,(j*500+(500-pic.width)//2,y+30))
  dr.text((j*500+10,y+2),view.replace('_',' ')+' / '+('input' if j==0 else 'NOT METRIC' if j==1 else 'baseline'),font=F,fill='white')
board.save(r/'comparisons/five-view-reference-depth-v04.jpg',quality=94)
con=sqlite3.connect(r/'calibration/registration.db');s=json.loads((r/'logs/sfm-result.json').read_text());names=dict(con.execute('select image_id,name from images'))
rows=[]
for pair,n,config in s['verified_pairs']:
 a,b=divmod(pair,2147483647);rows.append({'image1':names[a],'image2':names[b],'verified_inliers':n,'configuration':config})
(r/'calibration/pair-summary.json').write_text(json.dumps(rows,indent=2))
sumstats={'images_submitted':8,'images_registered':0,'sparse_points':0,'features':sum(n for _,n in s['features']),'pairs_tested':len(s['raw_matches']),'raw_matches':sum(n for _,n in s['raw_matches']),'pairs_with_verified_inliers':sum(n>0 for _,n,_ in s['verified_pairs']),'verified_inliers_sum':sum(n for _,n,_ in s['verified_pairs']),'max_pair_inliers':max(n for _,n,_ in s['verified_pairs']),'accepted_models':len(s['models'])}
assert sumstats['pairs_tested']==28 and not s['models']
(r/'logs/summary.json').write_text(json.dumps(sumstats,indent=2));print(sumstats)
