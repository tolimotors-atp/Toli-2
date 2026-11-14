import bpy,sys,os
from pathlib import Path
from mathutils import Vector
P=Path(__file__).resolve().parents[4];B=P/'tools/3d/isuzu-mux';R=B/'code-generator/renders/existing-photo-production-v01';sys.path.insert(0,str(P/'tools/blender-addons'))
from toli_mux_generator.surface_diagnostics import setup,zebra
previous=os.environ.get('M1_PREVIOUS')=='1';source=B/'source/production'/('isuzu-mux-generated-v04.blend' if previous else 'isuzu-mux-existing-photo-production-v01.blend');bpy.ops.wm.open_mainfile(filepath=str(source));s=bpy.context.scene
if previous:
 setup(s)
 for o in bpy.data.objects:
  if o.type=='MESH' and any(n in o.name.upper() for n in ['GUIDE','REFERENCE','FLOOR','GROUND','BADGE','TEXT']) and o.name!='PROTO_Floor':o.hide_render=True
  if o.type in ['CURVE','FONT','EMPTY']:o.hide_render=True
  if o.type=='MESH' and o.name!='PROTO_Floor':
   o['m1_previous']=True
   for i in range(len(o.data.materials)):
    name=o.name.lower()+' '+(o.data.materials[i].name.lower() if o.data.materials[i] else '');v=.075 if any(t in name for t in ['glass','window','glazing']) else .08 if any(t in name for t in ['rubber','tire']) else .30
    m=bpy.data.materials.new('Previous diagnostic clay');m.diffuse_color=(v,v,v,1);m.use_nodes=True;bs=m.node_tree.nodes['Principled BSDF'];bs.inputs['Base Color'].default_value=m.diffuse_color;bs.inputs['Roughness'].default_value=.55;o.data.materials[i]=m
views={'front':(-9,0,1.2),'front34':(-7,-7,3),'side':(0,-9,1.2),'rear34':(7,-7,3),'rear':(9,0,1.2)}
features={'bonnet-fender':((-1.48,-.7,1.12),'front34',2.2),'cowl-a-root':((-.65,-.70,1.40),'front34',1.6),'d-pillar':((1.93,-.70,1.55),'rear34',1.6),'rear-quarter':((1.46,-.80,1.0),'rear34',2.4),'rear-corner':((2.17,-.70,.85),'rear34',1.8)}
job=os.environ.get('M1_JOB','clay-front34');mode,view=job.split('-',1);close=view in features;center,camview,scale=features[view] if close else ((0,0,.93),view,6.1)
cam=bpy.data.objects['PROTO_Camera'];pos=Vector(views[camview]);cam.location=Vector(center)+(pos-Vector((0,0,.93)));cam.rotation_euler=(Vector((0,0,.93))-pos).to_track_quat('-Z','Y').to_euler();cam.data.ortho_scale=scale;s.camera=cam
for o in bpy.data.objects:
 if o.type=='LIGHT' and o.name.startswith('PROTO_'):o.hide_render=(o.name.startswith('PROTO_STRIP'))!=(mode=='reflection')
 if o.type!='MESH' or o.name=='PROTO_Floor':continue
 for modifier in o.modifiers:
  if modifier.type=='SUBSURF':modifier.show_render=mode!='wire'
 if o.name.startswith(('ANCHOR_','PLAIN_')):continue
 if mode in ['zebra','reflection']:
  for m in o.data.materials:
   if not m:continue
   if mode=='reflection':m.node_tree.nodes['Principled BSDF'].inputs['Roughness'].default_value=.14
  if mode=='zebra':
   o.data.materials.clear();o.data.materials.append(zebra())
 if mode=='wire':
  o.show_wire=True
  w=o.modifiers.new('Diagnostic actual control edges','WIREFRAME');w.thickness=.003;w.use_replace=False
  dark=bpy.data.materials.get('Actual cage dark') or bpy.data.materials.new('Actual cage dark');dark.diffuse_color=(.025,.025,.025,1);dark.use_nodes=True;dark.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=dark.diffuse_color
  o.data.materials.append(dark);w.material_offset=1
s.render.filepath=str(R/(('previous-' if previous else '')+job+'.png'));bpy.ops.render.render(write_still=True);print('SAVED',s.render.filepath,flush=True);os._exit(0)
