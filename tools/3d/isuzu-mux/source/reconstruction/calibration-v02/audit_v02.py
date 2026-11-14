"""Audit observations by physical identity/visibility, never by residual alone."""
from pathlib import Path
import json,csv,hashlib
from PIL import Image,ImageDraw
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'source/reconstruction/calibration-v02';PROJECT=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');OLD=PROJECT/'tools/3d/isuzu-mux/source/reconstruction'
S=json.loads((OLD/'joint-solution.json').read_text());D=json.loads((OLD/'observations.json').read_text());P=json.loads((OLD/'shared-landmarks.json').read_text());CORE=[6,7,9,8,11,12]
# Classifications apply before V02 fitting. No point is excluded just for exceeding a numeric cutoff.
def classify(o):
 b=o['base'];i=o['camera'];side=o['side']
 if b.startswith('wc_'):return 'A','visible rim/hub center','static wheel reference','core eligible'
 if b.startswith('contact_'):return 'A','visible tire/floor contact with finite-width patch uncertainty','static contact measurement','core eligible'
 if b.startswith('tiretop_'):return 'C','apparent tire silhouette tangent is view-dependent, not a verified fixed 3D surface point','view-dependent tangent','reject fixed-point assumption; retain as visual tire reference'
 if b in ['h_out','h_in']:return 'A','fixed lamp envelope corner, visually identifiable; annotation uncertainty remains','static body lamp','core eligible'
 if b in ['tl_top','tl_low']:return 'A','fixed outer body lamp segment only; moving hatch segments absent','static body lamp','core eligible'
 if b.startswith('ws_'):
  if i==6 or (i==11 and side=='L') or (i==10 and side=='R'):return 'A','closed visible windshield border; corrected V01 semantic definition','closed glass structural border','core eligible'
  return 'B','grazing or far windshield/cowl corner; possible trim/occlusion ambiguity','partial/grazing static glass','validation only in initial structural solve'
 if b in ['g_top','g_low','bumper']:return 'B','fixed fascia/bumper but trim/curvature-boundary definition is less certain','static facade reference','validation/detail only in structural solve'
 if b in ['arch_F','arch_R']:
  return ('B','near-profile opening apex, uncertain relation to physical crown','near-profile apparent contour','validation only') if i in [2,4,7,9] else ('C','oblique arch apex is an apparent contour, not assured identical physical point','view-dependent tangent','reject fixed-point assumption')
 if b in ['q_ft','q_fb']:return 'B','quarter-glass fillet/trim transition has no subpixel corner; small in oblique views','rounded fixed glazing border','validation/detail only; do not fit initial core'
 if b in ['q_rt','q_rb']:return 'C','rounded rear glass/seal silhouette; camera-dependent tangent location','view-dependent rounded glazing','reject fixed-point identity until a stable feature is verified'
 if b in ['rw_top','rw_base']:
  far=(i==12 and side=='R') or (i==13 and side=='L')
  if far:return 'C','far rounded black-glazing border lacks an identifiable corresponding physical corner; perspective/partial visibility','far/grazing rounded glazing','reject current shared-point observation'
  return 'B','outer ceramic/glazing corner definition remains rounded/partially under spoiler','rounded static glazing border','validation only; initial frame solve excludes this ambiguity'
 if b=='hatch_low':return 'C','rounded closed hatch seam changes apparent corner with perspective; no exact repeatable physical point established','closed but view-dependent seam pick','reject current fixed-point correspondence; not open-panel contamination'
 raise ValueError(b)
rows=[]
for o in S['observations']:
 c,why,visible,action=classify(o);u,v=o['projected'];x,y=o['xy'];r={**o,'dx':u-x,'dy':v-y,'category':o['base'],'confidence':c,'confidence_reason':why,'visibility':visible,'static_or_moving':'STATIC / viewpoint-dependent if noted','core_camera':o['camera'] in CORE,'v02_initial_use':bool(c=='A' and o['camera'] in CORE),'decision':action}
 rows.append(r)
rows.sort(key=lambda x:x['error_pixels'],reverse=True)
(OUT/'v01-residual-audit.json').write_text(json.dumps(rows,indent=2)+'\n')
fields=['camera','landmark','category','confidence','visibility','confidence_reason','core_camera','v02_initial_use','decision','observed_x','observed_y','predicted_x','predicted_y','dx','dy','euclidean_residual','v01_heldout']
with (OUT/'v01-residual-audit.csv').open('w',newline='') as f:
 w=csv.DictWriter(f,fieldnames=fields);w.writeheader()
 for o in rows:w.writerow({**{k:o[k] for k in fields if k in o},'observed_x':o['xy'][0],'observed_y':o['xy'][1],'predicted_x':o['projected'][0],'predicted_y':o['projected'][1],'dx':o['dx'],'dy':o['dy'],'euclidean_residual':o['error_pixels'],'v01_heldout':o['heldout']})
# Audit every V01 named landmark, including zero-use or rejected identities.
landmarks=[]
for name,xyz in P.items():
 obs=[o for o in rows if o['landmark']==name];a=[o for o in obs if o['v02_initial_use']]
 landmarks.append({'landmark':name,'observations':len(obs),'v01_rms':(sum(o['error_pixels']**2 for o in obs)/len(obs))**.5 if obs else None,'v01_max':max([o['error_pixels'] for o in obs],default=None),'confidence_classes':sorted(set(o['confidence'] for o in obs)),'v02_structural_observations':len(a),'status':'CORE CANDIDATE' if a else 'VALIDATION/DETAIL ONLY OR REJECTED FIXED-POINT IDENTITY','per_observation_decisions':[{'camera':o['camera'],'class':o['confidence'],'reason':o['confidence_reason'],'decision':o['decision']} for o in obs]})
(OUT/'v01-landmark-audit.json').write_text(json.dumps(landmarks,indent=2)+'\n')
compat=[]
for i in [1,2,3,4,6,7,8,9,10,11,12,13]:
 for j in [1,2,3,4,6,7,8,9,10,11,12,13]:
  if i==j:label='same view';why='identical image'
  elif (i<5)!=(j<5):label='compatible for structural calibration only';why='visually matching fixed body, but open/closed panels displaced; no cross-state panel corners'
  elif i>=6 and j>=6:label='strongly compatible';why='matching visible body/trim/wheels and closed configuration; geometric calibration still must be validated'
  else:label='limited compatibility';why='matching open vehicle but occlusions and moving panel identities limit common stable features'
  compat.append({'image_a':i,'image_b':j,'classification':label,'reason':why})
(OUT/'view-compatibility.json').write_text(json.dumps(compat,indent=2)+'\n')
selection=[]
for i in range(1,14):
 if i in CORE:role='CALIBRATION + DETAIL';reason='one selected closed view for required front/left/right/rear/front-quarter/rear-quarter constraints'
 elif i in [2,4,10,13]:role='CALIBRATION ONLY';reason='external structural validation/pose candidates; not used to fit shared landmark geometry; detail remains available qualitatively'
 elif i in [1,3]:role='DETAIL ONLY';reason='sparse static anchors and open-panel occlusion; project for diagnosis, not trusted core pose validation'
 else:role='EXCLUDED';reason='interior panorama does not share stable exterior anchors'
 selection.append({'image':i,'role':role,'core':i in CORE,'reason':reason})
(OUT/'core-selection.json').write_text(json.dumps(selection,indent=2)+'\n')
exif=[]
for im in D['images']:
 photo=Image.open(im['path']);exif.append({'image':im['image'],'size':photo.size,'exif':dict(photo.getexif()),'metadata_keys':list(photo.info),'reliable_focal_metadata':False})
(OUT/'image-metadata.json').write_text(json.dumps(exif,indent=2)+'\n')
# Exact worst V01 evidence, preserving the original photo and both point locations.
w=rows[0];path=next(i['path'] for i in D['images'] if i['image']==w['camera']);im=Image.open(path).convert('RGB');dr=ImageDraw.Draw(im);x,y=w['xy'];u,v=w['projected'];dr.line((x,y,u,v),fill='#ff2020',width=3);dr.ellipse((x-5,y-5,x+5,y+5),outline='#ffff00',width=2);dr.rectangle((u-4,v-4,u+4,v+4),outline='#00ffff',width=2)
im.crop((100,150,420,290)).resize((960,420)).save(ROOT/'renders/v01-worst-residual-review-v02.jpg',quality=95)
worst={'camera':w['camera'],'landmark':w['landmark'],'category':w['category'],'residual_pixels':w['error_pixels'],'observed':w['xy'],'projected':w['projected'],'primary_failure':['H — shared-landmark identity not established for rounded apparent glazing boundary','E — oblique perspective/tangency ambiguity'],'possible_contributors':['A — uncertain manual point definition','F — depth/pose tradeoff'],'not_supported_by_evidence':['B — different trim','C — open-panel displacement (image 13 is closed)','G — lens distortion as the cause'],'conclusion':'Reject current far-corner observation by semantic visibility rule, not merely because residual is large. Apply same rule to other far rounded glass corners.'}
(OUT/'worst-residual-diagnosis.json').write_text(json.dumps(worst,indent=2)+'\n')
print('Audited',len(rows),'observations,',len(landmarks),'named landmarks; core A counts:',{i:sum(o['v02_initial_use'] and o['camera']==i for o in rows) for i in CORE})
# Read-only preservation manifest: full static src/public/config and protected project source/config, no dependency trees.
manifest={}
for root in [PROJECT,PROJECT.parent/'toli-3d-website',PROJECT.parent/'tolimotors-main']:
 if not root.exists():continue
 candidates=[]
 for folder in ['src']:
  p=root/folder
  if p.exists():candidates+=list(p.rglob('*'))
 candidates += [p for p in root.iterdir() if p.is_file() and p.suffix in ['.json','.ts','.js','.html','.css']]
 if root==PROJECT:
  candidates+=list((root/'public').rglob('*'))
  candidates+=list((root/'tools/3d/isuzu-mux/source').rglob('*.blend'))
  candidates += [OLD/'joint-solution.json',OLD/'observations.json',PROJECT/'tools/3d/isuzu-mux/MULTIVIEW_RECONSTRUCTION.md']
 for p in candidates:
  if p.is_file():manifest[str(p)]=hashlib.sha256(p.read_bytes()).hexdigest()
(ROOT/'preservation-before.json').write_text(json.dumps(manifest,indent=2)+'\n')
