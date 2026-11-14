import bpy,os
from pathlib import Path
P=Path(__file__).resolve().parents[3];r=P/'tools/3d/isuzu-mux/code-generator/renders/reference-curve-cage-v02'
for version in ['v01','v02']:
 bpy.ops.wm.open_mainfile(filepath=str(P/f'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-{version}.blend'));s=bpy.context.scene
 s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=960;s.render.resolution_y=640;s.render.resolution_percentage=100;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA';s.view_settings.view_transform='Standard';s.view_settings.exposure=.5
 col=bpy.data.collections['TOLI_MUX_REFERENCE_CAGE']
 for o in col.objects:
  if o.data.materials:
   mat=o.data.materials[0].copy();o.data.materials.clear();o.data.materials.append(mat);bs=mat.node_tree.nodes.get('Principled BSDF')
   if o.name.endswith('_R'):
    # Presentation only: exact symmetric far-side geometry remains in the scene.
    near=col.objects.get(o.name[:-2]);color=near.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value if near else bs.inputs['Base Color'].default_value;shade=tuple(v*.18 for v in color[:3])+(1,);bs.inputs['Base Color'].default_value=shade;bs.inputs['Emission Color'].default_value=shade;bs.inputs['Emission Strength'].default_value=.1
   else:bs.inputs['Emission Strength'].default_value=1.4
  o.hide_render=bool(o.get('station_slice'))
 wheel=bpy.data.materials.new('Diagnostic graphite');wheel.use_nodes=True;wheel.node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value=(.09,.105,.12,1)
 for o in bpy.data.objects:
  if o.name.startswith('CAGE_WHEEL'):o.data.materials.clear();o.data.materials.append(wheel)
 if version=='v02':bpy.ops.wm.save_as_mainfile(filepath=str(P/'tools/3d/isuzu-mux/source/production/isuzu-mux-reference-curve-cage-v02.blend'))
 out=r if version=='v02' else r/'baseline-v01';out.mkdir(exist_ok=True)
 for view in ['FRONT','FRONT34','SIDE','REAR34','REAR']:
  for o in col.objects:
   kind=o.get('trace_class','section');o.hide_render=bool(o.get('station_slice')) or (view=='FRONT' and kind not in ['front','section']) or (view=='REAR' and kind not in ['rear','section']) or (view=='SIDE' and kind in ['front','rear'])
   if o.name.endswith('_R') and o.data.materials:
    near=col.objects.get(o.name[:-2])
    if near and near.data.materials:
     color=near.data.materials[0].node_tree.nodes['Principled BSDF'].inputs['Base Color'].default_value
     factor=1 if view in ['FRONT','REAR'] else .18
     bs=o.data.materials[0].node_tree.nodes['Principled BSDF'];shade=tuple(v*factor for v in color[:3])+(1,)
     bs.inputs['Base Color'].default_value=shade;bs.inputs['Emission Color'].default_value=shade;bs.inputs['Emission Strength'].default_value=1.4 if factor==1 else .1
  s.camera=bpy.data.objects['CAM_'+view];s.render.filepath=str(out/(view.lower()+'.png'));bpy.ops.render.render(write_still=True)
print('MATCHED DIAGNOSTICS COMPLETE',flush=True);os._exit(0)
