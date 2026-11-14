from pathlib import Path
from PIL import Image,ImageDraw,ImageOps,ImageFont
import json,hashlib,os,math,itertools,shutil,textwrap,sqlite3
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';I=B/'references/authoritative-folder';R=B/'renders/new-image-evidence-audit';D=B/'controlled-capture/reconstruction/current-folder-audit/small';S=P.parent/'Isuzu MU-X';d=json.loads((I/'current-inventory.json').read_text());rows=d['images'];by={v['id']:v for v in rows};c=d['counts'];reg=json.loads((D/'logs/registration-result.json').read_text())
F=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',24);SM=ImageFont.truetype('/usr/share/fonts/noto/NotoSans-Regular.ttf',18)
comparisons=[('Bonnet / front fender','MUX-016',(140,230,540,480),'MUX-030',(70,130,510,445),'More side falloff and arch/bonnet relationship; no trustworthy compound-depth reconstruction.'),('Cowl / A-pillar','MUX-016',(300,145,610,330),'MUX-030',(300,70,680,270),'Closer intermediate angle makes the junction easier to see; root section still inferred.'),('Roof / greenhouse','MUX-012',(390,110,920,290),'MUX-043',None,'New top view supplies planform information; single uncalibrated image has no height partner.'),('D-pillar / rear quarter','MUX-017',(450,120,820,420),'MUX-023',(600,110,1040,590),'Additional rear-angle transitions clarify shape; no validated D/quarter depth.'),('Rear bumper corner','MUX-017',(580,290,900,495),'MUX-025',(650,360,1040,670),'More corner-wrap appearance; registration did not establish rear-body geometry.')]
out=Image.new('RGB',(2550,5*620),'#191e25');draw=ImageDraw.Draw(out)
for i,(label,old,crop1,new,crop2,note) in enumerate(comparisons):
 for col,key,crop in [(0,old,crop1),(1,new,crop2)]:
  with Image.open(S/by[key]['relative_path']) as src:im=ImageOps.exif_transpose(src).convert('RGB');im=im.crop(crop) if crop else im;im=ImageOps.contain(im,(818,535));out.paste(im,(col*850+(850-im.width)//2,i*620+60+(535-im.height)//2))
  draw.text((col*850+14,i*620+12),label+' / '+('OLD ' if col==0 else 'NEW ')+key,font=F,fill='white')
 draw.text((1715,i*620+30),'VISUAL IMPROVEMENT: YES\nVALIDATED DEPTH: NO',font=F,fill='#ffd18a');draw.multiline_text((1715,i*620+150),'\n'.join(textwrap.wrap(note,48)),font=F,fill='white',spacing=10)
out.save(R/'difficult-regions-before-after.jpg',quality=95)
# Keep every executed script and raw test record; no old inventory/report is replaced.
(R/'scripts').mkdir(exist_ok=True)
for name in ['inventory.py','prepare_test.py','run_sfm.py','duplicates.py','project_points.py','classify.py']:
 shutil.copyfile(Path('/tmp/mux-image-audit')/name,R/'scripts'/name)
unique=[v for v in rows if not v['near_duplicate_of']];seq=sorted([v for v in unique if v['sequence_group']=='RED_VIEWER_SERIES'],key=lambda v:v['approximate_visual_azimuth']);angles=[v['approximate_visual_azimuth'] for v in seq];gaps=[{'from':a,'to':b%360,'estimated_gap':b-a} for a,b in zip(angles,angles[1:]+[angles[0]+360])]
con=sqlite3.connect(D/'registration.db');names=dict(con.execute('select image_id,name from images').fetchall());pairs=[]
for pair_id,n,config in reg['verified_pairs']:
 a=pair_id//2147483647;b=pair_id%2147483647;pairs.append({'a':names[a],'b':names[b],'verified_matches':n,'configuration_code':config})
for m in reg['models']:
 lengths=[math.dist(a['center'],b['center']) for a,b in itertools.combinations(m['cameras'],2)];m['baseline_diagnostic']={'minimum':min(lengths),'maximum':max(lengths),'max_min_ratio':max(lengths)/min(lengths)}
# Preservation: unchanged old evidence/website/protected assets; new source files have their own beginning-of-audit hashes.
frozen=json.loads((B/'FREEZE_PRESERVATION_MANIFEST.json').read_text());changed=[];checked=0
for name,v in frozen['files'].items():
 if name==str(B/'RECONSTRUCTION_STATUS.md'):continue
 f=Path(name)
 if 'symlink' in v:ok=f.is_symlink() and os.readlink(f)==v['symlink']
 else:
  h=hashlib.sha256()
  with f.open('rb') as stream:
   for part in iter(lambda:stream.read(1024*1024),b''):h.update(part)
  ok=h.hexdigest()==v['sha256']
 checked+=1
 if not ok:changed.append(name)
assert not changed,changed
for v in rows:assert hashlib.sha256((S/v['relative_path']).read_bytes()).hexdigest()==v['sha256'],v['relative_path']
validation={'decision':'B — USEFUL NEW REFERENCES, BUT GEOMETRY REMAINS UNDERCONSTRAINED','old_manifest_files_verified':checked,'source_images_hash_verified':len(rows),'unexpected_changes':[],'all_images_readable':True,'all_images_have_classification':True,'duplicate_accounting':'43 files - 4 repeated-view extra copies = 39 distinct visual images; 25 new files - 4 repeats = 21 new distinct references','registration':'ATTEMPTED — camera-geometry gate FAIL','full_sparse_expansion':'NOT ATTEMPTED','dense':'NOT ATTEMPTED','new_production_body':'NOT GENERATED','new_glb':'NOT EXPORTED','website':'UNCHANGED','controlled_capture':'PRESERVED; new isolated test appended','protected_projects':'UNCHANGED (manifest scope; runtime directories excluded)','cost':'₹0 / $0','deployment':'NOT PERFORMED','git_commit':'NOT PERFORMED'}
(R/'validation.json').write_text(json.dumps(validation,indent=2));(R/'overlap-and-camera-diagnostics.json').write_text(json.dumps({'visual_sequence_order':[v['id'] for v in seq],'approximate_angular_gaps':gaps,'pairwise_verified_matches':pairs,'models':reg['models'],'physical_camera_orbit_gate':'FAIL','camera_consistency':'UNKNOWN; files/crops inconsistent; no EXIF','focal_caution':'Estimated camera parameters are failed reconstruction outputs, not metadata or real lens measurements.'},indent=2))
# Consolidated report.
L=['# MU-X new image evidence audit','', '**B — USEFUL NEW REFERENCES, BUT GEOMETRY REMAINS UNDERCONSTRAINED**','',
'Authoritative source: '+str(S)+'. Recursively scanned directly. No request to move images into incoming. No modeling or Blender production-body generation occurred.','',
'## Previous state reviewed','',
'Read the current reconstruction status, reusable-data summary, best-evidence index, authoritative-folder reconciliation, Existing-photo Production V01 report, historical 18-image inventory and saved audit metadata. Prior exterior candidates remain failed research, never geometric truth. The old 18 images were not substituted for the newly uploaded series in the registration test.','',
'## Exact inventory and duplicate counts','',
'| Measure | Count |','|---|---:|']
for label,key in [('Previous known images','previous_known'),('Total current files','current_total_files'),('Readable images','readable_images'),('New files discovered','new_files_discovered'),('New distinct visual images','new_unique_visual_images'),('Exact duplicate extra files','exact_duplicate_extra_files'),('Near-duplicate extra files','near_duplicate_extra_files'),('Unreadable','unreadable'),('Total current distinct visual images','current_unique_visual_images'),('Whole-file SHA-256 unique images','current_byte_unique_images')]:L.append(f'| {label} | {c[key]} |')
L += ['',
'All 43 files have different whole-file and decoded-image hashes. Four are redundant viewer crops/scale variants, in three groups: MUX-020/041/042 (two extra copies), MUX-026/033 (one), MUX-023/032 (one). Representatives are 020, 026 and 023. The first two groups have identical normalized red-vehicle crop pixels; the third has aligned RGB mean absolute difference about 0.60/255 and 97.85% SIFT homography inliers. Visual inspection confirms repeated pose/content. These are near duplicates at file level, not modified originals. Ordinary neighboring poses such as 021/022 and 024/025 are retained because perspective/visible surfaces actually change.',
'',
'“Unique” means distinct visual views after those confirmed repeat groups, not only a new filename or byte encoding. This is why 43 byte-unique images correspond to 39 distinct visual references, and 25 new files correspond to 21 new distinct references. No original historical inventory was overwritten.',
'',
'## Source type, same-vehicle and body-family assessment','',
'- New-image type: **MIXED**. Nineteen distinct red viewer-series angles, one independent silver studio/promotional view and one roof-only reference. The red series has turntable/CGI-style appearance; that is a visual inference, not verified source provenance. It is not documented controlled photography.',
'- Same physical vehicle: **UNCERTAIN**. The red series likely depicts the same visual asset/configuration, judging by wheels, roof rails, steps, glazing and body/light details. This does not establish a shared physical vehicle/camera session, and the silver/top references are not proven to belong to it.',
'- Body family: **NEEDS REVIEW at exact trim/source level; broadly compatible** with the canonical tall/upright body, angular chrome-bar fascia and broad split rear-lamp family. No clearly incompatible generation is positively identified in the new red series. Roof-only 043 cannot verify generation/trim alone; wheels/tyre treatment and replaceable fascia trim are not canonical dimensional evidence.',
'',
'## Metadata and camera consistency','',
'EXIF present: **0/43**. Camera model, lens, physical focal length, 35mm equivalent and capture timestamp are **UNKNOWN**, not fabricated. Pixel dimensions and aspect/orientation are recorded for every image. All new files are landscape, but their resolutions and crops vary. Across the full inventory there is also a portrait/near-square interior composite. Source formats: PNG, AVIF and JPEG; all were locally readable. No HEIC/TIFF file was present.',
'',
'Same camera: **UNKNOWN**. Same lens: **UNKNOWN**. Resolution/crop consistency: **INCONSISTENT**. Overall physical-camera consistency: **UNKNOWN**; visual styling within the red viewer group is mostly consistent. Filenames resembling screenshot times are not EXIF exposure times. No sensor size, camera intrinsics or real zoom sequence is inferred from filenames.',
'',
'## Visual angle coverage and sequence','',
'**APPROXIMATE VISUAL AZIMUTH**, typically uncertain by roughly 10–15 degrees; not calibrated camera poses. Front=0, canonical left profile≈90, rear≈180, right≈270. Left/right follows the existing canonical profile convention and is not a recovered pose solution.',
'',
'| Sector | Previous supporting examples | New distinct supporting examples |','|---|---|---|']
sectors=[('Front',0),('Front-left',45),('Left',90),('Rear-left',135),('Rear',180),('Rear-right',225),('Right',270),('Front-right',315)]
for label,az in sectors:
 group=lambda old:[v['id'] for v in unique if v['geometric_class']=='G2' and v['previous_hash_match']==old and v['approximate_visual_azimuth'] is not None and abs((v['approximate_visual_azimuth']-az+180)%360-180)<=22.5]
 L.append('| '+label+' | '+', '.join(group(True))+' | '+', '.join(group(False))+' |')
L += ['',
'The red viewer series spans all principal sectors, with approximate intermediate angles '+', '.join(map(str,angles))+' degrees. Largest estimated gaps are about '+str(max(v['estimated_gap'] for v in gaps))+' degrees. Angle uncertainty and source differences prevent treating this as a measured orbit.',
'',
'- Normal orbit: **plausible viewer-style visual sequence**, substantially better intermediate coverage than the old sparse views; not a validated physical-camera orbit.',
'- Elevated orbit: **ABSENT**. One independent top-down image (043) improves planform understanding but has no overlapping elevated sequence.',
'- Low orbit: **ABSENT**. No continuous new low-view sequence identified.',
'- Overlap: **MODERATE visually, WEAK for validated geometric linkage**. Adjacent images share vehicle structure, but several tested cross-view pairs fail useful matching and the resulting camera fragments are inconsistent. No unrelated silver/roof image was forced into the red sequence.',
'',
'## Geometric classifications','',
'All-file classifications: **G3=0, G2=31, G1=8, G0=4**. Among 39 distinct visual images, 31 are supporting G2 references and eight are G1. G0 entries are redundant viewer copies. G3 is reserved for strong accepted geometric evidence; none was established by this test. G2 means supporting design/proportion evidence, not calibrated depth.',
'',
'## Previous failure regions — before and after','',
'| Region | Old evidence | New evidence | Visual improvement | Reliable depth resolved? |','|---|---|---|---|',
'| Bonnet crown / side falloff | Sparse silver front/3Q views | Red intermediate front/side angles; roof reference | YES | NO |',
'| Front fender / bonnet relationship | Front/side/3Q silhouette but weak cross-section | 029/030/031 show a closer transition | YES | NO |',
'| Cowl / A-pillar root | Silver 016 and profile 012 | Red 030/038/039 provide more viewing directions | YES | NO |',
'| Windscreen / greenhouse | Sparse front/side/rear examples | Red intermediate views and new roof planform 043 | YES | NO |',
'| Quarter glass / D-pillar | 017/018 rear3Q and profile | 022–026, 034/035 clarify shape progression | YES | NO |',
'| Rear-quarter depth | Sparse rear/3Q views | Denser red rear-angle transitions | YES | NO |',
'| Tail-lamp / quarter relationship | Canonical rear and rear3Q | Additional oblique wrap views | YES | NO |',
'| Rear bumper corner | Rear and two 3Q examples | Several red intermediate corner angles | YES | NO |',
'| Rear taper | Profile/rear/3Q | Additional left/right rear transitions plus top outline | YES | NO |',
'',
'New images solve gaps in visual coverage and clarify appearance/planform. They do not yet resolve a trustworthy compound cross-section for the bonnet/fender, root, D-pillar, quarter or corner. “YES” above is visual understanding, not a geometric approval.',
'',
'## Bounded registration test','',
'**ATTEMPTED**, because a plausible overlapping new series exists. Existing local PyCOLMAP 4.2.1 / OpenCV 5.0.0 were used on CPU with two threads; no installation, paid service, API or cloud reconstruction.',
'',
'Selected six new images: 027, 028, 029, 041, 030, 031. 041 is a repeat of 020, but 020 was not included, so the subset contains no confirmed duplicate pair. New source images only; original files unchanged. Full-resolution RGB PNG derivatives and reviewed coarse vehicle-envelope masks exclude the blank backdrop and viewer-floor graphics. Some lower tyre pixels can be omitted by the conservative mask; it is not precision segmentation. Mask overlays are preserved.',
'',
'Images attempted: **6**. Independent SIMPLE_PINHOLE camera per image, unknown default focal prior; 4096 maximum SIFT features, maximum image dimension 1200, CPU extraction/exhaustive matching, random seed 0, minimum fragment size three and mapper runtime cap 120 seconds. Minimum fragment size is a test setting, not a success criterion. The run took approximately '+f'{reg["elapsed_seconds"]:.2f}'+' seconds.',
'',
'| Fragment | Raw registered | Percentage of six | Sparse points | Mean / median / max error (px) | Mean track length |','|---|---:|---:|---:|---:|---:|']
for m in reg['models']:L.append(f'| {m["model"]} | {m["registered_images"]} | {m["registration_percentage"]:.1f}% | {m["sparse_points"]} | {m["point_error_mean"]:.5f} / {m["point_error_median"]:.5f} / {m["point_error_max"]:.5f} | {m["track_length_mean"]:.3f} |')
L += ['',
'The fragments overlap in images; do not add their registered counts together or call them one orbit. No fragment was accepted as reliable vehicle geometry.',
'',
'### Camera orbit gate: FAIL','',
'- Fragment 0 has three nominal registered poses but all 79 tracks are two-view tracks between 028/029; registered 027 has zero surviving observed 3D tracks. Its fitted focal for 027 is **negative (~−709 px)**; another focal is ~9813 px on an 1146-pixel-wide image. The negative focal is not a physical camera solution.',
'- Fragment 1 registers four images, but three camera centres almost coincide while the fourth is far away: baseline minimum ~0.00286 versus maximum ~9.998 arbitrary units, ratio **3492.6**. A fitted focal is ~295,214 px on a 1011-pixel-wide screenshot. The apparent side camera does not produce a coherent source-view orbit.',
'- These are failed estimated parameters, not actual EXIF/lens values. Unknown viewer projection, variable crops/zoom, sparse/repetitive features and correspondence ambiguity may contribute; no unique cause was proven.',
'',
'### Vehicle geometry evidence','',
'Observed surviving tracks occur mainly on grille/model-plate/fog surrounds, wheels and side-step details, with little support on broad painted bonnet/fender/quarter surfaces. The overlays use actual observed point tracks, not projected unobserved points. This is not merely a background reconstruction, but it is also not trustworthy body-depth evidence. Low reprojection errors do not rescue invalid/degenerate camera geometry.',
'',
'Full sparse expansion: **NOT ATTEMPTED**, because the small geometric gate did not succeed. Dense reconstruction: **NOT ATTEMPTED**. Scale/wheelbase fitting: **NOT ATTEMPTED**; nominal 4.825/1.860/1.860 m, wheelbase 2.845 m and approximate 0.764 m tyres remain interpretation-only constraints. No old model or nominal dimension was used to force the reconstruction into a convincing orbit.',
'',
'## Outputs and commands','',
'- Current inventory: '+str(I/'current-inventory.json'),'- Reconciliation: '+str(I/'new-image-reconciliation.json'),'- Derivative test dataset, database, sparse fragments, masks and logs: '+str(D),'- Registration result: '+str(D/'logs/registration-result.json'),'- Observed point overlays: '+str(D/'diagnostics/observed-vehicle-tracks.json'),'- Duplicate alignment checks: '+str(R/'near-duplicate-candidates.json'),'- Coverage/pair/camera diagnostics: '+str(R/'overlap-and-camera-diagnostics.json'),'- Preservation validation: '+str(R/'validation.json'),'',
'Executed local command for registration (with console redirected to `small/logs/console.txt`):','',
'```sh','/home/thunder/Documents/Codex/mux-reconstruction-env/bin/python '+str(D/'run_sfm.py'),'```','',
'Inventory, duplicate, projection and classification scripts are preserved under '+str(R/'scripts')+'. They document this specific audit; manual view/duplicate decisions must be reviewed rather than blindly reused for another folder revision.','',
'## Diagnostics','']
for name in ['all-images-contact-sheet.jpg','new-images-contact-sheet.jpg','geometric-evidence-contact-sheet.jpg','angle-coverage-map.jpg','sequence-map.jpg','difficult-regions-before-after.jpg','registered-camera-orbit.jpg','sparse-vehicle-evidence.jpg']:L.append('- '+str(R/name))
L += ['',
'## Per-image classification','',
'| ID | File | New? | View | Approx. azimuth | Height | Coverage | Class | Duplicate of |','|---|---|---|---|---:|---|---|---|']
for r in rows:L.append('| '+r['id']+' | '+r['relative_path']+' | '+('NO' if r['previous_hash_match'] else 'YES')+' | '+r['view']+' | '+str(r['approximate_visual_azimuth'] if r['approximate_visual_azimuth'] is not None else 'N/A')+' | '+r['height_view']+' | '+r['vehicle_coverage']+' | '+r['geometric_class']+' | '+str(r['near_duplicate_of'] or '')+' |')
L += ['',
'Full per-image resolution, aspect ratio, sizes, SHA-256, decoded hashes, EXIF/null metadata, source consistency, family and ambiguity notes are in the JSON inventory. No original image was changed or renamed.','',
'## Final decision','',
'**B — USEFUL NEW REFERENCES, BUT GEOMETRY REMAINS UNDERCONSTRAINED.**','',
'**RECONSTRUCTION REMAINS FROZEN.** The added intermediate/roof views materially improve visual reference coverage, so this is not “no new value.” They do not yet demonstrate coherent cross-view 3D evidence capable of resolving the old surface blockers. No new production or authored/procedural branch starts in this run.',
'',
'Production model: **NOT GENERATED**. Deep detailing: **NOT STARTED**. GLB: **NOT EXPORTED**. Website/Hero/navigation/TOLI AI: **UNCHANGED**. Controlled-capture guide, validator, manifests and previous experiments: **PRESERVED**; only the isolated new test directory was appended. Protected projects: **UNCHANGED**. Cost **₹0 / $0**. Deployment/Git commit: **NOT PERFORMED**.',
'',
'Preservation: '+str(checked)+' pre-existing manifest files match (authorized status updates excluded); all 43 source hashes match this audit’s initial inventory. The test generated sparse evidence fragments/PLYs only, not a production body.']
(B/'NEW_IMAGE_EVIDENCE_AUDIT.md').write_text('\n'.join(L)+'\n')
status=B/'RECONSTRUCTION_STATUS.md';shutil.copyfile(status,R/'pre-audit-status.md');status.write_text('# RECONSTRUCTION FROZEN — NEW IMAGE AUDIT DECISION B\n\n**USEFUL NEW REFERENCES, BUT GEOMETRY REMAINS UNDERCONSTRAINED.**\n\nThe authoritative folder now contains 43 readable image files (39 distinct visual references), including 21 new distinct references. The plausible viewer sequence produced only rejected camera fragments in a six-image CPU test; production modeling may not resume automatically. Audit: [NEW_IMAGE_EVIDENCE_AUDIT.md]('+str(B/'NEW_IMAGE_EVIDENCE_AUDIT.md')+'). No production body or GLB generated; website unchanged.\n\nPrevious status, authorization and failed branches are preserved below as history, not restart instructions.\n\n'+(R/'pre-audit-status.md').read_text())
print('Decision B audit complete. Source hashes verified:',len(rows),'; preserved manifest files:',checked,flush=True)
