import bpy,sys,json,os,math
from pathlib import Path
from mathutils import Vector
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');B=P/'tools/3d/isuzu-mux';W=B/'manual-overlay-reconstruction';R=W/'renders/v01';sys.path.insert(0,str(P/'tools/blender-addons'))
from toli_mux_generator.surface_diagnostics import setup,zebra
views={'front':(-9,0,1.2),'front34':(-7,-7,3),'side':(0,-9,1.2),'rear34':(7,-7,3),'rear':(9,0,1.2),'overhead':(0,0,10)}
closeups={'bonnet-fender':((-1.48,-.70,1.17),'front34',2.25),'fender-a-pillar':((-.95,-.74,1.30),'front34',1.7),'cowl-windscreen':((-.64,-.38,1.55),'front34',1.85),'greenhouse':((.65,-.70,1.57),'side',3.3),'d-pillar':((1.9,-.70,1.58),'rear34',1.7),'rear-quarter':((1.5,-.82,1.03),'rear34',2.3),'rear-bumper-corner':((2.18,-.72,.70),'rear34',1.6)}
args=sys.argv[sys.argv.index('--')+1:];assert args
for job in args:
 previous=job.startswith('previous-');name=job.removeprefix('previous-');mode,view=name.split('-',1)
 bpy.ops.wm.open_mainfile(filepath=str(B/'source/production'/('isuzu-mux-existing-photo-production-v01.blend' if previous else 'isuzu-mux-manual-overlay-v01.blend')));s=bpy.context.scene
 if previous:setup(s)
 isref=view.isdigit();isclose=view in closeups
 if isref:
  cam=bpy.data.objects.get('REFERENCE_FIT_MUX-'+view)
  if previous:
   # Reuse exact new camera extrinsics and intrinsics, not the old comparison framing.
   fit=next(f for f in json.loads((W/'cameras/reference-fits.json').read_text()) if f['id']=='MUX-'+view);cam=bpy.data.objects['PROTO_Camera'];cam.location=fit['position'];cam.rotation_euler=(Vector(fit['target'])-cam.location).to_track_quat('-Z','Y').to_euler();cam.data.type='PERSP';cam.data.lens=fit['lens_mm_assumed_36mm_sensor'];cam.data.sensor_width=36;cam.data.sensor_fit='HORIZONTAL';cx,cy=fit['principal_point'];cam.data.shift_x=(400-cx)/800;cam.data.shift_y=(cy-260)/800
 else:
  center,base,scale=closeups[view] if isclose else ((0,0,.93),view,6.1)
  cam=bpy.data.objects['PROTO_Camera'];pos=Vector(views[base]);cam.location=Vector(center)+pos-Vector((0,0,.93));cam.rotation_euler=(Vector((0,0,.93))-pos).to_track_quat('-Z','Y').to_euler();cam.data.type='ORTHO';cam.data.ortho_scale=scale
  if base=='overhead':cam.rotation_euler=(0,0,0)
 s.camera=cam;s.render.resolution_x=800;s.render.resolution_y=520;s.render.resolution_percentage=100;s.cycles.samples=8;s.render.threads_mode='FIXED';s.render.threads=4;s.render.film_transparent=isref;s.render.image_settings.color_mode='RGBA'
 for o in bpy.data.objects:
  if o.name=='PROTO_Floor':o.hide_render=isref
  if o.type=='LIGHT' and o.name.startswith('PROTO_'):o.hide_render=(o.name.startswith('PROTO_STRIP'))!=(mode=='reflection')
  if o.type!='MESH' or o.name=='PROTO_Floor':continue
  # Restrict diagnostic mutations to this in-memory loaded candidate.
  for mod in o.modifiers:
   if mod.type=='SUBSURF' and mode=='wire':mod.show_render=False
  if o.name.startswith(('Wheel_','ANCHOR_','PLAIN_')):continue
  if mode=='wire':
   m=bpy.data.materials.new('Wire actual control edges');m.use_nodes=True;m.diffuse_color=(.02,.02,.02,1);m.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=m.diffuse_color;o.data.materials.append(m);w=o.modifiers.new('Actual base-cage wire','WIREFRAME');w.thickness=.0025;w.use_replace=False;w.material_offset=len(o.data.materials)-1
  elif mode=='zebra':o.data.materials.clear();o.data.materials.append(zebra())
  elif mode=='reflection':
   for m in o.data.materials:
    if m and m.use_nodes:m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.14
 s.render.filepath=str(R/(job+'.png'));bpy.ops.render.render(write_still=True);print('SAVED',job,flush=True)
os._exit(0)
