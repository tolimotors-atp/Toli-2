import bpy,json,hashlib,os
from pathlib import Path
from mathutils import Vector
O=Path(os.environ.get('MUX_V02_OUTPUT',Path(__file__).resolve().parents[3]));D=O/'source/production';R=O/'renders/refinement-v02';A=D/'generated';R.mkdir(parents=True,exist_ok=True)
p=D/'milestones/isuzu-mux-generated-v01.blend';bpy.ops.wm.open_mainfile(filepath=str(p));s=bpy.context.scene;s.frame_set(1)
assert all(bpy.data.objects.get(n) for n in ['MUX_ROOT','BODY — editable half control cage','WINDSCREEN','DOOR_FL','DOOR_FR','DOOR_RL','DOOR_RR','BONNET','TAILGATE'])
(A/'v01-open-check.json').write_text(json.dumps({'opened':str(p),'passed':True,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()},indent=2))
views={'FRONT':((-9,0,1.25),(0,0,.95),'ORTHO',3.4),'FRONT_34':((-7,-8,3.0),(0,0,.92),'PERSP',58),'SIDE':((0,-9,1.0),(.08,0,.95),'ORTHO',5.9),'REAR_34':((7,-8,2.8),(.1,0,.92),'PERSP',58),'REAR':((9,0,1.25),(.1,0,.95),'ORTHO',3.4)}
manifest={}
for name,(loc,tar,typ,scale) in views.items():
 bpy.ops.object.camera_add(location=loc);cam=bpy.context.object;cam.name='CAM_COMPARE_'+name;cam.rotation_euler=(Vector(tar)-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type=typ
 if typ=='ORTHO':cam.data.ortho_scale=scale
 else:cam.data.lens=scale
 manifest[name]={'matrix_world':[list(row) for row in cam.matrix_world],'location':list(cam.location),'rotation':list(cam.rotation_euler),'type':typ,'scale_or_lens':scale}
s.render.engine='CYCLES';s.cycles.device='CPU';s.cycles.samples=12;s.cycles.use_denoising=True;s.render.resolution_x=960;s.render.resolution_y=640;s.render.resolution_percentage=100;s.render.image_settings.file_format='PNG';s.camera=bpy.data.objects['CAM_COMPARE_FRONT_34']
(A/'fixed-cameras-v02.json').write_text(json.dumps(manifest,indent=2));bpy.ops.wm.save_as_mainfile(filepath=str(D/'milestones/isuzu-mux-v01-comparison-rig.blend'))
for name in views:
 s.camera=bpy.data.objects['CAM_COMPARE_'+name];s.render.filepath=str(R/('baseline-'+name.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('V01 VERIFIED AND BASELINE COMPLETE',flush=True)

# All outputs are saved; bypass a headless audio-shutdown hang in this Blender runtime.
os._exit(0)
