import bpy,sys,json,os
from pathlib import Path
from mathutils import Vector
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(P/'tools/blender-addons'))
import toli_mux_generator as addon
from toli_mux_generator.geometry.flow_cage import JOIN_CURVES
r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v04';joints=json.loads((r/'join-crops.json').read_text());addon.register()
for version in ['v04']:
 bpy.ops.wm.open_mainfile(filepath=str(P/f'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-{version}.blend'));s=bpy.context.scene
 s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=1100;s.render.resolution_y=700;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='Standard';s.view_settings.exposure=.5
 col=bpy.data.collections['TOLI_MUX_REFERENCE_CAGE']
 for o in col.objects:
  if o.data.materials:
   mat=o.data.materials[0].copy();o.data.materials.clear();o.data.materials.append(mat);bs=mat.node_tree.nodes['Principled BSDF']
   if o.name.endswith('_R'):
    near=col.objects.get(o.name[:-2]);color=near.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value if near else mat.diffuse_color;shade=tuple(v*.18 for v in color[:3])+(1,);bs.inputs['Base Color'].default_value=shade;bs.inputs['Emission Color'].default_value=shade;bs.inputs['Emission Strength'].default_value=.1
   else:bs.inputs['Emission Strength'].default_value=1.4
 cd=bpy.data.cameras.new('JOIN closeup');camera=bpy.data.objects.new('JOIN closeup',cd);s.collection.objects.link(camera);cd.type='ORTHO'
 out=r/'comb-renders';out.mkdir(parents=True,exist_ok=True)
 for name,meta in joints.items():
  if name not in ['J01','J02','J04','J05','J07']:continue
  if os.environ.get('MUX_COMB_JOIN') and name!=os.environ['MUX_COMB_JOIN']:continue
  s.toli_mux.join_debug=name;s.toli_mux.show_curvature_combs=True;base=bpy.data.objects['CAM_'+meta['view'].upper()];camera.location=base.location+Vector(meta['center_m'])-Vector((0,0,.93));camera.rotation_euler=base.rotation_euler;cd.ortho_scale=1.85 if name=='J05' else 1.50;s.camera=camera
  s.render.filepath=str(out/(name.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('V04 LOCAL COMB RENDERS COMPLETE',flush=True);os._exit(0)
