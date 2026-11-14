from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageChops,ImageFilter
import json,shutil,math
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');W=P/'tools/3d/isuzu-mux/code-reference-car';A=W/'analysis/reference-v04';O=W/'renders/reference-v04';R=P.parent/'Isuzu MU-X';O.mkdir(exist_ok=True)
views=['front','front-right','right','rear-right','rear','front-left','rear-left'];labels=['front','front34','side','rear34','rear','oppositeFront','oppositeRear'];sources=['18-17-10','18-17-27','18-17-14','18-17-31','18-17-18','18-17-25','18-17-35'];refs=[R/f'Screenshot From 2026-11-06 {s}.png' for s in sources]
for key in ['06','comparison-v02','comparison-v03']+[f'comparison-checkpoint-{n:02}' for n in range(2,6)]:
 d=O/key;d.mkdir(exist_ok=True)
 for f in Path('/tmp/mux-reference-v04-'+key).glob('*'):shutil.copy2(f,d/f.name)
d=O/'modes';d.mkdir(exist_ok=True)
for f in Path('/tmp/mux-reference-v04-modes').glob('*.jpg'):shutil.copy2(f,d/f.name)
for k in ['hero','ai']:shutil.copy2('/tmp/mux-reference-v04-site-'+k+'.jpg',O/('site-'+k+'.jpg'))
def tile(f,label,w=500,h=320):
 im=ImageOps.contain(Image.open(f).convert('RGB'),(w-10,h-37));b=Image.new('RGB',(w,h),'#ddd');b.paste(im,((w-im.width)//2,33+(h-37-im.height)//2));ImageDraw.Draw(b).text((9,9),label,fill='#222');return b
def board(items,title,name,cols=3,w=500,h=320):
 b=Image.new('RGB',(cols*w,42+math.ceil(len(items)/cols)*h),'#ccc');ImageDraw.Draw(b).text((12,12),title,fill='#222')
 for i,(f,label) in enumerate(items):b.paste(tile(f,label,w,h),(i%cols*w,42+i//cols*h))
 b.save(O/name,quality=94)
items=[]
for i,v in enumerate(views[:5]):items.extend([(refs[i],labels[i]+' / supplied original'),(O/'comparison-v02'/(v+'.jpg'),'V02'),(O/'comparison-v03'/(v+'.jpg'),'V03'),(O/'06'/(v+'.jpg'),'V04 / NOT APPROVED')])
board(items,'ORIGINAL | FROZEN V02 | FROZEN V03 | V04 / IDENTICAL CAMERA CODE AND 964x520 CANVAS','v02-v03-v04-five-view.jpg',4)
board([(O/'06'/(v+'.jpg'),l) for v,l in zip(views[:5],labels)],'V04 NEUTRAL CLAY / NO BRANDING OR INTERNAL LAMP DETAIL','v04-clay-five-view.jpg',3,600,370)
shutil.copy2(O/'v04-clay-five-view.jpg',O/'v04-badgeless-five-view.jpg')
for mode in ['reflection','zebra','wireframe']:board([(d/(mode+'-'+v+'.jpg'),l) for v,l in zip(views[:5],labels)],'V04 '+mode.upper()+' / SAME CAMERA / GEOMETRY GATE','v04-'+mode+'-five-view.jpg',3,600,370)
board([(O/'06'/(v+'.jpg'),l) for v,l in zip(views,labels)],'V04 ALL SEVEN REQUIRED VIEWS / SAME SHARED GEOMETRY','v04-seven-view.jpg',3)
board([(d/'front-curves.jpg','Actual closed 3D headlight aperture'),(O/'fresh-front-traces.jpg','Fresh source design traces')],'V04 NEW APERTURE CURVES / BODY-MAPPED DEPTH, NOT V03 LAMP SHELL','new-headlight-curves.jpg',2,800,500)
board([(d/'patches-front-right.jpg','New front patches only / quarter'),(d/'patches-front-left.jpg','New front patches only / opposite quarter'),(d/'wireframe-front-right.jpg','Joined candidate wireframe')],'V04 HEADLIGHT / BONNET / FENDER / GRILLE PATCH INSPECTION','headlight-fender-patch.jpg')
board([(d/'patches-rear-right.jpg','New rear patches only'),(d/'patches-rear-left.jpg','Opposite rear patches'),(d/'wireframe-rear-right.jpg','Shared candidate wireframe')],'V04 NEW D-PILLAR / QUARTER / APERTURE / TAILGATE / BUMPER PATCHES','rear-patch-network.jpg')
for idx,name in [(1,'headlight-reference-comparison.jpg'),(3,'rear-quarter-reference-comparison.jpg'),(3,'dpillar-reference-comparison.jpg'),(4,'taillight-reference-comparison.jpg'),(3,'bumper-wrap-reference-comparison.jpg')]:
 board([(refs[idx],'SUPPLIED REFERENCE'),(O/'comparison-v03'/(views[idx]+'.jpg'),'V03'),(O/'06'/(views[idx]+'.jpg'),'V04')],'V04 REFERENCE CHECK / GEOMETRY STILL UNAPPROVED',name)
projections=json.loads((A/'curve-projections.json').read_text());reg=json.loads((W/'analysis/identity-v02/overlay-registration.json').read_text())['transforms'];registration={};annotated=[]
for i,(v,l,ref) in enumerate(zip(views[:5],labels,refs)):
 s=reg[v]['uniformScale'];tx,ty=reg[v]['translation'];photo=Image.open(ref).convert('RGB');draw=ImageDraw.Draw(photo)
 mask=Image.open(d/('silhouette-'+v+'.jpg')).convert('L').point(lambda x:255 if x<80 else 0);m=mask.transform(photo.size,Image.Transform.AFFINE,(1/s,0,-tx/s,0,1/s,-ty/s),resample=Image.Resampling.NEAREST);edge=ImageChops.subtract(m.filter(ImageFilter.MaxFilter(3)),m.filter(ImageFilter.MinFilter(3)));photo.paste(Image.new('RGB',photo.size,'#a71dd8'),(0,0),edge)
 draw=ImageDraw.Draw(photo)
 for curve in projections[v]['networks'].values():
  pts=[(x*s+tx,y*s+ty) for x,y in curve];draw.line(pts+[pts[0]],fill='#ff198a',width=3)
 photo.save(O/(l+'-overlay-source.jpg'),quality=95)
 board([(ref,'REFERENCE'),(O/'06'/(v+'.jpg'),'V04'),(O/(l+'-overlay-source.jpg'),'Purple actual silhouette / magenta actual apertures')],'FIXED WHEEL-ANCHOR UNIFORM SCALE + TRANSLATION / NO CAMERA OR IMAGE WARP',l+'-reference-overlay.jpg')
 reference=Image.open(ref).convert('RGB');model=Image.open(O/'06'/(v+'.jpg')).convert('RGB');dr=ImageDraw.Draw(reference);dm=ImageDraw.Draw(model)
 for n,(name,point) in enumerate(projections[v]['landmarks'].items(),1):
  if l not in point['observations']:continue
  for painter,xy in [(dr,point['observations'][l]),(dm,point['pixel'])]:x,y=xy;painter.ellipse((x-4,y-4,x+4,y+4),fill='#ffd900',outline='#111');painter.text((x+5,y-12),str(n),fill='#d60022',stroke_width=1,stroke_fill='white')
 reference.save(O/(l+'-landmarks-reference.jpg'),quality=94);model.save(O/(l+'-landmarks-model.jpg'),quality=94);annotated.extend([(O/(l+'-landmarks-reference.jpg'),l+' / observed pixel picks'),(O/(l+'-landmarks-model.jpg'),l+' / shared actual 3D landmarks')]);registration[v]={'scale':s,'translation':[tx,ty],'rotation':0,'wheelProjectionError':projections[v]['wheelProjectionError']}
board(annotated,'CROSS-VIEW SEMANTIC LANDMARKS / SHARED 3D POINTS / UNCALIBRATED OBSERVATIONS / KEY IN reference-data/v04','cross-view-landmarks.jpg',2,700,430)
(A/'overlay-registration.json').write_text(json.dumps({'method':'unchanged V02 wheel anchored uniform scale/translation, no per-part fitting, calibrated-accuracy claim or geometry warp','views':registration},indent=2))
# Native same-camera closeup crops, enlarged uniformly; two angles for every rear region.
for v,tag in [('rear-right','left'),('rear-left','right')]:
 im=Image.open(O/'06'/(v+'.jpg'));w,h=im.size
 for name,box in [('rear-quarter',(int(w*.47),int(h*.42),int(w*.78),int(h*.86))),('dpillar',(int(w*.51),int(h*.27),int(w*.79),int(h*.63))),('taillight',(int(w*.56),int(h*.44),int(w*.83),int(h*.68))),('bumper-corner',(int(w*.57),int(h*.57),int(w*.84),int(h*.84)))]:
  if tag=='right':box=(w-box[2],box[1],w-box[0],box[3])
  im.crop(box).resize((700,round((box[3]-box[1])*700/(box[2]-box[0])))).save(O/(name+'-'+tag+'-closeup.jpg'),quality=95)
for v,tag in [('front-right','left'),('front-left','right')]:
 im=Image.open(O/'06'/(v+'.jpg'));w,h=im.size;box=(int(w*.20),int(h*.43),int(w*.48),int(h*.76))
 if tag=='right':box=(w-box[2],box[1],w-box[0],box[3])
 im.crop(box).resize((700,round((box[3]-box[1])*700/(box[2]-box[0])))).save(O/('headlight-fender-grille-'+tag+'-closeup.jpg'),quality=95)
board([(refs[1],'REFERENCE front34'),(O/'06/front-right.jpg','V04 / FAIL identity'),(refs[3],'REFERENCE rear34'),(O/'06/rear-right.jpg','V04 / FAIL identity')],'V04 FINAL CLAY COMPARISON / ISOLATED, NOT ACTIVE','reference-v04-summary.jpg',2,600,370)
board([(O/f'comparison-checkpoint-{n:02}'/(v+'.jpg'),f'CP{n} / {v}') for n in range(2,6) for v in views[:5]]+[(O/'06'/(v+'.jpg'),'CP6 / '+v) for v in views[:5]],'FIVE GEOMETRY CHECKPOINTS / CP1 TRACES SAVED SEPARATELY / SAME CANVAS/CAMERAS','checkpoint-five-view.jpg',5,400,250)
print('Saved V04 requested diagnostics, overlays, landmark comparisons and two-angle closeups')
