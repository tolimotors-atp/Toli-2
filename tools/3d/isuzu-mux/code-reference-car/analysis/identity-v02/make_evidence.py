"""Diagnostic assembly only: unchanged photo copies, uniform-fit renders, approximate hand traces."""
from pathlib import Path
from PIL import Image, ImageOps, ImageDraw, ImageChops, ImageStat, ImageFilter
import json, shutil, math
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website'); W=P/'tools/3d/isuzu-mux/code-reference-car'; O=W/'renders/identity-v02'; A=W/'analysis/identity-v02'; O.mkdir(parents=True,exist_ok=True)
views=['front','front-right','right','rear-right','rear']; labels=['front','front34','side','rear34','rear']; suffixes=['18-17-10','18-17-27','18-17-14','18-17-31','18-17-18']; R=P.parent/'Isuzu MU-X'
for n in range(1,6):
 d=O/f'iteration-{n:02}';d.mkdir(exist_ok=True)
 for p in Path(f'/tmp/mux-identity-{n:02}').iterdir():shutil.copy2(p,d/p.name)
for mode in ['reflection','wireframe','silhouette']:
 d=O/mode;d.mkdir(exist_ok=True)
 for p in Path('/tmp/mux-identity-'+mode).glob('*.jpg'):shutil.copy2(p,d/p.name)
for p in Path('/tmp').glob('mux-identity-*.jpg'):
 if any(s in p.name for s in ['before-','after-','-ai']):shutil.copy2(p,O/p.name.replace('mux-identity-',''))
def tile(path,label,w=500,h=310):
 im=Image.open(path).convert('RGB');im=ImageOps.contain(im,(w-10,h-32));out=Image.new('RGB',(w,h),'#dedede');out.paste(im,((w-im.width)//2,30+(h-32-im.height)//2));ImageDraw.Draw(out).text((8,8),label,fill='#202020');return out
refs=[R/f'Screenshot From 2026-11-06 {s}.png' for s in suffixes]
def board(paths,title,out,cols=5,w=500,h=310):
 im=Image.new('RGB',(cols*w,40+math.ceil(len(paths)/cols)*h),'#ccc');ImageDraw.Draw(im).text((12,12),title,fill='#222')
 for i,(p,l) in enumerate(paths):im.paste(tile(p,l,w,h),(i%cols*w,40+i//cols*h))
 im.save(O/out,quality=94)
board([(O/f'iteration-{n:02}'/(v+'.jpg'),f'iteration {n} / {l}') for n in range(1,6) for v,l in zip(views,labels)],'FIVE CONTROLLED PASSES / SAME GEOMETRY AND CAMERAS PER ROW','iterations-five-view.jpg',5,400,250)
for mode in ['clay','reflection','wireframe']:
 board([((O/'iteration-05' if mode=='clay' else O/mode)/(v+'.jpg'),l+' / '+mode) for v,l in zip(views,labels)],'MU-X CODED IDENTITY V02 / NOT APPROVED / BADGES ABSENT',mode+'-five-view.jpg',3)
paths=[]
for ref,v,l in zip(refs,views,labels):paths.extend([(ref,l+' / supplied reference'),(W/'renders/section-03-05'/('clay-'+v+'.jpg'),l+' / previous Section 03/05 candidate'),(O/'iteration-05'/(v+'.jpg'),l+' / identity V02, pass 5')])
board(paths,'REFERENCE | PRE-IDENTITY BASELINE (V01 FOR THIS COMPARISON) | IDENTITY V02','reference-v01-v02-five-view.jpg',3)
# User-visible source coordinates; approximate hand-picked evidence, NOT camera calibration.
refAnchors=[[[397,421],[665,421]],[[432,410],[791,354]],[[274,386],[790,382]],[[326,365],[622,388]],[[390,425],[650,425]]]
keys=[['frontWheelFar','frontWheelNear'],['frontWheelNear','rearWheelNear'],['frontWheelNear','rearWheelNear'],['frontWheelNear','rearWheelNear'],['rearWheelNear','rearWheelFar']]
contours=[
[(347,224),(355,166),(389,125),(465,113),(620,119),(650,155),(674,222),(706,224),(706,251),(687,262),(688,394),(678,465),(651,479),(630,473),(626,442),(424,443),(420,476),(391,480),(377,461),(369,368),(366,269),(348,259)],
[(164,316),(177,274),(253,233),(329,192),(421,137),(516,120),(762,127),(808,153),(844,191),(859,300),(845,366),(810,399),(779,396),(755,373),(747,346),(514,405),(489,449),(450,479),(417,481),(389,459),(376,421),(279,403),(223,400),(177,374)],
[(140,319),(152,281),(233,245),(325,218),(395,153),(448,132),(535,121),(794,123),(846,144),(876,183),(902,257),(924,292),(926,352),(903,385),(853,393),(844,436),(819,457),(779,459),(746,440),(730,407),(337,409),(317,442),(285,461),(251,458),(222,439),(211,407),(168,398),(145,366)],
[(269,310),(299,241),(359,191),(437,152),(489,143),(640,152),(719,182),(774,235),(810,299),(810,381),(774,419),(716,426),(704,458),(671,483),(633,479),(603,448),(591,418),(377,391),(358,421),(325,423),(299,398),(288,365)],
[(359,267),(359,236),(382,211),(405,169),(436,149),(597,143),(638,163),(661,207),(680,237),(685,270),(678,372),(677,446),(653,479),(625,477),(617,449),(425,449),(416,475),(387,476),(370,449),(363,375)]
]
frames=json.loads((O/'iteration-05/frames.json').read_text());transforms={}
for i,(v,l,ref) in enumerate(zip(views,labels,refs)):
 photo=Image.open(ref).convert('RGB');coded=Image.open(O/'silhouette'/(v+'.jpg')).convert('L');mask=coded.point(lambda p:255 if p<80 else 0)
 anchors=[frames[i]['landmarks'][k]['pixel'] for k in keys[i]];ra=refAnchors[i]
 s=math.dist(*ra)/math.dist(*anchors);tx=sum(p[0] for p in ra)/2-s*sum(p[0] for p in anchors)/2;ty=sum(p[1] for p in ra)/2-s*sum(p[1] for p in anchors)/2
 transforms[v]={'uniformScale':s,'translation':[tx,ty],'modelAnchors':anchors,'referenceAnchors':ra,'rotation':0,'note':'Approximate manual wheel anchors; no anisotropic scaling/rotation/warping. Different camera pitch remains visible.'}
 fit=mask.transform(photo.size,Image.Transform.AFFINE,(1/s,0,-tx/s,0,1/s,-ty/s),resample=Image.Resampling.NEAREST)
 edge=ImageChops.subtract(fit.filter(ImageFilter.MaxFilter(5)),fit.filter(ImageFilter.MinFilter(3)));overlay=photo.copy();overlay.paste(Image.new('RGB',photo.size,'#ff20ca'),(0,0),edge);d=ImageDraw.Draw(overlay);d.line(contours[i]+[contours[i][0]],fill='#00a77d',width=3)
 overlay.save(O/(l+'-overlay-source.jpg'),quality=95)
 board([(ref,'REFERENCE'),(O/'iteration-05'/(v+'.jpg'),'CODED CLAY, SAME FIXED CAMERA'),(O/(l+'-overlay-source.jpg'),'GREEN approx. hand trace / MAGENTA actual model outline')],l.upper()+' / UNCALIBRATED SILHOUETTE DIAGNOSTIC / UNIFORM SCALE + TRANSLATION ONLY',l+'-reference-overlay.jpg',3)
(A/'overlay-registration.json').write_text(json.dumps({'method':'manual approximate source traces; actual rendered binary model mask; no similarity accuracy score claimed','referenceContours':dict(zip(views,contours)),'transforms':transforms},indent=2))
# Read-only landmark annotations, supporting internal as well as outline comparisons.
refPoints={
'front':{'windscreenLowerNear':[653,245],'windscreenUpperNear':[625,165],'bonnetFrontNear':[672,306],'headlight0':[593,321],'headlight1':[683,301],'frontBumper1':[617,440]},
'front-right':{'windscreenLowerNear':[545,228],'windscreenUpperNear':[566,149],'bonnetFrontNear':[341,303],'bonnetCowlNear':[530,249],'headlight0':[324,316],'headlight1':[275,306],'frontWindowRear':[662,243],'quarterFront':[769,153],'quarterRear':[814,158]},
'right':{'bonnetCowlNear':[342,229],'windscreenLowerNear':[342,217],'windscreenUpperNear':[437,149],'frontWindowUpper':[440,150],'frontWindowRear':[582,256],'rearWindowRear':[728,241],'quarterFront':[792,162],'quarterRear':[845,167],'roofFront':[435,134]},
'rear-right':{'quarterFront':[526,177],'quarterRear':[594,182],'rearGlassLower':[742,272],'tailLamp0':[599,274],'tailLamp1':[653,293],'rearBumper1':[724,416]},
'rear':{'rearGlassLower':[412,260],'tailLamp0':[384,277],'tailLamp1':[423,289],'rearBumper1':[427,421]}}
annotated=[]
for i,(v,l,ref) in enumerate(zip(views,labels,refs)):
 a=Image.open(ref).convert('RGB');b=Image.open(O/'iteration-05'/(v+'.jpg')).convert('RGB');da=ImageDraw.Draw(a);db=ImageDraw.Draw(b)
 pts=dict(zip(keys[i],refAnchors[i]));pts.update(refPoints[v]);legend=[]
 for n,(k,p) in enumerate(pts.items(),1):
  q=frames[i]['landmarks'][k]['pixel'];legend.append(f'{n}={k}')
  for draw,xy in [(da,p),(db,q)]:x,y=xy;draw.ellipse((x-4,y-4,x+4,y+4),fill='#ffdc00',outline='#111');draw.text((x+5,y-12),str(n),fill='#d90019',stroke_width=1,stroke_fill='#fff')
 a.save(O/(l+'-reference-landmarks.jpg'),quality=95);b.save(O/(l+'-coded-landmarks.jpg'),quality=95)
 annotated.extend([(O/(l+'-reference-landmarks.jpg'),l+' / approximate reference landmarks'),(O/(l+'-coded-landmarks.jpg'),l+' / actual projected geometry landmarks')])
 transforms[v]['landmarkLegend']=legend
board(annotated,'INTERNAL LANDMARKS / APPROXIMATE PHOTO PICKS vs ACTUAL PROJECTED CONTROL POINTS / NUMBER KEY IN overlay-registration.json','internal-landmarks.jpg',2,700,430)
(A/'overlay-registration.json').write_text(json.dumps({'method':'approximate hand picks, uniform scale+translation, no accuracy claim','referenceContours':dict(zip(views,contours)),'transforms':transforms},indent=2))
for v,crop,name in [('front-right',(205,120,605,435),'front34-closeup.jpg'),('right',(290,105,870,265),'greenhouse-closeup.jpg'),('rear-right',(475,150,760,325),'dpillar-closeup.jpg'),('rear-right',(295,150,770,440),'rear34-closeup.jpg')]:
 Image.open(O/'iteration-05'/(v+'.jpg')).crop(crop).save(O/name,quality=96)
# An explicit error-map image, using unchanged before photos plus concise causes.
board([(refs[1],'REFERENCE front34'),(W/'renders/section-03-05/clay-front-right.jpg','BASELINE front34'),(refs[3],'REFERENCE rear34'),(W/'renders/section-03-05/clay-rear-right.jpg','BASELINE rear34')],'ERROR MAP BEFORE EDITING / see IDENTITY_ERROR_MAP_V02.md','identity-error-map.jpg',2,700,420)
im=Image.open(O/'identity-error-map.jpg');out=Image.new('RGB',(im.width,im.height+165),'#ddd');out.paste(im,(0,0));d=ImageDraw.Draw(out)
for i,line in enumerate(['1 Cowl too far rearward -> bonnetCentre / cabinOutline / windscreen','2 Shallow glass -> upper body bands / window loops / greenhouseY','3 Bonnet/fender nose fins -> unmatched patch end boundaries','4 Generic D-pillar and hatch -> quarterWindow / roofSide / rearGlass / rear profile','5 Flat wheel surround -> section width bands and localized fender volume','6 Weak front/rear envelopes -> headlamp / grille / tailLamp / fasciaSections']):d.text((14,im.height+12+i*24),line,fill='#222')
out.save(O/'identity-error-map.jpg',quality=95)
Image.open(O/'after-hero.jpg').crop((0,0,990,64)).save(O/'after-navigation.jpg',quality=100,subsampling=0)
metrics={}
for name in ['hero','navigation']:
 a=Image.open(O/f'before-{name}.jpg').convert('RGB');b=Image.open(O/f'after-{name}.jpg').convert('RGB');assert a.size==b.size
 if name=='navigation':
  a=Image.open(O/'before-hero.jpg').convert('RGB').crop((0,0,990,64));b=Image.open(O/'after-hero.jpg').convert('RGB').crop((0,0,990,64))
 diff=ImageChops.difference(a,b);metrics[name]={'size':a.size,'pixelIdentical':diff.getbbox() is None,'meanAbsoluteRGB':sum(ImageStat.Stat(diff).mean)/3,'changedPixels':sum(max(p)>0 for p in diff.getdata())}
 board([(O/f'before-{name}.jpg','BEFORE'),(O/f'after-{name}.jpg','AFTER')],name.upper()+' / PROTECTED REGRESSION',name+'-regression.jpg',2,700,630 if name=='hero' else 100)
heroA=Image.open(O/'before-hero.jpg').convert('RGB').crop((0,64,990,891));heroB=Image.open(O/'after-hero.jpg').convert('RGB').crop((0,64,990,891));metrics['heroBelowNavbarPixelIdentical']=ImageChops.difference(heroA,heroB).getbbox() is None
(A/'regression-image-metrics.json').write_text(json.dumps(metrics,indent=2));print(json.dumps(metrics));print('Saved evidence',len(list(O.rglob('*.jpg'))))
