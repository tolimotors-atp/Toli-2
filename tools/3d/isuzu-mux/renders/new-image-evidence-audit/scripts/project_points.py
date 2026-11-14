from pathlib import Path
import pycolmap,json
from PIL import Image,ImageDraw,ImageOps,ImageFont
R=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/controlled-capture/reconstruction/current-folder-audit/small');out=[];F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',20)
for k in [0,1]:
 model=pycolmap.Reconstruction(R/'sparse'/str(k))
 for im in model.images.values():
  if not im.has_pose:continue
  image=Image.open(R/'images'/im.name).convert('RGB');d=ImageDraw.Draw(image);coords=[]
  for p in im.points2D:
   if int(p.point3D_id) not in model.points3D:continue
   x,y=map(float,p.xy);d.ellipse((x-3,y-3,x+3,y+3),fill='#00ffb7',outline='#002f25');coords.append([x,y])
  d.rectangle((0,0,image.width,40),fill='#171b22');d.text((10,7),f'Model {k} / {im.name} / observed tracks {len(coords)} / GEOMETRY NOT VALIDATED',font=F,fill='white');name=f'model-{k}-{im.name}.jpg';image.save(R/'diagnostics'/name,quality=94);out.append({'model':k,'image':im.name,'observed_track_count':len(coords),'points2D':coords,'overlay':str(R/'diagnostics'/name)})
(R/'diagnostics/observed-vehicle-tracks.json').write_text(json.dumps(out,indent=2));print([(x['model'],x['image'],x['observed_track_count']) for x in out])
