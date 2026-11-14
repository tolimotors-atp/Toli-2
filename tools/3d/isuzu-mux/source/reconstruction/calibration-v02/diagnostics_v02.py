from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import json,math
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'source/reconstruction/calibration-v02';S=json.loads((OUT/'v02-solution.json').read_text());A=json.loads((OUT/'all-observations-v02.json').read_text());OLD=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/reconstruction');D=json.loads((OLD/'observations.json').read_text());images={r['image']:r for r in D['images']};ids=sorted(map(int,S['per_camera']))
W,H=1800,1880
sheet=Image.new('RGB',(W,H),(27,29,33));heat=Image.new('RGB',(W,H),(27,29,33));sd=ImageDraw.Draw(sheet);hd=ImageDraw.Draw(heat)
sd.text((12,10),'V02 STRUCTURAL CALIBRATION — GATE FAIL / CORE8 + ALL EXTERNAL VIEWS SHOWN',fill='white');sd.text((12,32),f'Train {S["training"]["rms"]:.2f}px / held-out {S["heldout"]["rms"]:.2f}px / geometry-LOVO {S["lovo_aggregate"]["rms"]:.2f}px / worst LOVO {S["lovo_aggregate"]["max"]:.2f}px',fill='#ffb87a');sd.text((12,54),'Yellow A / blue B observed; white squares held out; cyan projected; red vectors >10px. Grey marks = not fitted.',fill='white')
hd.text((12,10),'V02 LANDMARK-SAMPLED RESIDUAL HEATMAP — NOT A DENSE SURFACE ERROR ESTIMATE',fill='white');hd.text((12,32),'Green <=3px / yellow 3-5px / orange 5-10px / red >10px. Grey excluded picks have NO V02 error estimate.',fill='white');hd.text((12,54),'Largest current residuals: held-out rear lamps and external static-lamp projections. Removed picks stay grey.',fill='#ffb87a')
def color(e):return '#29d37d' if e<=3 else '#ffe54f' if e<=5 else '#ff9a32' if e<=10 else '#ff2639'
for k,i in enumerate(ids):
 x=k%3*600;y=k//3*450+85;c=S['per_camera'][str(i)];im=Image.open(images[i]['path']).convert('RGB');hm=Image.blend(im,Image.new('RGB',im.size,(20,22,26)),.35);draw=ImageDraw.Draw(im);dh=ImageDraw.Draw(hm)
 for o in [o for o in A if o['camera']==i]:
  a,b=o['xy'];v=o['v02_prediction']
  if v is None:
   for d in [draw,dh]:d.line((a-3,b-3,a+3,b+3),fill='#999999');d.line((a-3,b+3,a+3,b-3),fill='#999999')
   continue
  u,v=v;res=o['v02_residual'];col='#ff2525' if res>10 else '#00ccef';draw.line((a,b,u,v),fill=col,width=2)
  if 'HELD' in o['v02_status'] or o['v02_status']=='EXTERNAL VALIDATION':draw.rectangle((a-4,b-4,a+4,b+4),outline='white',width=2)
  else:draw.ellipse((a-3,b-3,a+3,b+3),outline='#ffdf50' if o['confidence']=='A' else '#75c5ff',width=2)
  draw.line((u-4,v,u+4,v),fill='#00ffff',width=2);draw.line((u,v-4,u,v+4),fill='#00ffff',width=2)
  radius=5+min(12,int(res*.5));dh.ellipse((a-radius,b-radius,a+radius,b+radius),outline=color(res),width=3);dh.line((a,b,u,v),fill=color(res),width=2)
 role='CORE' if c['included'] else 'EXTERNAL / NOT GEOMETRY FIT'
 if not c['included'] and c['pose_rank']<6:role+=' / POSE UNDERCONSTRAINED'
 for d in [sd,hd]:d.text((x+8,y+5),f'Image {i} / {role}',fill='white')
 for target,img in [(sheet,im),(heat,hm)]:
  img=ImageOps.contain(img,(590,355));target.paste(img,(x+(600-img.width)//2,y+36+(355-img.height)//2))
 held=c['heldout']['rms'] if c['included'] else c['independent_projection']['rms'];label='held-out' if c['included'] else 'independent'
 text=f'N={c["observations"]} RMS={c["all"]["rms"]:.2f}px Median={c["all"]["median"]:.2f}px Max={c["all"]["max"]:.2f}px'
 for d in [sd,hd]:d.text((x+8,y+399),text,fill='#ffb87a');d.text((x+8,y+420),f'{label}: {held:.2f}px / focal convention {c["focal_36mm"]:.2f}mm / GLOBAL FAIL',fill='white')
sheet.save(ROOT/'renders/multiview-camera-solve-v02.jpg',quality=95);heat.save(ROOT/'renders/multiview-residual-heatmap-v02.jpg',quality=95)
# Separate twelve-view visual audit still shows every excluded camera, not just the lower-error core.
(OUT/'visual-inspection-v02.json').write_text(json.dumps({'status':'FAIL','required_manual_review':'All 12 exterior projection panels and sampled heatmap','known_failed_regions':['Core image 12/13 held-out fixed lamp corners','LOVO image 9 structural windshield projections','External rear image 3 static lamp projection'],'excluded_observations_shown_in_grey':True,'no_dense_surface_error_claim':True},indent=2)+'\n')
print('Saved V02 projection diagnostics and sampled heatmap for all 12 exterior views.')
