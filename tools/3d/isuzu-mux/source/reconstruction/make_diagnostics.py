from pathlib import Path
from PIL import Image,ImageDraw,ImageOps
import json
R=Path(__file__).resolve().parents[2];D=json.loads((R/'source/reconstruction/observations.json').read_text());S=json.loads((R/'source/reconstruction/joint-solution.json').read_text())
rows={r['image']:r for r in D['images']};ids=sorted(map(int,S['per_camera']));sheet=Image.new('RGB',(1800,4*440+85),(28,30,34));draw=ImageDraw.Draw(sheet)
draw.text((14,10),'JOINT MULTI-VIEW LANDMARK CANDIDATE — GLOBAL GATE FAIL / NO BODY OR CONTOURS',fill='white');draw.text((14,30),f'12 cameras / 198 observations / ALL RMS {S["overall_rms_pixels"]:.2f}px / HELD-OUT RMS {S["heldout_rms_pixels"]:.2f}px / MAX {S["max_error_pixels"]:.2f}px',fill='#ffbb88');draw.text((14,50),'Yellow = training picks; white squares = held out; cyan crosses = projection; red residuals >12px. No poor view hidden.',fill='white')
for k,i in enumerate(ids):
 x=k%3*600;y=k//3*440+85;e=S['per_camera'][str(i)];im=Image.open(rows[i]['path']).convert('RGB');mark=ImageDraw.Draw(im)
 for n,o in enumerate([o for o in S['observations'] if o['camera']==i],1):
  a,b=o['xy'];u,v=o['projected'];color='#ff3030' if o['error_pixels']>12 else '#21c9f6';mark.line((a,b,u,v),fill=color,width=2)
  if o['heldout']:mark.rectangle((a-4,b-4,a+4,b+4),outline='white',width=2)
  else:mark.ellipse((a-3,b-3,a+3,b+3),outline='#ffe855',width=2)
  mark.line((u-4,v,u+4,v),fill='#00ffff',width=2);mark.line((u,v-4,u,v+4),fill='#00ffff',width=2);mark.text((a+4,b+4),str(n),fill='#ffdf65')
 im=ImageOps.contain(im,(590,360));sheet.paste(im,(x+(600-im.width)//2,y+34+(360-im.height)//2))
 draw.text((x+8,y+5),f'Image {i}: {rows[i]["view"][:67]}',fill='white');held='not available' if e['heldout_rms_pixels'] is None else f'{e["heldout_rms_pixels"]:.2f}px'
 draw.text((x+8,y+400),f'N={e["observations"]} RMS={e["rms_pixels"]:.2f}px Max={e["max_pixels"]:.2f}px Held-out={held}',fill='#ffbb88');draw.text((x+8,y+419),f'Local fit {e["landmark_gate"]}; global shared-landmark gate FAIL',fill='white')
sheet.save(R/'renders/multiview-camera-solve-v01.jpg',quality=94)
audit=[]
for i in range(1,14):
 row=rows[i];w,h=Image.open(row['path']).size;isopen=i<5;interior=i==5
 if interior:
  wheels='No exterior wheel centers';tire='No';body='No common exterior corners';glass='Interior/panoramic only';lamps='No';grille='No';occl='Cabin-only panorama; cannot link reliable exterior landmarks';suit='EXCLUDED';dist='Strong panoramic distortion; not a pinhole exterior view'
 elif i in [1,6]:
  wheels='Hub centers occluded; tire contact picks only';tire='Partial front tire sides/contact edges';body='Fixed fascia/bumper corners visible';glass='Blocked by bonnet in 1; visible in 6';lamps='Front lamp outlines visible';grille='Fixed grille corners visible';occl='Raised bonnet hides windscreen; moving doors excluded' if isopen else 'Hubs hidden by frontal body; mirrors overlap edges';suit='Joint candidate, planar/depth weakness' if i==1 else 'Joint candidate';dist='Near frontal perspective/cropped screenshot; lens metadata absent'
 elif i in [3,8]:
  wheels='Rear hubs occluded; tire contact picks only';tire='Partial rear tire sides/contact edges';body='Fixed rear shoulders/body lamp borders visible';glass='Moving raised hatch excluded in 3; closed rear glass in 8';lamps='Fixed outer body lamp segments; hatch-mounted segments excluded when open';grille='Not visible';occl='Raised hatch and open doors exclude moving geometry' if isopen else 'Hubs hidden by bumper; rounded glazing corners uncertain';suit='Weak candidate: six observations, no independent held-out view test' if i==3 else 'Joint candidate';dist='Near rear perspective/cropped screenshot; lens metadata absent'
 elif i in [2,4,7,9]:
  side='left' if i in [2,7] else 'right';wheels=f'Both near {side} hub centers';tire='Both near tire silhouettes/ellipses';body='Fender/arch/quarter corners visible';glass='Fixed rear quarter glass; windshield partly obscured when open' if isopen else 'Windscreen oblique, fixed quarter glass and door glass visible';lamps='Near fixed front/rear lamp corners';grille='Mostly edge-on; ambiguous corners not picked';occl='Open panels cover door/hinge regions; moving door glass excluded' if isopen else 'Mirror hides some cowl; grazing glass edges and far side occluded';suit='Joint candidate';dist='Near profile, not orthographic; tire apparent size changes with depth'
 else:
  rear=i in [12,13];wheels='Both near-side hub centers; far hubs mostly occluded';tire='Near front/rear ellipse silhouettes';body='Fender/quarter and fascia/hatch regions visible';glass='Rear and fixed quarter glass' if rear else 'Windscreen and small fixed quarter glass';lamps='Rear body lamp outlines' if rear else 'Near headlight outline and grille boundaries';grille='Not visible' if rear else 'Upper/lower broad corners visible';occl='Far glass/hatch corners ambiguous; reflections and black ceramic borders' if rear else 'Mirror/cowl and far windshield corner ambiguities';suit='Joint candidate; quarter fit currently FAIL';dist='Oblique perspective with substantial near/far scale differences'
 audit.append({'image':i,'path':row['path'],'size':[w,h],'canonical_vehicle_match':'NO — exterior identity unverified in interior panorama' if interior else 'YES — visually compatible with canonical body/trim; physical vehicle/VIN not proven','exterior_usable':not interior,'camera_position_class':row['view'],'wheel_centers':wheels,'tire_ellipse':tire,'body_corners':body,'glass_corners':glass,'lamp_corners':lamps,'grille_landmarks':grille,'perspective_distortion':dist,'occlusions':occl,'open_panels':'Not applicable' if interior else 'Doors/bonnet/hatch open; only fixed-body features used' if isopen else 'Closed','camera_solve_suitability':suit})
(R/'source/reconstruction/image-geometric-audit.json').write_text(json.dumps(audit,indent=2)+'\n')
(R/'source/reconstruction/stage-status.json').write_text(json.dumps({'landmark_gate':'FAIL','contour_gate':'NOT REACHED','surfaces':'NOT CREATED','withheld_outputs':{'multiview-contours-v01.jpg':'No contour curves before joint landmark gate passes','reconstructed-body-comparison-v01.jpg':'No body surfaces permitted before contour gate passes','reconstructed-surface-diagnostics-v01.jpg':'No body or reflection surface to evaluate'},'reference_coverage':'All six requested exterior camera classes supplied; no duplicate-angle photo request justified by this audit','no_photogrammetry_success_claim':True},indent=2)+'\n')
print('Saved camera diagnostic and geometric audit; later-stage outputs deliberately withheld.')
