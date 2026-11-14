import sys,bpy,json,os
from pathlib import Path
P=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(P/'tools/blender-addons'));import toli_mux_generator as a
from toli_mux_generator.parameters import values
from toli_mux_generator.validation import validate
a.register();src=P/'tools/3d/isuzu-mux/source/production/isuzu-mux-code-generated-v02.blend';bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene;r=P/'tools/3d/isuzu-mux/code-generator/renders/v02';v=validate(s,values(s));s.toli_mux.quality='QUALITY';bpy.ops.toli_mux.regenerate();q=validate(s,values(s));q['topology_gate']=q['symmetry'] and q['nonmanifold_edges']==0 and q['degenerate_faces']==0;q['reopen_test']='PASS';(r/'quality-validation.json').write_text(json.dumps(q,indent=2));bpy.ops.wm.open_mainfile(filepath=str(src));s=bpy.context.scene
s.render.engine='CYCLES';s.cycles.samples=8;s.render.resolution_x=720;s.render.resolution_y=480;s.render.resolution_percentage=100
m=bpy.data.materials.new('Validation clay');m.use_nodes=True;bs=m.node_tree.nodes.get('Principled BSDF');bs.inputs['Base Color'].default_value=(.45,.45,.45,1);bs.inputs['Roughness'].default_value=.65;s.view_layers[0].material_override=m;s.render.film_transparent=True;s.render.image_settings.color_mode='RGBA'
for name in ['FRONT','FRONT34','SIDE','REAR34','REAR']:
 s.camera=bpy.data.objects['CAM_'+name];s.render.filepath=str(r/('clay-'+name.lower()+'.png'));bpy.ops.render.render(write_still=True)
s.render.film_transparent=False;s.world.node_tree.nodes['Background'].inputs[1].default_value=.08;s.view_layers[0].material_override=None
for o in s.objects:
 if o.type=='LIGHT':o.data.shape='RECTANGLE';o.data.size=7;o.data.size_y=.25;o.data.energy=2200
for name in ['FRONT34','SIDE','REAR34']:
 s.camera=bpy.data.objects['CAM_'+name];s.render.filepath=str(r/('strips-'+name.lower()+'.png'));bpy.ops.render.render(write_still=True)
print(json.dumps(q),flush=True);os._exit(0)
