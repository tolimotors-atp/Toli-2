from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont,ExifTags
import hashlib,json,math
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';S=P.parent/'Isuzu MU-X';R=B/'renders/new-image-evidence-audit';R.mkdir(parents=True,exist_ok=True);old=json.loads((B/'references/authoritative-folder/inventory.json').read_text());hashes={r['sha256']:i for i,r in enumerate(old)}
paths=[f for f in S.rglob('*') if f.is_file()];extensions={'.jpg','.jpeg','.png','.webp','.heic','.heif','.tiff','.tif','.avif','.bmp'};rows=[]
for f in paths:
 if f.suffix.lower() not in extensions:continue
 h=hashlib.sha256(f.read_bytes()).hexdigest();row={'relative_path':str(f.relative_to(S)),'filename':f.name,'extension':f.suffix.lower(),'file_size':f.stat().st_size,'sha256':h,'previous_hash_match':h in hashes,'previous_id':old[hashes[h]]['id'] if h in hashes else None,'old_order':hashes.get(h,999),'readable':False}
 try:
  with Image.open(f) as src:
   exif=src.getexif();ex={ExifTags.TAGS.get(k,str(k)):str(v) for k,v in exif.items()};im=ImageOps.exif_transpose(src).convert('RGB');im.load()
   row.update(readable=True,width=im.width,height=im.height,aspect_ratio=im.width/im.height,format=src.format,exif_presence=bool(exif),exif=ex,camera_model=ex.get('Model'),camera_make=ex.get('Make'),lens=ex.get('LensModel'),focal_length=ex.get('FocalLength'),focal_length_35mm=ex.get('FocalLengthIn35mmFilm'),orientation=ex.get('Orientation'),timestamp=ex.get('DateTimeOriginal') or ex.get('DateTime'),decoded_sha256=hashlib.sha256(str(im.size).encode()+im.tobytes()).hexdigest())
   gray=im.convert('L').resize((9,8));pixels=list(gray.getdata());bits=[pixels[y*9+x]>pixels[y*9+x+1] for y in range(8) for x in range(8)];row['dhash']=hex(sum(int(v)<<i for i,v in enumerate(bits)))
 except Exception as e:row['error']=str(e)
 rows.append(row)
rows.sort(key=lambda r:(r['old_order'],r['relative_path']))
for i,r in enumerate(rows):r['id']=f'MUX-{i+1:03d}';r.pop('old_order')
F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',19);sm=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',14)
def sheet(items,name):
 out=Image.new('RGB',(5*420,max(1,math.ceil(len(items)/5))*320),'#1a1d23');d=ImageDraw.Draw(out)
 for i,r in enumerate(items):
  x=i%5*420;y=i//5*320
  if r['readable']:
   with Image.open(S/r['relative_path']) as src:im=ImageOps.contain(ImageOps.exif_transpose(src).convert('RGB'),(404,246));out.paste(im,(x+(420-im.width)//2,y+35+(246-im.height)//2))
  d.text((x+8,y+5),r['id']+(' / OLD' if r['previous_hash_match'] else ' / NEW FILE'),font=F,fill='white');d.text((x+8,y+285),r['filename'][:52],font=sm,fill='#d3d8df')
 out.save(R/name,quality=94)
sheet(rows,'all-images-contact-sheet.jpg');sheet([r for r in rows if not r['previous_hash_match']],'new-images-contact-sheet.jpg')
(B/'references/authoritative-folder/current-inventory.json').write_text(json.dumps({'source':str(S),'total_files':len(paths),'image_files':len(rows),'ignored_files':[str(f.relative_to(S)) for f in paths if f.suffix.lower() not in extensions],'status':'Inventory complete; visual classification pending','images':rows},indent=2))
print(json.dumps({'total_files':len(paths),'images':len(rows),'known':sum(r['previous_hash_match'] for r in rows),'new_files':sum(not r['previous_hash_match'] for r in rows),'unreadable':sum(not r['readable'] for r in rows),'exif_images':sum(r.get('exif_presence',False) for r in rows)}))
