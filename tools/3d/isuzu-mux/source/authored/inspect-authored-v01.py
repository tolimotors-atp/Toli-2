import bpy,math,json,sys
from pathlib import Path
from mathutils import Vector
from bpy_extras.object_utils import world_to_camera_view
R=Path(__file__).resolve().parents[2];sc=bpy.context.scene;cam=sc.camera
mode=sys.argv[-1] if '--' in sys.argv else 'principal'
def aim(o,p):o.rotation_euler=(Vector(p)-o.location).to_track_quat('-Z','Y').to_euler()
views={'front':(10,0,1.65),'left':(1,10.5,1.8),'right':(1,-10.5,1.8),'rear':(-10,0,1.65),'front-three-quarter':(8,6,2.8),'rear-three-quarter':(-8,6,2.8)}
sc.render.engine='CYCLES';sc.cycles.samples=6;sc.view_layers[0].material_override=None
if mode=='principal':
 # Fit only the clear canonical side view's tire anchors. Focal length is constrained,
 # not claimed to be the original lens. Other views remain estimates.
 sc.render.resolution_x=1060;sc.render.resolution_y=522
 targets=[((1.425,.96,.39),(218/1060,1-354/522)),((-1.425,.96,.39),(767/1060,1-348/522)),((1.425,.96,.78),(218/1060,1-277/522)),((1.425,.96,0),(218/1060,1-431/522)),((-1.425,.96,.78),(767/1060,1-273/522)),((-1.425,.96,0),(767/1060,1-424/522))]
 def apply(p):
  d,yaw,h,tx,tz=p;cam.location=(d*math.sin(yaw),d*math.cos(yaw),h);cam.data.type='PERSP';cam.data.lens=70;aim(cam,(tx,0,tz));bpy.context.view_layer.update()
 def error(p):
  if not(5<p[0]<20 and abs(p[1])<.45 and .8<p[2]<3 and abs(p[3])<1 and .3<p[4]<1.8):return 1e6
  apply(p);return sum((world_to_camera_view(sc,cam,Vector(co))[i]-target[i])**2 for co,target in targets for i in [0,1])
 p=[10.5,.095,1.8,0,.95];steps=[.5,.04,.15,.12,.12];best=error(p)
 for iteration in range(100):
  changed=False
  for i,step in enumerate(steps):
   for sign in [-1,1]:
    q=p.copy();q[i]+=step*sign;e=error(q)
    if e<best:p=q;best=e;changed=True
  if not changed:steps=[v*.6 for v in steps]
  if max(steps)<.0002:break
 apply(p)
 projected=[list(world_to_camera_view(sc,cam,Vector(co)))[:2] for co,t in targets]
 pixerr=math.sqrt(sum(((a[0]-t[0])*1060)**2+((a[1]-t[1])*522)**2 for a,(co,t) in zip(projected,targets))/len(targets))
 pose={'location':list(cam.location),'rotation':list(cam.rotation_euler),'focal_mm':70,'anchor_rms_pixels':pixerr,'reference':'Canonical left 1060x522','limits':'Manual pixel anchors; simplified tire circles; focal length constrained; non-unique pose; no certified calibration PASS'}
 (R/'source/authored/side-camera-fit.json').write_text(json.dumps(pose,indent=2))
 sc.render.resolution_x=1000;sc.render.resolution_y=650
for name in (['left'] if mode=='left' else ['front','left','rear'] if mode=='principal' else ['right','front-three-quarter','rear-three-quarter'] if mode=='quarter' else []):
 if name=='left':
  sc.render.resolution_x=1060;sc.render.resolution_y=522
  pose=json.loads((R/'source/authored/side-camera-fit.json').read_text());cam.location=pose['location'];cam.rotation_euler=pose['rotation'];cam.data.lens=pose['focal_mm']
 else:sc.render.resolution_x=1000;sc.render.resolution_y=650;cam.location=views[name];aim(cam,(0,0,.95));cam.data.lens=70
 sc.render.filepath=str(R/'renders/authored-v01'/('study-'+name+'.png'));bpy.ops.render.render(write_still=True)
if mode=='strips':
 # Three actual positions of a broad rectangular source, not painted-on stripes.
 light=bpy.data.objects['STRIP_SIDE'];light.data.energy=2500;light.data.size=.45;light.data.size_y=5.5
 for index,x in enumerate([1.8,0,-1.8]):
  light.location=(x,3.7,2.2);aim(light,(x,0,1.0));cam.location=views['front-three-quarter'] if index<2 else views['rear-three-quarter'];aim(cam,(0,0,.95));sc.render.filepath=str(R/'renders/authored-v01'/('reflection-sweep-'+str(index)+'.png'));bpy.ops.render.render(write_still=True)

if mode=='silhouette':
 pose=json.loads((R/'source/authored/side-camera-fit.json').read_text());cam.location=pose['location'];cam.rotation_euler=pose['rotation'];cam.data.lens=70
 sc.render.resolution_x=1060;sc.render.resolution_y=522;sc.render.film_transparent=True;sc.render.image_settings.color_mode='RGBA';bpy.data.objects['STUDIO_FLOOR'].hide_render=True
 sc.render.engine='BLENDER_WORKBENCH';sc.display.shading.light='FLAT';sc.display.shading.color_type='SINGLE';sc.display.shading.single_color=(0,0,0)
 sc.render.filepath=str(R/'renders/authored-v01/model-silhouette-left.png');bpy.ops.render.render(write_still=True)
