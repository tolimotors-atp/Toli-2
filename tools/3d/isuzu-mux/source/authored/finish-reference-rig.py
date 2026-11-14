import bpy,json,hashlib
from pathlib import Path
R=Path(__file__).resolve().parents[2];sc=bpy.context.scene;body=bpy.data.objects['AUTHORED_BODY_V01']
def sig():return hashlib.sha256(repr([(tuple(v.co)) for v in body.data.vertices]).encode()).hexdigest()
before=sig();pose=json.loads((R/'source/authored/side-camera-fit.json').read_text());cam=bpy.data.objects['CAL_left'];cam.location=pose['location'];cam.rotation_euler=pose['rotation'];cam.data.lens=70;cam['native_reference_size']='1060x522';cam['anchor_rms_pixels']=pose['anchor_rms_pixels'];cam['calibration']='Tire-anchor fit only, constrained focal length, non-unique solution'
col=bpy.data.collections['LANDMARK_CURVES / STATIONS']
def add(name,pts):
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';s=c.splines.new('POLY');s.points.add(len(pts)-1)
 for p,v in zip(s.points,pts):p.co=(*v,1)
 o=bpy.data.objects.new(name,c);col.objects.link(o);o.hide_render=True
for n,p in {'BONNET_TRANSVERSE_CROWN':[(1.425,0,1.208),(1.425,.5,1.196),(1.425,.855,1.163)],'FRONT_FENDER_CROWN':[(1.425,.855,1.163),(1.425,.958,1.088),(1.425,.97,.89)],'FRONT_BUMPER_WIDTH':[(2.27,0,.35),(2.30,.55,.55),(2.25,.87,.75)],'REAR_D_PILLAR': [(-2.04,.75,1.75),(-2.38,.855,1.209)],'REAR_ROOF': [(-2.04,0,1.785),(-2.04,.75,1.75)]}.items():add(n,p)
# Guide-section endpoints use the appropriate hood, windscreen or hatch region, not a roof at every station.
for o in col.objects:
 if not o.name.startswith('S') or not o.name[1:3].isdigit():continue
 pts=o.data.splines[0].points;x=pts[-1].co.x
 if x>1.07:pts[-1].co=(x,.855,1.18-.012*x,1)
 elif x>.35:
  t=(x-.35)/.72;pts[-1].co=(x,.73+(.855-.73)*t,1.76+(1.16716-1.76)*t,1)
 elif x< -2.04:
  t=(-x-2.04)/.34;pts[-1].co=(x,.75+(.855-.75)*t,1.75+(1.20856-1.75)*t,1)
assert before==sig()
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/authored/isuzu-mux-authored-v01.blend'))
(R/'source/authored/rig-validation.json').write_text(json.dumps({'body_signature':sig(),'rig_update_kept_body_identical':True,'reference_collections':list(o.name for o in bpy.data.collections['REFERENCE_RIG'].children)},indent=2))
