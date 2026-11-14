"""Small synthetic checks: originals/copies, metadata, flags, gaps and empty state."""
from pathlib import Path
from tempfile import TemporaryDirectory
from PIL import Image
import numpy as np
from validate_capture import inspect, fingerprint

with TemporaryDirectory() as temp:
    root=Path(temp);(root/'incoming/normal').mkdir(parents=True)
    assert inspect(root)['status']=='WAITING_FOR_CONTROLLED_PHOTOS'
    rng=np.random.default_rng(1)
    im=Image.fromarray(rng.integers(0,255,(1000,1800,3),dtype=np.uint8))
    ex=Image.Exif();ex[271]='Phone';ex[272]='Model A';ex[274]=1;ex[306]='2026:11:07 12:00:00';ex[37386]=4.5;ex[33434]=.005;ex[42036]='Main'
    one=root/'incoming/normal/normal_001.jpg';im.save(one,exif=ex)
    two=root/'incoming/normal/normal_003.jpg';two.write_bytes(one.read_bytes())
    ex[272]='Model B';ex[274]=6;im.save(root/'incoming/normal/normal_004.jpg',exif=ex)
    Image.new('RGB',(400,300),'gray').save(root/'incoming/normal/normal_005.jpg')
    (root/'incoming/broken.jpg').write_bytes(b'not an image')
    before={p:fingerprint(p) for p in (root/'incoming').rglob('*') if p.is_file()}
    result=inspect(root);assert len(result['images'])==5
    records={r['original_filename']:r for r in result['images']}
    good=records['normal/normal_001.jpg'];assert good['classification']=='passes_automatic_checks' and good['camera_make']=='Phone'
    assert good['focal_length_mm']==4.5 and good['exposure_seconds']==.005
    assert any('duplicate' in s for s in records['normal/normal_003.jpg']['review_reasons'])
    assert any('Low resolution' in s for s in records['normal/normal_005.jpg']['review_reasons'])
    assert any('blur' in s for s in records['normal/normal_005.jpg']['review_reasons'])
    assert any('Cannot decode' in s for s in records['broken.jpg']['review_reasons'])
    assert result['sequence_gaps']['normal']==[2]
    assert any('camera_model varies' in s for s in good['warnings'])
    assert any('display_orientation varies' in s for s in good['warnings'])
    assert all(fingerprint(p)==h for p,h in before.items())
    assert inspect(root)['images']==result['images'],'Rerun must preserve mappings and flags'
print('PASS: empty state, EXIF, orientation, camera change, duplicates, gaps, blur, resolution, corrupt files, originals, idempotent copies')
