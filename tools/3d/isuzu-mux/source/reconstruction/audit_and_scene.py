"""Save a FAILED/UNVALIDATED joint landmark framework and fitted camera candidates only.
No body, contour curves, borrowed mesh, material or export is constructed.
"""
import bpy,json,math
from pathlib import Path
from mathutils import Matrix,Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[2]
D=json.loads((R/'source/reconstruction/observations.json').read_text());S=json.loads((R/'source/reconstruction/joint-solution.json').read_text());P=json.loads((R/'source/reconstruction/shared-landmarks.json').read_text())
bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene;sc.unit_settings.system='NONE'
sc['stage']='JOINT CAMERA / LANDMARK CANDIDATE — GLOBAL GATE FAIL — NO BODY'
sc['scale']='Wheelbase=1 dimensionless gauge; no verified manufacturer dimensions'
sc['overall_rms_pixels']=S['overall_rms_pixels'];sc['heldout_rms_pixels']=S['heldout_rms_pixels'];sc['old_models_used']=False
land=bpy.data.collections.new('UNVALIDATED_SHARED_LANDMARKS');sc.collection.children.link(land)
for name,co in P.items():
 o=bpy.data.objects.new(name,None);land.objects.link(o);o.empty_display_type='SPHERE';o.empty_display_size=.008;o.location=co;o.show_name=True;o['status']='Candidate shared landmark; failed validation';o.color=(1,.3,.1,1)
frame=bpy.data.collections.new('AXLES_AND_GAUGE_ONLY');sc.collection.children.link(frame)
for name,ends in [('FRONT_AXLE',['wc_F_L','wc_F_R']),('REAR_AXLE',['wc_R_L','wc_R_R']),('WHEELBASE_L',['wc_F_L','wc_R_L']),('WHEELBASE_R',['wc_F_R','wc_R_R'])]:
 cu=bpy.data.curves.new(name,'CURVE');cu.dimensions='3D';ss=cu.splines.new('POLY');ss.points.add(1)
 for point,key in zip(ss.points,ends):point.co=(*P[key],1)
 o=bpy.data.objects.new(name,cu);frame.objects.link(o)
cams=bpy.data.collections.new('JOINT_FIT_CANDIDATES_NOT_APPROVED');sc.collection.children.link(cams)
allerrors=[]
for row in D['images']:
 i=row['image']
 if str(i) not in S['per_camera']:continue
 result=S['per_camera'][str(i)];yaw,el,roll=result['yaw_pitch_roll_radians'];sy,cy=math.sin(yaw),math.cos(yaw);se,ce=math.sin(el),math.cos(el)
 right=Vector((-sy,cy,0));down=Vector((cy*se,sy*se,-ce));forward=Vector((-cy*ce,-sy*ce,-se));cr,sr=math.cos(roll),math.sin(roll);rx=right*cr-down*sr;dy=right*sr+down*cr
 data=bpy.data.cameras.new('FIT_'+str(i).zfill(2));o=bpy.data.objects.new('CAM_'+str(i).zfill(2)+'_'+result['landmark_gate'],data);cams.objects.link(o);o.matrix_world=Matrix((rx,-dy,-forward)).transposed().to_4x4();o.location=result['camera_center_wheelbase_units']
 im=bpy.data.images.load(row['path'],check_existing=True);im.pack();w,h=im.size;data.sensor_fit='HORIZONTAL';data.sensor_width=36;data.lens=result['focal_pixels']/w*36;cx,cy=result['principal_point_pixels'];data.shift_x=.5-cx/w;data.shift_y=(cy-h*.5)/w
 data.show_background_images=True;bg=data.background_images.new();bg.image=im;bg.alpha=.55;bg.display_depth='BACK';bg.frame_method='FIT'
 for k in ['rms_pixels','max_pixels','observations','training','heldout','landmark_gate']:o[k]=result[k]
 o['reference_width']=w;o['reference_height']=h;o['reference_file']=row['path'];o['scale']='dimensionless wheelbase units'
 sc.camera=o;sc.render.resolution_x=w;sc.render.resolution_y=h;sc.render.resolution_percentage=100;bpy.context.view_layer.update()
 for ob in S['observations']:
  if ob['camera']!=i:continue
  q=world_to_camera_view(sc,o,Vector(P[ob['landmark']]));actual=(q.x*w,(1-q.y)*h);err=math.dist(actual,ob['projected']);allerrors.append(err)
sc.camera=bpy.data.objects['CAM_06_'+S['per_camera']['6']['landmark_gate']];sc.render.resolution_x=1038;sc.render.resolution_y=587
assert max(allerrors)<.01,(max(allerrors),'Blender projection does not match solver')
assert not [o for o in sc.objects if o.type=='MESH'],'No body or surface mesh permitted'
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
bpy.ops.wm.save_as_mainfile(filepath=str(R/'source/reconstruction/isuzu-mux-multiview-v01.blend'))
(R/'source/reconstruction/blender-projection-check.json').write_text(json.dumps({'max_solver_blender_difference_pixels':max(allerrors),'checked_observations':len(allerrors),'body_mesh_count':0,'camera_count':len(cams.objects),'landmarks':len(P),'status':'Projection implementation checked; reconstruction gate remains FAIL'},indent=2)+'\n')
print('Projection equivalence max pixel error:',max(allerrors))
