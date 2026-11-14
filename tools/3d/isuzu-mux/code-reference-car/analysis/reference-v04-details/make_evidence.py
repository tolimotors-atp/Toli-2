from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,shutil,math
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');W=P/'tools/3d/isuzu-mux/code-reference-car';O=W/'renders/reference-v04/exterior-details';A=W/'analysis/reference-v04-details';R=P.parent/'Isuzu MU-X';raw=O/'raw';raw.mkdir(exist_ok=True)
for f in Path('/tmp/mux-v04-details').glob('*'):shutil.copy2(f,raw/f.name)
def tile(path,label,w=600,h=370):
 im=ImageOps.contain(Image.open(path).convert('RGB'),(w-12,h-37));out=Image.new('RGB',(w,h),'#ddd');out.paste(im,((w-im.width)//2,33+(h-37-im.height)//2));ImageDraw.Draw(out).text((10,9),label,fill='#222');return out
def board(items,title,name,cols=3,w=600,h=370):
 out=Image.new('RGB',(cols*w,42+math.ceil(len(items)/cols)*h),'#ccc');ImageDraw.Draw(out).text((12,12),title,fill='#222')
 for i,(f,label) in enumerate(items):out.paste(tile(f,label,w,h),(i%cols*w,42+i//cols*h))
 out.save(O/name,quality=95)
def crop(path,box,name,width=700):
 im=Image.open(path).convert('RGB').crop(box);im.resize((width,round(width*im.height/im.width))).save(O/name,quality=96)
views=['front','front-right','right','rear-right','rear'];labels=['Front','Front quarter','Side','Rear quarter','Rear']
board([(raw/(v+'.jpg'),l) for v,l in zip(views,labels)],'V04 EXTERIOR DETAILS / ISOLATED CANDIDATE, SAME-CAR GATE NOT PASSED','details-five-view.jpg')
board([(raw/('badgeless-'+v+'.jpg'),l+' / all plates hidden') for v,l in zip(views,labels)],'V04 BADGELESS CLAY / DETAILS DO NOT OVERRIDE PRIMARY BODY FAILURE','badgeless-five-view.jpg')
board([(R/'Screenshot From 2026-11-06 18-17-27.png','Reference front quarter'),(R/'Screenshot From 2026-11-06 18-17-14.png','Reference side'),(R/'Screenshot From 2026-11-06 18-17-31.png','Reference rear quarter'),(raw/'front-right.jpg','Coded front quarter'),(raw/'right.jpg','Coded side'),(raw/'rear-right.jpg','Coded rear quarter')],'FEATURE SCALE / WHEELS, MIRRORS, WINDOWS, LAMPS, HANDLES AND PLATES / UNCALIBRATED PHOTOS','feature-scale-validation.jpg')
board([(raw/('reflection-'+v+'.jpg'),v) for v in ['front-right','right','rear-right']],'V04 REFLECTION CHECK / EXISTING BODY DEFECTS REMAIN VISIBLE','details-reflection.jpg')
crop(R/'Screenshot From 2026-11-06 18-17-10.png',(636,279,707,357),'front-headlight-reference-closeup.jpg')
crop(raw/'close-front.jpg',(665,255,825,377),'front-headlight-coded-closeup.jpg')
crop(R/'Screenshot From 2026-11-06 18-17-31.png',(563,246,677,310),'rear-light-reference-closeup.jpg')
crop(raw/'close-rear-right.jpg',(700,307,845,419),'rear-light-coded-closeup.jpg')
crop(raw/'close-front-right.jpg',(449,214,552,298),'coded-mirror-front34.jpg')
crop(raw/'close-right.jpg',(180,128,290,221),'coded-mirror-side.jpg')
crop(raw/'close-rear-right.jpg',(223,168,297,226),'coded-mirror-rear34.jpg')
board([(O/'reference-0.jpg','Original mirror / front quarter'),(O/'coded-mirror-front34.jpg','Coded mirror / front quarter'),(O/'reference-1.jpg','Original mirror / side'),(O/'coded-mirror-side.jpg','Coded mirror / side'),(O/'reference-2.jpg','Original mirror / rear quarter'),(O/'coded-mirror-rear34.jpg','Coded mirror / rear quarter')],'REFERENCE-SIZED CURVED MIRROR / HOUSING SHAPE STILL NEEDS WORK','mirror-reference-comparison.jpg',2,700,430)
crop(raw/'close-right.jpg',(439,185,850,252),'door-handle-side-closeup.jpg',1000)
crop(raw/'close-right.jpg',(170,45,870,456),'door-cuts-side-closeup.jpg',1000)
shutil.copy2(raw/'close-left.jpg',O/'door-cuts-opposite-side-closeup.jpg')
crop(raw/'close-front-plate.jpg',(385,384,548,443),'front-number-plate-closeup.jpg')
crop(raw/'close-rear.jpg',(369,284,596,376),'rear-number-plate-closeup.jpg')
shutil.copy2(raw/'rear-full-detail.jpg',O/'rear-full-detail.jpg')
board([(O/'reference-3.jpg','Original doors / handles'),(O/'door-cuts-side-closeup.jpg','Coded definitions / same continuous body'),(O/'door-handle-side-closeup.jpg','Coded shallow 3D handles')],'FOUR DOOR DEFINITIONS / 3mm SURFACE-FOLLOWING CUT RIBBONS / NO BODY HOLES','doors-reference-comparison.jpg')
board([(O/'front-headlight-reference-closeup.jpg','Reference front lamp'),(O/'front-headlight-coded-closeup.jpg','Coded outer aperture / internals deferred'),(O/'rear-light-reference-closeup.jpg','Reference rear lamp'),(O/'rear-light-coded-closeup.jpg','Coded recessed aperture / internals deferred')],'LAMP SHAPE AND INTEGRATION REMAIN UNAPPROVED','lamp-reference-comparison.jpg',2,700,450)
board([(raw/'front-right.jpg','V04 with requested exterior features'),(O/'front-number-plate-closeup.jpg','FRONT / TOLI MOTORS'),(raw/'rear-right.jpg','V04 rear / still isolated'),(O/'rear-number-plate-closeup.jpg','REAR / TOLI MOTORS')],'V04 EXTERIOR DETAIL ADDITION / NOT APPROVED FOR ACTIVATION','details-summary.jpg',2,600,370)
board([(raw/'front-right.jpg','With requested details'),(raw/'underlying-body-front34.jpg','Mirrors, door cuts, handles and plates hidden')],'UNDERLYING BODY INSPECTION / NO DETAILS USED AS RECOGNITION PROOF','underlying-body-comparison.jpg',2,700,430)
(A/'visual-gates.json').write_text(json.dumps({'sideMirrors':'NEEDS WORK','headlightShape':'NEEDS WORK','headlightFenderIntegration':'FAIL','rearLightShape':'NEEDS WORK','rearLightBodyIntegration':'NEEDS WORK','doors':'NEEDS WORK','doorHandles':'NEEDS WORK','frontPlate':'PASS','rearPlate':'PASS','overallSameCar':'FAIL','activation':'DEFERRED','note':'Detail construction/presence tests do not certify MU-X visual identity. Mirror/profile and door/handle placement still depend on the inaccurate underlying body.'},indent=2))
print('Saved required exterior closeups, scale validation, independent-body and badgeless evidence')
