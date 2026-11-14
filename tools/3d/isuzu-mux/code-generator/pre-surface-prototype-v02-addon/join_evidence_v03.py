import bpy,sys,json,os,itertools
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
P=Path(__file__).resolve().parents[3];sys.path.insert(0,str(P/'tools/blender-addons'))
from toli_mux_generator.geometry.flow_cage import join_samples,points
r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v03'
bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v02.blend'))
base={code:join_samples(bpy.data.objects['TRACE_'+a],ai,bpy.data.objects['TRACE_'+b],bi) for code,a,ai,b,bi in [('J03','A_PILLAR',-1,'ROOF_EDGE',0),('J04','ROOF_EDGE',-1,'D_PILLAR',0),('J05','SHOULDER',-1,'REAR_QUARTER_RETURN',1),('J07','REAR_QUARTER_RETURN',-1,'REAR_BUMPER',1)]};(r/'flow-constraints-v02.json').write_text(json.dumps(base,indent=2))
bpy.ops.wm.open_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v03.blend'));s=bpy.context.scene
joints={'J01':('FRONT34',(-1.4225,-.86,1.17),(.36,.23,.25)),'J02':('FRONT34',(-.937,-.82,1.332),(.24,.20,.23)),'J04':('REAR34',(1.931,-.69,1.65),(.29,.20,.25)),'J05':('REAR34',(1.60,-.91,1.03),(.45,.20,.25)),'J06':('REAR34',(2.15,-.79,1.15),(.25,.30,.22)),'J07':('REAR34',(2.30,-.85,.52),(.23,.25,.26)),'J08':('REAR34',(2.16,-.73,1.40),(.30,.28,.30))}
out={}
for name,(view,center,radii) in joints.items():
 s.camera=bpy.data.objects['CAM_'+view];s.render.resolution_x=960;s.render.resolution_y=640;bpy.context.view_layer.update()
 projected=[world_to_camera_view(s,s.camera,Vector(tuple(a+sign*d for a,sign,d in zip(center,signs,radii)))) for signs in itertools.product([-1,1],repeat=3)]
 box=[max(0,int(min(v.x for v in projected)*960)),max(0,int((1-max(v.y for v in projected))*640)),min(960,int(max(v.x for v in projected)*960)),min(640,int((1-min(v.y for v in projected))*640))]
 out[name]={'view':view.lower(),'box':box,'center_m':center,'radii_m':radii}
(r/'join-crops.json').write_text(json.dumps(out,indent=2));print(json.dumps(out),flush=True);os._exit(0)
