from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageChops,ImageStat
import json,shutil,math
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');W=P/'tools/3d/isuzu-mux/code-reference-car';A=W/'analysis/identity-v03';O=W/'renders/identity-v03';O.mkdir(parents=True,exist_ok=True);R=P.parent/'Isuzu MU-X';V02=W/'renders/identity-v02/iteration-05'
views=['front','front-right','right','rear-right','rear'];labels=['front','front34','side','rear34','rear'];suffix=['18-17-10','18-17-27','18-17-14','18-17-31','18-17-18'];refs=[R/f'Screenshot From 2026-11-06 {s}.png' for s in suffix]
for mode in ['clay','reflection','zebra','silhouette']:
 d=O/mode;d.mkdir(exist_ok=True)
 for f in Path('/tmp/mux-v03-'+mode).glob('*'):shutil.copy2(f,d/f.name)
for f in ['headlight-debug','headlight-front-debug','rear-debug','hero-after','ai']:shutil.copy2('/tmp/mux-v03-'+f+'.jpg',O/(f+'.jpg'))
for i in range(2):shutil.copy2('/tmp/mux-v03-reference-sheet-'+str(i)+'.jpg',O/('reference-inventory-'+str(i)+'.jpg'))
def tile(path,label,w=600,h=370):
 im=ImageOps.contain(Image.open(path).convert('RGB'),(w-10,h-38));out=Image.new('RGB',(w,h),'#ddd');out.paste(im,((w-im.width)//2,34+(h-38-im.height)//2));ImageDraw.Draw(out).text((9,9),label,fill='#222');return out

def board(items,title,name,cols=3,w=600,h=370):
 out=Image.new('RGB',(w*cols,42+h*math.ceil(len(items)/cols)),'#ccc');ImageDraw.Draw(out).text((12,12),title,fill='#222')
 for i,(p,l) in enumerate(items):out.paste(tile(p,l,w,h),(i%cols*w,42+i//cols*h))
 out.save(O/name,quality=94)
items=[]
for v,l,r in zip(views,labels,refs):items.extend([(r,l+' / supplied reference'),(V02/(v+'.jpg'),l+' / preserved V02'),(O/'clay'/(v+'.jpg'),l+' / isolated V03')])
board(items,'REFERENCE | V02 | V03 / SAME COMPARISON CAMERAS / NOT APPROVED','v02-v03-five-view.jpg')
for mode in ['clay','reflection','zebra']:board([(O/mode/(v+'.jpg'),l+' / '+mode) for v,l in zip(views,labels)],'V03 '+mode.upper()+' / SAME GEOMETRY / NO BADGES','v03-'+mode+'-five-view.jpg')
for k,n in [(0,'headlight-front-comparison.jpg'),(1,'headlight-front34-comparison.jpg'),(3,'rear34-reference-comparison.jpg'),(4,'rear-reference-comparison.jpg')]:board([(refs[k],'REFERENCE'),(V02/(views[k]+'.jpg'),'V02'),(O/'clay'/(views[k]+'.jpg'),'V03')],'ISOLATED V03 / UNCALIBRATED VISUAL COMPARISON',n)
board([(refs[4],'REFERENCE rear'),(V02/'rear.jpg','V02 rear'),(refs[3],'REFERENCE rear34'),(V02/'rear-right.jpg','V02 rear34')],'REAR ERROR MAP BEFORE V03 EDITS / analysis/REAR_IDENTITY_ERROR_MAP_V03.md','rear-error-map.jpg',2,700,420)
im=Image.open(O/'rear-error-map.jpg');b=Image.new('RGB',(im.width,im.height+140),'#ddd');b.paste(im,(0,0));d=ImageDraw.Draw(b)
for i,s in enumerate(['1 Roof/glass/D-pillar: generic wedge and straight screen boundaries','2 Quarter: flat body beside wheel; insufficient compound volume','3 Lamps: projected flat quadrilateral with no corner wrap','4 Hatch: insufficient separation of glass/lamp/recess depth','5 Bumper: same smooth barrel as hatch; uncontrolled corner tangents']):d.text((12,im.height+12+i*24),s,fill='#222')
b.save(O/'rear-error-map.jpg',quality=94)
# Approximate observed headlight contours on compatible front photo; H6/H7 depth is inferred across views.
photo=R/'Screenshot From 2026-11-06 18-08-46.png';im=Image.open(photo).convert('RGB');d=ImageDraw.Draw(im)
traces={'H1':[(480,180),(495,173),(508,165)],'H2':[(454,190),(465,186),(480,180)],'H3':[(452,217),(470,223),(498,220),(515,217)],'H4':[(508,165),(514,176),(516,198),(515,217)],'H5':[(454,190),(454,200),(452,217)],'H8':[(508,165),(514,154),(517,147)]}
colors=['#d31f3b','#007cda','#2e9954','#c27b00','#8e27c4','#3344dd']
for (name,pts),color in zip(traces.items(),colors):d.line(pts,fill=color,width=2);d.text((pts[0][0]-18,pts[0][1]-10),name,fill=color,stroke_width=1,stroke_fill='white')
im.crop((420,130,550,240)).resize((650,550)).save(O/'headlight-photo-trace.jpg',quality=95)
(A/'headlight-photo-trace.json').write_text(json.dumps({'file':str(photo),'originalSize':im.size,'traces':traces,'note':'approximate observed 2D contour polylines; H6/H7 depth/crown authored from multiple views, not measured from a single photograph'},indent=2))
board([(O/'headlight-photo-trace.jpg','Observed photo contours H1-H5/H8; H6/H7 inferred depth'),(O/'headlight-debug.jpg','Actual 3D H1-H8, controls and lens / closeup zoom .65')],'REFERENCE CONTOURS | ACTUAL H1-H8 CURVE NETWORK / SEE DATA FOR FULL XYZ','headlight-reference-curves.jpg',2,800,500)
board([(refs[3],'REFERENCE rear34'),(O/'rear-debug.jpg','Actual tail-lamp/glass/bumper curves / zoom .65')],'V03 CURVE-DRIVEN TAIL LAMPS / NO FLAT REAR-FACING QUAD','taillight-curves.jpg',2,800,500)
# All overlays share the V02 fixed wheel-anchor registration. No image warp or per-part fitting.
reg=json.loads((W/'analysis/identity-v02/overlay-registration.json').read_text())['transforms'];projections=json.loads((A/'curve-projections.json').read_text());registration={}
for i,(v,l,r) in enumerate(zip(views,labels,refs)):
 photo=Image.open(r).convert('RGB');s=reg[v]['uniformScale'];tx,ty=reg[v]['translation'];draw=ImageDraw.Draw(photo)
 def fit(points):return[(s*x+tx,s*y+ty) for x,y in points]
 # Actual projected internal lamp perimeter, independent of the silhouette, stays on the wheel-anchored fit.
 for name in ['headlight','taillight']:
  pts=fit(projections[v][name]);draw.line(pts+[pts[0]],fill='#ff20cb',width=3)
 # Add the actual silhouette edge from the renderer rather than a hand-generated model outline.
 mask=Image.open(O/'silhouette'/(v+'.jpg')).convert('L').point(lambda p:255 if p<80 else 0);m=mask.transform(photo.size,Image.Transform.AFFINE,(1/s,0,-tx/s,0,1/s,-ty/s),resample=Image.Resampling.NEAREST)
 from PIL import ImageFilter
 edge=ImageChops.subtract(m.filter(ImageFilter.MaxFilter(3)),m.filter(ImageFilter.MinFilter(3)));photo.paste(Image.new('RGB',photo.size,'#9b1cd1'),(0,0),edge)
 photo.save(O/(l+'-overlay-source.jpg'),quality=95)
 board([(r,'REFERENCE'),(O/'clay'/(v+'.jpg'),'V03 same camera'),(O/(l+'-overlay-source.jpg'),'Purple actual silhouette / magenta projected lamp boundary')],'FIXED WHEEL-ANCHOR UNIFORM SCALE + TRANSLATION / NO WARP / CAMERA MISMATCH REMAINS',l+'-reference-overlay.jpg')
 registration[v]={'uniformScale':s,'translation':[tx,ty],'rotation':0,'numericalCameraWheelError':projections[v]['wheelProjectionError']}
Image.open(O/'front-overlay-source.jpg').crop((560,275,715,380)).resize((775,525)).save(O/'headlight-reference-overlay.jpg',quality=95)
(A/'overlay-registration.json').write_text(json.dumps({'method':'V02 wheel anchored scale/translation unchanged; no rotations/anisotropic scaling/part fitting; actual curve projections self-checked against browser wheel positions','transforms':registration},indent=2))
for src,box,dest in [('clay/rear-right.jpg',(475,235,730,442),'rear-quarter-closeup.jpg'),('clay/rear-right.jpg',(505,160,750,333),'dpillar-rear-closeup.jpg'),('clay/rear-right.jpg',(555,300,775,410),'bumper-wrap-closeup.jpg'),('clay/front-right.jpg',(260,275,420,365),'headlight-closeup.jpg')]:Image.open(O/src).crop(box).resize((700,round((box[3]-box[1])*700/(box[2]-box[0])))).save(O/dest,quality=95)
# Existing Hero comparison: same resolution/background, allow only the pre-existing navbar animation phase.
a=Image.open(W/'renders/identity-v02/before-hero.jpg').convert('RGB');b=Image.open(O/'hero-after.jpg').convert('RGB');assert a.size==b.size
metrics={}
for name,box in [('full',(0,0,990,891)),('heroBelowNavbar',(0,64,990,891)),('navbar',(0,0,990,64))]:
 diff=ImageChops.difference(a.crop(box),b.crop(box));metrics[name]={'pixelIdentical':diff.getbbox() is None,'diffBounds':diff.getbbox(),'meanAbsoluteRGB':sum(ImageStat.Stat(diff).mean)/3}
(A/'hero-navbar-regression.json').write_text(json.dumps(metrics,indent=2));board([(W/'renders/identity-v02/before-hero.jpg','PRESERVED BASELINE'),(O/'hero-after.jpg','V03 AFTER / WEBSITE UNCHANGED')],'HERO AND NAVBAR PROTECTION / SAME 1000x900 VIEWPORT','hero-navbar-protection.jpg',2,700,650)
board([(refs[1],'REFERENCE'),(O/'clay/front-right.jpg','V03 / ISOLATED / NOT APPROVED'),(refs[3],'REFERENCE'),(O/'clay/rear-right.jpg','V03 / SAME-CAR FAIL')],'V03 HEADLIGHT + REAR / EVIDENCE, NOT ACTIVATED','reference-v03-summary.jpg',2,600,370)
print(json.dumps(metrics));print('Required and supporting render evidence saved:',len(list(O.rglob('*.jpg'))))
