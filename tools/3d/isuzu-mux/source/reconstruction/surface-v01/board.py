from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageFont
import json,os
O=Path(os.environ.get('MUX_SURFACE_OUTPUT',Path(__file__).resolve().parents[3]));A=O/'source/reconstruction/surface-v01';R=O/'renders';P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux');data=json.loads((A/'projection-diagnostics.json').read_text());font=ImageFont.load_default(size=17)
for name,key in [('side','O07'),('front','O06')]:
 im=Image.open(P/f'references/complete-library/{key}.png').convert('RGB');dr=ImageDraw.Draw(im);q=data[name]
 if name=='side':a=q['front_axle'];b=q['rear_axle'];scale=506/(b[0]-a[0]);dx=280-scale*a[0];dy=455-scale*a[1]
 else:a=q['front_wheel_left'];b=q['front_wheel_right'];lo=min(a[0],b[0]);hi=max(a[0],b[0]);scale=277/(hi-lo);dx=398-scale*lo;dy=475-scale*(a[1]+b[1])/2
 for edge in q['boundary']:dr.line([(x*scale+dx,y*scale+dy) for x,y in edge],fill=(255,85,0),width=2)
 dr.rectangle((4,4,1034,42),fill='white');dr.text((10,10),'Orange = actual NURBS boundary; manual stance anchors only, NOT a solved camera fit.',fill='black',font=ImageFont.load_default(size=15));im.save(R/f'g1-windscreen-{name}-overlay-surface-v01.jpg',quality=96)
 q['overlay_similarity']=dict(scale=scale,dx=dx,dy=dy,reference=key,uncertainty='approximate contact picks; no calibrated pixel RMS')
(A/'projection-diagnostics.json').write_text(json.dumps(data,indent=2))
sheet=Image.new('RGB',(1500,2100),'#ececec');dr=ImageDraw.Draw(sheet)
rows=[('front','O06',(395,155,675,260),'PRIMARY / front'),('side','O07',(320,145,485,245),'SECONDARY / side (partly occluded; not an orthographic blueprint)'),('front-left','O11',(315,140,545,250),'VALIDATION / front 3Q'),('front-right','O10',(515,120,800,265),'CONTEXT ONLY / opposite 3Q (not another fitting target)')]
for i,(name,key,crop,label) in enumerate(rows):
 y=i*390;dr.text((12,y+8),label,fill='black',font=font)
 ref=ImageOps.contain(Image.open(P/f'references/complete-library/{key}.png').crop(crop).convert('RGB'),(725,325));sheet.paste(ref,((750-ref.width)//2,y+42))
 mod=ImageOps.contain(Image.open(R/f'g1-windscreen-close-{name}-surface-v01.png').crop((160,200,950,570)),(725,325));sheet.paste(mod,(750+(750-mod.width)//2,y+42))
dr.text((12,1570),'G1 only: 16 control points. Broad curvature diagnostic below; no roof/header or G6 evaluation.',fill='black',font=font)
im=ImageOps.contain(Image.open(R/'g1-windscreen-curvature-surface-v01.png').crop((230,200,870,560)),(1000,420));sheet.paste(im,((1500-im.width)//2,1620))
sheet.save(R/'surface-windscreen-v01.jpg',quality=96)
