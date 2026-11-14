#!/usr/bin/env python3
"""Inspect local originals and copy classifications; never modify incoming files."""
from pathlib import Path
from collections import Counter
import argparse, hashlib, json, re, shutil
from datetime import datetime, timezone
from PIL import Image, ImageOps, ExifTags
import numpy as np

SEQUENCES = {'normal','elevated','low','detail','open-panel','interior','engine'}
PRIMARY = {'normal','elevated','low'}
EXTENSIONS = {'.jpg','.jpeg','.png','.tif','.tiff','.webp','.heic','.heif','.dng'}

def fingerprint(path):
    h = hashlib.sha256()
    with path.open('rb') as f:
        for chunk in iter(lambda:f.read(1024*1024), b''): h.update(chunk)
    return h.hexdigest()

def inspect(root):
    root = root.resolve()
    incoming = root/'incoming'
    assert incoming.is_dir(), 'Missing incoming folder'
    paths = sorted(p for p in incoming.rglob('*') if p.is_file())
    records, seen, numbers = [], {}, {}
    for p in paths:
        rel = p.relative_to(incoming)
        sequence = rel.parts[0] if len(rel.parts)>1 and rel.parts[0] in SEQUENCES else 'unassigned'
        record = {'original_filename':str(rel),'sequence':sequence,'sha256':None,'width':None,'height':None,'display_orientation':None,'timestamp':None,'camera_make':None,'camera_model':None,'lens':None,'focal_length_mm':None,'exposure_seconds':None,'exif_orientation':None,'derived_working_filename':None,'warnings':[],'review_reasons':[]}
        records.append(record)
        if p.is_symlink():
            record['review_reasons'].append('Symlink not imported'); continue
        record['sha256'] = fingerprint(p)
        if record['sha256'] in seen: record['review_reasons'].append('Exact duplicate of '+seen[record['sha256']])
        else: seen[record['sha256']] = str(rel)
        if sequence == 'unassigned': record['review_reasons'].append('Assign a sequence subfolder before calibration')
        if p.suffix.lower() not in EXTENSIONS:
            record['review_reasons'].append('Unsupported file type; original retained'); continue
        try:
            with Image.open(p) as im:
                im.load(); ex = im.getexif(); photo = {}
                try: photo = ex.get_ifd(ExifTags.IFD.Exif)
                except (KeyError,ValueError,TypeError): pass
                def value(tag): return photo.get(tag, ex.get(tag))
                def scalar(tag):
                    v=value(tag)
                    try: return float(v) if v is not None else None
                    except (ValueError,TypeError,ZeroDivisionError): return None
                record.update(width=im.width,height=im.height,timestamp=str(value(36867) or value(306) or '') or None,camera_make=str(value(271) or '') or None,camera_model=str(value(272) or '') or None,lens=str(value(42036) or '') or None,focal_length_mm=scalar(37386),exposure_seconds=scalar(33434),exif_orientation=value(274))
                display=ImageOps.exif_transpose(im).convert('L'); w,h=display.size
                record['display_orientation']='landscape' if w>h else 'portrait' if h>w else 'square'
                if min(w,h)<900 or max(w,h)<1600: record['review_reasons'].append('Low resolution: below advisory 1600-long / 900-short pixels')
                display.thumbnail((1024,1024));a=np.asarray(display,dtype=np.float32)
                if min(a.shape)>=3:
                    lap=-4*a[1:-1,1:-1]+a[:-2,1:-1]+a[2:,1:-1]+a[1:-1,:-2]+a[1:-1,2:]
                    score=float(lap.var());record['blur_laplacian_variance_1024']=round(score,3)
                    # shortcut: texture and sharpening affect this heuristic; visually review before rejecting real capture.
                    if score<10: record['review_reasons'].append('Possible severe blur/low texture: manually inspect at full size')
                    elif score<25: record['warnings'].append('Possible softness; inspect at full size')
                missing=[key for key in ['timestamp','camera_make','camera_model','lens','focal_length_mm','exposure_seconds','exif_orientation'] if record[key] is None]
                if missing: record['warnings'].append('Missing metadata: '+', '.join(missing))
        except (OSError,ValueError,Image.DecompressionBombError) as e:
            record['review_reasons'].append('Cannot decode locally: '+str(e));continue
        match = re.fullmatch(r'(normal|elevated|low)_(\d+)',p.stem)
        if sequence in PRIMARY:
            if match and match[1]==sequence: numbers.setdefault(sequence,[]).append(int(match[2]))
            else: record['warnings'].append('Original naming does not prove sequence continuity; confirm capture order manually')
    primary=[r for r in records if r['sequence'] in PRIMARY and r['width']]
    for key in ['camera_make','camera_model','lens','focal_length_mm','display_orientation']:
        counts=Counter(str(r[key]) for r in primary if r[key] is not None)
        if len(counts)>1:
            for r in primary: r['warnings'].append('Primary sequence '+key+' varies: '+', '.join(counts))
    resolutions=Counter((r['width'],r['height']) for r in primary)
    if len(resolutions)>1:
        for r in primary: r['warnings'].append('Primary resolution varies; inspect camera settings/crops')
    gaps={seq:[n for n in range(1,min(max(ns),10000)+1) if n not in ns] for seq,ns in numbers.items()}
    for seq,ns in numbers.items():
        if max(ns)>10000:
            for r in records:
                if r['sequence']==seq:r['warnings'].append('Sequence number exceeds 10000; gap scan capped, inspect names manually')
    for seq,ns in gaps.items():
        if ns:
            for r in records:
                if r['sequence']==seq:r['warnings'].append('Named sequence gaps: '+str(ns))
    ordinal=Counter()
    for r in records:
        seq=r['sequence'];ordinal[seq]+=1
        r['classification']='review' if r['review_reasons'] else 'passes_automatic_checks'
        r['manual_visual_review']='PENDING'
        p=incoming/r['original_filename']
        if not r['sha256']: continue
        bucket='rejected' if r['review_reasons'] else 'accepted'
        out=Path(bucket)/seq/(f'{seq}_{ordinal[seq]:03d}_{r["sha256"][:12]}'+p.suffix.lower())
        dest=root/out;dest.parent.mkdir(parents=True,exist_ok=True)
        if dest.exists():
            assert fingerprint(dest)==r['sha256'], f'Refusing overwrite: {dest}'
        else: shutil.copy2(p,dest)
        r['derived_working_filename']=out.as_posix()
        assert fingerprint(p)==r['sha256']==fingerprint(dest),'Copy verification failed'
    manifest={'schema_version':1,'generated_utc':datetime.now(timezone.utc).isoformat(),'status':'WAITING_FOR_CONTROLLED_PHOTOS' if not records else 'MANUAL_REVIEW_REQUIRED','originals_preserved':True,'accepted_means':'Passed automatic checks only; not approved for calibration','rejected_means':'Review copies only; originals remain in incoming; never auto-delete','naming_order':'Deterministic original-path order; not inferred chronological order','sequence_gaps':gaps,'expected_approximate_counts':{'normal':36,'elevated':18,'low_optional':12},'images':records}
    meta=root/'metadata';meta.mkdir(exist_ok=True)
    temp=meta/'capture-manifest.json.tmp';temp.write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n');temp.replace(meta/'capture-manifest.json')
    return manifest

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);args=parser.parse_args()
    result=inspect(args.root)
    print(json.dumps({'status':result['status'],'images':len(result['images']),'automatic_passes':sum(r['classification']=='passes_automatic_checks' for r in result['images']),'review':sum(r['classification']=='review' for r in result['images'])},indent=2))
