from pathlib import Path
from PIL import Image,ImageOps,ImageDraw
import json,hashlib
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';S=P.parent/'Isuzu MU-X';audit=B/'renders/new-image-evidence-audit';d=json.loads((B/'references/authoritative-folder/current-inventory.json').read_text());R=B/'controlled-capture/reconstruction/current-folder-audit';assert not R.exists(),'Preserve any previous registration: choose a versioned test folder.'
for n in ['small/images','small/masks','small/sparse','small/logs','small/diagnostics']:(R/n).mkdir(parents=True,exist_ok=True)
ids=['MUX-027','MUX-028','MUX-029','MUX-041','MUX-030','MUX-031'];out=[]
for row in d['images']:
 if row['id'] not in ids:continue
 with Image.open(S/row['relative_path']) as src:im=ImageOps.exif_transpose(src).convert('RGB')
 # A conservative red-seeded vehicle envelope excludes the blank backdrop and viewer-floor graphics.
 pix=im.load();hits=[(x,y) for y in range(im.height) for x in range(im.width) if pix[x,y][0]>70 and pix[x,y][0]>pix[x,y][1]*1.35 and pix[x,y][0]>pix[x,y][2]*1.25]
 assert hits;xs,ys=zip(*hits);x0,x1,y0,y1=min(xs),max(xs),min(ys),max(ys);w=x1-x0;h=y1-y0
 polygon=[(x0+.14*w,y0-24),(x1-.12*w,y0-24),(x1+12,y0+.25*h),(x1+12,y1+.10*h),(x1-.08*w,y1+.34*h),(x0+.08*w,y1+.34*h),(x0-12,y1+.10*h),(x0-12,y0+.25*h)]
 mask=Image.new('L',im.size,0);ImageDraw.Draw(mask).polygon(polygon,fill=255)
 name=row['id']+'.png';im.save(R/'small/images'/name);mask.save(R/'small/masks'/(name+'.png'))
 overlay=Image.blend(im,Image.new('RGB',im.size,'#802020'),.65);overlay.paste(im,mask=mask);overlay.save(R/'small/diagnostics'/(row['id']+'-mask.jpg'))
 out.append({'id':row['id'],'source':str(S/row['relative_path']),'source_sha256':row['sha256'],'derivative':str(R/'small/images'/name),'mask':str(R/'small/masks'/(name+'.png')),'mask_note':'Coarse vehicle envelope, not pixel-perfect segmentation. Review overlay; no old geometry used.'})
(R/'small/dataset-manifest.json').write_text(json.dumps({'images':out,'selection_order':ids,'rationale':'Adjacent front-to-left sequence from the same apparent red turntable viewer; unknown physical/synthetic provenance, no EXIF. New files only.'},indent=2));print('Small new-image registration dataset:',len(out))
# Keep reproducible extraction code; historical inventories remain intact.
(audit/'inventory-script.py').write_text(Path('/tmp/mux-image-audit/inventory.py').read_text())
