import bpy,json,math
from pathlib import Path
from mathutils import Matrix,Vector
from bpy_extras.object_utils import world_to_camera_view
ROOT=Path(__file__).resolve().parents[3];OUT=ROOT/'source/reconstruction/calibration-v02';S=json.loads((OUT/'v02-solution.json').read_text());V=json.loads((OUT/'validation-summary-v02.json').read_text())
OLD=Path('/home/thunder/shared/tolimotors-main1/toli-static-website/tools/3d/isuzu-mux/source/reconstruction');D=json.loads((OLD/'observations.json').read_text());images={i['image']:i for i in D['images']}
bpy.ops.wm.read_factory_settings(use_empty=True);sc=bpy.context.scene;sc.unit_settings.system='NONE'
sc['status']='CALIBRATION FAILED — CAMERA PARAMETERS UNDERCONSTRAINED';sc['prohibited_next_step']='NO CONTOURS / NO BODY / NO GLB';sc['scale']='Dimensionless wheelbase=1; absolute metric scale unverified';sc['core_cameras']=json.dumps(S['core_cameras']);sc['training_rms_pixels']=S['training']['rms'];sc['heldout_rms_pixels']=S['heldout']['rms'];sc['LOVO_rms_pixels']=S['lovo_aggregate']['rms'];sc['LOVO_max_pixels']=S['lovo_aggregate']['max']
land=bpy.data.collections.new('20_STRUCTURAL_LANDMARKS_UNVALIDATED');sc.collection.children.link(land)
for name,co in S['points'].items():
 o=bpy.data.objects.new(name,None);land.objects.link(o);o.empty_display_type='SPHERE';o.empty_display_size=.008;o.location=co;o.show_name=True;o['confidence']='Structural A/B candidate; global validation FAILED';o.color=(1,.25,.1,1)
frame=bpy.data.collections.new('NORMALIZED_AXLE_GAUGE');sc.collection.children.link(frame)
for name,ends in [('FRONT_AXLE',['wc_F_L','wc_F_R']),('REAR_AXLE',['wc_R_L','wc_R_R']),('WHEELBASE_L',['wc_F_L','wc_R_L']),('WHEELBASE_R',['wc_F_R','wc_R_R'])]:
 c=bpy.data.curves.new(name,'CURVE');c.dimensions='3D';p=c.splines.new('POLY');p.points.add(1)
 for point,n in zip(p.points,ends):point.co=(*S['points'][n],1)
 o=bpy.data.objects.new(name,c);frame.objects.link(o)
core=bpy.data.collections.new('CORE8_FAILED_ACCEPTANCE');external=bpy.data.collections.new('EXTERNAL_POSE_CANDIDATES_NOT_GEOMETRY_FIT');sc.collection.children.link(core);sc.collection.children.link(external);errors=[]
for key,c in sorted(S['per_camera'].items(),key=lambda kv:int(kv[0])):
 i=int(key);yaw,el,roll=c['yaw_pitch_roll'];right=Vector((-math.sin(yaw),math.cos(yaw),0));down=Vector((math.cos(yaw)*math.sin(el),math.sin(yaw)*math.sin(el),-math.cos(el)));forward=Vector((-math.cos(yaw)*math.cos(el),-math.sin(yaw)*math.cos(el),-math.sin(el)));rx=right*math.cos(roll)-down*math.sin(roll);dy=right*math.sin(roll)+down*math.cos(roll)
 data=bpy.data.cameras.new('REF_'+str(i).zfill(2));o=bpy.data.objects.new('CAM_'+str(i).zfill(2)+('_CORE' if c['included'] else '_EXTERNAL'),data);(core if c['included'] else external).objects.link(o);o.matrix_world=Matrix((rx,-dy,-forward)).transposed().to_4x4();o.location=c['position'];data.sensor_fit='HORIZONTAL';data.sensor_width=36;data.lens=c['focal_36mm'];data.shift_x=0;data.shift_y=0
 photo=bpy.data.images.load(images[i]['path'],check_existing=True);photo.pack();w,h=photo.size;data.show_background_images=True;b=data.background_images.new();b.image=photo;b.alpha=.55;b.display_depth='BACK';b.frame_method='FIT'
 o['role']=c['status'];o['global_gate']='FAIL';o['observations']=c['observations'];o['all_structural_rms_pixels']=c['all']['rms'];o['max_pixels']=c['all']['max'];o['reference_width']=w;o['reference_height']=h;o['fixed_principal_point']='center';o['focal_model']='One constrained common focal; no free per-camera principal shift'
 if c['included']:o['heldout_rms_pixels']=c['heldout']['rms']
 else:o['pose_anchor_count']=c['pose_anchors']['n'];o['pose_rank']=c['pose_rank'];o['independent_test_rms_pixels']=c['independent_projection']['rms']
 sc.camera=o;sc.render.resolution_x=w;sc.render.resolution_y=h;sc.render.resolution_percentage=100;bpy.context.view_layer.update()
 for r in S['rows']:
  if r['camera']!=i:continue
  q=world_to_camera_view(sc,o,Vector(S['points'][r['landmark']]));errors.append(math.dist((q.x*w,(1-q.y)*h),r['predicted_v02']))
assert max(errors)<.01,max(errors);assert not [o for o in sc.objects if o.type=='MESH']
sc.camera=bpy.data.objects['CAM_06_CORE'];sc.render.resolution_x=1038;sc.render.resolution_y=587
for screen in bpy.data.screens:
 for area in screen.areas:
  if area.type=='VIEW_3D':area.spaces.active.region_3d.view_perspective='CAMERA'
path=ROOT/'source/reconstruction/isuzu-mux-multiview-v02.blend';assert not path.exists(),'Preserve previous V02 candidate';bpy.ops.wm.save_as_mainfile(filepath=str(path))
(OUT/'blender-projection-check-v02.json').write_text(json.dumps({'max_solver_blender_difference_pixels':max(errors),'observations_checked':len(errors),'cameras':len(S['per_camera']),'active_landmarks':len(S['points']),'body_meshes':0,'gate':'FAIL'},indent=2)+'\n')
print('Saved failed calibration-only V02; max projection difference:',max(errors))
