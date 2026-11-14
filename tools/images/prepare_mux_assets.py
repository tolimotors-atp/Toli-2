"""Create responsive copies of the supplied MU-X images; never edit the originals."""
from pathlib import Path
from PIL import Image
import hashlib, json
project=Path(__file__).resolve().parents[2]
reference=project.parent/'Isuzu MU-X'
output=project/'src/assets/vehicles/isuzu-mux'; output.mkdir(parents=True,exist_ok=True)
sources={'front':'Screenshot 2026-11-08 213542.png','rear':'Screenshot 2026-11-08 213451.png'}
records=[]
for view,name in sources.items():
    path=reference/name
    image=Image.open(path).convert('RGB')
    # Neutral padding protects roof, bumpers and tires inside the shaped studio frame.
    canvas=Image.new('RGB',(1100,660),'white')
    fitted=image.copy()
    fitted.thumbnail((1008,600),Image.Resampling.LANCZOS)
    canvas.paste(fitted,((1100-fitted.width)//2,(660-fitted.height)//2))
    for width in [640,1100]:
        resized=canvas.resize((width,width*3//5),Image.Resampling.LANCZOS)
        for ext,options in [('avif',{'quality':78,'speed':6}),('webp',{'quality':91,'method':6})]:
            dest=output/f'mux-{view}-{width}.{ext}';resized.save(dest,**options)
            records.append({'file':str(dest.relative_to(project)),'width':resized.width,'height':resized.height,'bytes':dest.stat().st_size,'source':name,'sourceSha256':hashlib.sha256(path.read_bytes()).hexdigest(),'sourceSize':image.size,'processing':'Uniform fit, white edge padding, resize and encode only; no vehicle/background/plate retouch.'})
    assert canvas.width==1100 and canvas.height==660
(project/'docs/mux-2d/assets.json').write_text(json.dumps(records,indent=2))
print('Saved',len(records),'AVIF/WebP assets;',sum(r['bytes'] for r in records),'bytes total.')
