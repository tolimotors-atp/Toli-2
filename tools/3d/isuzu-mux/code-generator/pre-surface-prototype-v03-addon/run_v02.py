import sys,bpy,json,hashlib,os
from pathlib import Path
ROOT=Path('/home/thunder/shared/tolimotors-main1/toli-static-website');sys.path.insert(0,str(ROOT/'tools/blender-addons'))
import toli_mux_generator as addon
from toli_mux_generator.parameters import values
from toli_mux_generator.validation import validate
bpy.ops.wm.read_factory_settings(use_empty=True);addon.register()
bpy.ops.toli_mux.generate()
def sig():
 return hashlib.sha256(json.dumps([(o.name,[list(v.co) for v in o.data.vertices]) for o in sorted(bpy.data.collections['TOLI_MUX_GENERATED'].objects,key=lambda o:o.name)],sort_keys=True).encode()).hexdigest()
a=sig();bpy.ops.toli_mux.regenerate();b=sig();assert a==b
s=bpy.context.scene;s.world=bpy.data.worlds.new('Coded review');s.world.use_nodes=True;s.world.node_tree.nodes['Background'].inputs[0].default_value=(.28,.28,.28,1);s.world.node_tree.nodes['Background'].inputs[1].default_value=.6
from mathutils import Vector
for name,pos in [('key',(-4,-5,6)),('fill',(3,4,6))]:
 d=bpy.data.lights.new(name,'AREA');d.energy=1400;d.size=5;o=bpy.data.objects.new(name,d);s.collection.objects.link(o);o.location=pos;o.rotation_euler=(Vector((0,0,1))-o.location).to_track_quat('-Z','Y').to_euler()
r=ROOT/'tools/3d/isuzu-mux/code-generator/renders/v02';r.mkdir(parents=True,exist_ok=True);v=validate(s,values(s));v['delete_and_regenerate_identical']=a==b;(r/'validation.json').write_text(json.dumps(v,indent=2));assert v['finite'] and abs(v['ground_z'])<1e-4 and v['symmetry'],v
out=ROOT/'tools/3d/isuzu-mux/source/production/isuzu-mux-code-generated-v02.blend';bpy.ops.wm.save_as_mainfile(filepath=str(out));
from toli_mux_generator import operators
operators.OUTPUT=r
bpy.ops.toli_mux.render();print(json.dumps(v),flush=True);os._exit(0)
