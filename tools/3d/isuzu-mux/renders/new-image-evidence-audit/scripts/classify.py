from pathlib import Path
from PIL import Image,ImageOps,ImageDraw,ImageFont
import json,math,itertools,sqlite3
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';S=P.parent/'Isuzu MU-X';R=B/'renders/new-image-evidence-audit';I=B/'references/authoritative-folder';D=B/'controlled-capture/reconstruction/current-folder-audit/small'
d=json.loads((I/'current-inventory.json').read_text());rows=d['images'];by={r['id']:r for r in rows}
# Side convention follows the existing canonical left/right profile inventory, not a solved camera pose.
angles={2:315,5:0,6:0,7:90,8:180,9:270,11:0,12:90,13:180,14:270,15:315,16:45,17:135,18:225,19:315,20:45,21:100,22:115,23:130,24:145,25:160,26:170,27:0,28:15,29:30,30:65,31:95,32:130,33:170,34:200,35:225,36:245,37:265,38:290,39:310,40:335,41:45,42:45}
view={0:'FRONT',15:'FRONT-LEFT',30:'FRONT-LEFT 3/4',45:'FRONT-LEFT 3/4',65:'LEFT-FRONT TRANSITION',90:'LEFT SIDE',95:'LEFT SIDE',100:'LEFT SIDE',115:'LEFT-REAR TRANSITION',130:'REAR-LEFT 3/4',135:'REAR-LEFT 3/4',145:'REAR-LEFT 3/4',160:'REAR-LEFT 3/4',170:'REAR',180:'REAR',200:'REAR-RIGHT 3/4',225:'REAR-RIGHT 3/4',245:'RIGHT-REAR TRANSITION',265:'RIGHT SIDE',270:'RIGHT SIDE',290:'RIGHT-FRONT TRANSITION',310:'FRONT-RIGHT 3/4',315:'FRONT-RIGHT 3/4',335:'FRONT-RIGHT 3/4'}
dups={'MUX-041':'MUX-020','MUX-042':'MUX-020','MUX-033':'MUX-026','MUX-032':'MUX-023'}
for r in rows:
 n=int(r['id'][-3:]);az=angles.get(n);exterior=n not in [3,4,10];g='G2' if n in [2,5,11,12,13,14,15,16,17,18] or n>=19 else 'G1'
 notes=[]
 if n in [1,4]:coverage='DETAIL';notes.append('Composite; not a single camera view.')
 elif n in [3,10]:coverage='DETAIL'
 else:coverage='FULL VEHICLE'
 if n in [30,31]:coverage='PARTIAL VEHICLE';notes.append('Tightly cropped; rear edge has little or no margin.')
 if n in [6,7,8,9]:notes.append('Open bonnet/doors/tailgate; displaced panels excluded from closed-body reconstruction.')
 if 20<=n<=42:notes.append('Consistent red turntable/viewer appearance; apparent CGI/render-style source is an inference, not verified provenance.')
 if n==19:notes.append('Independent silver studio/promotional view; not part of red sequence.')
 if n==43:notes.append('Single top-down reference; exact body/trim and association with red sequence unverified. No triangulation partner.')
 if r['id'] in dups:g='G0';notes.append('Repeated viewer pose/content after crop/scale normalization; representative '+dups[r['id']]+'.')
 r.update(exterior=exterior,view=view.get(az,'ENGINE DETAIL' if n==3 else 'INTERIOR' if n in [4,10] else 'MULTI-VIEW COLLAGE' if n==1 else 'TOP VIEW'),approximate_visual_azimuth=az,azimuth_note='APPROXIMATE VISUAL AZIMUTH; generally ±10–15°, not calibrated. Canonical side-label convention.' if az is not None else 'No single horizontal azimuth assigned.',height_view='HIGH VIEW' if n==43 else 'NORMAL VIEW' if n not in [3,4,10] else 'NOT APPLICABLE',vehicle_coverage=coverage,pixel_orientation='LANDSCAPE' if r['width']>=r['height'] else 'PORTRAIT',camera_consistency='UNKNOWN — no EXIF; resolution/crop inconsistent',body_family='UNCERTAIN — roof only' if n==43 else 'COMPATIBLE broad canonical body family; exact trim not verified' if exterior else 'Not an exterior-family constraint',same_physical_vehicle='UNCERTAIN',sequence_group='RED_VIEWER_SERIES' if 20<=n<=42 else 'INDEPENDENT_REFERENCE',geometric_class=g,near_duplicate_of=dups.get(r['id']),notes=notes)
unique=[r for r in rows if not r['near_duplicate_of']];new=[r for r in unique if not r['previous_hash_match']];evidence=[r for r in unique if r['geometric_class'] in ['G2','G3']]
exact={};decoded={}
for r in rows:exact.setdefault(r['sha256'],[]).append(r['id']);decoded.setdefault(r.get('decoded_sha256','unreadable'),[]).append(r['id'])
counts={'previous_known':18,'current_total_files':d['total_files'],'readable_images':sum(r['readable'] for r in rows),'new_files_discovered':sum(not r['previous_hash_match'] for r in rows),'new_unique_visual_images':len(new),'exact_duplicate_extra_files':sum(len(v)-1 for v in exact.values()),'decoded_duplicate_extra_files':sum(len(v)-1 for v in decoded.values()),'near_duplicate_extra_files':len(dups),'near_duplicate_groups':3,'unreadable':sum(not r['readable'] for r in rows),'current_byte_unique_images':len(exact),'current_unique_visual_images':len(unique),'geometric_classes_all_files':{k:sum(r['geometric_class']==k for r in rows) for k in ['G3','G2','G1','G0']}}
d.update(status='COMPLETE — visual audit and bounded registration test; Decision B',counts=counts,definitions={'unique_visual_images':'Distinct visual source views after confirmed near-repeat groups; ordinary adjacent changing views are retained.','exact_unique':'Whole-file SHA-256 uniqueness, reported separately from repeated crop/scale versions.','G3':'Validated strong geometric evidence; none accepted after the camera test.','G2':'Supporting design/proportion/overlap evidence; not validated 3D depth.'})
(I/'current-inventory.json').write_text(json.dumps(d,indent=2))
recon={'decision':'B — USEFUL NEW REFERENCES, BUT GEOMETRY REMAINS UNDERCONSTRAINED','source':str(S),'historical_inventory_preserved':str(I/'inventory.json'),'counts':counts,'new_image_ids':[r['id'] for r in rows if not r['previous_hash_match']],'new_unique_image_ids':[r['id'] for r in new],'exact_duplicate_groups':[v for v in exact.values() if len(v)>1],'near_duplicate_groups':[['MUX-020','MUX-041','MUX-042'],['MUX-026','MUX-033'],['MUX-023','MUX-032']],'duplicate_method':'Whole-file and decoded RGB hashes; red-envelope crop/scale SIFT homography checks; visual review. First two groups have identical normalized vehicle pixels, third aligned RGB mean absolute difference ~0.60/255 and 97.85% homography inliers. Other similar neighboring poses are not collapsed.','same_vehicle':'UNCERTAIN physically; likely same depicted asset within red viewer group.','new_image_type':'MIXED — consistent viewer-style sequence plus independent general references; no controlled physical capture verified.','registration_test':str(D/'logs/registration-result.json'),'modeling':'NOT STARTED','limitations':'No EXIF, unknown source projection/lens, variable screenshots/crops; blank backdrop/viewer floor. No inference from the old failed bodies.'}
(I/'new-image-reconciliation.json').write_text(json.dumps(recon,indent=2))
F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',19);SM=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',14);BIG=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',30)
def sheet(items,name,title):
 out=Image.new('RGB',(2100,70+math.ceil(len(items)/5)*330),'#191e25');draw=ImageDraw.Draw(out);draw.text((15,15),title,font=BIG,fill='white')
 for i,r in enumerate(items):
  x=i%5*420;y=70+i//5*330
  with Image.open(S/r['relative_path']) as src:im=ImageOps.contain(ImageOps.exif_transpose(src).convert('RGB'),(404,240));out.paste(im,(x+(420-im.width)//2,y+40+(240-im.height)//2))
  draw.text((x+8,y+5),f'{r["id"]} / {r["geometric_class"]} / '+('OLD' if r['previous_hash_match'] else 'NEW'),font=F,fill='white');draw.text((x+8,y+285),r['view'],font=SM,fill='#d5dce6');draw.text((x+8,y+307),r['filename'][:48],font=SM,fill='#b5bdca')
 out.save(R/name,quality=95)
sheet(unique,'all-images-contact-sheet.jpg','39 distinct visual images / 43 files; repeated-view copies indexed in inventory')
sheet(new,'new-images-contact-sheet.jpg','21 new distinct references / not verified controlled photography')
sheet(sorted(evidence,key=lambda r:(r['approximate_visual_azimuth'] is None,r['approximate_visual_azimuth'] or 0)),'geometric-evidence-contact-sheet.jpg','G2 supporting views arranged by apparent azimuth / not a reconstructed orbit')
# Diagram: previous/new visual coverage must not be mistaken for metric camera poses.
out=Image.new('RGB',(1600,1350),'#191e25');draw=ImageDraw.Draw(out);cx,cy=800,610;rad=400
for rr in [rad,rad-90]:draw.ellipse((cx-rr,cy-rr,cx+rr,cy+rr),outline='#737e8c',width=2)
for a,label in [(0,'FRONT 0'),(45,'FRONT-LEFT'),(90,'LEFT 90'),(135,'REAR-LEFT'),(180,'REAR 180'),(225,'REAR-RIGHT'),(270,'RIGHT 270'),(315,'FRONT-RIGHT')]:
 th=math.radians(a);x=cx-(rad+110)*math.sin(th);y=cy-(rad+110)*math.cos(th);draw.text((x-65,y-10),label,font=F,fill='white')
for old,rr,color in [(True,rad-90,'#80b7ff'),(False,rad,'#ff8791')]:
 for i,r in enumerate([r for r in unique if r['previous_hash_match']==old and r['approximate_visual_azimuth'] is not None and r['geometric_class']=='G2']):
  a=r['approximate_visual_azimuth'];th=math.radians(a);radius=rr+(i%3-1)*14;x=cx-radius*math.sin(th);y=cy-radius*math.cos(th);draw.ellipse((x-6,y-6,x+6,y+6),fill=color);draw.text((x+8,y-9),r['id'][-3:],font=SM,fill=color)
seq=sorted([r for r in unique if r['sequence_group']=='RED_VIEWER_SERIES'],key=lambda r:r['approximate_visual_azimuth']);angs=[r['approximate_visual_azimuth'] for r in seq]
for a,b in zip(angs,angs[1:]+[angs[0]+360]):
 if b-a>25:
  pts=[(cx-(rad+32)*math.sin(math.radians(t)),cy-(rad+32)*math.cos(math.radians(t))) for t in range(a,b+1)];draw.line(pts,fill='#e4ba63',width=6)
draw.text((30,20),'APPROXIMATE VISUAL AZIMUTH / COVERAGE',font=BIG,fill='white');draw.text((cx-150,cy-55),'Decision B\nMore visual angles\nNO VALIDATED 3D ORBIT',font=BIG,fill='white')
for i,text in enumerate(['Blue inner ring: old supporting references / Red outer ring: new distinct supporting views','Amber arcs: estimated new-sequence gaps >25 degrees; no calibrated angular measurement','Main eight sectors have visual examples. No verified elevated/low orbit; one independent top view.','Dense angle coverage is not reliable depth. Sources/crops differ; physical capture provenance unknown.']):draw.text((40,1140+i*42),text,font=F,fill='#d5dce6')
out.save(R/'angle-coverage-map.jpg',quality=95)
sheet(seq,'sequence-map.jpg','Apparent red viewer orbit / visual overlap MODERATE; camera-geometry gate FAILED')
# Exact model camera positions and unfiltered sparse points in three orthogonal projections.
reg=json.loads((D/'logs/registration-result.json').read_text());out=Image.new('RGB',(2100,1500),'#191e25');draw=ImageDraw.Draw(out)
for row,m in enumerate(reg['models']):
 pts=json.loads((D/'sparse'/f'model-{m["model"]}-points.json').read_text());co=[p['xyz'] for p in pts];cams=m['cameras'];allpts=co+[p['center'] for p in cams]
 for col,(ax,ay,label) in enumerate([(0,1,'XY'),(0,2,'XZ'),(1,2,'YZ')]):
  x0=col*700+40;y0=row*700+85;w=620;h=560;lo=[min(v[k] for v in allpts) for k in [ax,ay]];hi=[max(v[k] for v in allpts) for k in [ax,ay]];scale=min(w/max(hi[0]-lo[0],1e-6),h/max(hi[1]-lo[1],1e-6))*.85
  mid=[(lo[i]+hi[i])/2 for i in [0,1]]
  def screen(v):return (x0+w/2+(v[ax]-mid[0])*scale,y0+h/2-(v[ay]-mid[1])*scale)
  draw.rectangle((x0,y0,x0+w,y0+h),outline='#637080');draw.text((x0,y0-45),f'Model {m["model"]} / {label} / REJECTED',font=BIG,fill='white')
  for p in co:
   x,y=screen(p);draw.ellipse((x-2,y-2,x+2,y+2),fill='#aab4c2')
  for cam in cams:
   x,y=screen(cam['center']);draw.ellipse((x-6,y-6,x+6,y+6),fill='#ff7b89');draw.text((x+7,y+4),cam['name'][4:7],font=SM,fill='#ffb0ba')
   rot=cam['rotation_world_to_camera'];forward=rot[2];end=[cam['center'][k]+forward[k]*max(hi[0]-lo[0],hi[1]-lo[1])*.08 for k in range(3)];draw.line([(x,y),screen(end)],fill='#ff7b89',width=2)
  draw.text((x0,y0+h+8),f'{m["registered_images"]}/6 cameras, {m["sparse_points"]} points, mean error {m["point_error_mean"]:.3f}px',font=SM,fill='white')
draw.text((25,1430),'Unscaled SfM coordinates. All sparse points shown; no vehicle-shape prior or nominal-dimension fit. Low residual != valid geometry.',font=F,fill='white');out.save(R/'registered-camera-orbit.jpg',quality=95)
tracks=json.loads((D/'diagnostics/observed-vehicle-tracks.json').read_text());out=Image.new('RGB',(2400,math.ceil(len(tracks)/3)*570),'#191e25');draw=ImageDraw.Draw(out)
for i,t in enumerate(tracks):
 im=ImageOps.contain(Image.open(t['overlay']).convert('RGB'),(780,510));x=i%3*800;y=i//3*570;out.paste(im,(x+(800-im.width)//2,y+40));draw.text((x+8,y+8),f'Model {t["model"]} / {t["image"]} / {t["observed_track_count"]} tracks',font=F,fill='white')
out.save(R/'sparse-vehicle-evidence.jpg',quality=95)
print(json.dumps(counts,indent=2));print('Classifications, coverage, contact sheets and rejected camera diagnostics saved')
