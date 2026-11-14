from pathlib import Path
import json,hashlib,collections
from PIL import Image,ImageDraw,ImageOps,ImageFont
import numpy as np,cv2
O=Path(__file__).resolve().parents[1];SRC=Path('/home/thunder/shared/tolimotors-main1/Isuzu MU-X');inv=json.loads(Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/references/authoritative-folder/inventory.json').read_text());manifest=[]
# Conservative hand-assisted polygon ROIs, expanded 8 px. They preserve thin geometry at the expense of some background.
polys={
'18-17-10':[(372,132),(650,112),(686,191),(729,206),(729,251),(710,257),(710,490),(368,490),(363,255),(340,250),(340,207),(370,198)],
'18-17-14':[(135,272),(338,215),(438,145),(493,117),(854,118),(904,164),(931,238),(944,371),(866,405),(852,460),(710,463),(704,413),(375,415),(365,467),(224,467),(211,405),(135,388)],
'18-17-18':[(390,139),(655,130),(688,190),(697,193),(700,232),(706,277),(709,488),(351,488),(351,269),(356,229),(355,193),(375,185)],
'18-17-21':[(92,259),(127,174),(172,130),(516,118),(621,139),(710,211),(860,240),(940,303),(940,392),(900,405),(868,468),(724,468),(713,416),(360,416),(348,466),(210,467),(197,412),(105,391)],
'18-17-25':[(207,205),(226,150),(264,115),(641,109),(705,153),(792,224),(868,295),(876,410),(826,452),(676,491),(536,490),(518,448),(351,420),(326,453),(225,438),(208,350)],
'18-17-27':[(154,281),(306,211),(430,125),(771,113),(832,143),(869,228),(882,365),(847,420),(713,451),(683,426),(500,459),(479,495),(346,492),(321,451),(158,409)],
'18-17-31':[(114,267),(294,174),(420,121),(726,112),(841,155),(877,241),(891,399),(835,473),(690,494),(663,459),(417,429),(376,462),(251,453),(228,413),(113,386)],
'18-17-35':[(132,245),(330,154),(451,119),(725,110),(844,143),(886,239),(886,409),(840,470),(701,495),(660,454),(406,423),(365,457),(236,445),(210,404),(132,384)]}
for row in inv:
 p=SRC/row['filename'];t=p.stem[-8:];im=Image.open(p).convert('RGB');assert hashlib.sha256(p.read_bytes()).hexdigest()==row['sha256'];tags=[];used=False
 if t.startswith('18-17-'):cl='EXTERIOR-GEOMETRY';group='primary';used=True
 elif t in ['18-05-23','18-08-46']:cl='EXTERIOR-GEOMETRY';group='supplemental';tags=['PROMOTIONAL','POTENTIALLY_DIFFERENT_PHYSICAL_VEHICLE']
 elif t in ['18-09-21','18-09-40','18-09-48','18-10-06']:cl='OPEN-PANEL';group='excluded'
 elif t in ['18-06-24','18-11-39']:cl='INTERIOR';group='excluded';tags=['COLLAGE'] if t=='18-06-24' else []
 elif t=='18-05-58':cl='ENGINE';group='excluded'
 else:cl='COLLAGE';group='supplemental'
 entry={'original':str(p),'original_sha256':row['sha256'],'class':cl,'tags':tags,'derived':[],'submitted_to_sfm':used}
 if used:
  crop=(5,65,1033,530);out=im.crop(crop);name=t+'.png';dest=O/'input/primary'/name;out.save(dest);mask=Image.new('L',im.size,0);ImageDraw.Draw(mask).polygon(polys[t],fill=255);a=np.asarray(mask).copy();a=cv2.dilate(a,np.ones((17,17),np.uint8));mask=Image.fromarray(a).crop(crop);mask.save(O/'masks'/(name+'.png'));entry['derived'].append({'path':'input/primary/'+name,'crop_xyxy':crop,'pixels_unchanged_except_lossless_crop':True,'mask':'masks/'+name+'.png','mask_method':'conservative manually assisted polygon ROI + 8px dilation, not exact semantic segmentation'})
 elif cl=='EXTERIOR-GEOMETRY':
  im.save(O/'input/supplemental'/(t+'.png'));entry['derived'].append({'path':'input/supplemental/'+t+'.png','crop_xyxy':[0,0,*im.size],'excluded_reason':'Different capture/paint/possibly physical vehicle; do not contaminate the canonical eight-view registration test.'})
 elif cl=='COLLAGE':
  for name,crop in [('profile',(5,5,355,235)),('rear',(380,5,731,235)),('rear3q',(5,262,735,683))]:
   dst=O/'input/supplemental'/('collage-'+name+'.png');im.crop(crop).save(dst);entry['derived'].append({'path':str(dst.relative_to(O)),'crop_xyxy':crop,'excluded_reason':'Clean exterior panel, but different wheel/trim/source and small/duplicate viewpoint; kept supplementary only.'})
 else:entry['exclusion_reason']='Open panel changes/obscures closed-body geometry' if cl=='OPEN-PANEL' else 'Not exterior geometry; interior collage intentionally not split for this experiment.'
 manifest.append(entry)
assert len(manifest)==18;assert sum(x['submitted_to_sfm'] for x in manifest)==8
(O/'input/manifest.json').write_text(json.dumps({'originals':manifest,'classification_counts':dict(collections.Counter(x['class'] for x in manifest)),'collage_tag_count':2,'derived_files':sum(len(x['derived']) for x in manifest),'primary_count':8,'supplemental_count':5,'notes':'Exterior detail-only category has zero sources. Interior collage overlaps COLLAGE tag but counts as INTERIOR. Original screenshots and references are read-only.'},indent=2))
F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',18);canvas=Image.new('RGB',(1600,4*260),(28,29,32));d=ImageDraw.Draw(canvas)
for i,p in enumerate(sorted((O/'input/primary').glob('*.png'))):
 im=Image.open(p).convert('RGB');mask=Image.open(O/'masks'/(p.name+'.png'));arr=np.asarray(im).copy();ma=np.asarray(mask)>0;arr[~ma]=(arr[~ma]*.18).astype(np.uint8);marked=Image.fromarray(arr)
 for j,pic in enumerate([im,marked]):
  x=(i%2)*800+j*400;y=(i//2)*260;pic=ImageOps.contain(pic,(394,220));canvas.paste(pic,(x+(400-pic.width)//2,y+30));d.text((x+6,y+4),p.stem+(' / input' if j==0 else ' / ROI mask'),font=F,fill='white')
canvas.save(O/'comparisons/input-mask-contact.jpg',quality=93);print('Dataset classified; 8 primary crops, 5 supplementary derivatives and separate masks saved')
